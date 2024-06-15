import torch

def results_to_coordinates(results):
    cls = results[0].boxes.cls.tolist()
    conf = results[0].boxes.conf.tolist()
    xywh = results[0].boxes.xywh.tolist()

    try:
        g_idx = cls.index(2.)
    except Exception:
        return [], []
    g_width = xywh[g_idx][2]
    g_height = xywh[g_idx][3]
    g_xmin = xywh[g_idx][0] - g_width / 2
    g_xmax = xywh[g_idx][0] + g_width / 2
    g_ymin = xywh[g_idx][1] - g_height / 2
    g_ymax = xywh[g_idx][1] + g_height / 2

    cell_width = g_width // 19
    cell_height = g_height // 19

    idx_to_delete = []

    for i in range(len(cls)):
        if cls[i] == 2.:
            idx_to_delete.append(i)

    for idx in idx_to_delete[::-1]:
        del cls[idx]
        del conf[idx]
        del xywh[idx]

    black_stones = []
    white_stones = []

    for stone, confidence, coords in zip(cls, conf, xywh):
        if confidence > 0.5:
            x_coord = coords[0]
            y_coord = coords[1]
            if x_coord >= g_xmin and x_coord <= g_xmax and y_coord >= g_ymin and y_coord <= g_ymax:
                int_coords = (round((x_coord - g_xmin) / cell_width) - 1, round((y_coord - g_ymin) / cell_height) - 1)
                if int_coords not in black_stones and int_coords not in white_stones:
                    if stone == 1.:
                        black_stones.append(int_coords)
                    elif stone == 3.:
                        white_stones.append(int_coords)

    return black_stones, white_stones

def results_to_string(results):
    black_stones, white_stones = results_to_coordinates(results)

    moves = ""

    for i in range(max(len(black_stones), len(white_stones))):
        try:
            moves = moves + chr(97 + black_stones[i][0]) + chr(97 + black_stones[i][1])
        except Exception:
            moves = moves + ".."

        try:
            moves = moves + chr(97 + white_stones[i][0]) + chr(97 + white_stones[i][1])
        except Exception:
            moves = moves + ".."

    return moves