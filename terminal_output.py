from os import get_terminal_size
from math import ceil
from textwrap import wrap


def display_table(rows, header, ratios):
    terminal_size = get_terminal_size().columns
    remainder = terminal_size // sum(ratios)
    ratios = [ceil(ratio) * remainder for ratio in ratios]
    max_message_len = ratios[2]
    template = ""

    for ratio in ratios:
        template += "{" f":-^{ratio}" "}"

    header = template.format(*header)

    # Header
    print("=" * len(header))

    print(header)

    print("=" * len(header))

    print()
    template = str(template).replace("-", " ")

    for i, reminder in enumerate(rows):
        temp = list(({"priority": i + 1} | reminder.to_dict()).values())
        temp_message = []
        if len(temp[2]) > max_message_len:
            temp[2], *temp_message = wrap(temp[2], max_message_len)
            # print("Message too big!")

        print(template.format(
            *temp
        ))
        for sentence in temp_message:
            print(template.format(
                *["", "", sentence, "", ""]
            ))
    #         print("Printed stuff")
    print("=" * len(header))
