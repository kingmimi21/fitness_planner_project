import unittest
from history import add_exercise_dictionary


class TestExerciseFunctions(unittest.TestCase):

    def test_add_exercise(self):
        dic = {}
        updated = add_exercise_dictionary(dic, "bench press", "100", "10")
        self.assertIn("bench press", updated)


if __name__ == '__main__':
    unittest.main()
