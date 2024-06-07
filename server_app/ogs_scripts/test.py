from time import sleep
import os
from dotenv import load_dotenv, find_dotenv

from utility.ogsrest import *
from utility.ogsrealtime import *

if __name__ == "__main__":

    load_dotenv(f'{os.path.dirname(__file__)}/pass.env')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    CLIENT_ID = os.getenv('CLIENT_ID')
    GRANT_TYPE = os.getenv('GRANT_TYPE')

    assert(USERNAME is not None)
    assert(PASSWORD is not None)
    assert(CLIENT_ID is not None)
    assert(GRANT_TYPE is not None)

    accessToken = generate_access_token(USERNAME, PASSWORD, CLIENT_ID, GRANT_TYPE)

    config = get_ui_config(accessToken)
    chatAuth = config['chat_auth']
    notificationAuth = config['notification_auth']
    incidentAuth = config['incident_auth']
    userID = config['user']['id']
    jwt = config['user_jwt']
    
    board_name = "test_board"

    reviewID, _ = create_demo_board(accessToken, board_name, 'bplayer', 10, 'wplayer', 10, 19, 19, 'japanese', 'false')
    print(reviewID)

    socket = generate_ogs_socket_handler()
    listen_hostinfo(socket)
    listen_review_full_state(socket, reviewID)
    listen_review_move_response(socket, reviewID)
    emit_authenticate(socket, chatAuth, userID, USERNAME, jwt)
    emit_connect_review(socket, chatAuth, reviewID, userID)
    sleep(1)
    emit_review_append_move(socket, 'avsdfpoij', reviewID, userID)
    emit_hostinfo(socket)