import json
from flask import Flask
from flask import request
from flask import jsonify
import const

app = Flask(__name__)

chatsWaitingBD=[]
chatsRelayingBD=[]
chatsSentBD=[]

@app.route('/chat/message', methods=['POST'])
def sendMessage():
    print("RELAYING MSG: " + request.json['text'] + " - FROM: " + request.json['nameSender'] + 
        " - TO: " + request.json['nameDestination'])
    try:
        const.registry[request.json['nameDestination']]
    except:
        return 'NOT OK'
    else:
        dat = {
            'number': request.json['number'],
            'text': request.json['text'],
            'nameSender': request.json['nameSender'],
            'nameDestination': request.json['nameDestination'],
        }
        if request.json['numberReply'] == 0:
            dat['messageReply'] = ''
        else:
            aux = [chat for chat in chatsSentBD if (chat['number'] == request.json['numberReply'])]
            dat['messageReply'] = aux['text']
        chatsWaitingBD.append(dat)
        return 'OK'

@app.route('/chat/message', methods=['GET'])
def relayMessage():
    while True:
        auxChat = chatsWaitingBD
        for chat in auxChat:
            chatsWaitingBD.remove(chat)
            chatsRelayingBD.append(chat)
        auxChat = chatsRelayingBD
        for chat in auxChat:
            dest_addr = const.registry[chat['nameDestination']]
            dest_ip = dest_addr[0]
            dest_port = dest_addr[1]
            if dest_ip == request.json['ip'] and dest_port == request.json['port']:
                chatsRelayingBD.remove(chat)
                chatsSentBD.append(chat)
                return chat

if __name__ == '__main__':
    app.run(host=const.CHAT_SERVER_HOST, port=const.CHAT_SERVER_PORT)