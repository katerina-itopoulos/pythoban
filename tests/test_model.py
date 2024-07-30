import pytest
from typing import Any
from game import Game, Level, Box, Wall, Floor, Goal, Player
import tempfile
import os
import json

#This video was used to gain a better understanding of how to unit test with pytest
#https://www.youtube.com/watch?v=YbpKMIUjvK8&ab_channel=pixegami

# Define a fixture that sets up a temporary file with test data
@pytest.fixture
def level_file():
    # Define a test map string using hjson format
    test_map = "WWW    \nWGWWWWW\nWGG    \nW BBBPW\nW    WW\nWWWWWW "

    # Create test level data including the map and score using hjson syntax
    level_data = {
        "map": test_map,
        "score": {
            "time": 0,
            "steps": 0
        }
    }

    # Create a temporary file and write the HJSON data into it
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w+")
    temp_file.write(json.dumps(level_data))
    temp_file.close()

    # Yield the file path to the test function
    yield temp_file.name

    # Clean up the file after tests complete
    os.remove(temp_file.name)

# Test to verify loading from file
def test_load_from_file(level_file):
    # Load the level from the temporary file
    level = Level.load_from_file(level_file)

    # Assert that the map string matches the expected test map
    expected_map = "WWW    \nWGWWWWW\nWGG    \nW BBBPW\nW    WW\nWWWWWW "
    assert str(level.map) == expected_map

    # Assert that the initial score values are correctly set
    assert level.score.time == 0
    assert level.score.steps == 0

    # Verify that the file path is correctly stored in the level object
    assert level.file_path == level_file

# Test to verify score updates are correctly applied

def test_update_score_improves_score(level_file):
    # Load the level from the file
    level = Level.load_from_file(level_file)

    # Update the score and verify the change
    level.update_score(10, 5)
    assert level.score.time == 10
    assert level.score.steps == 5

    # Update with a better score and verify the change
    level.update_score(8, 3)
    assert level.score.time == 8
    assert level.score.steps == 3

    # Try updating with worse scores and verify no change
    level.update_score(12, 7)  # Should not update because 12 > 8 and 7 > 3
    assert level.score.time == 8
    assert level.score.steps == 3



# Test to ensure that saving works as expected
def test_save(level_file):
    # Load the level from the file
    level = Level.load_from_file(level_file)
    
    # Update the score and save the level
    level.update_score(10, 5)
    level.save()

    # Open the file and verify the HJSON contents
    with open(level_file, "r") as file:
        data = json.load(file)

    # Assert that the map and score in the file match expected values
    assert data["map"] == "WWW    \nWGWWWWW\nWGG    \nW BBBPW\nW    WW\nWWWWWW "
    assert data["score"]["time"] == 10
    assert data["score"]["steps"] == 5

# Test for updating the score from an initial zero state
def test_update_score_with_initial_zero(level_file):
    # Load the level from the file
    level = Level.load_from_file(level_file)
    
    # Attempt to update the score with zero values
    level.update_score(0, 0)
    assert level.score.time == 0
    assert level.score.steps == 0

    # Update the score with non-zero values and verify
    level.update_score(8, 3)
    assert level.score.time == 8
    assert level.score.steps == 3