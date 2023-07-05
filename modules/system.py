import msvcrt, time, sys
from colorama import Fore as color

COLORCODES = {"&2": color.GREEN, "&f": color.WHITE, "&4": color.RED, "&e": color.YELLOW, "&9": color.LIGHTBLUE_EX, "&a": color.LIGHTGREEN_EX}

def out(out_text: list[str], input_mode: bool = False, end_newline: bool = True, colors: bool = False) -> str:
    for out_line_idx, out_line in enumerate(out_text):
        if colors:
            for text_color in COLORCODES.keys(): out_line = out_line.replace(text_color, COLORCODES.get(text_color))
        for out_char in out_line:
            msvcrt.putwch(out_char)
            sleep(.001)
        if out_line_idx != len(out_text)-1: msvcrt.putwch('\n')

    if input_mode: return input()
    elif end_newline: msvcrt.putwch('\n')


def sleep(duration: float):
    now = time.perf_counter()
    end = now + duration
    while now < end: now = time.perf_counter()

    return
