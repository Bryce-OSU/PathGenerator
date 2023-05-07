# PathGenerator
This program generates a file path given the following information: user name and location.

This program sets up a local server using the ZeroMQ libraries. Unless specified, it will connect to the port: "5555". To start the server just run the PathGenerator.py file like any other python file. For example:
```
python3 PathGenerator.py
```
To send and receive data from the server, please connect to the server: "tcp://localhost:5555" using the socket type: "REQ"

### Quick Guide
There are 2 things that can be sent to the server. Anything else and the server will send a error message back.
1) A dictionary as a json object. The dictionary must include values at these keys: "user_name" and "location". The server will return a file path as a dictionary. the file path will be at the key: "path". The file path will be in this format: "./user_name/pictures/location/"
2) Either "quit" or "exit". This will tell the server to shutdown.


### How to REQUEST data
There are two ways to request that the server does an action.
1) Send a string.
The sent string will be used to command the server to do something. There are two commands, "exit" and "quit", but they do the same thing, they shutdown the server.
The string must be encoded into raw bytes before sending to the server. If using ZeroMQ, using the function send_string() will encode the string for you.
Example call:
```
socket.send_string("exit")
```

2) Send a dictionary as a json object.
The sent dictionary will be used to generate a file path. The dictionary must contain the following keys: "user_name" and "location". If it doesn't contain both of those keys, the server will return an error. Otherwise it will generate a file path using the values at those key index.
The dictionary must be dumped before sending to the server. If using ZeroMQ, using the function send_json() will dump the dictionary for you.
Example call:
```
socket.send_json({
    "user_name": "bob",
    "location": "nagoya_japan"
})
```

### How to RECEIVE data
After requesting data (i.e. sending a message to the server), one will need to receive the data from the server. If the message sent to the server was a string, the returned message will also be a string. If the message sent to the server was a json object, the returned message may be a json object or a string (if an error occured). Returned messages will also be encoded or dumped, so the user will need to account for this. If using ZeroMQ, the functions recv_string() and recv_json() will handle the decoding and loading respectivly.

If no error occurred when sending a dictionary to the server, the server will create a new dictionary containing the generated file path and place it in the message queue. The generated dictionary will have one entry. The key will be "path" and the value will be the generated file path.
Using the above example, the generated dictionary will be:
```
{"path": "./bob/pictures/nagoya_japan/}
```
To receive this from the server, use:
```
path = socket.recv_json()
```

### UML sequence diagram
![alt text](https://github.com/Bryce-OSU/PathGenerator/blob/master/UML_Sequence_Diagram.png?raw=true)