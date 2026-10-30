#!/usr/bin/env python3
"""Build, verify and archive the Castiel release artifact.

Usage:
    python3 amk/scripts/build_release.py build [--out dist] [--strict]
                                               [--include-open-items] [--archive]
    python3 amk/scripts/build_release.py verify <release-dir>
    python3 amk/scripts/build_release.py archive <release-dir>

build   Regenerates every merged specification (one *-spec-full.md per spec area)
        from the source files, copies the publishable files, and writes
        release/MANIFEST.json and release/SHA256SUMS. Output is deterministic: it
        contains no timestamps, so an unchanged source gives an identical tree.
        Without --strict, placeholder (TODO) files are reported as warnings so CI
        can run on a draft. With --strict (used for a release tag) any placeholder,
        an invalid VERSION, a missing publishable file, a merge error or a dirty
        working tree fails the build.
verify  Recomputes every hash in a built release directory and compares it with
        release/SHA256SUMS and release/MANIFEST.json. Exit code 1 on any mismatch.

The release signature (release/SHA256SUMS.sig) is added by the release workflow, not
by this script; verify accepts it but does not check it. archive verifies the tree,
then writes a deterministic <release-dir>.tar.gz and <release-dir>.tar.gz.sha256.

Standard library only. Exit codes: 0 ok, 1 validation error, 2 usage error.
"""
import argparse
import gzip
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$")
MERGED_HASH_RE = re.compile(r"^Merged content hash: ([0-9a-f]{12})$", re.M)
RELEASE_META = ("release/MANIFEST.json", "release/SHA256SUMS", "release/SHA256SUMS.sig")

# (source directory, path of the merged file inside the release)
AREAS = [
    ("amk/abstract-kernel", "amk/abstract-kernel-spec-full.md"),
    ("amk/protocols", "amk/protocols-spec-full.md"),
    ("amk/package-framework", "amk/packages-spec-full.md"),
    ("amk/cross-cutting-requirements", "amk/cross-cutting-spec-full.md"),
    ("amk/implementation-specification", "amk/implementation-spec-full.md"),
    ("amk/governance", "amk/governance-spec-full.md"),
    ("amk/conformance", "conformance/conformance-spec-full.md"),
]
ROOT_FILES = ["README.md", "VERSION", "CHANGELOG.md", "LICENSE", "SECURITY.md", "GOVERNANCE.md", "CONTRIBUTING.md"]
SCHEMA_SOURCES = ["amk/conformance/declaration-schema", "amk/conformance/compliance-model/certification-output-schema"]


def load_merge_spec():
    spec = importlib.util.spec_from_file_location("merge_spec", HERE / "merge_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_placeholder(path: Path) -> bool:
    try:
        return path.read_text(encoding="utf-8-sig").strip() in ("", "TODO")
    except UnicodeDecodeError:
        return False


def read_text_line(path: Path):
    if not path.is_file() or is_placeholder(path):
        return None
    lines = path.read_text(encoding="utf-8-sig").strip().splitlines()
    return lines[0].strip() if lines else None


def git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def payload_files(directory: Path):
    """Files under directory other than README.md placeholders, as sorted relative paths."""
    out = []
    for p in sorted(directory.rglob("*")):
        if p.is_file() and p.name != "README.md":
            out.append(p.relative_to(directory))
    return out


def tree_files(release_dir: Path):
    return sorted(p.relative_to(release_dir).as_posix() for p in release_dir.rglob("*") if p.is_file())


def build(out_root: Path, strict: bool, include_open_items: bool):
    ms = load_merge_spec()
    errors, warnings = [], []

    version = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip() if (ROOT / "VERSION").is_file() else ""
    if not VERSION_RE.match(version):
        (errors if strict else warnings).append(f"VERSION is not a valid version (found {version!r}); expected for example 0.1.0")
        version = "unversioned"
    suite_version = read_text_line(ROOT / "amk" / "VERSION")

    areas = list(AREAS)
    for comp in sorted((ROOT / "amk" / "components").glob("amk-*")):
        if comp.is_dir():
            areas.append((comp.relative_to(ROOT).as_posix(), f"amk/components/{comp.name}-spec-full.md"))

    release_dir = out_root / (f"castiel-v{version}" if version != "unversioned" else "castiel-unversioned")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True)

    # Strict checks on sources.
    required = list(ROOT_FILES) + ["amk/amk-ssot.md"]
    for rel in required:
        p = ROOT / rel
        if not p.is_file():
            (errors if strict else warnings).append(f"missing publishable file: {rel}")
        elif is_placeholder(p):
            (errors if strict else warnings).append(f"placeholder file: {rel}")
    licenses = [p for p in (ROOT / "LICENSES").glob("*") if p.is_file()] if (ROOT / "LICENSES").is_dir() else []
    if not licenses or all(is_placeholder(p) for p in licenses):
        (errors if strict else warnings).append("LICENSES/ has no license text")
    if strict:
        status = git("status", "--porcelain")
        if status is None:
            errors.append("cannot read git status; strict builds must run in a git checkout")
        elif status:
            errors.append("working tree is not clean")

    # Merged specifications.
    generated = []
    placeholders = 0
    for src_rel, out_rel in areas:
        src = ROOT / src_rel
        if not src.is_dir():
            errors.append(f"spec area not found: {src_rel}")
            continue
        for md in src.rglob("*.md"):
            if is_placeholder(md):
                placeholders += 1
                if strict:
                    errors.append(f"placeholder file: {md.relative_to(ROOT).as_posix()}")
        merged, _, merr, mwarn, nfiles, nrules = ms.build(src, f"{src.name}-spec-full.md")
        errors.extend(f"{src_rel}: {e}" for e in merr)
        dest = release_dir / out_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(merged, encoding="utf-8", newline="\n")
        m = MERGED_HASH_RE.search(merged)
        generated.append({"output": out_rel, "source_dir": src_rel, "files_merged": nfiles,
                          "merged_content_hash": m.group(1) if m else None})
    if placeholders and not strict:
        warnings.append(f"{placeholders} placeholder (TODO) files are included in the merged specifications")

    # Plain copies.
    for rel in ROOT_FILES:
        if (ROOT / rel).is_file():
            copy(ROOT / rel, release_dir / rel)
    for p in licenses:
        copy(p, release_dir / "LICENSES" / p.name)
    if (ROOT / "amk/amk-ssot.md").is_file():
        copy(ROOT / "amk/amk-ssot.md", release_dir / "amk/amk-ssot.md")
    if include_open_items and (ROOT / "amk/OPEN-ITEMS.md").is_file():
        copy(ROOT / "amk/OPEN-ITEMS.md", release_dir / "amk/OPEN-ITEMS.md")
    schemas_dir = ROOT / "amk/protocols/schemas"
    if schemas_dir.is_dir():
        for rel in payload_files(schemas_dir):
            copy(schemas_dir / rel, release_dir / "amk/protocols/schemas" / rel)
    seen = {}
    for src_rel in SCHEMA_SOURCES:
        d = ROOT / src_rel
        if d.is_dir():
            for rel in payload_files(d):
                if rel.name in seen:
                    errors.append(f"conformance schema name collision: {rel.name} ({seen[rel.name]} and {src_rel})")
                    continue
                seen[rel.name] = src_rel
                copy(d / rel, release_dir / "conformance/schemas" / rel.name)
    vectors = ROOT / "amk/conformance/test-vectors"
    if vectors.is_dir():
        for rel in payload_files(vectors):
            copy(vectors / rel, release_dir / "conformance/test-vectors" / rel)
    schema = ROOT / "amk/releases/manifest.schema.json"
    if schema.is_file():
        copy(schema, release_dir / "release/manifest.schema.json")
    else:
        errors.append("amk/releases/manifest.schema.json is missing")

    if errors:
        return None, errors, warnings

    # Manifest and checksums.
    files = [rel for rel in tree_files(release_dir) if rel not in RELEASE_META]
    manifest = {
        "format_version": 1,
        "name": "castiel",
        "version": version,
        "suite_version": suite_version,
        "source_commit": git("rev-parse", "HEAD"),
        "generator": {
            "build_release.py": sha256_file(HERE / "build_release.py"),
            "merge_spec.py": sha256_file(HERE / "merge_spec.py"),
        },
        "generated": sorted(generated, key=lambda g: g["output"]),
        "files": [{"path": rel, "sha256": sha256_file(release_dir / rel), "size": (release_dir / rel).stat().st_size}
                  for rel in files],
    }
    (release_dir / "release").mkdir(exist_ok=True)
    (release_dir / "release/MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    sums = files + ["release/MANIFEST.json"]
    (release_dir / "release/SHA256SUMS").write_text(
        "".join(f"{sha256_file(release_dir / rel)}  {rel}\n" for rel in sorted(sums)), encoding="utf-8", newline="\n")
    return release_dir, errors, warnings


def verify(release_dir: Path):
    errors = []
    sums_path = release_dir / "release/SHA256SUMS"
    manifest_path = release_dir / "release/MANIFEST.json"
    if not sums_path.is_file() or not manifest_path.is_file():
        return ["release/SHA256SUMS or release/MANIFEST.json is missing"]
    listed = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([0-9a-f]{64})  (\S.*)$", line)
        if not m:
            errors.append(f"malformed SHA256SUMS line: {line!r}")
            continue
        listed[m.group(2)] = m.group(1)
    for rel, digest in sorted(listed.items()):
        p = release_dir / rel
        if not p.is_file():
            errors.append(f"listed file is missing: {rel}")
        elif sha256_file(p) != digest:
            errors.append(f"checksum mismatch: {rel}")
    extra = set(tree_files(release_dir)) - set(listed) - {"release/SHA256SUMS", "release/SHA256SUMS.sig"}
    for rel in sorted(extra):
        errors.append(f"file is not listed in SHA256SUMS: {rel}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return errors + [f"MANIFEST.json is not valid JSON: {exc}"]
    entries = {e["path"]: e for e in manifest.get("files", [])}
    for rel, e in sorted(entries.items()):
        if listed.get(rel) != e.get("sha256"):
            errors.append(f"MANIFEST.json and SHA256SUMS disagree: {rel}")
    for rel in sorted(set(listed) - set(entries) - {"release/MANIFEST.json"}):
        errors.append(f"file is in SHA256SUMS but not in MANIFEST.json: {rel}")
    return errors


def make_archive(release_dir: Path):
    """Deterministic tar.gz next to release_dir, plus a .sha256 file for it."""
    archive = release_dir.parent / (release_dir.name + ".tar.gz")
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for rel in [release_dir.name] + [f"{release_dir.name}/{r}" for r in tree_files(release_dir)]:
            path = release_dir.parent / rel
            info = tar.gettarinfo(str(path), arcname=rel)
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            info.mode = 0o755 if path.is_dir() else 0o644
            info.pax_headers = {}
            if path.is_dir():
                tar.addfile(info)
            else:
                with path.open("rb") as f:
                    tar.addfile(info, f)
    with archive.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(buf.getvalue())
    digest = sha256_file(archive)
    (archive.parent / (archive.name + ".sha256")).write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive, digest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--out", default="dist", help="output root (default: dist)")
    b.add_argument("--strict", action="store_true")
    b.add_argument("--include-open-items", action="store_true", help="ship amk/OPEN-ITEMS.md")
    b.add_argument("--archive", action="store_true", help="also write castiel-v<version>.tar.gz and its .sha256")
    v = sub.add_parser("verify")
    v.add_argument("release_dir")
    a = sub.add_parser("archive")
    a.add_argument("release_dir")
    args = ap.parse_args()

    if args.cmd == "archive":
        errs = verify(Path(args.release_dir))
        for e in errs:
            print(f"error: {e}", file=sys.stderr)
        if errs:
            return 1
        archive, digest = make_archive(Path(args.release_dir))
        print(f"archive {archive} sha256 {digest}")
        return 0

    if args.cmd == "verify":
        errs = verify(Path(args.release_dir))
        for e in errs:
            print(f"error: {e}", file=sys.stderr)
        print("verified" if not errs else f"{len(errs)} problem(s)", file=sys.stderr if errs else sys.stdout)
        return 1 if errs else 0

    release_dir, errs, warns = build(Path(args.out), args.strict, args.include_open_items)
    for w in warns:
        print(f"warning: {w}", file=sys.stderr)
    for e in errs:
        print(f"error: {e}", file=sys.stderr)
    if errs:
        return 1
    problems = verify(release_dir)
    for e in problems:
        print(f"error: {e}", file=sys.stderr)
    if problems:
        return 1
    print(f"built {release_dir} ({len(tree_files(release_dir))} files)")
    if args.archive:
        archive, digest = make_archive(release_dir)
        print(f"archive {archive} sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
