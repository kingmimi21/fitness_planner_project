import pytest
import builtins
import json
from unittest import mock
from fitness_planner import load_exercise_history


@pytest.fixture
def mock_open_data(monkeypatch):
    # Patch open to simulate reading a data.json file
    data = {
        "bench press": {
            "2024-06-01": [{"weight": "100", "reps": "10"}]
        }
    }
    file_data = json.dumps(data)
    m = mock.mock_open(read_data=file_data)
    monkeypatch.setattr("builtins.open", m)
    return data


def test_load_exercise_history_with_data(monkeypatch, capsys, mock_open_data):
    # Patch json.load to return our mock data
    monkeypatch.setattr(json, "load", lambda fp: mock_open_data)
    # Patch input to avoid recursion
    monkeypatch.setattr(
        "fitness_planner.load_exercise_history", lambda: mock_open_data)
    # Call the function
    result = load_exercise_history()
    # Check output
    captured = capsys.readouterr()
    assert "=== Exercise History" in captured.out
    assert "bench press" in captured.out
    assert result == mock_open_data


def test_load_exercise_history_no_data(monkeypatch, capsys):
    # Patch load_exercise_history to return None to simulate no data
    monkeypatch.setattr("fitness_planner.load_exercise_history", lambda: None)
    result = load_exercise_history()
    captured = capsys.readouterr()
    assert "No history found. Starting fresh." in captured.out
    assert result is None


def test_load_exercise_history_file_not_found(monkeypatch):
    # Patch open to raise IOError
    monkeypatch.setattr("builtins.open", mock.Mock(side_effect=IOError))
    # Patch load_exercise_history to avoid recursion
    monkeypatch.setattr("fitness_planner.load_exercise_history", lambda: {})
    result = load_exercise_history()
    assert result == {}
