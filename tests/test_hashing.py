from app.utils.hashing import sha256_text


def test_same_text_produces_same_hash() -> None:
    first = sha256_text("insurance policy")

    second = sha256_text("insurance policy")

    assert first == second


def test_different_text_produces_different_hash() -> None:
    first = sha256_text("motor policy")

    second = sha256_text("health policy")

    assert first != second


def test_sha256_has_64_hex_characters() -> None:
    result = sha256_text("insurance")

    assert len(result) == 64
