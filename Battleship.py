import curses
import time

size = 10
ships = [5,4,3,3,2]

water="~"
ship="S"
hit="X"
miss="O"


def make_board():
    b=[]
    for i in range(size):
        r=[]
        for j in range(size):
            r.append(water)
        b.append(r)
    return b


def draw(stdscr, board ,y,x, show ,cur):
    for i in range(size):
        for j in range(size):
            ch = board[i][j]
            if show == False and ch == ship:
                ch = water

            if cur != None and cur[0]==i and cur[1]==j:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y+i , x+j*2 , ch)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y+i , x+j*2 , ch)


def all_dead(b):
    for i in b:
        if ship in i:
            return False
    return True


def put_ship(b , r , c , s , h):
    try:
        if h == True:
            for i in range(s):
                if b[r][c+i] != water:
                    return False

            for i in range(s):
                b[r][c+i] = ship
        else:
            for i in range(s):
                if b[r+i][c] != water:
                    return False

            for i in range(s):
                b[r+i][c] = ship

        return True
    except:
        return False


def setup(stdscr , b , name):
    cur=[0,0]
    hor=True
    i=0

    while i < len(ships):
        s = ships[i]
        placed=False

        while placed == False:
            stdscr.clear()
            stdscr.addstr(0,2,name+" place ship size "+str(s))
            stdscr.addstr(1,2,"Arrow move, R rotate, ENTER put")
            stdscr.addstr(2,2,"Dir: "+("HORIZONTAL" if hor else "VERTICAL"))

            draw(stdscr , b , 4 , 2 , True , cur)
            stdscr.refresh()

            k = stdscr.getch()

            if k == curses.KEY_UP:
                cur[0] = cur[0] - 1
                if cur[0] < 0:
                    cur[0] = 0
            elif k == curses.KEY_DOWN:
                cur[0] = cur[0] + 1
                if cur[0] > 9:
                    cur[0] = 9
            elif k == curses.KEY_LEFT:
                cur[1] -= 1
                if cur[1] < 0:
                    cur[1] = 0
            elif k == curses.KEY_RIGHT:
                cur[1] += 1
                if cur[1] > 9:
                    cur[1] = 9
            elif k == ord("r") or k == ord("R"):
                hor = not hor
            elif k == 10:
                ok = put_ship(b , cur[0] , cur[1] , s , hor)
                if ok:
                    placed = True
                else:
                    # invalid place
                    pass

        stdscr.addstr(16,2,"Placed ship!")
        stdscr.refresh()
        time.sleep(0.4)

        i=i+1


def shoot(b , r , c):
    if b[r][c] == ship:
        b[r][c] = hit
        return "HIT"
    if b[r][c] == water:
        b[r][c] = miss
        return "MISS"
    
    return "AGAIN"


def turn(stdscr , me , en , name):
    cur=[0,0]
    msg="ENTER to fire"

    done=False

    while done == False:
        stdscr.clear()

        stdscr.addstr(0,2,name+" TURN")
        stdscr.addstr(1,2,msg)

        stdscr.addstr(3,2,"Your Board")
        draw(stdscr , me , 4 , 2 , True , None)

        stdscr.addstr(3,30,"Enemy Board")
        draw(stdscr , en , 4 , 30 , False , cur)

        stdscr.refresh()
        k = stdscr.getch()

        if k == curses.KEY_UP:
            cur[0]-=1
            if cur[0] < 0: cur[0]=0
        elif k == curses.KEY_DOWN:
            cur[0]+=1
            if cur[0] > 9: cur[0]=9
        elif k == curses.KEY_LEFT:
            cur[1]-=1
            if cur[1] < 0: cur[1]=0
        elif k == curses.KEY_RIGHT:
            cur[1]+=1
            if cur[1] > 9: cur[1]=9
        elif k == 10:
            r = shoot(en , cur[0] , cur[1])

            if r == "AGAIN":
                msg = "Already there"
            else:
                msg = name+" "+r
                stdscr.refresh()
                time.sleep(1)
                done=True


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    p1 = make_board()
    p2 = make_board()

    setup(stdscr , p1 , "PLAYER 1")
    stdscr.clear()
    stdscr.addstr(10,10,"Player 1 done, press key")
    stdscr.getch()

    setup(stdscr , p2 , "PLAYER 2")
    stdscr.clear()
    stdscr.addstr(10,10,"Player 2 done, press key")
    stdscr.getch()

    t = 1

    while True:
        if t == 1:
            turn(stdscr , p1 , p2 , "PLAYER 1")

            if all_dead(p2):
                stdscr.clear()
                stdscr.addstr(10,10,"PLAYER 1 WINS")
                stdscr.refresh()
                time.sleep(3)
                break

            t = 2

        else:
            turn(stdscr , p2 , p1 , "PLAYER 2")

            if all_dead(p1):
                stdscr.clear()
                stdscr.addstr(10,10,"PLAYER 2 WINS")
                stdscr.refresh()
                time.sleep(3)
                break

            t = 1


curses.wrapper(main)
