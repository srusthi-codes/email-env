import random
from pydantic import BaseModel

class Observation(BaseModel):
    text: str

class Action(BaseModel):
    spam: str
    category: str
    urgent: str
    reply: str


class EmailEnv:
    def __init__(self):
        self.emails = [
            {"text": "Win a free iPhone now!", "label": "spam", "category": "promotion"},
            {"text": "Limited offer! Buy now", "label": "spam", "category": "promotion"},
            {"text": "Meeting at 5 PM", "label": "not_spam", "category": "work"},
            {"text": "Submit assignment by tonight", "label": "not_spam", "category": "urgent"},
            {"text": "Happy Birthday dear!", "label": "not_spam", "category": "personal"},
            {"text": "Your bank OTP is 1234", "label": "not_spam", "category": "important"},
            {"text": "Congratulations you won lottery", "label": "spam", "category": "promotion"},
            {"text": "Team meeting rescheduled", "label": "not_spam", "category": "work"},
            {"text": "Dinner tonight?", "label": "not_spam", "category": "personal"},
            {"text": "Urgent: Server down fix now", "label": "not_spam", "category": "urgent"}
        ]
        self.current = 0

    def reset(self):
        random.shuffle(self.emails)
        self.current = 0
        return Observation(text=self.emails[self.current]["text"]).dict()

    def state(self):
        return Observation(text=self.emails[self.current]["text"]).dict()

    def step(self, action):
        correct = self.emails[self.current]
        reward = 0.0

        correct_urgency = "yes" if "urgent" in correct["text"].lower() else "no"

        if action.get("urgent") == correct_urgency:
            reward += 0.2

        if action.get("spam") == correct["label"]:
            reward += 0.3

        if action.get("category") == correct["category"]:
            reward += 0.3

        if "reply" in action:
            if any(word in action["reply"].lower() for word in ["thanks", "noted", "received"]):
                reward += 0.2   # reduced from 0.4

        reward = min(reward, 1.0)  # ✅ FIX

        self.current += 1
        done = self.current >= len(self.emails)

        next_state = self.state() if not done else None

        return next_state, reward, done, {}