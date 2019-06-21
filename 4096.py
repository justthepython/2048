import curses
import numpy
from random import randrange, choice,randint
from collections import defaultdict
letter=[ord(ch) for ch in 'WSADQRwsadqr']
actions=['up','down','left','right','exit','restart']
actions_dict=dict(zip(letter,actions*2))
separater='+------'
def get_user_action(keyboard):
	char=keyboard.getch()
	if char in letter:
		return actions_dict[char]
	else:
		pass
def transpose(matrix):
	return numpy.transpose(matrix)
def invert(matrix):
	return [row[::-1] for row in matrix]
class Matrix_Deal(object):
    def __init__(self, Win = 2048):
        self.win_score=Win
    def reset(self):
        self.field=[[0 for i in range(4)] for j in range(4)]
        self.refresh()
    def refresh(self):
        i, j = (2 if randint(0, 101) > 20 else 4), (2 if randint(0, 101) > 20 else 4)
        m=[i,j]
        for k in range(2):
            (x,y)=choice([(x,y) for x in range(4) for y in range(4) if self.field[x][y]==0])
            self.field[x][y]=m[k]
        def draw(self, screen):
            screen.addstr('Score: %s' %self.score)
            for row in self.field:
                screen.addstr(separater * 4 + '+' + '\n')
                screen.addstr(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|' + '\n')
            screen.addstr(separater * 4 + '+' + '\n')
            help_string1 = '(W)Up (S)Down (A)Left (D)Right'
            help_string2 = '     (R)Restart (Q)Exit'
            screen.addstr(help_string1 + '\n')
            screen.addstr(help_string2 + '\n')
    def move(self,action):
            def move_left(row):
                def squeeze(matrix):
                    new_row = [i for i in matrix if i != 0]
                    return new_row
                def extend(mat):
                    for j in range(4 - len(mat)):
                        mat.append(0)
                    return mat
                new_row = squeeze(row)
                for i in range(len(new_row)):
                    if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                        new_row[i] = new_row[i] * 2
                        new_row[i + 1] = 0
                    else:
                        new_row[i] = new_row[i]
                new_row = extend(squeeze(new_row))
                return new_row
            moves={}
            moves['left'] = lambda field:\
                                [move_left(row) for row in self.field]
            moves['up'] = lambda field:\
                                transpose([move_left(row) for row in transpose(self.field)])
            moves['right'] = lambda field:\
                                invert([move_left(row) for row in invert(self.field)])
            moves['down'] = lambda field:\
                                transpose(invert([move_left(row) for row in invert(transpose(self.field))]))
            self.field=moves[action](self.field)

def main(stdscr):
    def start():
        matrix_deal.reset()
        return 'Game'
    def game():
        global field
        stdscr.clear()
        matrix_deal.draw(stdscr)
        action=get_user_action(stdscr)
        if action=='up' or action=='down' or action=='left' or action=='right':
            matrix_deal.move(action)
            matrix_deal.refresh()
            return 'Game'
        elif action=='exit':
            return 'exit'
        elif action=='restart':
                return 'restart'
        else:
            return 'Game'
    states={'restart':start,'init':start,'Game':game}
    matrix_deal = Matrix_Deal(Win=2048)
    state = 'init'
    while state!='exit':
        state = states[state]()
curses.wrapper(main)
