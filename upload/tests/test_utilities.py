import sys
import os

import pytest
from app.utilities.utilities import get_uuid, get_datenow_iso
from datetime import datetime
from freezegun import freeze_time


# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_uuid():
    uuid1 = get_uuid()
    uuid2 = get_uuid()

    assert uuid1 != uuid2

@freeze_time("2023-01-01 12:00:00")
def test_get_datenow_iso():
    # Call the function
    result = get_datenow_iso()

    # Assertions
    expected_result = '2023-01-01T12:00:00'
    assert result == expected_result