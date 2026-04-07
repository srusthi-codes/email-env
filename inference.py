import os
from env import EmailEnv

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "")


def run_inference(email_text):
    print("[START] Email AI Running")

    env = EmailEnv()
    state = env.reset()

    total_reward = 0
    email_lower = email_text.lower()

    print("[STEP] Processing email")

    # CATEGORY
    if "meeting" in email_lower or "project" in email_lower:
        category = "work"
    elif "urgent" in email_lower or "asap" in email_lower:
        category = "urgent"
    elif "birthday" in email_lower or "dinner" in email_lower:
        category = "personal"
    elif "offer" in email_lower or "win" in email_lower or "lottery" in email_lower:
        category = "promotion"
    else:
        category = "general"

    # SMART REPLY
    if "urgent" in email_lower:
        reply = "I will handle this urgently."
    elif category == "work":
        reply = "Noted, I will work on this."
    elif category == "personal":
        reply = "Sounds great! Looking forward to it."
    elif "lottery" in email_lower or "win" in email_lower:
        reply = "This looks like spam. Ignoring."
    else:
        reply = "Thanks for your message!"

    # SPAM + URGENCY
    spam = "spam" if ("win" in email_lower or "lottery" in email_lower) else "no"
    urgent = "yes" if "urgent" in email_lower else "no"

    # CONFIDENCE
    confidence = "80%" if category != "general" else "60%"

    # ACTION SUGGESTION
    if spam == "spam":
        suggestion = "Move to Spam Folder"
    elif urgent == "yes":
        suggestion = "Mark as Important"
    else:
        suggestion = "Keep in Inbox"

    action = {
        "spam": spam,
        "category": category,
        "urgent": urgent,
        "reply": reply
    }

    print(f"[STEP] Action: {action}")

    # ENV STEP
    try:
        result = env.step(action)
        if len(result) == 4:
            state, reward, done, _ = result
        else:
            state, reward, done = result

        total_reward += reward

    except Exception as e:
        print(f"[STEP] Error: {e}")
        total_reward = 0

    print(f"[END] Total Reward: {total_reward}")

    return {
        "final_action": action,
        "confidence": confidence,
        "suggestion": suggestion,
        "total_reward": total_reward
    }