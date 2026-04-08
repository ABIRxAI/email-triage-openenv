from env.models import Reward
from config.constants import REWARD_CONFIG
from env.utils import is_phishing, is_promotional


def grade_action(task, action, step):
    email = task["email"]
    expected = task["expected_action"]

    reward = 0.0
    reason = []
    done = False

    # Correct / Wrong action
    if action.action_type == expected:
        reward += REWARD_CONFIG["correct_action"]
        reason.append("Correct action")
        done = True
    else:
        reward += REWARD_CONFIG["wrong_action"]
        reason.append("Wrong action")

    # Spam / phishing detection
    if is_phishing(email) or is_promotional(email):
        if action.action_type == "mark_spam":
            reward += REWARD_CONFIG["spam_bonus"]
            reason.append("Correct spam detection")
        else:
            reward -= 0.3
            reason.append("Missed spam/phishing")
    else:
        if action.action_type == "mark_spam":
            reward -= 0.3
            reason.append("Incorrect spam classification")

    # Priority handling
    if email.get("priority") == "high":
        if action.action_type == "mark_important":
            reward += REWARD_CONFIG["priority_bonus"]
            reason.append("Handled high priority")

        elif action.action_type == "ignore":
            reward += REWARD_CONFIG["ignore_urgent_penalty"]
            reason.append("Ignored urgent email")

        else:
            reward -= 0.2
            reason.append("Suboptimal handling of urgent email")

    # Reply quality
    if expected == "reply":
        if action.content:
            content_lower = action.content.lower()
            if any(word in content_lower for word in ["thanks", "sorry", "okay"]):
                reward += 0.3
                reason.append("Good reply tone")
            else:
                reward += 0.1
                reason.append("Basic reply")
        else:
            reward -= 0.2
            reason.append("No reply content")

    # Attachment awareness
    if email.get("attachments"):
        if action.action_type in ["reply", "mark_important"]:
            reward += 0.2
            reason.append("Handled attachment email")
        elif action.action_type == "ignore":
            reward += REWARD_CONFIG["attachment_ignore_penalty"]
            reason.append("Ignored attachment email")

    # Step penalty & termination
    if step >= 5:
        reward += REWARD_CONFIG["step_penalty"]
        reason.append("Too many steps")
        done = True

    # Normalize reward to [0, 1]
    reward = round(max(0.0, min(1.0, reward)),3)

    return Reward(
        value=reward,
        reason=" | ".join(reason)
    ), done