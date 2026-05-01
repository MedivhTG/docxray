import os
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).parent / "examples"


@pytest.fixture
def test_file() -> Path:
    file_name = os.getenv("TEST_FILE", "abc.docx")
    return EXAMPLES_DIR / file_name
