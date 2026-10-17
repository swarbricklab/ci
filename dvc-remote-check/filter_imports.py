#!/usr/bin/env python3
"""Drop DVC imports from a `dvc data status --not-in-remote` path list.

Imported data (``dvc import`` from another repo, or ``dvc import-url`` from a URL)
lives in its **source** remote, not in this repo's own DVC remote — so it must not
be required by the remote-presence check. An output is an import iff its tracking
``<path>.dvc`` file has a ``deps:`` section (a plain ``dvc add`` output has only
``outs:``). Everything else (native outputs, frozen pipeline stages) is kept and
still validated.

Stdlib-only (the runner is not guaranteed to have PyYAML); the ``deps:`` top-level
key is detected textually, which is unambiguous in the canonical DVC file format.

Usage: filter_imports.py <dvc-data-status-json>   # prints kept (non-import) paths
"""
import json
import os
import sys


def is_import(path):
    """True if <path> is tracked by a .dvc import / import-url (has top-level deps)."""
    dvc_file = path + ".dvc"
    try:
        with open(dvc_file) as fh:
            return any(line.startswith("deps:") for line in fh)
    except (FileNotFoundError, NotADirectoryError):
        # No sidecar .dvc (e.g. a pipeline-stage output tracked in dvc.lock) ->
        # not an import; keep it.
        return False


def main():
    with open(sys.argv[1]) as fh:
        paths = json.load(fh).get("not_in_remote", [])
    kept = [p for p in paths if not is_import(p)]
    sys.stdout.write("\n".join(kept))


if __name__ == "__main__":
    main()
