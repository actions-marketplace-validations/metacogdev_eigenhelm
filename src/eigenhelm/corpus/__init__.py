"""Corpus manifest schema and materializer."""

from eigenhelm.corpus.manifest import (
    CompositionManifest,
    CorpusManifest,
    CorpusTarget,
    load_any_manifest,
    load_composition,
    load_manifest,
)
from eigenhelm.corpus.sync import (
    BulkSyncResult,
    SyncResult,
    discover_manifests,
    sync_all_manifests,
    sync_composition,
    sync_manifest,
)

__all__ = [
    "BulkSyncResult",
    "CompositionManifest",
    "CorpusManifest",
    "CorpusTarget",
    "SyncResult",
    "discover_manifests",
    "load_any_manifest",
    "load_composition",
    "load_manifest",
    "sync_all_manifests",
    "sync_composition",
    "sync_manifest",
]
