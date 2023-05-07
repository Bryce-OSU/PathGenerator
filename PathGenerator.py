import zmq, json

class PathGenerator:
    def __init__(self, port = "5555") -> None:
        '''
        Init for PathGenerator.

        param port: str - default "5555"
        '''
        self._run = True # boolean to keep the server running
        self._hostName = "localhost"
        self._port = port # socket port, default "5555"
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP) # use zmq.REQ as client
        self._socket.bind("tcp://*:%s" % (self._port))
        print("Server started http://%s:%s" % (self._hostName, self._port))

    def run(self):
        '''
        Run ZeroMQ server at assigned port.
        The server will only except a dumped json object or a string.
        If the server receives a json object it will return a dict as a json object with this format:
            key = "path" | value = "file path"
        If the server receives the str "exit" or "quit", the server will stop.
        '''
        while(self._run):
            message = self._socket.recv() # receive message
            message = self.generate_return_message(message) # generate a return message
            self.send(message) # send message

    def send(self, message):
        '''
        Send the given message.
        The sent message will either be a string or a dumped json object.

        param message:  any
        '''
        print("Sending: ", message)
        if type(message) == str: # message is a string
            self._socket.send_string(message)
        elif type(message) == dict: # message is a dictionary
            self._socket.send_json(message)
        else: # message is neither a string nor a dictionary
            self._socket.send_string("Unrecognized format")

    def generate_return_message(self, message):
        '''
        If the given message is a string send to "command"
        If the given message is a dictionary send to "generate_file_path"
        Else the message is something else and can't be used by this program, return error

        param message:  any
        '''
        message = self.convert(message) # convert message into something useful
        if type(message) == str: 
            message = self.command(message)
        elif type(message) == dict:
            message = self.generate_file_path(message)
        else:
            message = "Unrecognized format"
        return message

    def convert(self, message):
        '''
        Tries to convert the given message into a json object. 
        If that fails, try to convert it into a string. 
        If that also fails return an error string.

        param message:  any
        '''
        try: # try to load message as json
            message = json.loads(message)
        except json.decoder.JSONDecodeError: # if json can't load message
            try: # try to load message as str
                message = message.decode('utf-8')
            except: # message is not json nor str
                message = "Unrecognized format"
        return message
    
    def command(self, message):
        '''
        Execute the command from the given message if it is a understood command.
        Other wise return an error.

        param message:  str
        '''
        if message == "exit" or message == "quit":
            self._run = False
            print("Exiting")
            return "Server exiting"
        else:
            print("Recieved message is an unrecognized command")
            return "Unrecognized command"

    def generate_file_path(self, message):
        '''
        Try to create a file path using info from the given message.
        If the info can't be found from the message, return an error.

        param message:  dict
        '''
        print("Received message is a json object")
        try:
            user_name = message["user_name"]
            location = message['location']
            return json.dumps({"path": "./" + user_name + "/pictures/" + location + "/"})
        except KeyError:
            return "Couldn't find the key 'user_name' or 'location'"


if __name__ == "__main__":
    pg = PathGenerator()
    try:
        pg.run()
    except KeyboardInterrupt:
        print("Exiting")