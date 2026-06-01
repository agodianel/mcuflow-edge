from mcuflow_edge.capture.session import AXES, CaptureSession


class ValidationError(Exception):
    pass


def validate_session(session: CaptureSession) -> list[str]:
    errors: list[str] = []
    if not session.session_id:
        errors.append("session_id is required")
    if session.target not in ("esp32", "stm32"):
        errors.append(f"invalid target: {session.target}")
    if not session.samples:
        errors.append("session has no samples")
    for i, s in enumerate(session.samples):
        for axis in AXES:
            if axis not in s.values:
                errors.append(f"sample {i}: missing axis '{axis}'")
                break
        if not s.label:
            errors.append(f"sample {i}: missing label")
    return errors


def assert_valid_session(session: CaptureSession) -> None:
    errors = validate_session(session)
    if errors:
        raise ValidationError("; ".join(errors))
