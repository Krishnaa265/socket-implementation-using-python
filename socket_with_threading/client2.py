

import socket
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5)


def send_request(request):
    try:
        data = json.dumps(request).encode()
        client_socket.sendto(data, (SERVER_HOST, SERVER_PORT))
        response, address = client_socket.recvfrom(4096)
        return json.loads(response.decode())

    except socket.timeout:
        return {"message": "Server did not respond. Try again."}
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"message": "Invalid response received from server."}
    except OSError as error:
        return {"message": f"Network error: {error}"}


while True:
    print("\n===== IT HELPDESK SYSTEM =====")
    print("1. Submit Complaint")
    print("2. Check Ticket Status")
    print("3. Resolve Ticket")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        complaint = input("Enter your complaint: ")
        response = send_request({
            "action": "submit",
            "complaint": complaint
        })

        for key, value in response.items():
            print(f"{key}: {value}")

    elif choice == "2":
        try:
            ticket_id = int(input("Enter ticket number: "))
            response = send_request({
                "action": "status",
                "ticket_id": ticket_id
            })

            for key, value in response.items():
                print(f"{key}: {value}")

        except ValueError:
            print("Please enter a valid ticket number.")

    elif choice == "3":
        try:
            ticket_id = int(input("Enter ticket number to resolve: "))
            resolution = input("Enter resolution message: ")

            response = send_request({
                "action": "resolve",
                "ticket_id": ticket_id,
                "resolution": resolution
            })

            for key, value in response.items():
                print(f"{key}: {value}")

        except ValueError:
            print("Please enter a valid ticket number.")

    elif choice == "4":
        print("Exiting IT Helpdesk System.")
        break

    else:
        print("Invalid choice. Please try again.")

client_socket.close()