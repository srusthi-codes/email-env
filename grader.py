def grade(action, correct_email):
    score = 0.0

    if action.get("spam") == correct_email["label"]:
        score += 0.4

    if action.get("category") == correct_email["category"]:
        score += 0.3

    correct_urgency = "yes" if "urgent" in correct_email["text"].lower() else "no"

    if action.get("urgent") == correct_urgency:
        score += 0.3

    return min(score, 1.0)