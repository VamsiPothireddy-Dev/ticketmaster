"""In-memory "database" — Python dicts standing in for the NoSQL collections.

These dicts are the single source of truth for the running process. All
endpoints read from and mutate them directly, so state changes (e.g. a
ticket moving available -> booked) persist until the app restarts.
Swap the contents for real DB calls later without changing the views.
"""

# eventID -> event document: {performer, eventDate, eventID, location, tickets[]}
EVENTS = {
    "123": {
        "performer": "Taylor Swift",
        "eventDate": "Nov 15 2026",
        "eventID": "123",
        "location": "San Jose",
        "tickets": [f"{i:03d}" for i in range(1, 11)],
    },
    "456": {
        "performer": "Drake",
        "eventDate": "Dec 01 2026",
        "eventID": "456",
        "location": "Los Angeles",
        "tickets": [f"{i:03d}" for i in range(1, 11)],
    },
    "789": {
        "performer": "Beyonce",
        "eventDate": "Jan 10 2027",
        "eventID": "789",
        "location": "New York",
        "tickets": [f"{i:03d}" for i in range(1, 11)],
    },
}

# "<eventID>:<ticketID>" -> ticket document: {EventID, TicketID, Price, status}
# TicketID is only unique within an event, so the composite key is required.
# status: "available" | "booked"
TICKETS = {}
for _event_id, _price in (("123", 250.0), ("456", 180.0), ("789", 300.0)):
    for _i in range(1, 11):
        _tid = f"{_i:03d}"
        TICKETS[f"{_event_id}:{_tid}"] = {
            "EventID": _event_id,
            "TicketID": _tid,
            "Price": _price,
            "status": "available",
            "purchasedBy": None,
        }
TICKETS["123:001"]["status"] = "booked"
TICKETS["456:005"]["status"] = "booked"
