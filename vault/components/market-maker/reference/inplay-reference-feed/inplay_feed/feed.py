"""The published feed: record schema and ingest validation.

The schema here is field-for-field the one in item 3 of the spec email.
validate_records() implements the email's ingest rules, so InPlay runs it
before publishing and novosapien can run the identical checks on ingest —
any file that leaves us broken gets caught on both ends.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

METHODOLOGY_VERSION = "1.0.0"


@dataclass
class TeamRecord:
    team_id: str                     # Sportradar competitor ID
    league: str                      # "NFL" or "NCAA"
    effective_time: str              # ISO-8601 UTC
    revision: int                    # starts at 1; bumps only on correction
    is_correction: bool
    expected_remaining_wins: float   # full precision, remaining games only
    sigma: float
    games_remaining: int
    methodology_version: str = METHODOLOGY_VERSION

    def to_dict(self) -> dict:
        return asdict(self)


def build_record(team_id: str, league: str, effective_time: str,
                 game_probs: list[float], revision: int = 1,
                 is_correction: bool = False) -> TeamRecord:
    """Turn a team's remaining-game win probs into a feed record."""
    exp_wins = sum(game_probs)
    from .devig import schedule_sigma
    sigma = schedule_sigma(game_probs)  # schedule dispersion — NOT sigma_mkt
    return TeamRecord(
        team_id=team_id,
        league=league,
        effective_time=effective_time,
        revision=revision,
        is_correction=is_correction,
        expected_remaining_wins=exp_wins,
        sigma=sigma,
        games_remaining=len(game_probs),
    )


def validate_records(records: list[dict], expected_team_count: int) -> list[str]:
    """Return a list of violations; empty list means the file is good.

    Implements the ingest rules from the email:
      - all teams present (count check + no duplicate team_ids)
      - 0 <= expected_remaining_wins <= games_remaining
      - sigma > 0 whenever games_remaining > 0
      - league is NFL or NCAA; revision >= 1
    """
    errors: list[str] = []
    seen: set[str] = set()
    for r in records:
        tid = r.get("team_id", "<missing>")
        if tid in seen:
            errors.append(f"{tid}: duplicate team_id")
        seen.add(tid)
        if r.get("league") not in ("NFL", "NCAA"):
            errors.append(f"{tid}: bad league {r.get('league')!r}")
        gr = r.get("games_remaining", -1)
        ew = r.get("expected_remaining_wins", -1.0)
        if not (0 <= ew <= gr):
            errors.append(f"{tid}: expected_remaining_wins {ew} outside [0, {gr}]")
        if gr > 0 and not (r.get("sigma", 0) > 0):
            errors.append(f"{tid}: sigma must be > 0 with {gr} games remaining")
        if gr == 0 and r.get("sigma", 0) != 0:
            errors.append(f"{tid}: sigma must be 0 with no games remaining")
        if r.get("revision", 0) < 1:
            errors.append(f"{tid}: revision must be >= 1")
    if len(seen) != expected_team_count:
        errors.append(f"expected {expected_team_count} teams, file has {len(seen)}")
    return errors
