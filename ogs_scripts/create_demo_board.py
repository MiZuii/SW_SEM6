from utility.ogsrest import generate_access_token, create_demo_board
from dotenv import load_dotenv
import os
import sys

load_dotenv("pass.env")
accessToken = generate_access_token(os.environ.get("USERNAME"), 
                                    os.environ.get("PASSWORD"), 
                                    os.environ.get("CLIENT_ID"), 
                                    os.environ.get("GRANT_TYPE"))
board_name = sys.argv[1]
reviewID, _ = create_demo_board(accessToken, board_name, 'bplayer', 10, 'wplayer', 10, 19, 19, 'japanese', 'false')
sys.exit(reviewID)