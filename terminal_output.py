from os import get_terminal_size
from math import floor
from textwrap import wrap


def calculate_ratios(terminal_size, rows, header,
                     ratios):

    ratios = [floor(terminal_size * (ratio/sum(ratios))) for ratio in ratios]
    return [ratio for ratio in ratios]


def max_depth(list_obj):
    max_ = 0
    for item in list_obj:
        try:
            max_ = max(len(item), max_)
        except TypeError:
            continue
    return max_


def display_table(rows, header, ratios):
    
    terminal_size = get_terminal_size().columns
    ratios = calculate_ratios(terminal_size, rows, header, ratios)

    template = "".join(["{" f":-^{ratio}" "}" for ratio in ratios])

    header = template.format(*header)

    # Header
    print("=" * terminal_size)
    print(header)
    print("=" * terminal_size)

    print()

    template = str(template).replace("-", " ")

    for reminder in rows:
        to_wrap = []
        temp = list(reminder.to_dict(to_str=True).values())
        for i, item in enumerate(temp):
            temp_str = []
            if len(item) > ratios[i]:
                temp[i], *temp_str = wrap(item, ratios[i])
                to_wrap.append(temp_str)
            else:
                to_wrap.append(0)

        print(template.format(
            *temp
        ))

        print_leftover = []

        depth = max_depth(to_wrap)

        for temp_string in to_wrap:
            if temp_string:
                while len(temp_string) < depth:
                    temp_string.append("")
                print_leftover.append(temp_string)
            else:
                print_leftover.append([""]*depth)

        for column in range(depth):
            to_print = []
            for row in range(len(to_wrap)):
                to_print.append(print_leftover[row][column])
            print(template.format(
                *to_print
            ))
        print()
