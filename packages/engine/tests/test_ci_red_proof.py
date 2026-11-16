def test_ci_turns_red() -> None:
    # Deliberately failing: proves CI fails on a broken test (#6). Never merged.
    assert 1 + 1 == 3
