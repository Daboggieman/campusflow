# CampusFlow: Planning Decisions

Planning record for a Python command-line helpdesk ticket manager · Prepared 9 October 2026 · Owner: Raph'el Ogah

## What this is

CampusFlow is a text-only Python command-line app for Learn2Earn campus staff. It records support problems (Wi-Fi outages, faulty laptops, broken development environments, inaccessible platforms), works out priority, assigns responsibility, and tracks progress. There is no GUI and no website. The menu runs until the user exits.

The priority engine is ordinary Python business logic, not an AI model. AI is used to learn and build, not as the engine.

Every decision below was picked by the owner from at least three options. Items still open are listed at the end.

## 1.1 Understanding the problem

**Decision: Approach A, an Inputs / Process / Outputs / Failures table, one row per feature.**

Template to fill in (one row for each feature):

| Feature | Inputs | What it calculates or does | Outputs | What could go wrong | What must be saved |
| --- | --- | --- | --- | --- | --- |
| F1 Create |  |  |  |  |  |
| F2 List / View |  |  |  |  |  |
| F3 Assign |  |  |  |  |  |
| F4 Workflow |  |  |  |  |  |
| F5 Work queue |  |  |  |  |  |
| F6 Reports |  |  |  |  |  |
| F7 Persistence |  |  |  |  |  |

## 1.2 Ticket fields

Each ticket stores: `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.

Rules from the brief: IDs are unique and generated automatically (T001, T002, ...). Categories are Network, Hardware, Software, Other. Urgency is low, medium or high. The title must not be blank. `affected_users` must be a positive integer. Valid case variations are normalized consistently, and invalid input shows a useful error.

**1.2a How a ticket is held: a dataclass.**

**1.2b Validation: inside the dataclass, so a bad ticket can never be created.** Following the F1 decision, the field checks live in small helper functions. The dataclass calls them, and so does the menu when it asks for each field.

**1.2c Unique IDs: a `latest_ticket_id` value holding the highest ID so far.** To make a new ticket, read the value (for example T029), add 1 to get T030, then update the value to T030. An ID is never reused, even if a ticket is deleted or modified. The value is stored in its own `counter.json` file (see F7) so it survives restarts.

## 1.3 Priority calculation

Rules are checked in this order, and the first match wins:

1. High urgency AND 10 or more affected users: **critical**
2. High urgency OR 10 or more affected users: **high**
3. Medium urgency OR 3 or more affected users: **medium**
4. Everything else: **low**

**1.3a Written as an if / elif chain**, top to bottom, exactly as the rules are listed.

**1.3b Lives in a separate function in its own file** (`priority.py`), so it is easy to test alone.

## 1.4 The seven features

### F1: Create

Ask for one field at a time and re-ask only that field until it is valid, with input validation on every input. Then calculate priority, generate the ID and store the ticket.

### F2: List / View

Two steps. First a short list (ID, title, priority, status). Then the user enters an ID to see full details.

### F3: Assign

The user picks a staff member from a saved staff list. Unknown ticket IDs are rejected. Tickets are kept in memory in a dictionary keyed by ID, so lookup is instant. A resolved ticket cannot be assigned until it is reopened. The staff list is read from \`staff.json\` (see 1.5).

### F4: Workflow

A table of allowed status moves:

| From | Allowed to |
| --- | --- |
| open | in\_progress |
| in\_progress | resolved |
| resolved | open (explicit reopen) |

An `in_progress` ticket cannot go back to `open`. An unassigned ticket cannot move to `in_progress`. A resolved ticket can only be modified after it is reopened.

### F5: Work queue

Shows tickets that are `open` or `in_progress`. Sorted with one sort using a two-part key: (priority rank, numeric ticket number). The rank is critical = 0, high = 1, medium = 2, low = 3. The number inside the ID (the 12 in T012) must be pulled out and sorted as a number, otherwise T100 would sort before T20.

### F6: Reports

Two functions: one works out the numbers (total, counts by status, counts by priority) and returns them, and one prints them. With zero tickets it prints a "no tickets yet" message.

### F7: Persistence

- **Save timing:** after every change.
- **Broken tickets file** (bad JSON, or a ticket that fails the dataclass checks): show the error and ask whether to quit or start fresh. Starting fresh first copies the broken file to a backup name, so nothing is lost.
- **File locations:** `tickets.json`, `counter.json` and the staff list file, all inside a `data/` folder.
- **Counter and tickets disagree at startup** (for example the counter is missing, or lower than the highest ticket): show a warning and ask the user to fix it or quit.
- **Assumption, not yet confirmed:** on a first run with no files, start fresh with the counter at zero, so the first ticket is T001.

## Decision log

| Item | Choice |
| --- | --- |
| 1.1 | A: Inputs / Process / Outputs / Failures table |
| 1.2a | Dataclass |
| 1.2b | Validation inside the dataclass |
| 1.2c | `latest_ticket_id`, kept in `counter.json` |
| 1.3a | if / elif chain |
| 1.3b | Separate function in its own file |
| F1 | One field at a time, re-ask until valid |
| F2 | Short list, then details by ID |
| F3 | Pick from saved staff list, tickets in a dict by ID |
| F4 | Table of allowed moves, no in\_progress back to open, no assigning resolved tickets |
| F5 | One sort, key (priority rank, ticket number), open + in\_progress, lives in `workflow.py` |
| F6 | Count function plus print function, "no tickets yet" when empty |
| F7a | Save after every change |
| F7b | Error, then quit or start fresh with backup copy |
| F7c | Three files inside `data/` |
| F7d | Warn, then ask |
| M1 | List of (label, function) pairs that also builds the menu |
| M2 | Package layout with `tests/` and `docs/`, plus `priority.py`, `test_priority.py`, `test_reports.py` |
| M3 | `unittest` |
| Staff list | Placeholder names created on first run, edited by hand |

## 1.5 Menu, file layout and tests

**M1 Menu loop: a list of (label, function) pairs that also builds the menu text.** Adding a menu option later is one new entry, and the menu display can never drift away from the actions.

**M2 File layout:** the owner's own tree, plus three additions (`priority.py`, `test_priority.py`, `test_reports.py`) and the runtime `data/` folder.

```
campusflow/
├── README.md
├── .gitignore
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── priority.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   ├── test_priority.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   └── test_reports.py
├── data/
│   ├── tickets.json
│   ├── counter.json
│   └── staff.json
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

What each file owns:

- `main.py`: the menu list and the prompts. The prompts call the field checks in `tickets.py`.
- `tickets.py`: the dataclass and the small field-check helpers it calls.
- `priority.py`: the priority function (the if / elif chain).
- `workflow.py`: the table of allowed status moves, the assignment rules and the work queue (F5).
- `storage.py`: loading and saving all three files in `data/`, the broken-file and counter-mismatch handling, and creating `staff.json` on first run.
- `reports.py`: the function that works out the totals and the function that prints them.

**M3 Tests: `unittest`.** Any test that touches files uses a temporary folder, so the real `data/` files are never touched.

**Staff list:** on first run, `storage.py` creates `staff.json` with a few placeholder names so the app is usable straight away. The list is edited by hand for now. An "add staff member" menu option is left out because the brief doesn't ask for it, and it can be added later as one new menu entry.
