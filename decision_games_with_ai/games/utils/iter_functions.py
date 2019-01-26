from itertools import tee, islice, chain


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


if __name__ == '__main__':
    some_list = ["apple", "banana", "orange"]

    d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    for prev_line, act_line, next_line in previous_and_next(d):
        if prev_line is None:
            prev_line = [None] * len(act_line)
        if next_line is None:
            next_line = [None] * len(act_line)
        print(" prev_line - {},  act_line - {},  next_line - {}".format(
            prev_line, act_line, next_line))

        for up_els, cen_els, dn_els in zip(previous_and_next(prev_line),
                                           previous_and_next(act_line),
                                           previous_and_next(next_line)):
            print("{}    {}    {}".format(up_els, cen_els, dn_els))

