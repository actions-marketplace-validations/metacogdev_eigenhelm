"""Corpus materializer: sync_manifest(), sentinel logic, and glob matching."""

from __future__ import annotations

import fnmatch
import json
import tarfile
import urllib.error
import urllib.request
import warnings
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from eigenhelm.corpus.manifest import (
    CompositionManifest,
    CorpusManifest,
    CorpusTarget,
    load_any_manifest,
)

_SENTINEL_NAME = ".eigenhelm-sync"
_SENTINEL_SCHEMA_VERSION = 1
_USER_AGENT = "eigenhelm-corpus-sync/1.0"


# ---------------------------------------------------------------------------
# SyncResult
# ---------------------------------------------------------------------------


@dataclass
class SyncResult:
    """Summary of a sync_manifest() run."""

    synced: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)
    total_files: int = 0
    files_by_target: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Glob matching — Python 3.11-compatible ** support
# ---------------------------------------------------------------------------


def _match_parts(path_parts: list[str], pat_parts: list[str]) -> bool:
    """Recursive glob matching with ** support."""
    if not pat_parts:
        return not path_parts
    if not path_parts:
        return all(p == "**" for p in pat_parts)
    if pat_parts[0] == "**":
        # ** matches zero or more segments
        if _match_parts(path_parts, pat_parts[1:]):
            return True
        return _match_parts(path_parts[1:], pat_parts)
    if fnmatch.fnmatch(path_parts[0], pat_parts[0]):
        return _match_parts(path_parts[1:], pat_parts[1:])
    return False


def _glob_match(path: str, pattern: str) -> bool:
    """Match a POSIX path against a glob pattern, honouring ** for any depth."""
    path_parts = path.split("/")
    pat_parts = pattern.split("/")
    return _match_parts(path_parts, pat_parts)


def _path_matches(rel_path: str, include: tuple[str, ...], exclude: tuple[str, ...]) -> bool:
    """Return True if rel_path matches any include pattern and no exclude pattern."""
    if not any(_glob_match(rel_path, pat) for pat in include):
        return False
    if any(_glob_match(rel_path, pat) for pat in exclude):
        return False
    return True


# ---------------------------------------------------------------------------
# Sentinel helpers
# ---------------------------------------------------------------------------


def _read_sentinel(sentinel_path: Path) -> dict | None:
    """Read and parse the sentinel JSON; return None on missing or corrupt."""
    try:
        return json.loads(sentinel_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _write_sentinel(dest_dir: Path, target: CorpusTarget, files_extracted: int) -> None:
    """Write .eigenhelm-sync sentinel JSON after successful extraction."""
    sentinel: dict = {
        "schema_version": _SENTINEL_SCHEMA_VERSION,
        "synced_at": datetime.now(UTC).isoformat(),
        "name": target.name,
        "url": target.url,
        "ref": target.ref,
        "include": list(target.include),
        "exclude": list(target.exclude),
        "entry_hash": target.entry_hash(),
        "files_extracted": files_extracted,
    }
    (dest_dir / _SENTINEL_NAME).write_text(json.dumps(sentinel, indent=2))


def _is_synced(dest_dir: Path, target: CorpusTarget) -> bool:
    """Return True if the sentinel exists and entry_hash matches the current manifest."""
    data = _read_sentinel(dest_dir / _SENTINEL_NAME)
    if data is None:
        return False
    if data.get("schema_version") != _SENTINEL_SCHEMA_VERSION:
        return False
    return data.get("entry_hash") == target.entry_hash()


# ---------------------------------------------------------------------------
# Streaming download + extraction
# ---------------------------------------------------------------------------


def _stream_target(target: CorpusTarget, dest_dir: Path) -> int:
    """Download and extract target archive, applying include/exclude patterns.

    Uses streaming tarfile extraction (``mode="r|gz"``) to avoid writing a
    temporary file. Extracts via ``tf.extractfile()`` + manual write to avoid
    the ``filter=`` parameter added in Python 3.12.

    Returns the number of files extracted. Emits a ``warnings.warn`` if no
    files matched the include patterns.
    """
    req = urllib.request.Request(
        target.archive_url,
        headers={"User-Agent": _USER_AGENT},
    )
    files_extracted = 0
    with urllib.request.urlopen(req) as resp:
        with tarfile.open(fileobj=resp, mode="r|gz") as tf:
            for member in tf:
                if not member.isreg():
                    continue
                # Strip first path component (GitHub wraps in "{repo}-{ref}/")
                parts = PurePosixPath(member.name).parts
                if len(parts) < 2:
                    continue
                rel_path = "/".join(parts[1:])
                if not _path_matches(rel_path, target.include, target.exclude):
                    continue

                # Path traversal protection: ensure out_path is inside dest_dir
                out_path = (dest_dir / rel_path).resolve()
                if not out_path.is_relative_to(dest_dir.resolve()):
                    warnings.warn(
                        f"{target.name}: skipping {member.name!r} (potential path traversal)",
                        stacklevel=2,
                    )
                    continue

                out_path.parent.mkdir(parents=True, exist_ok=True)
                file_obj = tf.extractfile(member)
                if file_obj is None:
                    continue
                out_path.write_bytes(file_obj.read())
                files_extracted += 1

    if files_extracted == 0:
        warnings.warn(
            f"{target.name}: include patterns {list(target.include)!r} matched 0 files in archive",
            stacklevel=2,
        )
    return files_extracted


# ---------------------------------------------------------------------------
# Main materializer
# ---------------------------------------------------------------------------


def sync_manifest(
    manifest: CorpusManifest,
    output_dir: Path,
    *,
    force: bool = False,
) -> SyncResult:
    """Materialize all targets in the manifest into ``output_dir``.

    Args:
        manifest: A validated :class:`CorpusManifest`.
        output_dir: Directory to write materialized targets into. Created if
            it does not exist.
        force: If ``True``, skip sentinel checks and re-download all targets.

    Returns:
        :class:`SyncResult` summarising synced, skipped, and failed targets.

    Raises:
        OSError: Only for unrecoverable errors such as permission failures on
            ``output_dir``. Per-target errors are captured in
            ``SyncResult.failed``.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    result = SyncResult()

    for target in manifest.targets:
        target_dir = output_dir / target.name
        target_dir.mkdir(parents=True, exist_ok=True)

        if not force and _is_synced(target_dir, target):
            result.skipped.append(target.name)
            continue

        # Warn when the ref has changed (entry_hash differs due to ref change)
        if not force:
            existing = _read_sentinel(target_dir / _SENTINEL_NAME)
            if existing is not None and existing.get("ref") != target.ref:
                warnings.warn(
                    f"{target.name}: ref changed from {existing['ref']!r} "
                    f"to {target.ref!r}, re-syncing",
                    stacklevel=2,
                )

        try:
            files_extracted = _stream_target(target, target_dir)
            _write_sentinel(target_dir, target, files_extracted)
            result.synced.append(target.name)
            result.total_files += files_extracted
            result.files_by_target[target.name] = files_extracted
        except Exception as exc:
            result.failed.append((target.name, str(exc)))

    return result


# ---------------------------------------------------------------------------
# BulkSyncResult
# ---------------------------------------------------------------------------


@dataclass
class BulkSyncResult:
    """Summary of a bulk sync (--all or composition) run."""

    per_manifest: dict[str, SyncResult] = field(default_factory=dict)
    failed_manifests: list[tuple[str, str]] = field(default_factory=list)

    @property
    def any_failed(self) -> bool:
        if self.failed_manifests:
            return True
        return any(r.failed for r in self.per_manifest.values())


# ---------------------------------------------------------------------------
# Manifest discovery
# ---------------------------------------------------------------------------


def discover_manifests(directory: Path) -> list[Path]:
    """Find all valid CorpusManifest .toml files in directory (non-recursive).

    Skips CompositionManifest files and unparseable files with warnings.
    """
    results: list[Path] = []
    for toml_path in sorted(directory.glob("*.toml")):
        try:
            m = load_any_manifest(toml_path)
            if isinstance(m, CorpusManifest):
                results.append(toml_path)
            else:
                warnings.warn(
                    f"skipping composition manifest: {toml_path.name}",
                    stacklevel=2,
                )
        except Exception:
            warnings.warn(
                f"skipping unparseable file: {toml_path.name}",
                stacklevel=2,
            )
    return results


# ---------------------------------------------------------------------------
# Bulk sync
# ---------------------------------------------------------------------------


def sync_all_manifests(
    directory: Path,
    output_dir: Path,
    *,
    force: bool = False,
) -> BulkSyncResult:
    """Discover and sync all corpus manifests in directory.

    Each manifest is synced into ``output_dir / manifest.name``.
    Per-manifest failures are captured without aborting.
    """
    from eigenhelm.corpus.manifest import load_manifest

    paths = discover_manifests(directory)
    result = BulkSyncResult()

    for manifest_path in paths:
        try:
            manifest = load_manifest(manifest_path)
            manifest_output = output_dir / manifest.name
            sr = sync_manifest(manifest, manifest_output, force=force)
            result.per_manifest[manifest.name] = sr
        except Exception as exc:
            result.failed_manifests.append((manifest_path.name, str(exc)))

    return result


# ---------------------------------------------------------------------------
# Composition sync
# ---------------------------------------------------------------------------


def sync_composition(
    composition: CompositionManifest,
    base_dir: Path,
    output_dir: Path,
    *,
    force: bool = False,
) -> BulkSyncResult:
    """Resolve and sync all manifests referenced by a composition manifest.

    Each resolved manifest is synced into ``output_dir / manifest.name``.
    """
    manifests = composition.resolve(base_dir)
    result = BulkSyncResult()

    for manifest in manifests:
        try:
            manifest_output = output_dir / manifest.name
            sr = sync_manifest(manifest, manifest_output, force=force)
            result.per_manifest[manifest.name] = sr
        except Exception as exc:
            result.failed_manifests.append((manifest.name, str(exc)))

    return result
