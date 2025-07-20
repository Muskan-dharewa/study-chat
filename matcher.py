import json

DATA_FILE = "users.json"

def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def topic_similarity(t1, t2):
    return len(set(t1) & set(t2)) / max(len(set(t1) | set(t2)), 1)

def match_user_to_group(new_user):
    users = load_users()
    group = []

    for user in users:
        if user["subject"].lower() == new_user["subject"].lower():
            sim = topic_similarity(user["topics"], new_user["topics"])
            if sim >= 0.3:  # Threshold can be adjusted
                group.append(user)

    users.append(new_user)
    save_users(users)

    return {"group": group}
