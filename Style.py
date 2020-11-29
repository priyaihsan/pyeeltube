# format use
# x;xx;xx
# x  = index of style
# xx = foreground
# xx = background

def style(style, fg, bg):
    return "\x1b[{};{};{}m".format(
        style, fg, bg
    )

def end():
    return "\x1b[0m"