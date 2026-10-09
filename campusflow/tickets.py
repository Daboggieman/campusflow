from dataclasses import dataclass
categories = ["network", "hardware", "software", "other"]
urgencies = ["low", "medium", "high", "critical"]

@dataclass
class Ticket:
    id: str
    title: str
    category: str
    urgency: str
    affected_users: int
    priority: str | "low"
    status: str
    assigned_to: bool
