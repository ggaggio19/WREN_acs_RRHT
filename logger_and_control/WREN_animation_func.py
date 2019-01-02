import datetime as dt
import matplotlib.pyplot as plt


# This function is called periodically from FuncAnimation
def animate(i, ys, val_l, x_len, line):
    val = val_l[0]
    # Add y to list
    ys.append(val)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step
