import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

tickets = {}
next_ticket = 1001
ticket_lock = threading.Lock()


def handle_client(data, address):
    global next_ticket

    try:
        request = json.loads(data.decode())
        action = request.get("action")

        with ticket_lock:
            if action == "submit":
                complaint = request.get("complaint", "").strip()

                if not complaint:
                    response = {"message": "Complaint cannot be empty."}
                else:
                    ticket_id = next_ticket
                    next_ticket += 1

                    tickets[ticket_id] = {
                        "complaint": complaint,
                        "status": "Open",
                        "resolution": "Not resolved yet"
                    }

                    response = {
                        "message": "Complaint submitted successfully.",
                        "ticket_id": ticket_id,
                        "complaint": complaint,
                        "status": "Open"
                    }

            elif action == "status":
                ticket_id = request.get("ticket_id")

                if ticket_id in tickets:
                    ticket = tickets[ticket_id]
                    response = {
                        "ticket_id": ticket_id,
                        "complaint": ticket["complaint"],
                        "status": ticket["status"],
                        "resolution": ticket["resolution"]
                    }
                else:
                    response = {"message": "Ticket not found."}

            elif action == "resolve":
                ticket_id = request.get("ticket_id")
                resolution = request.get("resolution", "").strip()

                if ticket_id not in tickets:
                    response = {"message": "Ticket not found."}
                elif tickets[ticket_id]["status"] == "Resolved":
                    response = {
                        "message": "Ticket is already resolved.",
                        "ticket_id": ticket_id,
                        "resolution": tickets[ticket_id]["resolution"]
                    }
                elif not resolution:
                    response = {
                        "message": "Resolution message cannot be empty."
                    }
                else:
                    tickets[ticket_id]["status"] = "Resolved"
                    tickets[ticket_id]["resolution"] = resolution

                    response = {
                        "message": "Ticket resolved successfully.",
                        "ticket_id": ticket_id,
                        "status": "Resolved",
                        "resolution": resolution
                    }

            else:
                response = {"message": "Invalid action."}

        server_socket.sendto(json.dumps(response).encode(), address)

    except (json.JSONDecodeError, UnicodeDecodeError):
        server_socket.sendto(
            json.dumps({"message": "Invalid request format."}).encode(),
            address
        )
    except Exception as error:
        print("Error:", error)


print(f"Helpdesk server listening on {HOST}:{PORT}")

while True:
    data, address = server_socket.recvfrom(4096)
    thread = threading.Thread(target=handle_client, args=(data, address))
    thread.start()



