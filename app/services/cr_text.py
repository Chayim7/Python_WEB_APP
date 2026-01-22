from typing import Dict, Iterable

from app.models import PatchEvent, Severity, Vulnerability


def _format_severity_counts(severity_counts: Dict[Severity, int]) -> str:
    parts = []
    for severity in [
        Severity.CRITICAL,
        Severity.HIGH,
        Severity.MEDIUM,
        Severity.LOW,
    ]:
        parts.append(
            f"{severity.value.title()}: {severity_counts.get(severity, 0)}"
        )
    return ", ".join(parts)


def build_stage_cr_text(
    patch_event: PatchEvent,
    fixed_vulnerabilities: Iterable[Vulnerability],
    severity_counts: Dict[Severity, int],
) -> str:
    fixed_list = list(fixed_vulnerabilities)
    total_fixed = len(fixed_list)
    severity_summary = _format_severity_counts(severity_counts)

    lines = [
        f"Service: {patch_event.service.name}",
        "Environment promotion: DEV -> STAGE",
        f"AMI ID: {patch_event.ami_id}",
        f"DEV patch date: {patch_event.patch_date}",
        "",
        f"Total fixed vulnerabilities in DEV: {total_fixed}",
        f"Breakdown by severity: {severity_summary}",
        "",
        "Summary:",
        (
            "This change promotes a synthetic AMI patch from DEV to "
            "STAGE. The DEV run demonstrated remediation of the "
            "vulnerabilities listed above."
        ),
        "",
        (
            "Note: This summary is generated from synthetic, "
            "non-production data and does not reflect any real "
            "systems, scans, or vulnerabilities."
        ),
    ]
    return "\n".join(lines)


def build_prod_cr_text(
    patch_event: PatchEvent,
    fixed_vulnerabilities: Iterable[Vulnerability],
    severity_counts: Dict[Severity, int],
) -> str:
    fixed_list = list(fixed_vulnerabilities)
    total_fixed = len(fixed_list)
    severity_summary = _format_severity_counts(severity_counts)

    lines = [
        f"Service: {patch_event.service.name}",
        "Environment promotion: STAGE -> PROD",
        f"AMI ID: {patch_event.ami_id}",
        f"Current lifecycle state: {patch_event.current_state_code}",
        "",
        f"Total fixed vulnerabilities validated in DEV: {total_fixed}",
        f"Breakdown by severity: {severity_summary}",
        "",
        "Summary:",
        (
            "This change promotes a synthetic AMI patch from STAGE to "
            "PROD, based on DEV evidence that the vulnerabilities above "
            "were remediated."
        ),
        "",
        (
            "Note: This summary is generated from synthetic, "
            "non-production data and does not reflect any real "
            "systems, scans, or vulnerabilities."
        ),
    ]
    return "\n".join(lines)
