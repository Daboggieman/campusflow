from dataclasses import dataclass
categories = ["network", "hardware", "software", "other"]
urgencies = ["low", "medium", "high", "critical"]

@dataclass
class Ticket:
    title: str
    