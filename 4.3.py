import turtle as trt

# Ця програма реалізує гру в шашки з наступними правилами:
# 1. Взяття є обов'язковим
# 2. Якщо шашка побила іншу і має змогу побити ще одну, то ця шашка (лише ця!) може і повинна побити ще одну шашку
#    (у такому разі хід закінчується лише тоді, коли ця шашка не може робити ні одну іншу)
# Реалізовано перетворення у дамки; вони виділяються світло- та темно- рожевими кольорами
# Червоний колір рамки поля дошки показує позицію курсора на полі;
# Жовтий - вибрану шашку;
# Зелений - єдину шашку, яка має право робити хід (у разі ситуації у правилі 2)
# Курсор можна переміщати клавішами W / Up, S / Down, A / Left, D / Right, а також кліком миші на відповідне поле
# Enter слугує для вибору шашки (якщо ніяка не вибрана) та для вибору поля для переміщення (якщо деяка шашка вибрана)
# Escape відміняє вибір шашки
# Черга ходу виводиться у консолі 


class Figure:
    def __init__(self, pos, outline_color, fill_color):
        self._pos = pos
        self._outline_color = outline_color
        self._fill_color = fill_color
    def setOutlineColor(self, color):
        self._outline_color = color
    def setFillColor(self, color):
        self._fill_color = color
    def _draw(self):
        pass    # virtual
    def show(self):
        self.setFillColor(self._fill_color)
        self.setOutlineColor(self._outline_color)
        self._draw()
    def hide(self):
        self.setFillColor(trt.bgcolor())
        self.setOutlineColor(trt.bgcolor())
        self._draw()
    def set_pos(self, pos):
        self._pos = pos

class Circle(Figure):
    def __init__(self, pos, outline_color, fill_color, rad):
        Figure.__init__(self, pos, outline_color, fill_color)
        self._rad = rad
    def _draw(self):
        trt.up()
        trt.setpos(self._pos[0], self._pos[1] - self._rad)
        trt.pencolor(self._outline_color)
        trt.fillcolor(self._fill_color)
        trt.down()
        trt.begin_fill()
        trt.circle(self._rad)
        trt.end_fill()

class Square(Figure):
    def __init__(self, pos, outline_color, fill_color, len):
        Figure.__init__(self, pos, outline_color, fill_color)
        self._len = len
    def get_len(self):
        return self._len
    def _draw(self):
        trt.up()
        trt.setpos(self._pos[0], self._pos[1])
        trt.pencolor(self._outline_color)
        trt.fillcolor(self._fill_color)
        trt.down()
        trt.begin_fill()
        trt.setpos(self._pos[0] + self._len, self._pos[1])
        trt.setpos(self._pos[0] + self._len, self._pos[1] + self._len)
        trt.setpos(self._pos[0], self._pos[1] + self._len)
        trt.setpos(self._pos[0], self._pos[1])
        trt.end_fill()
    def draw_outline(self, outline_color):
        trt.up()
        trt.setpos(self._pos[0], self._pos[1])
        trt.pencolor(outline_color)
        trt.down()
        trt.setpos(self._pos[0] + self._len, self._pos[1])
        trt.setpos(self._pos[0] + self._len, self._pos[1] + self._len)
        trt.setpos(self._pos[0], self._pos[1] + self._len)
        trt.setpos(self._pos[0], self._pos[1])

class Board:
    def __init__(self, pos, square):
        self._pos = pos
        self._square = square
    def get_pos(self):
        return self._pos
    def get_square_size(self):
        return self._square.get_len()
    def draw_board(self, fill_color, outline_color):
        self._square.setFillColor(fill_color)
        self._square.setOutlineColor(outline_color)
        for i in range(8):
            for j in range(8):
                self._square.set_pos((self._pos[0] + i * (self._square.get_len() + 1), (self._pos[1] + j * (self._square.get_len() + 1))))
                self._square.show()
    def draw_square(self, pos, fill_color, outline_color):
        self._square.setFillColor(fill_color)
        self._square.setOutlineColor(outline_color)
        self._square.set_pos((self._pos[0] + pos[0] * (self._square.get_len() + 1), (self._pos[1] + pos[1] * (self._square.get_len() + 1))))
        self._square.show()
    def draw_square_out(self, pos, outline_color):
        self._square.set_pos((self._pos[0] + pos[0] * (self._square.get_len() + 1), (self._pos[1] + pos[1] * (self._square.get_len() + 1))))
        self._square.draw_outline(outline_color)

class Game: 
    def __init__(self):
        self._processing_event = False

        self._is_white_turn = True
        
        self._cursor_pos = (0, 0)
        self._chosen_pos = None
        self._special_pos = None
        self._cursor_color = (255, 60, 60)
        self._chosen_color = (255, 255, 0)
        self._special_color = (0, 255, 0)
        self._square_fill_color = (140, 140, 140)
        self._square_out_color = (0, 0, 0)
        self._wq_color = (255, 204, 229)
        self._bq_color = (153, 0, 76)

        self._board = Board((-200, -200), Square((0, 0), self._square_out_color, self._square_fill_color, 50))
        self._checker = Circle((0, 0), (0, 0, 0), (0, 0, 0), 20)
        self._pieces = []
        for i in range(8):
            self._pieces.append([None] * 8)
        for j in range(8):
            if j == 0 or j == 2:
                for i in range(0, 8, 2):
                    self._pieces[i][j] = "w"
            elif j == 1:
                for i in range(1, 8, 2):
                    self._pieces[i][j] = "w"
            elif j == 5 or j == 7:
                for i in range(1, 8, 2):
                    self._pieces[i][j] = "b"
            elif j == 6:
                for i in range(0, 8, 2):
                    self._pieces[i][j] = "b"
    def start(self):
        self._board.draw_board(self._square_fill_color, self._square_out_color)
        for i, col in enumerate(self._pieces):
            for j, piece in enumerate(col):
                if piece != None:
                    self._checker.set_pos((self._board.get_pos()[0] + (i + 0.5) * (self._board.get_square_size() + 1), 
                                           self._board.get_pos()[1] + (j + 0.5) * (self._board.get_square_size() + 1)))
                    if piece == "w":
                        self._checker.setFillColor((255, 255, 255))
                        self._checker.setOutlineColor((255, 255, 255))
                    elif piece == "b":
                        self._checker.setFillColor((0, 0, 0))
                        self._checker.setOutlineColor((0, 0, 0))
                    self._checker.show()
        self._board.draw_square_out(self._cursor_pos, self._cursor_color)
    def _take_is_possible(self, pos):
        if self._pieces[pos[0]][pos[1]] == "w" or self._pieces[pos[0]][pos[1]] == "wq":
            if self._pieces[pos[0]][pos[1]] == "w":
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if 0 <= pos[0] + 2 * i <= 7 and 0 <= pos[1] + 2 * j <= 7:
                            if ((self._pieces[pos[0] + i][pos[1] + j] == "b" or self._pieces[pos[0] + i][pos[1] + j] == "bq") and 
                                 self._pieces[pos[0] + 2 * i][pos[1] + 2 * j] == None):
                                return True
                return False
            else:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        temp = pos[0] + i, pos[1] + j
                        if 0 <= temp[0] <= 7 and 0 <= temp[1] <= 7:
                            if (self._pieces[temp[0]][temp[1]] == "w" or self._pieces[temp[0]][temp[1]] == "wq"):
                                break
                            while 0 <= temp[0] + i <= 7 and 0 <= temp[1] + j <= 7:
                                if (self._pieces[temp[0] + i][temp[1] + j] == "w" or self._pieces[temp[0] + i][temp[1] + j] == "wq"):
                                    break
                                elif self._pieces[temp[0]][temp[1]] != None and self._pieces[temp[0] + i][temp[1] + j] == None:
                                    return True
                                elif self._pieces[temp[0]][temp[1]] != None and self._pieces[temp[0] + i][temp[1] + j] != None:
                                    break
                                else:
                                    temp = temp[0] + i, temp[1] + j
                return False
        elif self._pieces[pos[0]][pos[1]] == "b" or self._pieces[pos[0]][pos[1]] == "bq":
            if self._pieces[pos[0]][pos[1]] == "b":
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if 0 <= pos[0] + 2 * i <= 7 and 0 <= pos[1] + 2 * j <= 7:
                            if ((self._pieces[pos[0] + i][pos[1] + j] == "w" or self._pieces[pos[0] + i][pos[1] + j] == "wq") and 
                                 self._pieces[pos[0] + 2 * i][pos[1] + 2 * j] == None):
                                return True
                return False
            else:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        temp = pos[0] + i, pos[1] + j
                        if 0 <= temp[0] <= 7 and 0 <= temp[1] <= 7:
                            if (self._pieces[temp[0]][temp[1]] == "b" or self._pieces[temp[0]][temp[1]] == "bq"):
                                break
                            while 0 <= temp[0] + i <= 7 and 0 <= temp[1] + j <= 7:
                                if (self._pieces[temp[0] + i][temp[1] + j] == "b" or self._pieces[temp[0] + i][temp[1] + j] == "bq"):
                                    break
                                elif self._pieces[temp[0]][temp[1]] != None and self._pieces[temp[0] + i][temp[1] + j] == None:
                                    return True
                                elif self._pieces[temp[0]][temp[1]] != None and self._pieces[temp[0] + i][temp[1] + j] != None:
                                    break
                                else:
                                    temp = temp[0] + i, temp[1] + j
                return False
    def updateEvents(self, key):
        if not self._processing_event:
            self._processing_event = True
            if key == "Left":
                if self._cursor_pos[0] > 0:
                    self._board.draw_square_out(self._cursor_pos, (0, 0, 0))
                    self._cursor_pos = self._cursor_pos[0] - 1, self._cursor_pos[1]
                    if self._special_pos != None:
                        self._board.draw_square_out(self._special_pos, self._special_color)
                    if self._chosen_pos != None:
                        self._board.draw_square_out(self._chosen_pos, self._chosen_color)
                    self._board.draw_square_out(self._cursor_pos, self._cursor_color)
            elif key == "Right":
                if self._cursor_pos[0] < 7:
                    self._board.draw_square_out(self._cursor_pos, (0, 0, 0))
                    self._cursor_pos = self._cursor_pos[0] + 1, self._cursor_pos[1]
                    if self._special_pos != None:
                        self._board.draw_square_out(self._special_pos, self._special_color)
                    if self._chosen_pos != None:
                        self._board.draw_square_out(self._chosen_pos, self._chosen_color)
                    self._board.draw_square_out(self._cursor_pos, self._cursor_color)
            elif key == "Up":
                if self._cursor_pos[1] < 7:
                    self._board.draw_square_out(self._cursor_pos, (0, 0, 0))
                    self._cursor_pos = self._cursor_pos[0], self._cursor_pos[1] + 1
                    if self._special_pos != None:
                        self._board.draw_square_out(self._special_pos, self._special_color)
                    if self._chosen_pos != None:
                        self._board.draw_square_out(self._chosen_pos, self._chosen_color)
                    self._board.draw_square_out(self._cursor_pos, self._cursor_color)
            elif key == "Down":
                if self._cursor_pos[1] > 0:
                    self._board.draw_square_out(self._cursor_pos, (0, 0, 0))
                    self._cursor_pos = self._cursor_pos[0], self._cursor_pos[1] - 1
                    if self._special_pos != None:
                        self._board.draw_square_out(self._special_pos, self._special_color)
                    if self._chosen_pos != None:
                        self._board.draw_square_out(self._chosen_pos, self._chosen_color)
                    self._board.draw_square_out(self._cursor_pos, self._cursor_color)
            elif key == "Enter":
                if self._chosen_pos == None:
                    if ((self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] == "w" or self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] == "wq") and self._is_white_turn or 
                        (self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] == "b" or self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] == "b") and not self._is_white_turn):
                        self._board.draw_square_out(self._cursor_pos, self._chosen_color)
                        self._chosen_pos = self._cursor_pos
                else:
                    piece_is_taken = False
                    if self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] == None and (self._cursor_pos[0] + self._cursor_pos[1]) % 2 == 0:
                        special_legit = False
                        if self._special_pos != None:
                            if self._special_pos == self._chosen_pos:
                                special_legit = True
                        else:
                            special_legit = True
                        if special_legit:
                            take_legit = False
                            if self._is_white_turn:
                                for i, col in enumerate(self._pieces):
                                    for j, el in enumerate(col):
                                        if el == "w" or el == "wq":
                                            if self._take_is_possible((i, j)):
                                                take_legit = True
                                                break
                                    if take_legit:
                                        break
                            else:
                                for i, col in enumerate(self._pieces):
                                    for j, el in enumerate(col):
                                        if el == "b" or el == "bq":
                                            if self._take_is_possible((i, j)):
                                                take_legit = True
                                                break
                                    if take_legit:
                                        break
                            if (self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "w" or self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "wq") and self._is_white_turn:
                                if self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "w":
                                    if ((self._cursor_pos[0] == self._chosen_pos[0] - 1 or self._cursor_pos[0] == self._chosen_pos[0] + 1) and self._cursor_pos[1] == self._chosen_pos[1] + 1 or
                                         abs(self._cursor_pos[0] - self._chosen_pos[0]) == 2 and abs(self._cursor_pos[1] - self._chosen_pos[1]) == 2):
                                        if take_legit:
                                            if (abs(self._cursor_pos[0] - self._chosen_pos[0]) == 2 and abs(self._cursor_pos[1] - self._chosen_pos[1]) == 2 and
                                               (self._pieces[(self._cursor_pos[0] + self._chosen_pos[0]) // 2][(self._cursor_pos[1] + self._chosen_pos[1]) // 2] == "b" or
                                                self._pieces[(self._cursor_pos[0] + self._chosen_pos[0]) // 2][(self._cursor_pos[1] + self._chosen_pos[1]) // 2] == "bq")):
                                                # take enemy piece
                                                self._pieces[(self._cursor_pos[0] + self._chosen_pos[0]) // 2][(self._cursor_pos[1] + self._chosen_pos[1]) // 2] = None
                                                self._board.draw_square(((self._chosen_pos[0] + self._cursor_pos[0]) // 2, (self._chosen_pos[1] + self._cursor_pos[1]) // 2), self._square_fill_color, self._square_out_color)
                                                piece_is_taken = True
                                                self._special_pos = self._cursor_pos
                                            else:
                                                self._processing_event = False
                                                return
                                        if self._cursor_pos[1] == 7:
                                            # turn to queen
                                            self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] = "wq"
                                            self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] = None
                                            self._board.draw_square(self._chosen_pos, self._square_fill_color, self._square_out_color)
                                            self._checker.setFillColor(self._wq_color)
                                            self._checker.setOutlineColor(self._wq_color)
                                            self._checker.set_pos((self._board.get_pos()[0] + (self._cursor_pos[0] + 0.5) * (self._board.get_square_size() + 1), 
                                                                   self._board.get_pos()[1] + (self._cursor_pos[1] + 0.5) * (self._board.get_square_size() + 1)))
                                            self._checker.show()
                                            self._chosen_pos = None
                                        else:
                                            # default move
                                            self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] = "w"
                                            self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] = None
                                            self._board.draw_square(self._chosen_pos, self._square_fill_color, self._square_out_color)
                                            self._checker.setFillColor((255, 255, 255))
                                            self._checker.setOutlineColor((255, 255, 255))
                                            self._checker.set_pos((self._board.get_pos()[0] + (self._cursor_pos[0] + 0.5) * (self._board.get_square_size() + 1), 
                                                                   self._board.get_pos()[1] + (self._cursor_pos[1] + 0.5) * (self._board.get_square_size() + 1)))
                                            self._checker.show()
                                            self._chosen_pos = None
                                elif self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "wq":
                                    if abs(self._cursor_pos[0] - self._chosen_pos[0]) == abs(self._cursor_pos[1] - self._chosen_pos[1]):
                                        enemies = 0
                                        allies = 0
                                        enemy_pos = None
                                        sign_x = -1 if self._cursor_pos[0] - self._chosen_pos[0] < 0 else 1
                                        sign_y = -1 if self._cursor_pos[1] - self._chosen_pos[1] < 0 else 1
                                        for i in range(1, abs(self._cursor_pos[0] - self._chosen_pos[0])):
                                            temp = (self._chosen_pos[0] + i * sign_x, self._chosen_pos[1] + i * sign_y)
                                            if self._pieces[temp[0]][temp[1]] == "b" or self._pieces[temp[0]][temp[1]] == "bq":
                                                enemies += 1
                                                enemy_pos = temp
                                            if self._pieces[temp[0]][temp[1]] == "w" or self._pieces[temp[0]][temp[1]] == "wq":
                                                allies += 1
                                        if (enemies == 0 or enemies == 1) and allies == 0:
                                            if enemies == 1:
                                                # take enemy piece
                                                self._pieces[enemy_pos[0]][enemy_pos[1]] = None
                                                self._board.draw_square(enemy_pos, self._square_fill_color, self._square_out_color)
                                                piece_is_taken = True
                                                self._special_pos = self._cursor_pos
                                            elif take_legit:
                                                self._processing_event = False
                                                return
                                            # default move
                                            self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] = "wq"
                                            self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] = None
                                            self._board.draw_square(self._chosen_pos, self._square_fill_color, self._square_out_color)
                                            self._checker.setFillColor(self._wq_color)
                                            self._checker.setOutlineColor(self._wq_color)
                                            self._checker.set_pos((self._board.get_pos()[0] + (self._cursor_pos[0] + 0.5) * (self._board.get_square_size() + 1), 
                                                                    self._board.get_pos()[1] + (self._cursor_pos[1] + 0.5) * (self._board.get_square_size() + 1)))
                                            self._checker.show()
                                            self._chosen_pos = None
                                if self._special_pos != None:
                                    if not self._take_is_possible(self._special_pos):
                                        self._is_white_turn = False
                                        self._special_pos = None
                                    else:
                                        self._board.draw_square_out(self._special_pos, self._special_color)
                                else:
                                    self._is_white_turn = False
                                if self._is_white_turn:
                                    print("Turn of White")
                                else:
                                    print("Turn of Black")

                            elif (self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "b" or self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "bq") and not self._is_white_turn:
                                if self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "b":
                                    if ((self._cursor_pos[0] == self._chosen_pos[0] - 1 or self._cursor_pos[0] == self._chosen_pos[0] + 1) and self._cursor_pos[1] == self._chosen_pos[1] - 1 or
                                         abs(self._cursor_pos[0] - self._chosen_pos[0]) == 2 and abs(self._cursor_pos[1] - self._chosen_pos[1]) == 2):
                                        if take_legit:
                                            if (abs(self._cursor_pos[0] - self._chosen_pos[0]) == 2 and abs(self._cursor_pos[1] - self._chosen_pos[1]) == 2 and
                                               (self._pieces[(self._cursor_pos[0] + self._chosen_pos[0]) // 2][(self._cursor_pos[1] + self._chosen_pos[1]) // 2] == "w" or
                                                self._pieces[(self._cursor_pos[0] + self._chosen_pos[0]) // 2][(self._cursor_pos[1] + self._chosen_pos[1]) // 2] == "wq")):
                                                # take enemy piece
                                                self._pieces[(self._cursor_pos[0] + self._chosen_pos[0]) // 2][(self._cursor_pos[1] + self._chosen_pos[1]) // 2] = None
                                                self._board.draw_square(((self._chosen_pos[0] + self._cursor_pos[0]) // 2, (self._chosen_pos[1] + self._cursor_pos[1]) // 2), self._square_fill_color, self._square_out_color)
                                                piece_is_taken = True
                                                self._special_pos = self._cursor_pos
                                            else:
                                                self._processing_event = False
                                                return
                                        if self._cursor_pos[1] == 0:
                                            # turn to queen
                                            self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] = "bq"
                                            self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] = None
                                            self._board.draw_square(self._chosen_pos, self._square_fill_color, self._square_out_color)
                                            self._checker.setFillColor(self._bq_color)
                                            self._checker.setOutlineColor(self._bq_color)
                                            self._checker.set_pos((self._board.get_pos()[0] + (self._cursor_pos[0] + 0.5) * (self._board.get_square_size() + 1), 
                                                                   self._board.get_pos()[1] + (self._cursor_pos[1] + 0.5) * (self._board.get_square_size() + 1)))
                                            self._checker.show()
                                            self._chosen_pos = None
                                        else:
                                            # default move
                                            self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] = "b"
                                            self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] = None
                                            self._board.draw_square(self._chosen_pos, self._square_fill_color, self._square_out_color)
                                            self._checker.setFillColor((0, 0, 0))
                                            self._checker.setOutlineColor((0, 0, 0))
                                            self._checker.set_pos((self._board.get_pos()[0] + (self._cursor_pos[0] + 0.5) * (self._board.get_square_size() + 1), 
                                                                   self._board.get_pos()[1] + (self._cursor_pos[1] + 0.5) * (self._board.get_square_size() + 1)))
                                            self._checker.show()
                                            self._chosen_pos = None
                                elif self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] == "bq":
                                    if abs(self._cursor_pos[0] - self._chosen_pos[0]) == abs(self._cursor_pos[1] - self._chosen_pos[1]):
                                        enemies = 0
                                        allies = 0
                                        enemy_pos = None
                                        sign_x = -1 if self._cursor_pos[0] - self._chosen_pos[0] < 0 else 1
                                        sign_y = -1 if self._cursor_pos[1] - self._chosen_pos[1] < 0 else 1
                                        for i in range(1, abs(self._cursor_pos[0] - self._chosen_pos[0])):
                                            temp = (self._chosen_pos[0] + i * sign_x, self._chosen_pos[1] + i * sign_y)
                                            if self._pieces[temp[0]][temp[1]] == "w" or self._pieces[temp[0]][temp[1]] == "wq":
                                                enemies += 1
                                                enemy_pos = temp
                                            if self._pieces[temp[0]][temp[1]] == "b" or self._pieces[temp[0]][temp[1]] == "bq":
                                                allies += 1
                                        if (enemies == 0 or enemies == 1) and allies == 0:
                                            if enemies == 1:
                                                # take enemy piece
                                                self._pieces[enemy_pos[0]][enemy_pos[1]] = None
                                                self._board.draw_square(enemy_pos, self._square_fill_color, self._square_out_color)
                                                piece_is_taken = True
                                                self._special_pos = self._cursor_pos
                                            elif take_legit:
                                                self._processing_event = False
                                                return
                                            # default move
                                            self._pieces[self._cursor_pos[0]][self._cursor_pos[1]] = "bq"
                                            self._pieces[self._chosen_pos[0]][self._chosen_pos[1]] = None
                                            self._board.draw_square(self._chosen_pos, self._square_fill_color, self._square_out_color)
                                            self._checker.setFillColor(self._bq_color)
                                            self._checker.setOutlineColor(self._bq_color)
                                            self._checker.set_pos((self._board.get_pos()[0] + (self._cursor_pos[0] + 0.5) * (self._board.get_square_size() + 1), 
                                                                    self._board.get_pos()[1] + (self._cursor_pos[1] + 0.5) * (self._board.get_square_size() + 1)))
                                            self._checker.show()
                                            self._chosen_pos = None
                                if self._special_pos != None:
                                    if not self._take_is_possible(self._special_pos):
                                        self._is_white_turn = True
                                        self._special_pos = None
                                    else:
                                        self._board.draw_square_out(self._special_pos, self._special_color)
                                else:
                                    self._is_white_turn = True
                                if self._is_white_turn:
                                    print("Turn of White")
                                else:
                                    print("Turn of Black")

            elif key == "Escape":

                if self._chosen_pos != None:
                    self._board.draw_square_out(self._chosen_pos, (0, 0, 0))
                    self._chosen_pos = None

            self._processing_event = False

################################################################################################################
trt.speed(0)
trt.colormode(255)
trt.hideturtle()
game = Game()
game.start()

def event_left():
    global game
    game.updateEvents("Left")
def event_right():
    global game
    game.updateEvents("Right")
def event_up():
    global game
    game.updateEvents("Up")
def event_down():
    global game
    game.updateEvents("Down")
def event_enter():
    global game
    game.updateEvents("Enter")
def event_escape():
    global game
    game.updateEvents("Escape")
def event_mouse_click(x, y):
    global game
    game._processing_event = True
    if (game._board.get_pos()[0] <= x <= game._board.get_pos()[0] + game._board.get_square_size() * 8 and 
        game._board.get_pos()[1] <= y <= game._board.get_pos()[1] + game._board.get_square_size() * 8):
        pos = int((x - game._board.get_pos()[0]) // game._board.get_square_size()), int((y - game._board.get_pos()[1]) // game._board.get_square_size())
        game._board.draw_square_out(game._cursor_pos, (0, 0, 0))
        game._cursor_pos = pos
        if game._special_pos != None:
            game._board.draw_square_out(game._special_pos, game._special_color)
        if game._chosen_pos != None:
            game._board.draw_square_out(game._chosen_pos, game._chosen_color)
        game._board.draw_square_out(game._cursor_pos, game._cursor_color)
    game._processing_event = False

trt.onkeypress(event_left, "Left")
trt.onkeypress(event_left, "a")
trt.onkeypress(event_right, "Right")
trt.onkeypress(event_right, "d")
trt.onkeypress(event_up, "Up")
trt.onkeypress(event_up, "w")
trt.onkeypress(event_down, "Down")
trt.onkeypress(event_down, "s")
trt.onkeypress(event_enter, "Return")
trt.onkeypress(event_escape, "Escape")
trt.onscreenclick(event_mouse_click)
trt.listen()

trt.mainloop()