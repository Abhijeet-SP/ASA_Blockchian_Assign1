import socket
import threading

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) 
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

class PeerNode:

    def __init__(self, team_identifier, listening_port): 
        self.team_identifier = team_identifier
        self.host_ip = get_local_ip()
        self.listening_port = listening_port
        self.connected_peers = {}  

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_ip, self.listening_port))
        self.server_socket.listen(5)

        self.is_running = True
        threading.Thread(target=self.listen_for_incoming_connections, daemon=True).start()

    def listen_for_incoming_connections(self):
        print(f"Server listening on {self.host_ip}:{self.listening_port}...")
        while self.is_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_peer_message, args=(client_socket,), daemon=True).start()
            except OSError:
                break

    def handle_peer_message(self, client_socket):
        while self.is_running:
            try:
                received_data = client_socket.recv(1024).decode()
                if not received_data:
                    break

                data_parts = received_data.split(" ", 2)
                if len(data_parts) < 3:
                    print("Invalid message format received:", received_data)
                    continue

                peer_ip_port, peer_team, peer_message = data_parts
                peer_ip, peer_port = peer_ip_port.split(":")
                
                if peer_message.lower() == "exit":
                    if (peer_ip, peer_port) in self.connected_peers:
                        del self.connected_peers[(peer_ip, peer_port)]
                    print(f"Peer {peer_ip}:{peer_port} ({peer_team}) disconnected.")
                elif peer_message.lower() == "connect":
                    print(f"Received connection message from {peer_ip}:{peer_port} ({peer_team})")
                    self.connected_peers[(peer_ip, peer_port)] = client_socket  
                else:
                    print(f"Message from {peer_ip}:{peer_port} ({peer_team}) -> {peer_message}")
                    self.connected_peers[(peer_ip, peer_port)] = client_socket  
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error handling message: {e}")
                break

        client_socket.close()

    def send_message_to_peer(self, destination_ip, destination_port, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((destination_ip, int(destination_port)))
            formatted_message = f"{self.host_ip}:{self.listening_port} {self.team_identifier} {message}"
            client_socket.send(formatted_message.encode())
            print(f"Message sent to {destination_ip}:{destination_port}")
        except Exception as e:
            print(f"Failed to send message: {e}")
        finally:
            client_socket.close()

    def display_connected_peers(self):
        print("\nConnected Peers:")
        if self.connected_peers:
            for (peer_ip, peer_port) in self.connected_peers.keys():
                print(f"{peer_ip}:{peer_port}")
        else:
            print("No connected peers.")

    def connect_to_known_peers(self):
        print("\nConnecting to known peers...")
        if self.connected_peers:
            for (peer_ip, peer_port) in list(self.connected_peers.keys()):
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((peer_ip, int(peer_port)))
                    client_socket.send(f"{self.host_ip}:{self.listening_port} {self.team_identifier} connect".encode())
                    print(f"Connection message sent to {peer_ip}:{peer_port}")
                except Exception as e:
                    print(f"Failed to connect to {peer_ip}:{peer_port} - {e}")
                finally:
                    client_socket.close()
        else:
            print("No connected peers to connect to.")
    
    def disconnect_from_all_peers(self):
        print("\nDisconnecting from all peers...")
        for (peer_ip, peer_port) in list(self.connected_peers.keys()):
            self.send_message_to_peer(peer_ip, peer_port, "exit")
        self.connected_peers.clear()
        print("Disconnected successfully.")
     
    def stop_peer_server(self):
        self.is_running = False
        self.server_socket.close()

def main():
    team_identifier = input("Enter your team name: ")
    listening_port = int(input("Enter your port number: "))
    peer_node = PeerNode(team_identifier, listening_port)

    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query connected peers")
        print("3. Connect to known peers")
        print("0. Quit")
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            destination_ip = input("Enter recipient's IP address: ")
            destination_port = input("Enter recipient's port number: ")
            message_content = input("Enter your message: ")
            peer_node.send_message_to_peer(destination_ip, destination_port, message_content)
        elif user_choice == "2":
            peer_node.display_connected_peers()
        elif user_choice == "3":
            peer_node.connect_to_known_peers()
        elif user_choice == "0":
            print("Exiting...")
            peer_node.disconnect_from_all_peers() 
            peer_node.stop_peer_server()  
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
