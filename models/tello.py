import threading
import socket
import sys
import time
import threading

from threading import Thread

class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 9000
        self.local_addr = (self.local_ip, self.local_port)

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_addr = (self.tello_ip, self.tello_port)

        self.tello_video_ip = '0.0.0.0'
        self.tello_video_port = 11111
        self.tello_video_addr = (self.tello_video_ip, self.tello_video_port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.local_addr)

        self.response = None
        self.state = None
        self.video_data = None
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.video_socket.bind(self.tello_video_addr)

        self.tello_state_ip = '0.0.0.0'
        self.tello_state_port = 8890
        self.tello_state_addr = (self.tello_state_ip, self.tello_state_port)
        self.state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.state_socket.bind(self.tello_state_addr)

        # Command receiving on new thread
        thread = threading.Thread(target=self.receiver, args=())
        thread.daemon = True
        thread.start()
    

    def receiver(self):
        while True:
            try:
                self.response, _ = self.socket.recvfrom(1024)
                self.state, _ = self.state_socket.recvfrom(1024)
                self.video_data, _ = self.video_socket.recvfrom(2048)
            except Exception as e:
                print(e)
                break


    def send_command_continuous(self, cmd):
        self.socket.sendto(cmd.encode('utf-8'), self.tello_addr)
        

    def send_command_with_response(self, cmd):
        self.socket.sendto(cmd.encode('utf-8'), self.tello_addr)
        
        return self.response


    def end(self):
        self.socket.close()
    

    def get_state(self):
        from collections import defaultdict

        try:
            state = self.state.decode().split(';')
        except Exception as e:
            state = None
            print(e)

        if not state:
            return None

        state_dict = defaultdict(str)

        # last element is newline (/n) - delete it
        del state[-1]

        for item in state:
            key, value = item.split(':')
            state_dict[key] = value
        
        # make json without flask
        #return jsonify(state_dict)
        return None


    def test_rc(self, dx, dy, dz, yaw):
        print(f'I received: {dx}, {dy}, {dz}, {yaw}!')

    def emergency(self):
        self.socket.sendto('emergency'.encode('utf-8'), self.tello_addr)
        self.end()
