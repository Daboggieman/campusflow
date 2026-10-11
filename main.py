from campusflow.priority import calculate_priority
from campusflow.tickets import categories, urgencies, Ticket
from campusflow.storage import load_json, load_counter,tickets, save_json
from campusflow.workflow import move_ticket, assign_ticket, get_work_queue

def create_ticket():
    global counter
    while True:
        title = input("enter title: ").strip().lower()
        if title:
            break
        print("title cannot be empty")
    while True:
        category = input("enter category: ").strip().lower()
        if category in categories:
            break
        print("Invalid category")
    while True:
        urgency = input("enter urgency: ").strip().lower()
        if urgency in urgencies:
            break
        print("Invalid urgency")
    while True:
        try:
            affected_users = int(input("enter affected users: "))
            if affected_users > 0:
                break
            print("enter a number greater than zero.")
        except ValueError:
            print("enter a whole number.")
    priority = calculate_priority(urgency, affected_users)
    ticket = Ticket(
        id=id,
        title=title,
        category=category,
        urgency=urgency,
        affected_users=affected_users,
        priority=priority,
        status="open",
        assigned_to= False,
    )

    tickets[counter] = ticket
    counter += 1
    save_json()

    print(f"Ticket created: {ticket}")

def List_ticket():
    for ticket in tickets.values():
        print(
            ticket["id"],
            ticket["title"],
            ticket["priority"],
            ticket["status"],
        )

    try:
        ticket_id = int(input("enter ticket ID to view: "))
    except ValueError:
        print("Invalid ticket id.")
        return

    if ticket_id not in tickets:
        print("Ticket not found.")
        return

    print(tickets[ticket_id])

def main():
    load_json()
    load_counter()

    while True:
        for number, (label, action) in enumerate(menu, start=1):
            print(f"{number}.{label}")
            
        choice = input("choose an option: ")

        try:
            choice = int(choice)
        except ValueError:
            print("Enter a valid menu number.")
            continue
        if not 1 <= choice <= len(menu):
            print("Invalid menu option")
            continue
        
        action = menu[choice - 1][1]
        action()

menu = [
    ("Create ticket", create_ticket,)
    ("Move ticket", move_ticket)
    ("Assign ticket", assign_ticket),
    ("Work queue", get_work_queue),
    ("List_ticket", List_ticket)
]