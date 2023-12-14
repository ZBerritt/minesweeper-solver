def get_box_mouse_position(position: tuple[int, int], box_dimensions: tuple[int, int], board_pos: tuple[int, int]) -> tuple[int, int]:
    top_right_x_pos = position[0] + (box_dimensions[0] * board_pos[0])
    top_right_y_pos = position[1] + (box_dimensions[1] * board_pos[1])
    mouse_x_pos = top_right_x_pos + round(box_dimensions[0] / 2)
    mouse_y_pos = top_right_y_pos + round(box_dimensions[1] / 2)
    return mouse_x_pos, mouse_y_pos

def tile_range(position: tuple[int, int], box_dimensions: tuple[int, int], board_pos: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    left_x = position[0] + (box_dimensions[0] * board_pos[0])
    top_y = position[1] + (box_dimensions[1] * board_pos[1])
    right_x = left_x + box_dimensions[0] - 1
    bottom_y = top_y + box_dimensions[1] - 1
    return (left_x, right_x), (top_y, bottom_y)