"""Item 2 of the spec email: the double-count-safe share price.

    Price per share = $5 x ( T - sum over G of p_ref(g) + sum over G of x_g )

Definitions (identical to the email's definitions block):
  T        latest whole-season expected wins (banked + expected remaining),
           de-vigged mean per item 1
  G        the team's games that have kicked off since T's timestamp
  p_ref(g) the pregame win prob for g, frozen at the moment T was ingested
  x_g      live win prob in [0,1] while in play; {0, 0.5, 1} once final
           (0.5 = tie, per item 5's settlement rule)

TeamPricer walks the full lifecycle: ingest a total, snapshot reference
probs, open games, stream live probs, settle results, ingest the next
total (which clears G). The three unit tests from the email live in
tests/test_pricing.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field

PRICE_PER_WIN = 5.0


@dataclass
class _GameState:
    p_ref: float          # frozen pregame prob, embedded in the current T
    x: float              # live prob while in play; 0 / 0.5 / 1 once final
    final: bool = False


@dataclass
class TeamPricer:
    price_per_win: float = PRICE_PER_WIN
    T: float | None = None
    games: dict[str, _GameState] = field(default_factory=dict)  # the set G

    # -- reference number lifecycle --------------------------------------
    def ingest_total(self, T: float) -> None:
        """A new whole-season total T arrived. G resets: every game that
        has started or finished is now embedded in the new T."""
        self.T = T
        self.games.clear()

    # -- game lifecycle ---------------------------------------------------
    def game_kickoff(self, game_id: str, p_ref: float) -> None:
        """Game kicks off. p_ref is the pregame prob snapshotted when the
        current T was ingested (closing pregame prob if none existed then)."""
        self.games[game_id] = _GameState(p_ref=p_ref, x=p_ref)

    def live_update(self, game_id: str, live_prob: float) -> None:
        g = self.games[game_id]
        if g.final:
            raise ValueError(f"game {game_id} is final; no live updates")
        g.x = live_prob

    def settle(self, game_id: str, result: float) -> None:
        """result: 1.0 win, 0.0 loss, 0.5 tie (item 5 settlement rule)."""
        if result not in (0.0, 0.5, 1.0):
            raise ValueError("result must be 0, 0.5, or 1")
        g = self.games[game_id]
        g.x = result
        g.final = True

    # -- price ------------------------------------------------------------
    def price(self) -> float:
        if self.T is None:
            raise ValueError("no season total ingested yet")
        adj = sum(g.x - g.p_ref for g in self.games.values())
        return self.price_per_win * (self.T + adj)


def share_price(T: float, ref_probs: list[float], x_values: list[float],
                price_per_win: float = PRICE_PER_WIN) -> float:
    """Stateless form of the same formula, for spreadsheet-style checks."""
    return price_per_win * (T - sum(ref_probs) + sum(x_values))
