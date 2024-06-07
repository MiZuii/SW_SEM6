import requests

def b64image_to_position(b64image):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'https://www.crazy-sensei.com', 'Referer': 'https://www.crazy-sensei.com/?lang=en&location=kifu_snap'}
    response = requests.post("https://www.crazy-sensei.com/", 
    params={
        "location": "upload_image_ajax"
    },
    headers=headers,
    data={
        'resized_image': b64image
    })
    return response.json()['position'].replace(' ', '')
 
def b64image_to_string(b64image):
    position = b64image_to_position(b64image)

    black_stones = []
    white_stones = []

    for i, c in enumerate(position):
        if c == '.':
            pass
        elif c == 'O':
            white_stones.append(chr(97 + i % 19) + chr(97 + i // 19))
        elif c == '#':
            black_stones.append(chr(97 + i % 19) + chr(97 + i // 19))

    position_string = ""

    for i in range(max(len(black_stones), len(white_stones))):
        try:
            position_string += black_stones[i]
        except IndexError:
            position_string += '..'

        try:
            position_string += white_stones[i]
        except IndexError:
            position_string += '..'

    return position_string