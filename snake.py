#!/usr/bin/python

## Maybe make it go in an infinite loop
## restarting itself every time the game
## is over.
## Only way to exit would be to press q

import curses
import random
import time
import sys
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

X = 40
Y = 12

## Optional throw this garbage away

if len(sys.argv) > 2:
    if is_number(sys.argv[1]):
        if is_number(sys.argv[2]):
            n = int(sys.argv[1])
            m = int(sys.argv[2])
            if n % 2 == 0:
                if m % 2 == 0:
                    if n < 81:
                        if m < 25:
                            X = n
                            Y = m

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)


global screen
screen = [[' ' for i in range(Y+2)] for j in range(X+2)]

global LEN
LEN = 10

def curses_close(scr):
    curses.nocbreak()
    scr.keypad(0)
    curses.echo()
    curses.endwin()
    return

def erase(scr,y,x):
    try: scr.addch( y , x , ' ')
    except curses.error: pass
    screen[x][y] = ' '
    return

def move(scr,y,x):
    try: scr.addch( y , x , '*')
    except curses.error: pass
    screen[x][y] = '*'
    return

def draw_boundary(scr,Y,X):
    for i in range(0,Y):
        move(scr,i,X)
        move(scr,i,0)
    for i in range(0,X):
        move(scr,Y,i)
        move(scr,0,i)
    scr.refresh()
    return

global record
record = [[Y/2,X/2]]

def push(x,y):
    record.append([y,x])

def pop(scr):
    erase(scr,record[0][0],record[0][1])
    for i in range(len(record)):
        if i == len(record)-1:
            break
        record[i] = record[i + 1]
    record.pop()
    return

global rand
rand = 0

global nrand
nrand = 0

def randomize(scr):
    rx = random.randint(1,X-1)
    ry = random.randint(1,Y-1)
    if screen[rx][ry] == '*':
        return randomize(scr)
    jem(scr,ry,rx)
    return
    
def jem(scr,y,x):
    try: scr.addch( y , x , '#')
    except curses.error: pass
    screen[x][y] = '#'
    return

def update_points(scr):
    scr.addstr(Y+2,1,"Points " + str(nrand) + "    Length: " + str(LEN))
    scr.refresh()
    

def end_game():
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
    os.system("clear")
    for j in range(Y+1):
        for i in range(X+1):
            sys.stdout.write(screen[i][j])
        print 
    sys.stdout.write('\n')
    print " Points: " + str(nrand) + "    Length: " + str(LEN)
    print
    print " Score: " + str(nrand*LEN)
    print
    sys.stdout.flush()
    exit()

draw_boundary(stdscr,Y,X)
stdscr.addstr(Y/2,X/2,"*")
stdscr.refresh()

x = X/2
y = Y/2
xdir = 0
ydir = 0 
len2 = 0

rand = 1
randomize(stdscr)
LEN = 10
update_points(stdscr)

while 1:
    curses.halfdelay(1)
    ch = stdscr.getch()
    try: 
        if ch == curses.KEY_LEFT:
            ydir = 0
            xdir = -1
        elif ch == curses.KEY_RIGHT:
            xdir = +1
            ydir = 0
        elif ch == curses.KEY_UP:
            ydir = -1
            xdir = 0
        elif ch == curses.KEY_DOWN:
            ydir = 1
            xdir = 0
        elif ch == ord('q'):
            end_game()

        if xdir == 0:
            if ydir == 0:
                continue

        y = y + ydir
        x = x + xdir

        if screen[x][y] == '*':
            end_game()

        if screen[x][y] == '#':
            erase(stdscr,y,x)
            LEN = LEN + random.randint(1,nrand+1)
            rand = 0

    except:
        raise
    
    move(stdscr,y,x)
    push(x,y)
    stdscr.refresh()

    len2 = len2 + 1
    if len2 > LEN:
        len2 = len2 - 1
        pop(stdscr)

    if rand == 0:
        randomize(stdscr)
        rand = 1
        nrand = nrand + 1

    update_points(stdscr)


