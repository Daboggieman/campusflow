
def calculate_priority(urgency, affected_users):
    critical_user_count = 3
    affected_user_threshold = 3
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency =="high" or affected_users >= 8:
        return "high"
    elif urgency == "medium" and affected_users >= 3:
        return "medium"
    else:
        return "low"
    