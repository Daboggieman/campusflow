1. Begin the file by defining the function. Name it calculate_priority. Give it two inputs, in this order: urgency first, then affected_users. Two inputs rather than the whole ticket, because the doc's 1.3b decision was to keep this testable on its own — if it needed a fully-built ticket to run, every test would have to construct one first, and you'd be testing the ticket class as much as the priority rules.

2. Write a short description as the first line inside the function, saying what it takes in and what it gives back — something like "takes an urgency and a count of affected users, returns the priority". You'll read this again in three weeks when you've forgotten which way round the parameters go, and it's what stops you calling it with the arguments swapped.

3. Decide on the two thresholds before you write the conditions. The number 10 appears in two rules and the number 3 in one. If you scatter the raw numbers through the conditions, changing the policy later means hunting down each one and hoping you found them all. Name them at the top of the file — one for the critical user count at 10, one for the affected-users threshold at 3 — and use the names in the conditions. It's a small thing now and a real trap later.

The rule chain
4. Write the first condition as an if statement with two parts joined by "and". The first part checks that the urgency is the text high. The second checks that affected_users is greater than or equal to ten. Both have to be true together — that's rule 1 from the doc: high urgency and ten or more users.

5. Immediately inside that if, return the text critical. Then close the block. Nothing else goes inside it.

6. Now write the second rule, and this is the step where the ordering matters. Rather than a fresh if, continue as an "else if" hanging off the first one — so it's only reached when rule 1 was false. Its condition has two parts joined by "or": urgency is high, or affected_users is ten or more. Inside it, return high.

The thing to understand here is that rule 2 is deliberately broader than rule 1 — rule 1 is exactly rule 2 with the "or" swapped for an "and". That means every critical ticket would also satisfy rule 2. The only reason you ever get a critical out of this function is that rule 1 sits above rule 2 and returns before rule 2 is consulted. If you ever reorder these two, critical becomes unreachable and every high-urgency outage quietly reports as merely high.

7. Write the third rule as another else-if. Its condition is urgency is medium, or affected_users is three or more. Return medium.

The subtle part of this one: the user threshold here is 3, which is lower than rule 2's 10. So a medium-urgency ticket affecting ten people satisfies rule 3 — but it never reaches rule 3, because rule 2 already caught it on the user count and returned high. That's the intended behaviour, and it's worth being deliberate about: medium urgency does not mean medium priority when enough people are affected.

8. Finish with a plain else. No condition on it. Inside, return low. This is what catches everything the three rules missed — low urgency and under three users. Using a bare else rather than an else-if with an explicit condition means there's no hole in the chain where a ticket could fall through and return nothing.

What the function should not do
9. No lowercasing, and no checking that the urgency is one of the three valid words. By the time anything calls this, the ticket has already been validated and normalised — "High", "HIGH" and "high" all arrive here as high, because 1.2b put the field checks in tickets.py and the menu calls them before a ticket can exist. If you feel the urge to add a .lower() inside this function, that's the signal that normalisation belongs upstream at the point of input instead. Keeping this function narrow is what makes its tests short: seven assertions and no setup.

10. Return the priority strings in exactly this spelling — critical, high, medium, low. These same four words are what F5's work queue maps to sort ranks, so if the spelling here drifts the queue either sorts wrongly or hits a missing rank.

Then, tests/test_priority.py
11. Create the file and give it a class that inherits from the unittest test case, since M3 settled on unittest.

12. Write one method per row of the case table — the method name should describe the case so a failure tells you what broke without opening the body. Something like "high urgency with ten users gives critical".

13. Inside each method, call the function with the two values and assert the result equals the word you expect. A row passed, a row failed, that's the whole test.

14. Make sure the boundary rows are in there and not just the easy ones. Specifically: high with ten users (not nine), medium with ten users, medium with three (not two). Those are the ones that catch a wrong comparison operator or the two rules in the wrong order — the ordinary cases pass even when the function is subtly wrong.

##

## tickets.py — the dataclass and the field checks. Walking through it in order.

Before the functions: the allowed values
1. Start the file by writing down the two lists of allowed values as names at module level — one for the categories, one for the urgencies. Put them above everything else, since the checks below and the menu later both need them.

Categories are Network, Hardware, Software, Other. Urgencies are low, medium, high.

Watch the capitalisation here, because the doc is inconsistent about it and it will bite you. priority.py compares urgency against lowercase text — "high", "medium" — so your urgency list has to be lowercase or the two modules will never agree. Categories are written capitalised in the doc. Pick the canonical spelling for each list deliberately, because that spelling is what ends up stored in the file.

2. Then import the dataclass decorator from the standard dataclasses module at the top. Nothing else from outside the standard library is needed in this file.

The four field checks
3. Write the title check first. It takes the raw title text the user typed, and it does two things: strip the whitespace off both ends, then check the result isn't empty. If it is empty, raise an error carrying a message that tells the user what's wrong; otherwise hand back the stripped version.

Two reasons this is shaped that way. Stripping before the emptiness test matters because a string of spaces is non-empty but still blank — test first and that sneaks through as a "valid" title. And raising rather than returning a flag is what makes 1.2b's promise real: an exception stops the ticket from being built at all, whereas a returned error code is something a caller can forget to check.

4. Write the category check next. It takes the raw text, compares it against your category list ignoring case, and returns the canonical spelling from that list — not whatever the user typed. If nothing matches, raise with a message naming the valid options.

Returning the canonical spelling is the whole point. The doc asks that "valid case variations are normalized consistently", which means network, Network and NETWORK all have to end up stored as the same value. Compare loosely, store the exact one.

5. Write the urgency check as the same shape against the urgency list, returning the lowercase form. Yes, it's near-identical to the category check, and that's fine — they validate against different lists and raise different messages. You could collapse both into one generic helper that takes the allowed list and the field name as arguments, which is less code; the cost is that the menu's call sites get noisier and the error messages get less specific. Either is defensible, just make it a decision rather than an accident.

6. Write the affected-users check last. This one differs, because it has to convert as well as validate. Remember the menu hands you a string straight from the user, so the first job is turning that text into a whole number — and that conversion itself fails on anything that isn't numeric, which you need to catch and re-raise with a message naming the field rather than letting a bare conversion error escape.

Then check it's positive. The doc says "positive integer", so zero is not allowed — the comparison you want is strictly greater than zero, not greater-or-equal. This is the same off-by-one boundary trap from priority.py, and it's worth a test of its own.

7. Have all four checks accept the rawest possible input — strings from the user — and return the clean, correctly-typed value. The doc says both the dataclass and the menu call these, so they have to work when handed raw input. If they expected already-clean values they'd be useless to the menu, and you'd end up with validation written twice.

The dataclass
8. Declare the dataclass with the eight fields in the doc's order — id, title, category, urgency, affected_users, priority, status, assigned_to.

The ordering rule to keep in mind: any field with a default has to come after every field without one. status starts as "open" and assigned_to starts empty, so those two carry defaults and therefore belong at the end. Put a defaulted field in the middle and the decorator will refuse to build the class at all, before any of your code runs.

9. Decide whether the dataclass is frozen. F4 changes a ticket's status and F3 sets who it's assigned to, so tickets do get modified after creation. A frozen dataclass forces you to build a new ticket and swap it into the dict every time; a normal one lets you just assign the field. There's no requirement in the doc for immutability, so non-frozen is the simpler fit — but decide it now, because it changes the next step.

10. Write the __post_init__ method. This is the hook the dataclass runs automatically right after the object is constructed, and it's where 1.2b's decision actually lives. Inside it, run each of the four checks against its field and assign the returned value back onto that field.

Assigning the result back is not decoration — it's what turns a typed network into a stored Network. And because any failing check raises through this method, construction aborts and no half-valid ticket object is ever returned. That's the "a bad ticket can never be created" guarantee, and it only holds if every check runs in here rather than some of them living at the call sites.

If you did decide on frozen in step 9, you'll have to work around this with the object-level setter, which is a good reason to have picked non-frozen.

11. Decide how priority gets into the ticket, and settle it now. Two options. Either it arrives as a plain required field and whoever creates the ticket works it out first by calling priority.py — which mirrors F1's wording, where "calculate priority" is a step the create flow performs before storing. Or __post_init__ computes it itself from the urgency and user count it already has, which makes a ticket whose priority disagrees with its own fields structurally impossible, at the cost of tickets.py now depending on priority.py.

The second is safer, the first keeps the modules independent and matches how the doc narrates the create flow. Both are reasonable — it's a decision for you, but make it deliberately, because it determines whether the create flow in main.py has a priority step in it at all.

12. Don't validate the id. It comes from the counter in storage.py, never from a user, so there's nothing to correct and nobody to show an error to. If you want a cheap safety net, a check that it matches the T plus digits shape would catch a corrupted counter early, but it's optional and belongs to storage's problem.

Then tests/test_tickets.py
13. For each of the four checks, write three tests: one valid input, one case-variation input where you assert the normalised value comes back, and one invalid input where you assert it raises. The normalisation test is the one that catches a check that validates correctly but forgets to return the canonical form.

14. For the dataclass, two tests: one that a good ticket builds and comes out with normalised fields, and one that a bad field raises and leaves no object behind. The second is the direct test of 1.2b's claim.

15. Test the zero case explicitly on affected users, since that's where the off-by-one lives.