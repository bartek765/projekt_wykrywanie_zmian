import os
import unittest
import json
from file_monitor import FileChangeDetector

class TestFileChangeDetector(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_sample.txt"
        self.test_state = "test_states.json"
        
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Initial content")
            
        self.detector = FileChangeDetector(state_filepath=self.test_state)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_state):
            os.remove(self.test_state)

    def test_first_analysis_saves_state(self):
        result = self.detector.check_file(self.test_file)
        self.assertEqual(result, "nie zmieniło się")
        self.assertTrue(os.path.exists(self.test_state))

    def test_file_unchanged(self):
        self.detector.check_file(self.test_file)
        result = self.detector.check_file(self.test_file)
        self.assertEqual(result, "nie zmieniło się")

    def test_file_changed(self):
        self.detector.check_file(self.test_file)
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Modified content")
        result = self.detector.check_file(self.test_file)
        self.assertEqual(result, "zmieniło się")

    def test_non_existent_file(self):
        result = self.detector.check_file("ghost_file.txt")
        self.assertIsNone(result)

    def test_state_persistence_between_instances(self):
        self.detector.check_file(self.test_file)
        
        new_detector = FileChangeDetector(state_filepath=self.test_state)
        result = new_detector.check_file(self.test_file)
        self.assertEqual(result, "nie zmieniło się")

if __name__ == "__main__":
    unittest.main()