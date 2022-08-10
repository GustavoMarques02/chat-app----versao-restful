from email import message
import requests
import sys
import threading
import json
import const

class Client:

    def __init__(self):
        self.me = str(sys.argv[1])
        self.url = 'http://' + const.CHAT_SERVER_HOST + ':' + const.CHAT_SERVER_PORT + '/chat/message'
        threading.Thread(target=self.__listen_for_messages).start()

        while True:
            dest = input("ENTER DESTINATION: ")
            msg = input("ENTER MESSAGE: ")
            message = {
                'text': msg,
                'nameDestination': dest,
                'nameSende': self.me
            }
            response = requests.post(self.url, json=message).text
            if not response == 'OK':
                print("Error: Destination does not exist")


    def __listen_for_messages(self):
        me_addr = const.registry[self.me]
        me_ip = me_addr[0]
        me_port = me_addr[1]
        dat = {
            'ip': me_ip,
            'port': me_port
        }
        while True:
            message = requests.get(self.url, json=dat).text
            message = json.loads(message)
            print("\nMESSAGE: " + message['text'] + " - FROM: " + message['nameSender'])

if __name__ == '__main__':
    c = Client()