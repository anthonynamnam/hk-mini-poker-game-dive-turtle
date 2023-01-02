import time

import setting


def print_border(border="=", width=setting.ScreenWidth):
    print(border * width)


def print_line(
    text,
    width=setting.ScreenWidth,
    border="|",
    add_space=0,
    cut_space=0,
    left_more_right=0,
    right_more_left=0,
):
    assert left_more_right == 0 or right_more_left == 0
    empty_space_left = (
        width - len(border) * 2 - len(text) + add_space - cut_space
    ) // 2
    empty_space_right = (
        width - len(border) * 2 - len(text) + add_space - cut_space - empty_space_left
    )
    empty_space_left = empty_space_left - left_more_right + right_more_left
    empty_space_right = empty_space_right - right_more_left + left_more_right
    print(f"{border}{' '*empty_space_left}{text}{' '*empty_space_right}{border}")


#   Check if there is any space in the string
#   Input format:   list[str ... str][str,str]
#   Return format:  list[str ... str][str,str]
def check_if_any_space(string):
    for x in string:
        if x == "":
            return True
    return False


#   Delete all empty space in string
#   Input format:   str
#   Return format:  str
def delete_empty_space(inputstring):
    shorten = ""
    for x in inputstring:
        if not x == " ":
            shorten = shorten + x
    return shorten


#   display_heading -- Display a heading with specific format
#   Input format:   (str)
#   Return format:  None
def display_heading(texttoshow, tabNum):
    width = len(texttoshow)
    boundary = ""
    tab = ""
    for x in range(width):
        boundary = boundary + "="
    for y in range(tabNum):
        tab = tab + "\t"
    print(tab + boundary)
    print(tab + texttoshow)
    print(tab + boundary)


#   print_text_with_time_interval -- print the text with few times with certain time interval
#   Input format:   (str, int, float)
#   Return format:  None
def print_text_with_time_interval(showtext, showntime, interval):
    print("")
    for x in range(0, showntime):
        print("\t   " + showtext)
        if setting.Waiting:
            time.sleep(interval)
    print("")
