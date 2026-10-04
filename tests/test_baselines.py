from envq.adapters.controlled_dlm import ControlledDLMAdapter
from envq.adapters.phantom_style import PhantomStyleAdapter


def test_controlled_dlm():
    rows = ControlledDLMAdapter().run(["authority-conflict", "unknown-missing-evidence"])
    assert all(r.reward == 1 for r in rows)


def test_phantom():
    rows = PhantomStyleAdapter().run(["a", "b", "c"])
    assert all(r.reward == 1 for r in rows)
    assert all(r.capability == "multi-hop-composition" for r in rows)
