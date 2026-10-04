from envq.scoring import (
    capability_necessity, verifier_fidelity, shortcut_resistance,
    discriminative_power, transfer_yield, attribution,
    contamination_resistance, cost_efficiency,
)


def test_capability_necessity():
    cn, ang = capability_necessity([1, 1], [0, .5])
    assert cn == .75
    assert ang == .75


def test_verifier_fidelity_penalizes_false_positive():
    assert verifier_fidelity(90, 0, 10, 0) < verifier_fidelity(90, 0, 0, 10)


def test_shortcut_resistance():
    assert abs(shortcut_resistance(.8, {"lexical": .72, "structural": .64}) - .85) < 1e-12


def test_dp_midrange():
    assert 0 < discriminative_power([.2, .5, .8]) <= 1


def test_transfer_yield():
    bounded, raw = transfer_yield([.2, .3], [.4, .5], cost=1, reference_cost=1)
    assert bounded > .5 and raw > 0


def test_attribution():
    assert attribution(1, 1, 1, 1) == 1


def test_contamination():
    assert contamination_resistance(1, 1, 1, 1) == 1


def test_cost_efficiency():
    ce, ee = cost_efficiency(100, 10, 10)
    assert ce == 1 and ee == 10
