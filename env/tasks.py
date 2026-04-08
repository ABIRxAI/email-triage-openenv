import json
import os
import random

def load_emails():
    """Load emails from dataset"""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "emails.json")
    
    with open(data_path, "r") as f:
        return json.load(f)

def generate_task(email):
    """Generate a task dynamically based on email content"""

    # Task 1: Spam detection
    if email["label"] == "spam":
        return {
            "type": "spam_detection",
            "email": email,
            "expected_action": "mark_spam"
        }

    # Task 2: Priority handling
    elif email["priority"] == "high":
        return {
            "type": "priority_handling",
            "email": email,
            "expected_action": "mark_important"
        }

    # Task 3: Personal email → ignore or reply
    elif email["label"] == "personal":
        return {
            "type": "personal_handling",
            "email": email,
            "expected_action": "reply"
        }

    # Task 4: Work email → reply or process
    elif email["label"] == "work":
        return {
            "type": "work_handling",
            "email": email,
            "expected_action": "reply"
        }

    # Fallback
    return {
        "type": "general",
        "email": email,
        "expected_action": "ignore"
    }

def load_tasks():
    """Create task list from dataset"""
    emails = load_emails()

    tasks = []
    for email in emails:
        task = generate_task(email)
        tasks.append(task)

    return tasks