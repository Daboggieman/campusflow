from campusflow.priority import calculate_priority
menu = [
    ("Create_ticket", create_ticket),
    ("List_ticket", List_ticket),
    ("Quit", quit_program),
    ("Assign_ticket", assign_ticket),
    ("Change_status", Change_status),
    ("Work_queue", Work_queue),
    ("Reposts", reposts),
]

def create_ticket():
    global counter
    while True:
        title = input("enter title: ").strip()
        if title:
            break
        print("title cannot be empty".)
    while True:
        category = input("enter category: ").strip()
        if category in categories:
            break
        print("Invalid category")
    while True:
        urgency = input("enter urgency: ").strip()
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
    ticket = {
        "id": counter,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open"
    }

    ticket[counter] = ticket
    counter += 1
    save_data()

    print(f"Ticket created: {ticket}")

def List_ticket():
    for ticket in tickets.value():
        print(
            ticket["id"],
            ticket["title"],
            ticket["priority"],
            tticket["status"],
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
    load_data()
    check_counter()

    while True:
        for number, (label, action) in enumerate(menu, start=1):
            print(f"{number}.{label}")
            
        choice = input("choose an option": )

        try:
            choice = int(choce)
        except ValueError:
            print("Enter a valid menu number.")
            continue
        if not 1 <= choice <= len(menu):
            print("Invalid menu option".)
            continue
        
        action = menu[choice - 1][1]
        action()

        if action == quit_program:
            break