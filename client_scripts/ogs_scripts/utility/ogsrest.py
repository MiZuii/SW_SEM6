import requests

def create_demo_board(access_token, board_name, black_name, black_rank, white_name, white_rank, width, height, rules, is_private):
    url = "https://online-go.com/api/v1/demos"
    data = {
        "black_name": black_name,
        "black_ranking": black_rank,
        "height": height,
        "name": board_name,
        "private": is_private,
        "rules": rules,
        "white_name": white_name,
        "white_ranking": white_rank,
        "width": width,
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    demo_board_id = response.json()["id"]
    print(f"Demo board created: {demo_board_id}")
    return demo_board_id, response


def get_ui_config(access_token):
    url = "https://online-go.com/api/v1/ui/config"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    return response.json()

def generate_access_token(username, password, client_id, grant_type):

    url = "https://online-go.com/oauth2/token/"
    data = {
        "grant_type": grant_type,
        "username": username,
        "password": password,
        "client_id": client_id
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    timeout = 20

    response = requests.post(url, data=data, headers=headers, timeout=timeout)
    print(response.request.url)
    print(response.request.headers)
    print(response.request.body)
    print(response.status_code)
    print(response.text)
    # response = requests.post(url, json=data, timeout=timeout)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    access_token = response.json()["access_token"]
    return access_token
