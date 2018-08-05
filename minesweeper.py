from tkinter import *
from random import randrange as rand


class MainScreen:
    def __init__(self, screen):
        self.min_columns = 9
        self.min_rows = 9
        self.max_columns = 30
        self.max_rows = 20
        self.min_bombs = 1
        self.columns = 9
        self.rows = 9
        self.bombs = 10
        self.fields = []
        self.size_field = 30
        self.game_over = False
        self.canvas = None
        self.screen = screen
        self.screen.title('Minesweeper by Serhii Kubyk')
        self.screen.resizable(False, False)
        self.drawWidgets()
        self.creeateNewGame()

    def drawWidgets(self):
        self.label_rows = Label(self.screen, text='Rows:')
        self.label_rows.place(x=0, y=7)
        self.entry_rows = Entry(self.screen, width=4, justify='center')
        self.entry_rows.place(x=35, y=7)
        self.entry_rows.insert(0, self.rows)
        self.label_columns = Label(self.screen, text='Columns:')
        self.label_columns.place(x=60, y=7)
        self.entry_columns = Entry(self.screen, width=4, justify='center')
        self.entry_columns.place(x=115, y=7)
        self.entry_columns.insert(0, self.columns)
        self.label_bombs = Label(self.screen, text='Bombs:')
        self.label_bombs.place(x=140, y=7)
        self.entry_bombs = Entry(self.screen, width=4, justify='center')
        self.entry_bombs.place(x=185, y=7)
        self.entry_bombs.insert(0, self.bombs)
        self.button_new_game = Button(self.screen, text='New Game')
        self.button_new_game.place(x=220, y=2)
        self.button_new_game.bind('<Button-1>', lambda x: self.creeateNewGame())

    def drawCanvas(self):
        self.canvas = Canvas(self.screen, width=self.columns*(self.size_field+1), height=self.rows*(self.size_field+1), bg='grey')
        self.canvas.place(x=10, y=30)
        for i in range(1, self.columns):
            self.canvas.create_line(i*(self.size_field+1)+2, 0, i*(self.size_field+1)+2, self.rows*(self.size_field+1)+2)
        for i in range(1, self.rows):
            self.canvas.create_line(0, i*(self.size_field+1)+2, self.columns*(self.size_field+1)+2, i*(self.size_field+1)+2)

    def creeateNewGame(self):
        self.game_over = False
        self.checkOnDigit(self.entry_rows)
        self.rows = min(max(int(self.entry_rows.get()), self.min_rows), self.max_rows)
        self.entry_rows.delete(0, END)
        self.entry_rows.insert(0, self.rows)
        self.checkOnDigit(self.entry_columns)
        self.columns = min(max(int(self.entry_columns.get()), self.min_columns),self.max_columns)
        self.entry_columns.delete(0, END)
        self.entry_columns.insert(0, self.columns)
        self.checkOnDigit(self.entry_bombs)
        self.bombs = min(max(int(self.entry_bombs.get()), self.min_bombs), self.columns*self.rows)
        self.entry_bombs.delete(0, END)
        self.entry_bombs.insert(0, self.bombs)
        self.screen.geometry(str(self.columns*(self.size_field+1)+25)+'x'+str(self.rows*(self.size_field+1)+40))
        if self.canvas:
            self.canvas.destroy()
        self.drawCanvas()
        # Create all fields
        self.fields = [[Field(j, i, self) for i in range(self.columns)] for j in range(self.rows)]
        # Bombs positions
        curr_bombs = self.bombs
        while curr_bombs > 0:
            position = rand(self.columns*self.rows)
            field = self.fields[position // self.columns][position % self.columns]
            if not field.is_bomb:
                field.drawBomb()
                curr_bombs -= 1
        # Calculate neighbour bombs
        for col in self.fields:
            for field in col:
                if field.is_bomb:
                    for pos in range(8):
                        n_field = self.getNeighbourField(field, pos)
                        if field is not n_field and not n_field.is_bomb:
                            n_field.neighbour_Bombs += 1
        for col in self.fields:
            for field in col:
                field.drawCountNeighbourBombs()

    def onClick(self, row, column):
        if self.game_over:
            return None
        empty_fields = []
        field = self.fields[row][column]
        field.show()
        if field.is_bomb:
            self.game_over = True
            field.drawActiveBomb()
            MessageWindow('bomb')
            return None
        if field.neighbour_Bombs == 0:
            empty_fields.append(field)
            while empty_fields:
                field = empty_fields.pop()
                for pos in range(8):
                    neighbour_field = self.getNeighbourField(field, pos)
                    if neighbour_field is not field and not neighbour_field.opened:
                        neighbour_field.show()
                        if neighbour_field.neighbour_Bombs == 0:
                            empty_fields.append(neighbour_field)
        count_closed_fields = 0
        for item in self.fields:
            for field in item:
                if not field.opened:
                    count_closed_fields += 1
        if count_closed_fields == self.bombs:
            self.game_over = True
            MessageWindow('win')

    def checkOnDigit(self, widget):
        if not all([c in '0123456789' for c in widget.get()]):
            widget.delete(0, END)
            widget.insert(0, 10)

    def getNeighbourField(self, field, pos):
        new_row = 0
        new_column = 0
        if pos == 0:
            new_row = field.row - 1
            new_column = field.column
        elif pos == 1:
            new_row = field.row - 1
            new_column = field.column + 1
        elif pos == 2:
            new_row = field.row
            new_column = field.column + 1
        elif pos == 3:
            new_row = field.row + 1
            new_column = field.column + 1
        elif pos == 4:
            new_row = field.row + 1
            new_column = field.column
        elif pos == 5:
            new_row = field.row + 1
            new_column = field.column - 1
        elif pos == 6:
            new_row = field.row
            new_column = field.column - 1
        elif pos == 7:
            new_row = field.row - 1
            new_column = field.column - 1
        if 0 <= new_row < self.rows and 0 <= new_column < self.columns:
            return self.fields[new_row][new_column]
        return field


class Field:
    def __init__(self, row, column, main_screen):
        self.size = main_screen.size_field
        self.row = row
        self.column = column
        self.x = column*(self.size+1)+3
        self.y = row*(self.size+1)+3
        self.main_screen = main_screen
        self.canvas = main_screen.canvas
        self.is_bomb = False
        self.opened = False
        self.flag = 0
        self.neighbour_Bombs = 0
        self.drawFrame()

    def drawFrame(self):
        self.frame = Frame(self.main_screen.canvas, width=self.size, height=self.size, relief='raised', borderwidth=3)
        self.frame.place(x=self.x, y=self.y)
        self.frame.bind('<Button-1>', lambda x: self.main_screen.onClick(self.row, self.column))
        self.frame.bind('<Button-3>', self.drawFlag)

    def drawBomb(self):
        self.is_bomb = True
        self.canvas.create_oval(self.x+self.size//3, self.y+self.size//3, self.x+self.size//3*2, self.y+self.size//3*2, fill='black')
        self.canvas.create_line(self.x+self.size//5, self.y+self.size//5, self.x+self.size//5*4, self.y+self.size//5*4, width=1)
        self.canvas.create_line(self.x+self.size//5*4, self.y+self.size//5, self.x+self.size//5, self.y+self.size//5*4, width=1)

    def drawActiveBomb(self):
        self.canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size, fill='red4')
        self.drawBomb()

    def drawCountNeighbourBombs(self):
        colors = ['blue', 'dark green', 'red', 'purple4', 'brown4', 'navy', 'yellow', 'dark violet']
        if self.neighbour_Bombs > 0:
            self.canvas.create_text(self.x+self.size//2,
                                    self.y+self.size//2,
                                    text=self.neighbour_Bombs,
                                    fill=colors[self.neighbour_Bombs-1],
                                    font='Times ' + str(self.size//2) + ' bold')
    def drawFlag(self, event):
        self.flag = not self.flag
        if self.flag:
            self.flag_canvas = Canvas(self.frame, width=self.size-10, height=self.size-10)
            self.flag_canvas.place(x=0, y=0)
            self.flag_canvas.create_line(self.size//6, self.size//10, self.size//6, self.size-self.size//5)
            self.flag_canvas.create_rectangle(self.size//6, self.size//10, self.size-self.size//3, self.size//2, fill='coral')
            self.flag_canvas.bind('<Button-3>', self.drawFlag)
        else:
            self.flag_canvas.destroy()

    def show(self):
        self.frame.destroy()
        self.opened = True


class MessageWindow(Toplevel):
    def __init__(self, result):
        super().__init__(root)
        self.title('Message Window')
        self.geometry('250x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.canvas = Canvas(self, width=250, height=100, bg='grey76')
        self.canvas.place(x=0, y=0)
        self.canvas.create_text(120, 40, text='You win!!!' if result == 'win' else 'You lose!!!', fill='blue', font='Times 20 bold')


root = Tk()
MainScreen(root)
root.mainloop()
