def move_parser(command):
    try:
        start_pos, end_pos = command.lower().split(' to ')
        start_col, start_row = ord(start_pos[0]) - ord('a'), int(start_pos[1]) - 1
        end_col, end_row = ord(end_pos[0]) - ord('a'), int(end_pos[1]) - 1
        if 0 <= start_col < 8 and 0 <= start_row < 8 and 0 <= end_col < 8 and 0 <= end_row < 8:
            return start_row, start_col, end_row, end_col
        else:
            return None
    except (ValueError, IndexError):
        return None
