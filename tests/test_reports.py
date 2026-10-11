import unittest
from io import StringIO
from contextlib import redirect_stdout

from campusflow.reports import summarize, print_report


def make_ticket(
    ticket_id="T001",
    priority="medium",
    status="open",
):
    return {
        "id": ticket_id,
        "title": "Network issue",
        "category": "network",
        "urgency": "medium",
        "affected_users": 5,
        "priority": priority,
        "status": status,
        "assigned_to": None,
    }


class TestSummarize(unittest.TestCase):
    """summarize should count tickets by status and priority."""

    def test_empty_tickets_gives_zero_counts(self):
        summary = summarize({})
        self.assertEqual(summary["total"], 0)
        self.assertEqual(sum(summary["by_status"].values()), 0)
        self.assertEqual(sum(summary["by_priority"].values()), 0)

    def test_totals_by_status_and_priority(self):
        tickets = {
            "T001": make_ticket("T001", "high", "open"),
            "T002": make_ticket("T002", "medium", "in_progress"),
            "T003": make_ticket("T003", "low", "resolved"),
            "T004": make_ticket("T004", "critical", "open"),
        }
        summary = summarize(tickets)
        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["by_status"]["open"], 2)
        self.assertEqual(summary["by_status"]["in_progress"], 1)
        self.assertEqual(summary["by_status"]["resolved"], 1)
        self.assertEqual(summary["by_priority"]["critical"], 1)
        self.assertEqual(summary["by_priority"]["high"], 1)
        self.assertEqual(summary["by_priority"]["medium"], 1)
        self.assertEqual(summary["by_priority"]["low"], 1)


class TestPrintReport(unittest.TestCase):
    """The printer is a separate function from the counter."""

    def test_empty_prints_no_tickets_yet(self):
        buf = StringIO()
        with redirect_stdout(buf):
            print_report(summarize({}))
        self.assertIn("no tickets yet", buf.getvalue())

    def test_nonempty_prints_totals(self):
        tickets = {
            "T001": make_ticket("T001", "high", "open"),
            "T002": make_ticket("T002", "medium", "resolved"),
        }
        buf = StringIO()
        with redirect_stdout(buf):
            print_report(summarize(tickets))
        out = buf.getvalue()
        self.assertIn("total", out.lower())
        self.assertIn("2", out)
        self.assertIn("open", out)
        self.assertIn("high", out)


if __name__ == "__main__":
    unittest.main()
