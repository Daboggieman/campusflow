import unittest
from datetime import datetime
from campusflow.tickets import Ticket, check_title, check_category, check_urgency, check_affected_users

class TestTicket(unittest.TestCase):
    def test_ticket_creation(self):
        ticket = Ticket(
            id="1",
            title="Network issue",
            category="network",
            urgency="high",
            affected_users=15,
            priority="critical",
            status="open",
            assigned_to=False
        )
        self.assertEqual(ticket.title, "Network issue")
        self.assertEqual(ticket.category, "network")
        self.assertEqual(ticket.urgency, "high")
        self.assertEqual(ticket.affected_users, 15)
        self.assertEqual(ticket.priority, "critical")
        self.assertEqual(ticket.status, "open")
        self.assertFalse(ticket.assigned_to)
class TestCheckFunctions(unittest.TestCase):
    def test_check_title(self):
        assert check_title("valid title") == "valid title"
        try:
            check_title("   ")
        except ValueError as e:
            assert str(e) == "Title cannot be blank"

    def test_check_category(self):
        assert check_category("network") == "network"
    try:
            check_category("invalid")
    except ValueError as e:
        assert str(e) == "Choose one of: network, hardware, software, other"

    def test_check_urgency(self):
        assert check_urgency("high") == "high"
    try:
        check_urgency("invalid")
    except ValueError as e:
        assert str(e) == "choose one of: low, medium, high, critical"
    
    def test_check_affected_users(self):
        assert check_affected_users("5") == 5
        try:
            check_affected_users("-1")
        except ValueError as e:
            assert str(e) == "Affected users cannot be negative."
    try:
        check_affected_users("invalid")
    except ValueError as e:
        assert str(e) == "Affected users must be an integer."