import os

from flask import Blueprint, jsonify, request

from app import store

bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/version")
def version():
    return jsonify({"version": os.environ.get("IMAGE_TAG", "unknown")})


@bp.get("/search")
def search():
    """Return all events in partial form — enough for a list/card view.

    Event document fields (NoSQL): performer, eventDate, eventID,
    location, tickets[]. Only performer, location, and eventID are
    exposed here; full details come from /view/<event_id>.
    """
    events = [
        {
            "performer": e.get("performer"),
            "location": e.get("location"),
            "eventID": e.get("eventID"),
        }
        for e in store.EVENTS.values()
    ]
    return jsonify({"count": len(events), "events": events})


@bp.get("/view/<event_id>")
def view(event_id):
    """Full event details for a selected eventID.

    The tickets list only includes tickets that are still available;
    booked ones are filtered out using the TICKETS collection.
    """
    event = store.EVENTS.get(event_id)
    if not event:
        return jsonify({"error": "event not found"}), 404
    available = sorted(
        t["TicketID"]
        for t in store.TICKETS.values()
        if t.get("EventID") == event_id and t.get("status") == "available"
    )
    return jsonify({**event, "tickets": available})


@bp.post("/reserve/<event_id>/<ticket_id>")
def reserve(event_id, ticket_id):
    """Single-phase reservation: book a ticket immediately.

    TicketID is only unique within an event, so both IDs are required.
    Marks the ticket "booked" in the TICKETS collection.
    """
    body = request.get_json(silent=True) or {}
    username = body.get("username")
    if not username:
        return jsonify({"error": "username is required"}), 400

    ticket = store.TICKETS.get(f"{event_id}:{ticket_id}")
    if not ticket:
        return jsonify({"error": "ticket not found"}), 404
    if ticket.get("status") != "available":
        return (
            jsonify(
                {
                    "error": f"ticket is {ticket.get('status')}",
                    "purchasedBy": ticket.get("purchasedBy"),
                }
            ),
            409,
        )

    ticket["status"] = "booked"
    ticket["purchasedBy"] = username
    return jsonify(
        {
            "TicketID": ticket["TicketID"],
            "EventID": ticket.get("EventID"),
            "Price": ticket.get("Price"),
            "status": "booked",
            "purchasedBy": username,
        }
    ), 201
