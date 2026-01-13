import random
from typing import Dict, Any

POLICIES = {
    "standard": {
        "normalize_headers": True,
        "timing_jitter_ms": (0, 0),
    },
    "high_privacy": {
        "normalize_headers": True,
        "timing_jitter_ms": (25, 120),
    },
}

def apply_policy(policy_name: str, headers: Dict[str, str]) -> Dict[str, Any]:
    policy = POLICIES.get(policy_name, POLICIES["standard"])

    out_headers = dict(headers)

    if policy["normalize_headers"]:

        for h in ["x-forwarded-for", "via", "x-real-ip"]:
            out_headers.pop(h, None)

        out_headers.setdefault(
            "user-agent",
            "Mozilla/5.0 (API Privacy Gateway)"
        )

    low, high = policy["timing_jitter_ms"]
    jitter_ms = random.randint(low, high) if high > 0 else 0

    return {
        "headers": out_headers,
        "jitter_ms": jitter_ms,
    }
