from typing import Tuple, Dict, Any
import random
from env.models import Observation, Action, Reward
from env.tasks import load_tasks
from env.graders import grade_action
from config.constants import MAX_STEPS


class EmailEnv:
    def __init__(self):
        self.tasks = load_tasks()
        self.current_task = None
        self.current_email = None
        self.step_count = 0
        self.max_steps = MAX_STEPS

        self.history = []
        self.thread_memory = {}

    def reset(self) -> Observation:
        self.current_task = random.choice(self.tasks)
        self.current_email = self.current_task["email"]

        self.step_count = 0
        self.history = []

        thread_id = self.current_email.get("thread_id", "T000")
        self.thread_memory[thread_id] = self.current_email

        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        self.step_count += 1

        # Validate action
        VALID_ACTIONS = ["mark_spam", "mark_important", "reply", "ignore", "escalate"]
        if action.action_type not in VALID_ACTIONS:
            return self._get_observation(), Reward(value=0.0, reason="Invalid action"), True, {}

        # Clean history logging
        entry = action.action_type
        if action.content:
            entry += f": {action.content}"
        self.history.append(entry)

        # Get reward and done from grader
        reward, done = grade_action(self.current_task, action, self.step_count)

        # Enforce max step termination
        if self.step_count >= self.max_steps:
            done = True

        return self._get_observation(), reward, done, {}

    def _get_observation(self) -> Observation:
        email = self.current_email

        return Observation(
            email_id=email["id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            priority=email.get("priority", "low"),
            attachments=email.get("attachments", False),
            thread_id=email.get("thread_id", "T000"),
            history=self.history
        )

    def state(self) -> Dict[str, Any]:
        return {
            "task": self.current_task,
            "history": self.history,
            "step": self.step_count,
            "thread_memory": self.thread_memory
        }