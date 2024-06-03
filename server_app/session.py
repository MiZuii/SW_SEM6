import sys
import os
from functools import partial
import time

from dotenv import load_dotenv, find_dotenv
import yaml
import paho.mqtt.client as mqtt

from ogs_scripts import *


config = {}
running = True


def on_connect(cid, client, userdata, flags, rc, *args):
    if rc == 0:
        print(f"[{config['common']['session_prefix']+cid}] Connected with result code " + str(rc), file=sys.stderr)
        client.subscribe(config['common']['client_prefix'] + cid)
    else:
        print(f"[{config['common']['session_prefix']+cid}] Failed to connect, code " + str(rc), file=sys.stderr)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    payload: str
    print("Topic: " + msg.topic + "\nMessage: " + payload, file=sys.stderr)
    pl = payload.split(sep=":")
    payload_type, payload_msg = pl[0], pl[1]

    if payload_type == config['common']['message_types']['data'][:-1]:
        emit_review_append_move(socket, payload_msg, reviewID, userID)
        emit_hostinfo(socket)
    elif payload_type == config['common']['message_types']['config'][:-1]:
        print("not implemented", file=sys.stderr)
    else:
        print("Message Ignored", file=sys.stderr)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Invalid arguments", file=sys.stderr)
        print("Arg1: ID", file=sys.stderr)
        exit(1)
        
    with open("config.yaml", 'r') as stream:
        yaml_config = yaml.safe_load(stream)
        
        try:
            config.update(yaml_config)
        except KeyError as e:
            print("Failed loading configuration", file=sys.stderr)
            raise e
        
    load_dotenv(f'{os.path.dirname(__file__)}/pass.env')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    CLIENT_ID = os.getenv('CLIENT_ID')
    GRANT_TYPE = os.getenv('GRANT_TYPE')

    assert(USERNAME is not None)
    assert(PASSWORD is not None)
    assert(CLIENT_ID is not None)
    assert(GRANT_TYPE is not None)

    cid = sys.argv[1]

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=config['common']['session_prefix'] + cid,
    )

    client.on_connect = partial(on_connect, cid)
    client.on_message = on_message

    client.connect(config['session']['broker_address'], config['session']['broker_port'])

    accessToken = generate_access_token(USERNAME, PASSWORD, CLIENT_ID, GRANT_TYPE)

    ogsconfig = get_ui_config(accessToken)
    chatAuth = ogsconfig['chat_auth']
    notificationAuth = ogsconfig['notification_auth']
    incidentAuth = ogsconfig['incident_auth']
    userID = ogsconfig['user']['id']
    jwt = ogsconfig['user_jwt']
    
    board_name = config['session']['board_name_prefix'] + cid
    reviewID, _ = create_demo_board(accessToken, board_name, 'bplayer', 10, 'wplayer', 10, 19, 19, 'japanese', 'false')
    print(f"Client {cid} created board {reviewID}", file=sys.stderr)

    socket = generate_ogs_socket_handler()
    listen_hostinfo(socket)
    listen_review_full_state(socket, reviewID)
    listen_review_move_response(socket, reviewID)
    emit_authenticate(socket, chatAuth, userID, USERNAME, jwt)
    emit_connect_review(socket, chatAuth, reviewID, userID)
    time.sleep(0.3)

    # start

    client.loop_start()

    while running:
        emit_ping(socket)
        time.sleep(10)
