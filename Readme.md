# Peer-to-Peer Networking System

This project implements a Peer-to-Peer (P2P) Networking System that enables multiple peers to communicate directly with each other in a decentralized network. The program supports:

1. **Simultaneous message sending and receiving**
2. **Querying and retrieving a list of active peers**
3. **Connecting to all active peers**
4. **Graceful disconnection from peers**

Each peer runs an independent instance of the program in a terminal environment, allowing real-time message exchange and dynamic peer discovery.

## Authors:
| Name                 | Roll No       |
|----------------------|--------------|
| Abhash Raj          | 230001002     |
| Sanat Kumar Sukla   | 230005043     |
| Abhijeet Singh Parihar | 230005001 |

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Instructions to Use](#instructions-to-use)
3. [Features](#features)
4. [How the System Works](#how-the-system-works)
5. [Setup and Execution](#setup-and-execution)
6. [Menu Options](#menu-options)
7. [Peer Disconnection and Shutdown](#peer-disconnection-and-shutdown)

---

## Project Overview
This Peer-to-Peer (P2P) networking system enables direct communication between peers over a network using Python sockets. Each peer acts as both a client and a server, allowing them to receive and send messages simultaneously. The system supports querying connected peers and dynamically establishing connections with new peers.

---

## Features

1. **Simultaneous Communication**: Each peer can send and receive messages simultaneously using multi-threading.
2. **Active Peer Querying**: Retrieve the list of peers currently interacting with a given peer.
3. **Auto-Connection to Active Peers**: Establish connections with peers who have sent messages to the current peer.
4. **Dynamic Peer Management**: Peers can join and leave the network without affecting other connections.
5. **Graceful Disconnection**: Notify all connected peers before exiting the network.

---

## How the System Works

- Each peer runs a server socket listening for incoming connections.
- Peers send messages to each other using a client socket.
- The system tracks connected peers and manages their details.
- Peers can request a list of all known peers and establish new connections dynamically.
- On exiting, peers notify others and close all active connections.

---

## Setup and Execution

### Prerequisites
Ensure Python 3.x is installed on your system.

### Clone the Repository
```bash
   git clone https://github.com/Abhijeet-SP/ASA_Blockchian_Assign1.git
```

### Running Multiple Peers
To simulate multiple peers, open multiple terminal windows and run the program in each:
```bash
   python3 peer.py
```
After execution, each instance will prompt you to enter a port number for communication:
# you can give port as per your choice
```bash
   Enter your port number: port_number  
```

---

## Menu Options
```bash
   1. Send message
   2. Query connected peers
   3. Connect to active peers
   0. Quit
```

### 1. Send Message
- Send a message to a peer by entering their IP address, port number, and message content.
- The message format ensures that both sender and receiver details are recorded.

### 2. Query Connected Peers
- Displays a list of all peers currently interacting with the user.
- If no peers are connected, a notification is displayed.

### 3. Connect to Active Peers
- Attempts to establish a direct connection with all peers that have sent messages previously.
- If the connection is successful, the peer is added to the active peer list.

### 0. Quit
- Disconnects from all peers before safely shutting down the program.

---

## Peer Disconnection and Shutdown
When a peer decides to leave the network, the following steps occur:
1. **Notification to Peers**: Sends a "disconnect" message to all connected peers.
2. **Clearing Peer List**: Removes all peer details from the local database.
3. **Closing the Server Socket**: Stops listening for new connections.
4. **Program Termination**: Exits gracefully without affecting other peers.

---

This Peer-to-Peer networking system provides a foundation for decentralized communication, with future scope for additional features such as encryption, authentication, and file sharing.
