def input_handler(prompt='Your move (e.g., A2 to B3): '):
    while True:
        user_input = input(prompt).strip()
        if move_parser(user_input):
            return user_input
        else:
            print('Invalid move format. Please try again.')
