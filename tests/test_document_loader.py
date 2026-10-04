from pathlib import Path

import pytest

from app.ingestion.loader import (
    extract_title,
    load_document,
)


def test_extract_title() -> None:
    content = """
# Motor Insurance Policy

Some content.
"""

    assert extract_title(content) == "Motor Insurance Policy"


def test_extract_title_raises_when_missing() -> None:
    with pytest.raises(
        ValueError,
        match="H1 title",
    ):
        extract_title("No markdown title here.")


def test_load_motor_policy(
    tmp_path: Path,
) -> None:
    path = tmp_path / "motor-policy.md"

    path.write_text(
        "# Test Motor Policy\n\nContent.",
        encoding="utf-8",
    )

    document = load_document(path)

    assert document.source == "motor-policy.md"
    assert document.title == "Test Motor Policy"
    assert document.document_type == "motor_policy"
    assert document.version == "1.0"
