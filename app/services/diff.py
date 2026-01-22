from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List

from app.models import Severity, SnapshotType, Vulnerability


def compute_fixed_vulnerabilities(
    before_vulnerabilities: Iterable[Vulnerability],
    after_vulnerabilities: Iterable[Vulnerability],
) -> List[Vulnerability]:
    """Return vulnerabilities present in BEFORE but not in AFTER.

    Comparison is based on the synthetic_id field, which is uniquely
    generated for this synthetic dataset.
    Complexity: O(N + M) where N and M are the sizes of BEFORE and AFTER.
    """

    after_ids = {v.synthetic_id for v in after_vulnerabilities}
    return [
        v
        for v in before_vulnerabilities
        if v.synthetic_id not in after_ids
    ]


def count_by_severity(
    vulnerabilities: Iterable[Vulnerability],
) -> Dict[Severity, int]:
    """Count vulnerabilities by severity.

    Complexity: O(K) where K is the number of vulnerabilities.
    """

    counter = Counter(v.severity for v in vulnerabilities)
    return {severity: counter.get(severity, 0) for severity in Severity}


def extract_before_after_vulnerabilities(
    snapshots,
) -> Dict[SnapshotType, List[Vulnerability]]:
    """Helper to split vulnerabilities into BEFORE and AFTER collections.

    This function expects an iterable of ScanSnapshot objects and returns
    a mapping from SnapshotType to lists of vulnerabilities.
    """

    result: Dict[SnapshotType, List[Vulnerability]] = {
        SnapshotType.BEFORE: [],
        SnapshotType.AFTER: [],
    }
    for snapshot in snapshots:
        if snapshot.snapshot_type in result:
            result[snapshot.snapshot_type].extend(snapshot.vulnerabilities)
    return result
