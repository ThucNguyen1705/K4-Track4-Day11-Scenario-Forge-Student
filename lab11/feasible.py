"""Part B: physics check. TODO 3."""
from __future__ import annotations

import math

from avsim import core

G = 9.81


def is_feasible(p: dict) -> bool:
    """TODO 3. False for scenarios no real road user could produce. Reject if ANY of:

    - the lane change needs more sideways grip than the road has: the cosine lane change of 3.5 m over
      p["cutDur"] seconds peaks at a_lat = (pi / cutDur)^2 * 3.5 / 2; reject if a_lat > mu * g;
    - the post-merge braking p["cutBrake"] exceeds mu * g;
    - the pedestrian runs: p["pedV"] > 2.5 m/s;
    - the cut-in speed p["cutV"] is not in (0, 22] m/s.
    mu is p["mu"]. A search that keeps infeasible scenarios reports failures that cannot happen.
    """
    val = lambda key: float(p[key]) if p.get(key) is not None else float(core.DEFAULTS[key])   # noqa: E731
    grip = val("mu") * G                                   # the most the tyres can give, sideways or braking
    a_lat = (math.pi / val("cutDur")) ** 2 * 3.5 / 2       # peak sideways acceleration of the cosine lane change
    if a_lat > grip:
        return False
    if val("cutBrake") > grip:
        return False
    if val("pedV") > 2.5:                                  # a sprinting pedestrian, not a walking one
        return False
    if not 0.0 < val("cutV") <= 22.0:
        return False
    return True
