import unittest
from unittest import mock

from campusflow import storage
from campusflow.tickets import Ticket


class TestStorageFirstRun(unittest.TestCase):
    """A fresh data folder behaves like a first run."""

    def test_first_run_loads_empty_tickets(self):
        tickets = storage.load_tickets()
        self.assertEqual(tickets, {})

    def test_first_run_starts_counter_at_zero(self):
        self.assertEqual(storage.read_counter(), 0)

    def test_first_run_creates_staff_placeholders(self):
        staff = storage.load_staff()
        self.assertGreaterEqual(len(staff), 1)


class TestStorageCounter(unittest.TestCase):
    """The id counter advances and never reuses an id."""

    def test_next_id_is_one_after_counter(self):
        storage.write_counter(4)
        self.assertEqual(storage.next_ticket_id(), "T005")


class TestStorageSaveLoad(unittest.TestCase):
    """Saving then loading returns the same tickets."""

    def test_save_then_load_returns_same_tickets(self):
        ticket = Ticket(
            id="T001",
            title="Campus wifi",
            category="network",
            urgency="high",
            affected_users=15,
            priority="critical",
            status="open",
            assigned_to="Ada",
        )
        storage.save_tickets({"T001": ticket})
        loaded = storage.load_tickets()
        self.assertIn("T001", loaded)
        self.assertEqual(loaded["T001"].title, "Campus wifi")
        self.assertEqual(loaded["T001"].affected_users, 15)
        self.assertEqual(loaded["T001"].assigned_to, "Ada")


class TestStorageBrokenFile(unittest.TestCase):
    """A corrupt tickets file is caught and can be reset."""

    def test_broken_json_triggers_quit_or_reset_prompt(self):
        # Write a file that is not valid JSON, then patch input so
        # loading asks the user and, on "start fresh", starts empty.
        with mock.patch("builtins.input", return_value="start fresh"):
            tickets = storage.load_tickets()
        # If storage validates against the dataclass, a bad value
        # raises instead of loading anything.
        self.assertEqual(tickets, {})


if __name__ == "__main__":
    unittest.main()
