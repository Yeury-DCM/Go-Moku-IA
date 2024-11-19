from Board import GoMokuBoard
import copy
from MinimaxSolver import MinimaxSolver
import random
import numpy as np
import os

class GameSesion:

    def __init__(self, players = None, board = None, current_player = 1, minimax_time = 1):
        
        self.players = (1,2)
        self.board = GoMokuBoard()
        self.current_player = current_player
        self.minimax_time = minimax_time
    
    def play_turn(self,  option):
        row = option[0]
        col = option[1]
        self.board.mark_square(row,col, self.current_player)
        self.current_player = self.current_player % 2 + 1
       
       
        
    
    def get_available_desicions(self):

        options = []

        for row in range (self.board.rows):
            for col in range (self.board.cols):
                if self.board.is_square_available(row, col):
                    options.append((row,col))

        return options
    
    def get_winners_points(self):
        
        result_dict = {}

        if self.board.check_win(1):  # Si el jugador 1 gana
            result_dict[1] = 1000
            result_dict[2] = -1000

        elif self.board.check_win(2):  # Si el jugador 2 gana
            result_dict[1] = -1000
            result_dict[2] = 1000

        else:  # En caso de empate
            result_dict[1] = 0
            result_dict[2] = 0

        return result_dict


    def children(self):
        options = self.get_available_desicions()
        children = []

        for option in options:
            child = copy.deepcopy(self)
            child.play_turn(option)
            children.append((option, child))

        return children

    def is_terminal(self):
        
        return self.board.is_board_full()  | self.board.check_win(1) | self.board.check_win(2)
    
    def get_computer_decision_randomly(self):
        decision = random.choice(self.get_available_desicions())
        return decision
    
    def get_computer_decision_minimax(self):

        solver = MinimaxSolver(self.current_player)
        state = copy.deepcopy(self)
        state.hide_print = True
        decision = solver.solve(state, self.minimax_time)
        return decision

    import numpy as np

    """DEFINICIÓN DE MÉTODOS PARA LAS HEURISTICAS: """  

    def heuristic(self, player):
        
        opponent = 3 - player
        score = 0

        # 1. Cantidad de fichas propias
        score += np.sum(self.board.board == player)

        # 2. Bloqueo básico (fichas propias menos fichas del oponente)
        score += np.sum(self.board.board == player) - np.sum(self.board.board == opponent)

        # 3. Prioridad al centro
        center_row, center_col = self.board.rows // 2, self.board.cols // 2
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.board[row, col] == player:
                    distance = abs(row - center_row) + abs(col - center_col)
                    score += (self.board.rows + self.board.cols) - distance  # Más puntos para casillas cerca del centro

        # 4. Líneas potenciales (horizontal, vertical, diagonal)
        for row in range(self.board.rows):
            if player in self.board.board[row, :]:  # Línea horizontal
                score += 1
        for col in range(self.board.cols):
            if player in self.board.board[:, col]:  # Línea vertical
                score += 1
        for offset in range(-self.board.rows + 1, self.board.cols):  # Diagonales
            if player in self.board.board.diagonal(offset):
                score += 1
            if player in np.fliplr(self.board.board).diagonal(offset):  # Anti-diagonales
                score += 1

        # 5. Control de esquinas (básico)
        corners = [(0, 0), (0, self.board.cols - 1), (self.board.rows - 1, 0), (self.board.rows - 1, self.board.cols - 1)]
        for corner in corners:
            if self.board.board[corner] == player:
                score += 3  

        return score



    def human_vs_ia_loop(self):
        game = GameSesion(minimax_time = 4)

        print("Bienvenido a Go-Moku IA\n")
        input("\n Presiona Enter para Conmenzar")

        while True:

            os.system('cls')       
            game.board.print_board()
            print("\n")

            if(game.is_terminal()):
                
                points = game.get_winners_points()
                
                print("\nJUEGO FINALIZADO")
                if(points[1] == 1000):
                    print("\nHUMANO GANA!")
                elif(points[2] == 1000):
                    print("\nIA GANA!")
                else:
                    print("EMPATE")
            
                    
                break
            
            if game.current_player == 1:
                print("Tu turno, Humano \n")

                r = int(input("Ingresa La Fila: "))
                c = int(input("Ingresa La columna: "))
                human_decision = (r,c)
                game.play_turn(human_decision)
               

            elif game.current_player == 2:

                print("Turno de la IA (Se paciente)")

                decision = game.get_computer_decision_minimax()
                game.play_turn(decision)

    def ia_vs_ia_loop(self):
            game = GameSesion(minimax_time=4)
            print("IA vs IA: Iniciando juego...")
            while True:
                os.system('cls')
                game.board.print_board()
                print("\n")

                if game.is_terminal():
                    points = game.get_winners_points()
                    print("\nJUEGO FINALIZADO")
                    if points[1] == 1000:
                        print("\nIA 1 GANA!")
                    elif points[2] == 1000:
                        print("\nIA 2 GANA!")
                    else:
                        print("EMPATE")
                    break

                if game.current_player == 1:
                    print("Turno de IA 1")
                    decision = game.get_computer_decision_minimax()
                    game.play_turn(decision)

                elif game.current_player == 2:
                    print("Turno de IA 2")
                    decision = game.get_computer_decision_minimax()
                    game.play_turn(decision)

    def ia_vs_ia_random_loop(self):
        game = GameSesion(minimax_time=4)
        print("IA vs IA Random: Iniciando juego...")
        while True:
            os.system('cls')
            game.board.print_board()
            print("\n")

            if game.is_terminal():
                points = game.get_winners_points()
                print("\nJUEGO FINALIZADO")
                if points[1] == 1000:
                    print("\nIA 1 GANA!")
                elif points[2] == 1000:
                    print("\nIA 2 GANA!")
                else:
                    print("EMPATE")
                break

            if game.current_player == 1:
                print("Turno de IA 1")
                decision = game.get_computer_decision_minimax()
                game.play_turn(decision)

            elif game.current_player == 2:
                print("Turno de IA 2")
                decision = game.get_computer_decision_randomly()
                game.play_turn(decision)

    def human_vs_human_loop(self):
        game = GameSesion(minimax_time=4)
        print("Humano vs Humano: Iniciando juego...")
        while True:
            os.system('cls')
            game.board.print_board()
            print("\n")

            if game.is_terminal():
                points = game.get_winners_points()
                print("\nJUEGO FINALIZADO")
                if points[1] == 1000:
                    print("\nHUMANO 1 GANA!")
                elif points[2] == 1000:
                    print("\nHUMANO 2 GANA!")
                else:
                    print("EMPATE")
                break

            if game.current_player == 1:
                print("Turno de Humano 1")
                r = int(input("Ingresa La Fila: "))
                c = int(input("Ingresa La columna: "))
                human_decision = (r, c)
                game.play_turn(human_decision)

            elif game.current_player == 2:
                print("Turno de Humano 2")
                r = int(input("Ingresa La Fila: "))
                c = int(input("Ingresa La columna: "))
                human_decision = (r, c)
                game.play_turn(human_decision)

    def main(self):
        print("Bienvenido a Go-Moku IA\n")
        mode = int(input("\nSelecciona el modo de juego: \n1- Humano VS IA\n2- IA vs IA\n3- IA vs IA Random\n4- Humano vs Humano\n"))

        if mode == 1:
            self.human_vs_ia_loop()
        elif mode == 2:
            self.ia_vs_ia_loop()
        elif mode == 3:
            self.ia_vs_ia_random_loop()
        elif mode == 4:
            self.human_vs_human_loop()





game = GameSesion()

game.main()




    

