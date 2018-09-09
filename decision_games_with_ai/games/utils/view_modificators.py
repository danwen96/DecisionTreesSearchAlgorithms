

def create_string_board_from_output(*, should_add_indexes):
    def real_decorator(decorated_function):
        def wrapper(*args, **kwargs):
            lists_with_board_view = decorated_function(*args, **kwargs)

            x_index = b'a'
            y_index = 1

            def get_x_and_increment():
                nonlocal x_index
                x_ind_val = x_index
                x_index = bytes([x_index[0] + 1])
                return x_ind_val.decode('utf-8')

            def get_y_and_increment():
                nonlocal y_index
                y_ind_val = y_index
                y_index += 1
                return str(y_ind_val)

            if should_add_indexes:
                for part_list in reversed(lists_with_board_view):
                    part_list.insert(0, get_y_and_increment())
                lists_with_board_view.append([' '] + [
                    str(get_x_and_increment()) for i in range(len(lists_with_board_view[0])-1)])
            return "\n".join([" ".join(line_list) for line_list in lists_with_board_view])
        return wrapper
    return real_decorator