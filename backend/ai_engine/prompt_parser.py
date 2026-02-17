"""Rule-based prompt parser to extract directives from user prompts."""
import re
from typing import Dict, List


def parse(text: str) -> Dict:
    t = text.lower()
    directives = {
        "duration": None,
        "filter": None,
        "speed": None,
        "music": None,
        "include": [],
        "exclude": [],
    }

    # duration e.g. '30s' or '30 seconds' or '2 minutes'
    m = re.search(r"(\d+)\s*(s|sec|second|seconds)", t)
    if m:
        directives["duration"] = int(m.group(1))
    else:
        m2 = re.search(r"(\d+)\s*(m|min|minute|minutes)", t)
        if m2:
            directives["duration"] = int(m2.group(1)) * 60

    for f in ["vintage", "b&w", "sepia", "bw"]:
        if f in t:
            directives["filter"] = f
            break

    if "slow motion" in t or "slow-motion" in t:
        directives["speed"] = "slow"
    elif "fast" in t or "speed up" in t:
        directives["speed"] = "fast"

    if "music" in t or "with music" in t:
        directives["music"] = "upbeat"

    # include/exclude tags
    inc = re.findall(r"include ([a-z,\s]+)", t)
    exc = re.findall(r"exclude ([a-z,\s]+)", t)
    if inc:
        directives["include"] = [x.strip() for x in inc[0].split(",")]
    if exc:
        directives["exclude"] = [x.strip() for x in exc[0].split(",")]

    # defaults
    if not directives["duration"]:
        directives["duration"] = 30

    return directives
