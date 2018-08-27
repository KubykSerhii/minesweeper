
from minesweeperClasses import *

class Chaos(MainScreen):
    def __init__(self, screen):
        super().__init__(screen)

    def onClick(self, row, column):
        if self.game_over:
            return None
        field = self.fields[row][column]
        field.show()
        if field.is_bomb:
            self.game_over = True
            field.drawActiveBomb()
            MessageWindow('bomb', self.screen)
            return None
        self.bombs += 1
        count_closed_fields = 0
        for item in self.fields:
            for field in item:
                if not field.opened:
                    count_closed_fields += 1
        if count_closed_fields <= self.bombs:
            self.game_over = True
            MessageWindow('win', self.screen)
        else:
            self.redrawBombs()

    def redrawBombs(self):
        for items in self.fields:
            for field in items:
                field.clear()
        # Bombs positions
        curr_bombs = self.bombs
        while curr_bombs > 0:
            position = rand(self.columns * self.rows)
            field = self.fields[position // self.columns][position % self.columns]
            if not field.is_bomb and not field.opened:
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


root = Tk()
Chaos(root)
root.mainloop()