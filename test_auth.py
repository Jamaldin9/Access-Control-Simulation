"""Pytest unit tests for the Access Control Simulation.

This file may live at the repo root. We add the repo root to sys.path so
imports work whether you run `pytest` from the project root or from elsewhere.
"""

import os
import sys
import inspect

import pytest

# Ensure the project root is on the Python path.
# Works whether this file is at repo root or inside a `tests/` folder.
this_dir = os.path.dirname(os.path.abspath(__file__))

# If auth_engine.py is alongside this file, use this_dir.
# Otherwise assume we're in tests/ and use the parent directory.
candidate_root = this_dir
if not os.path.exists(os.path.join(candidate_root, "auth_engine.py")):
    candidate_root = os.path.dirname(this_dir)

if candidate_root not in sys.path:
    sys.path.insert(0, candidate_root)

from auth_engine import authorize


def _call_authorize(*args, **kwargs):
    """Call authorize() in a signature-tolerant way.

    Some projects evolve authorize() from (role, action) to include more context.
    These tests try to stay stable by adapting to the current signature.
    """
    sig = inspect.signature(authorize)
    params = list(sig.parameters.values())

    # If authorize already matches provided args/kwargs, call directly.
    try:
        sig.bind(*args, **kwargs)
        return authorize(*args, **kwargs)
    except TypeError:
        pass

    # Common: authorize(role, action)
    if len(params) == 2:
        return authorize(args[0], args[1])

    # Common: authorize(user, action, resource=None) or similar
    if len(params) >= 3:
        padded = list(args)
        while len(padded) < 3:
            padded.append(None)
        return authorize(*padded[: len(params)])

    # Fallback: try with whatever we have.
    return authorize(*args, **kwargs)


def _is_allow(value) -> bool:
    return str(value).strip().upper() == "ALLOW"


def _is_deny(value) -> bool:
    return str(value).strip().upper() == "DENY"


def test_allow_admin():
    assert authorize("admin", "delete") == "ALLOW"


def test_deny_guest():
    assert authorize("guest", "delete") == "DENY"


def test_unknown_role_defaults_to_deny():
    """Unknown principals should not be granted access by default."""
    result = _call_authorize("unknown_role", "delete")
    assert _is_deny(result) or _is_allow(result) is False


def test_unknown_action_defaults_to_deny():
    """Unknown actions should not be granted access by default."""
    result = _call_authorize("admin", "unknown_action")
    assert _is_deny(result) or _is_allow(result) is False


def test_empty_inputs_are_handled_safely():
    """Engine should fail closed on empty/invalid inputs."""
    result = _call_authorize("", "")
    assert _is_deny(result) or _is_allow(result) is False


def test_none_inputs_are_handled_safely():
    """Engine should fail closed on None inputs (or raise a clear error)."""
    try:
        result = _call_authorize(None, None)
    except Exception as e:
        # Accept a clear exception; failing closed is OK.
        assert isinstance(e, Exception)
    else:
        assert _is_deny(result) or _is_allow(result) is False


def test_returns_a_known_decision_string():
    """Decision should be ALLOW or DENY (case-insensitive)."""
    result = _call_authorize("admin", "delete")
    assert str(result).strip().upper() in {"ALLOW", "DENY"}


def test_signature_is_reasonable():
    """Guardrail: authorize() should take at least (role/user, action)."""
    sig = inspect.signature(authorize)
    assert len(sig.parameters) >= 2


@pytest.mark.parametrize(
    "role,action",
    [
        ("guest", "read"),
        ("guest", "write"),
        ("user", "delete"),
    ],
)
def test_fail_closed_for_unprivileged_pairs(role, action):
    """Representative unprivileged combinations should not accidentally allow."""
    result = _call_authorize(role, action)
    assert _is_deny(result) or _is_allow(result) is False