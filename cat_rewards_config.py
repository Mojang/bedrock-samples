# Configuration for owner actions, points, levels, and badges

ACTION_POINTS = {
    "log_diary_entry": 1,  # For the act of logging any entry
    "log_healthy_food": 3, # e.g., when 'wet food' or 'high quality' is mentioned
    "log_exercise": 5,     # For logging a play/exercise session
    "log_sufficient_sleep": 2, # e.g., if logged sleep meets a certain threshold
    "weekly_activity_goal_met": 10,
    "weekly_sleep_goal_met": 10,
    "consistent_logging_bonus": 5 # e.g., for logging 7 days in a row
}

LEVEL_THRESHOLDS = {
    1: 0,      # "New Pawrent"
    2: 50,     # "Attentive Owner"
    3: 150,    # "Super Cat Carer"
    4: 300,    # "Whisker Whisperer"
    5: 500     # "Purrfect Parent"
    # Future levels can be added here
}

BADGES = [
    {
        "name": "First Log!",
        "description": "Awarded for making your first diary entry.",
        "criteria": "user_total_diary_entries >= 1"
    },
    {
        "name": "Early Bird Logger",
        "description": "Awarded for logging an entry before 8 AM.",
        "criteria": "log_time < '08:00'"
    },
    {
        "name": "Playtime Pro",
        "description": "Awarded for logging 10 exercise sessions.",
        "criteria": "user_total_exercise_logs >= 10"
    },
    {
        "name": "Gourmet Chef",
        "description": "Awarded for logging healthy food 5 times.",
        "criteria": "user_total_healthy_food_logs >= 5"
    },
    {
        "name": "Sleep Guardian",
        "description": "Awarded for logging sufficient sleep for your cat 5 times.",
        "criteria": "user_total_sufficient_sleep_logs >= 5"
    },
    {
        "name": "Week 1 Logging Streak",
        "description": "Awarded for logging at least one entry every day for 7 consecutive days.",
        "criteria": "user_daily_logging_streak_days >= 7"
    },
    {
        "name": "Activity Goal Achiever",
        "description": "Awarded for meeting the weekly activity goal for the first time.",
        "criteria": "user_weekly_activity_goals_met >= 1"
    },
    {
        "name": "Sleep Goal Achiever",
        "description": "Awarded for meeting the weekly sleep goal for the first time.",
        "criteria": "user_weekly_sleep_goals_met >= 1"
    },
    {
        "name": "Dedicated Pawrent",
        "description": "Awarded for logging 30 diary entries.",
        "criteria": "user_total_diary_entries >= 30"
    },
    {
        "name": "Month Long Streaker",
        "description": "Awarded for logging at least one entry every day for 30 consecutive days.",
        "criteria": "user_daily_logging_streak_days >= 30"
    }
]
