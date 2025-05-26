import unittest
import os
from datetime import datetime, timedelta

# Import functions and globals from cat_app_main
# We need to be careful about how cat_app_main initializes itself (e.g., load_data on import)
# For testing, we will directly manipulate its global variables and use a test-specific data file.
import cat_app_main

# Import knowledge bases and configs
from cat_behavior_knowledge_base import BEHAVIOR_KNOWLEDGE_BASE
from cat_rewards_config import ACTION_POINTS, LEVEL_THRESHOLDS, BADGES

TEST_DATA_FILE = "test_cat_app_data.json"

class TestCatApp(unittest.TestCase):

    def setUp(self):
        """
        This method runs before each test.
        It resets the state of the application for each test.
        """
        # Override the main data file with a test-specific one
        self.original_data_file = cat_app_main.DATA_FILE
        cat_app_main.DATA_FILE = TEST_DATA_FILE

        # Clean up any existing test data file before each test for a clean slate
        if os.path.exists(TEST_DATA_FILE):
            os.remove(TEST_DATA_FILE)

        # Reset in-memory state of cat_app_main
        cat_app_main.diary_entries = []
        cat_app_main.owner_points = 0
        cat_app_main.owner_level = 1  # Default starting level
        cat_app_main.owner_badges = []
        cat_app_main.cat_profile = {}
        
        # After resetting, if load_data() is called by some functions implicitly, 
        # it will try to load from TEST_DATA_FILE (which is now clean or non-existent)
        # and then default to fresh state, which is what we want for isolated tests.
        # No explicit call to cat_app_main.load_data() here, as functions should manage their data needs,
        # or we test load_data explicitly. setUp ensures a clean in-memory state.

    def tearDown(self):
        """
        This method runs after each test.
        Clean up any created test data file.
        """
        if os.path.exists(TEST_DATA_FILE):
            os.remove(TEST_DATA_FILE)
        # Restore the original data file path in cat_app_main
        cat_app_main.DATA_FILE = self.original_data_file

    def test_behavior_interpretation_known(self):
        behavior_key = "Purring"
        result = cat_app_main.get_behavior_interpretation(behavior_key)
        self.assertEqual(result["interpretation"], BEHAVIOR_KNOWLEDGE_BASE[behavior_key]["interpretation"])
        self.assertEqual(result["points"], BEHAVIOR_KNOWLEDGE_BASE[behavior_key]["points"])

    def test_behavior_interpretation_unknown(self):
        result = cat_app_main.get_behavior_interpretation("Zoomies")
        self.assertEqual(result["interpretation"], "Behavior not found in knowledge base.")
        self.assertEqual(result["points"], 0)

    def test_log_diary_entry_basic(self):
        cat_app_main.log_diary_entry("feeding", "1/2 can wet food")
        self.assertEqual(len(cat_app_main.diary_entries), 1)
        self.assertEqual(cat_app_main.diary_entries[0]["entry_type"], "feeding")
        # Points check: log_diary_entry + potentially others if logic is complex
        # Assuming "log_diary_entry" is the base point for any log.
        self.assertEqual(cat_app_main.owner_points, ACTION_POINTS["log_diary_entry"])

    def test_log_diary_entry_exercise_points(self):
        cat_app_main.log_diary_entry("exercise", "laser pointer chase", duration_minutes=20)
        expected_points = ACTION_POINTS["log_diary_entry"] + ACTION_POINTS["log_exercise"]
        self.assertEqual(cat_app_main.owner_points, expected_points)
        self.assertEqual(len(cat_app_main.diary_entries), 1)

    def test_log_diary_entry_healthy_food_points(self):
        cat_app_main.log_diary_entry("feeding", "salmon pate", food_type="wet")
        expected_points = ACTION_POINTS["log_diary_entry"] + ACTION_POINTS["log_healthy_food"]
        self.assertEqual(cat_app_main.owner_points, expected_points)

    def test_level_up(self):
        # Find points for level 2. LEVEL_THRESHOLDS is {level_num: points_needed}
        points_for_level_2 = LEVEL_THRESHOLDS[2]
        
        # Simulate earning points. Directly set points then call check_and_update_level.
        cat_app_main.owner_points = points_for_level_2 
        cat_app_main.check_and_update_level() # This function updates cat_app_main.owner_level
        self.assertEqual(cat_app_main.owner_level, 2)

        # Test staying at current level if not enough points for next
        cat_app_main.owner_points = points_for_level_2 -1
        cat_app_main.owner_level = 1 # reset
        cat_app_main.check_and_update_level()
        self.assertEqual(cat_app_main.owner_level, 1)


    def test_badge_unlock_first_log(self):
        cat_app_main.log_diary_entry("observation", "cat is napping")
        # log_diary_entry calls check_and_award_badges
        self.assertIn("First Log!", cat_app_main.owner_badges)

    def test_badge_unlock_playtime_pro(self):
        # Needs 2 exercise logs based on simplified badge logic in main app for testing
        cat_app_main.log_diary_entry("exercise", "Feather wand", duration_minutes=15)
        cat_app_main.log_diary_entry("exercise", "Laser chase", duration_minutes=20)
        self.assertIn("Playtime Pro", cat_app_main.owner_badges)
        
    def test_badge_early_bird_logger(self):
        early_time = (datetime.now().replace(hour=7, minute=0, second=0)).strftime("%Y-%m-%d %H:%M:%S")
        cat_app_main.log_diary_entry("observation", "Early bird check", timestamp_override_str=early_time)
        self.assertIn("Early Bird Logger", cat_app_main.owner_badges)

    def test_weekly_insights_date_filtering(self):
        # Log an entry dated 8 days ago
        old_time = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        cat_app_main.log_diary_entry("observation", "Old entry", timestamp_override_str=old_time)

        # Log an entry dated today
        today_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cat_app_main.log_diary_entry("observation", "Today entry", timestamp_override_str=today_time)
        
        # Log another recent entry
        recent_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        cat_app_main.log_diary_entry("observation", "Recent entry", timestamp_override_str=recent_time)

        insights = cat_app_main.get_weekly_insights()
        # Should count "Today entry" and "Recent entry"
        self.assertEqual(insights["total_entries_this_week"], 2)

    def test_save_and_load_data_simple(self):
        # Set some data
        cat_app_main.owner_points = 123
        cat_app_main.cat_profile = {"name": "TestyCat", "age": 2, "baseline_metrics": {"target_sleep_hours_per_day": 15}}
        cat_app_main.owner_level = 2
        cat_app_main.owner_badges = ["First Log!"]
        cat_app_main.diary_entries.append({"timestamp": "2023-01-01 10:00:00", "entry_type": "test", "details": "save_load_test"})

        cat_app_main.save_data() # Uses TEST_DATA_FILE due to setUp

        # Reset in-memory state to simulate app restart
        cat_app_main.owner_points = 0
        cat_app_main.cat_profile = {}
        cat_app_main.owner_level = 1
        cat_app_main.owner_badges = []
        cat_app_main.diary_entries = []

        cat_app_main.load_data() # Should load from TEST_DATA_FILE

        self.assertEqual(cat_app_main.owner_points, 123)
        self.assertEqual(cat_app_main.cat_profile["name"], "TestyCat")
        self.assertEqual(cat_app_main.cat_profile["age"], 2)
        self.assertEqual(cat_app_main.owner_level, 2)
        self.assertIn("First Log!", cat_app_main.owner_badges)
        self.assertEqual(len(cat_app_main.diary_entries), 1)
        self.assertEqual(cat_app_main.diary_entries[0]["details"], "save_load_test")

    def test_get_weekly_insights_empty_data(self):
        # Ensure diary is empty
        cat_app_main.diary_entries = []
        insights = cat_app_main.get_weekly_insights()
        self.assertEqual(insights["total_entries_this_week"], 0)
        self.assertEqual(insights["average_sleep_per_log_hours"], 0)
        self.assertEqual(insights["exercise_sessions_logged"], 0)
        self.assertEqual(insights["most_common_behavior"], "N/A") # Updated based on main app's behavior
        self.assertEqual(len(insights["diagnostics"]), 1) # Should have "No specific diagnostics..."
        self.assertEqual(insights["diagnostics"][0], "No specific diagnostics based on current data and profile.")


if __name__ == '__main__':
    unittest.main()
