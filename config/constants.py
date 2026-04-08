# Available actions in the environment
ACTIONS = [
    "mark_spam",
    "mark_important",
    "reply",
    "ignore",
    "escalate"
]

# Email labels
LABELS = [
    "spam",
    "urgent",
    "work",
    "personal"
]

# Priority levels
PRIORITY_LEVELS = ["high", "medium", "low"]

# Reward values (can be tuned easily)
REWARD_CONFIG = {
    "correct_action": 0.6,
    "wrong_action": -0.2,
    "spam_bonus": 0.3,
    "priority_bonus": 0.2,
    "ignore_urgent_penalty": -0.4,
    "attachment_ignore_penalty": -0.1,
    "step_penalty": -0.05
}

# Max steps per episode
MAX_STEPS = 5