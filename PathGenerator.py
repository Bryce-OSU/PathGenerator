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
        If the server receives a json object it will return a dict as a json object with this format:
            key = "path" | value = "file path"
        If the server receives the str "exit" or "quit", the server will stop.
        '''
        while(self._run):
            message = self._socket.recv() # receive message
            try: # try to load message as json
                message = json.loads(message)
                print("Recieved json object:", message)
                self._socket.send_json({"path": "./" + message["name"] + "/" + message["location"] + "/"}) # send file path
            except json.decoder.JSONDecodeError: # if json can't load message
                try: # try to load message as str
                    message = message.decode('utf-8')
                    print("Recieved string:", message)
                    if message == "exit" or message == "quit":
                        self._run = False
                        print("Exiting")
                        self._socket.send_string("Server exiting")
                    else:
                        self._socket.send_string("?")
                except: # message is not json nor str
                    self._socket.send_string("?")

if __name__ == "__main__":
    pg = PathGenerator()
    try:
        pg.run()
    except KeyboardInterrupt:
        print("Exiting")