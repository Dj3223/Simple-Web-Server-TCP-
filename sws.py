import sys
import socket
import threading
import datetime

def handle_Client(conn, addr):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        bad_request = "HTTP/1.0 400 Bad Request\n"
        while connected:
            msg = conn.recv(1024)
            request = msg.decode().split(" ")
            if (len(request) != 3):
                conn.sendall(bytes(bad_request,"utf-8"))
                conn.sendall(bytes(print_Date(conn)+": "+addr[0]+": "+str(addr[1])+": "+msg.decode(), "utf-8"))
                conn.sendall(bytes("Connection: close\n", "utf-8"))
                break
            else :
                if ((request[0] != "GET") or (request[2] != "HTTP/1.0\n")):
                    conn.sendall(bytes(bad_request, "utf-8"))
                    conn.sendall(bytes(print_Date(conn)+": "+addr[0]+": "+str(addr[1])+": "+msg.decode(), "utf-8"))
                    conn.sendall(bytes("Connection: close\n", "utf-8"))
                    break
                else: 
                    filename = request[1].split("/")[1]
            
            try:
                f = open(filename, "r")
                fileFound = True
            except FileNotFoundError:
                fileFound = False

            connection = conn.recv(1024).decode()

            if connection.lower() != "connection: keep-alive\n" and connection.lower() != "connection:keep-alive\n":
                connected = False

            
            if fileFound:
                conn.sendall(bytes("\nHTTP/1.0 200 OK\n", "utf-8"))
                if connected == True:
                    conn.sendall(bytes(print_Date(conn)+": "+addr[0]+": "+str(addr[1])+": "+msg.decode(), "utf-8"))
                    conn.sendall(bytes("Connection: keep-alive\n\n", "utf-8"))
                else:
                    conn.sendall(bytes(print_Date(conn)+": "+addr[0]+": "+str(addr[1])+": "+msg.decode(), "utf-8"))
                    conn.sendall(bytes("Connection: close\n\n", "utf-8"))
                for x in f:
                    conn.sendall(bytes(x, "utf-8"))
                conn.sendall(bytes("\n\n", "utf-8"))
            else:
                conn.sendall(bytes("\nHTTP/1.0 404 Not Found\n", "utf-8"))
                if connected == True:
                    conn.sendall(bytes(print_Date(conn)+": "+addr[0]+": "+str(addr[1])+": "+msg.decode(), "utf-8"))
                    conn.sendall(bytes("Connection: keep-alive\n\n", "utf-8"))
                else:
                    conn.sendall(bytes(print_Date(conn)+": "+addr[0]+": "+str(addr[1])+": "+msg.decode(), "utf-8"))
                    conn.sendall(bytes("Connection: close\n\n", "utf-8"))
        
        conn.close()
    except socket.timeout:
        print(f"[TIMEOUT] {addr} has timed out.")
        conn.close()

def print_Date(conn):
    date = datetime.datetime.now()
    date = datetime.datetime.strftime(date, '%a %b %d %H:%M:%S PDT %Y')
    return date

def start(SERVER_IP, PORT):
    ADDR = (SERVER_IP, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}, PORT {PORT}")

    while True:
        conn, addr = server.accept()
        conn.settimeout(30)
        thread = threading.Thread(target = handle_Client, args = (conn,  addr))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1} ")


def main(argv):
    try:
        if len(argv) != 3:
            print("Invalid number of arguments:")
            print("Please run in the form 'sws.py [IP] [PORT]")
            sys.exit()
        else:
            SERVER = sys.argv[1]
            PORT = int(sys.argv[2])
            print("[SERVER] is starting...")
            start(SERVER,PORT)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

if __name__ == '__main__':
    main(sys.argv)

