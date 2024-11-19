import numpy as np
from colorama  import init
from termcolor import colored


class GoMokuBoard:

    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)  # Aseguramos que los valores sean enteros

    def mark_square(self, row, col, player):
        if self.is_square_available(row, col):
            self.board[row][col] = player

    def is_square_available(self, row, col):
        return self.board[row][col] == 0

    def is_board_full(self):
        return not np.any(self.board == 0)

    def check_win(self, player):

        # Verificar filas
        for row in range(self.rows):
            if self._check_sequence(self.board[row, :], player):
                return True

        # Verificar columnas
        for col in range(self.cols):
            if self._check_sequence(self.board[:, col], player):
                return True

        # Verificar diagonales
        for offset in range(-self.rows + 1, self.cols):

            
            main_diag = self.board.diagonal(offset)  # Diagonal desplazada a la derecha (offset positivo) o izquierda (offset negativo)
            if len(main_diag) >= 5 and self._check_sequence(main_diag, player):
                return True

           
            anti_diag = np.fliplr(self.board).diagonal(offset)  # Diagonal en la matriz volteada horizontalmente
            if len(anti_diag) >= 5 and self._check_sequence(anti_diag, player):
                return True

        return False

    def _check_sequence(self, line, player):
       
        count = 0
        for cell in line:
            if cell == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
        return False
    
    def print_board(self):
        space_cell = "   "
        row_number = 0
        column_number = 0

        print("     ", end="")
        for _ in self.board:
            #impresion de columnas indice 

            if column_number < 10:
                print(str(column_number) + space_cell, end="")
            else:
                print(str(column_number - 10) + space_cell, end="")
            column_number += 1
        
        print("\n")
        
        for row in self.board:
            
            #impresion de filas indice

            if row_number < 10:
                print(" " + str(row_number) + space_cell , end="")
            else:
                print(str(row_number) + space_cell , end="")


            print(space_cell.join(["+" if elem == 0 else "○" if elem == 1 else "●" for elem in row]))

            row_number += 1

        

    def reset_board(self):
        """Reinicia el tablero."""
        self.board = np.zeros((self.rows, self.cols), dtype=int)





