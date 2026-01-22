from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.models import PatchEvent

DEV_EVIDENCE_CAPTURED = "DEV_EVIDENCE_CAPTURED"
DEV_VERIFIED = "DEV_VERIFIED"
STAGE_CR_READY = "STAGE_CR_READY"
STAGE_PATCHED = "STAGE_PATCHED"
PROD_CR_READY = "PROD_CR_READY"
PROD_PATCHED = "PROD_PATCHED"
CLOSED = "CLOSED"


class PatchState(ABC):
    """Abstract base class for patch lifecycle states."""

    code: str

    def __init__(self, code: str) -> None:
        self.code = code

    @abstractmethod
    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        """Return the list of allowed next state codes for this context."""

    def can_transition_to(self, target_code: str, context: PatchEvent) -> bool:
        return target_code in self.allowed_transitions(context)

    def on_enter(self, context: PatchEvent) -> None:  # pragma: no cover - hook
        """Optional hook invoked after a successful transition."""


def _has_dev_evidence(context: PatchEvent) -> bool:
    """Return True if DEV evidence (fixed vulnerabilities) has been
    recorded.
    """

    return bool(context.dev_evidence_available)


class DevEvidenceCapturedState(PatchState):
    def __init__(self) -> None:
        super().__init__(DEV_EVIDENCE_CAPTURED)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        # After capturing evidence, the next normal step is verification.
        return [DEV_VERIFIED]


class DevVerifiedState(PatchState):
    def __init__(self) -> None:
        super().__init__(DEV_VERIFIED)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        # Cannot promote towards STAGE without DEV evidence.
        if not _has_dev_evidence(context):
            return []
        return [STAGE_CR_READY]


class StageCrReadyState(PatchState):
    def __init__(self) -> None:
        super().__init__(STAGE_CR_READY)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        # STAGE CR is ready; next step is to patch STAGE.
        if not _has_dev_evidence(context):
            return []
        return [STAGE_PATCHED]


class StagePatchedState(PatchState):
    def __init__(self) -> None:
        super().__init__(STAGE_PATCHED)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        # After STAGE is patched, we can prepare PROD CR.
        if not _has_dev_evidence(context):
            return []
        return [PROD_CR_READY]


class ProdCrReadyState(PatchState):
    def __init__(self) -> None:
        super().__init__(PROD_CR_READY)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        # Next normal step: patch PROD.
        if not _has_dev_evidence(context):
            return []
        return [PROD_PATCHED]


class ProdPatchedState(PatchState):
    def __init__(self) -> None:
        super().__init__(PROD_PATCHED)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:
        # After PROD is patched, we may close the event.
        return [CLOSED]


class ClosedState(PatchState):
    def __init__(self) -> None:
        super().__init__(CLOSED)

    def allowed_transitions(self, context: PatchEvent) -> List[str]:  # noqa: ARG002, E501
        # Terminal state.
        return []


def get_state_for_event(event: PatchEvent) -> PatchState:
    """Return the concrete PatchState instance for a PatchEvent's
    current state code.
    """

    mapping = {
        DEV_EVIDENCE_CAPTURED: DevEvidenceCapturedState,
        DEV_VERIFIED: DevVerifiedState,
        STAGE_CR_READY: StageCrReadyState,
        STAGE_PATCHED: StagePatchedState,
        PROD_CR_READY: ProdCrReadyState,
        PROD_PATCHED: ProdPatchedState,
        CLOSED: ClosedState,
    }

    state_code = event.current_state_code or DEV_EVIDENCE_CAPTURED
    state_cls = mapping.get(state_code, DevEvidenceCapturedState)
    return state_cls()


def transition_patch_event(event: PatchEvent, target_code: str) -> None:
    """Update a PatchEvent's state if the transition is allowed.

    Raises ValueError if the transition is not permitted.
    """

    current_state = get_state_for_event(event)

    # Enforce rule: cannot close unless PROD patched.
    if target_code == CLOSED and event.current_state_code != PROD_PATCHED:
        raise ValueError("Cannot close patch event unless PROD is patched.")

    if not current_state.can_transition_to(target_code, event):
        raise ValueError(
            "Transition from {0} to {1} is not allowed.".format(
                current_state.code,
                target_code,
            )
        )

    event.current_state_code = target_code
    current_state.on_enter(event)
