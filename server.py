# Import socket module
from socket import *
#import socket                                                         # Alternative (better) syntax

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Alternative (better) syntax

# Assign a port number
serverPort = 80

#print (hostname is ), gethostname()
# print 'hostname is: ', socket.gethostname()                           # Alternative (better) syntax

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))
# or
# serverSocket.bind((gethostname(), serverPort))
# serverSocket.bind((socket.gethostname(), serverPort))                 # Alternative (better) syntax

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print ("Ready to serve...")
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	print(connectionSocket)
	print(addr)
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receives the request message from the client
		message =  connectionSocket.recv(1024)
		print ('Message is: ', message)
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		first = int(message.split()[0])
		second = int(message.split()[1])
		ans = first+second

		connectionSocket.send(str(ans).encode('utf-8'))
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode('utf-8'))
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode('utf-8'))
		# Close the client connection socket
		connectionSocket.close()

serverSocket.close()  

