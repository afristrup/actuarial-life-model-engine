from __future__ import annotations

import numpy as np

from lifebook.models.mortality_table import MortalityTable
from lifebook.models.portfolio import Portfolio
from lifebook.models.smoker_multipliers import SmokerMultipliers


def encode_qx(
    portfolio: Portfolio,
    mortality: MortalityTable,
    smoker_multipliers: SmokerMultipliers | None,
    t_max: int,
) -> np.ndarray:
    keys = list(mortality.rates.keys())
    genders = sorted({g for g, _ in keys})
    gender_to_idx = {g: i for i, g in enumerate(genders)}
    max_age = max(a for _, a in keys)

    mort_table = np.full((len(genders), max_age + 1), np.nan, dtype=np.float64)
    src_g = np.fromiter((gender_to_idx[g] for g, _ in keys), dtype=np.int64, count=len(keys))
    src_a = np.fromiter((a for _, a in keys), dtype=np.int64, count=len(keys))
    mort_table[src_g, src_a] = np.fromiter(
        mortality.rates.values(), dtype=np.float64, count=len(keys)
    )

    policy_genders = [p.gender for p in portfolio.policies]
    unknown_genders = sorted(set(policy_genders) - set(gender_to_idx))
    if unknown_genders:
        raise ValueError(f"no mortality rates for genders {unknown_genders}")

    policy_gender_idx = np.array([gender_to_idx[g] for g in policy_genders], dtype=np.int64)
    policy_age = np.fromiter(
        (p.age for p in portfolio.policies), dtype=np.int64, count=len(portfolio.policies)
    )
    policy_term = np.fromiter(
        (p.term for p in portfolio.policies), dtype=np.int64, count=len(portfolio.policies)
    )

    t_idx = np.arange(t_max, dtype=np.int64)
    attained_age = policy_age[:, None] + t_idx[None, :]
    active = t_idx[None, :] < policy_term[:, None]

    out_of_range = attained_age > max_age
    if (active & out_of_range).any():
        raise ValueError("attained age exceeds mortality table max age")

    safe_age = np.where(out_of_range, 0, attained_age)
    qx_lookup = mort_table[policy_gender_idx[:, None], safe_age]
    if np.isnan(qx_lookup[active]).any():
        raise ValueError("missing mortality rate in active (gender, age) region")

    if smoker_multipliers is None:
        mults = np.ones(len(portfolio.policies), dtype=np.float64)
    else:
        smoker_statuses = [p.smoker_status for p in portfolio.policies]
        unknown = sorted(set(smoker_statuses) - set(smoker_multipliers.multipliers))
        if unknown:
            raise ValueError(f"no smoker multiplier for {unknown}")
        mults = np.array(
            [smoker_multipliers.multipliers[s] for s in smoker_statuses],
            dtype=np.float64,
        )

    qx = np.minimum(np.nan_to_num(qx_lookup, nan=0.0) * mults[:, None], 1.0)
    return np.where(active, qx, 0.0)
