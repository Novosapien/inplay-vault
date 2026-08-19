"""Publisher: writes the daily feed file with correction semantics.

File naming:
    reference_feed_YYYY-MM-DD.json          normal daily publish
    reference_feed_YYYY-MM-DD_r2.json       correction (revision 2), etc.

A correction reissues records with the ORIGINAL effective_time, a bumped
revision, and is_correction=true — never silently fixed in the next
daily file. The consumer replaces same-effective_time/lower-revision
records and holds everything else.
"""

from __future__ import annotations

import json
from pathlib import Path

from .feed import TeamRecord, validate_records


class ValidationError(RuntimeError):
    pass


def publish(records: list[TeamRecord], out_dir: str | Path, publish_date: str,
            expected_team_count: int, revision: int = 1) -> Path:
    """Validate and write one feed file. Raises rather than publish a bad file."""
    dicts = [r.to_dict() for r in records]
    errors = validate_records(dicts, expected_team_count)
    if errors:
        raise ValidationError("; ".join(errors))

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = "" if revision == 1 else f"_r{revision}"
    path = out_dir / f"reference_feed_{publish_date}{suffix}.json"
    payload = {
        "publish_date": publish_date,
        "revision": revision,
        "team_count": len(dicts),
        "records": dicts,
    }
    path.write_text(json.dumps(payload, indent=2))
    return path


def publish_correction(records: list[TeamRecord], out_dir: str | Path,
                       publish_date: str, expected_team_count: int,
                       revision: int) -> Path:
    """Reissue corrected records: same effective_time, bumped revision."""
    if revision < 2:
        raise ValueError("corrections start at revision 2")
    fixed = []
    for r in records:
        r.revision = revision
        r.is_correction = True
        fixed.append(r)
    return publish(fixed, out_dir, publish_date, expected_team_count, revision)
