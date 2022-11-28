import socket #importing socket programming
import threading # importing threading module to perform multithreading
import time


HEADER = 64 #fixed length header-> A message of 64 bytes will first be receieved from the client which will tell the server about the length of the actual message which will be sent by the client to the server next (If that first message is less that 64 bytes it will still be padded to make its length =64 bytes)
PORT= 5050
SERVER=socket.gethostbyname(socket.gethostname())  # to get the ip address of the current host so as to make it a local server
DISCONNECT_MESSAGE="!DISCONNECT"

print(socket.gethostname()) #will give the name that represents my computer on the network

# to make a socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creating a new socket(server), the first parameter tells about the type of ip address which in this case is ipv4 and second parameter basically tells that the data will be stramed through socket

ADDR= (SERVER,PORT)
FORMAT = 'utf-8' #character encoding

server.bind(ADDR)# binding the socket(server) with this address
# anything connected to this address will hit this socket

def handle_client(conn,addr):  #this function will handle all the communication between the client and the server to handle communication between one client and one server
    print(f"[NEW CONNECTION] {addr} connected.")               #this function will run in parallel for each client
    connected = True
    while connected: #receiving information from the client
        msg_length =conn.recv(HEADER).decode(FORMAT) #number of bytes of message from a client , the line of code will not pass until receive message from our client
        if msg_length: #if message is not null because first message is always a blank message telling about the length of the actual message which will be sent next
             msg_length=int(msg_length)
             msg = conn.recv(msg_length).decode(FORMAT)       #Decode the message from byte stream to the string using utf-8 character encoding
             if msg == DISCONNECT_MESSAGE:  #client gives the message to the server that it wants to disconnect
                connected = False
            
             print(f"[{addr}] {msg}")
             conn.send("Message received".encode(FORMAT))
    conn.close() #close the connection

        #cleanly disconnect the client from the server, if client leaves the connection without informing the server, it won't know that the client has disconnected and hence won't allow the client to reconnect later because it perceives the client to be already connected.
        


def start():           #to start the server  # to handle new connections
    server.listen()    # server starts listening the connections infintely with while loop until we don't want it to listen anymore
    while True:
        conn,addr = server.accept()   #server.accept() waits for a new connection, as soon as a new connection occurs it's ip and port address gets stored in addr and conn is a socket object that will send the information back to server.
        thread = threading.thread(target=handle_client,args =(conn,addr)) # creating a new thread for a client
        thread.start() # starting a thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #to print number of active connections to the server , one starting thread is always there to look for connection so that thread is excluded. Therefore where there are actual two threads running -> one active connection to the server
        
print("[STARTING] server is starting.... ")
start()



















