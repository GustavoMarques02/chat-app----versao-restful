from flask import Flask
from flask import request
from flask import jsonify
import const

app = Flask(__name__)

chatsWaitingBD=[]
chatsRelayingBD=[]

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
            'text': request.json['text'],
            'nameSender': request.json['nameSender'],
            'nameDestination': request.json['nameDestination']
        }
        chatsWaitingBD.append(dat)
        return 'OK'

@app.route('/chat/message', methods=['GET'])
def relayMessage():
    while True:
        auxChat = chatsWaitingBD
        for c in auxChat:
            chatsWaitingBD.remove(c)
            chatsRelayingBD.append(c)
        auxChat = chatsRelayingBD
        for c in auxChat:
            dest_addr = const.registry[c['nameDestination']]
            dest_ip = dest_addr[0]
            dest_port = dest_addr[1]
            if dest_ip == request.json['ip'] and dest_port == request.json['port']:
                    chatsRelayingBD.remove(c)
                    return jsonify(c)

if __name__ == '__main__':
    app.run(host=const.CHAT_SERVER_HOST, port=const.CHAT_SERVER_PORT)