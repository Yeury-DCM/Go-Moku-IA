import numpy as np
import time
import random

class MinimaxSolver:
    def __init__(self, player):
        self.player = player
        self.time_start = None
        self.max_time = None

    def __maximize(self, state, alpha, beta, depth):
        if time.time() - self.time_start >= self.max_time:
            raise StopIteration("Out of time!")

        if state.is_terminal():
            return None, state.get_winners_points()[self.player]

        if depth <= 0:
            return None, state.heuristic(self.player)

        max_child, max_utility = None, -np.inf

        for option, child in state.children():
            if child.current_player == self.player:
                _, utility = self.__maximize(child, alpha, beta, depth - 1)
            else:
                _, utility = self.__minimize(child, alpha, beta, depth - 1)

            if utility > max_utility:
                max_child, max_utility = option, utility

            if max_utility >= beta:
              
                break
            alpha = max(alpha, max_utility)

        return max_child, max_utility

    def __minimize(self, state, alpha, beta, depth):
        if time.time() - self.time_start >= self.max_time:
            raise StopIteration("Out of time!")

        if state.is_terminal():
            return None, state.get_winners_points()[self.player]

        if depth <= 0:
            return None, state.heuristic(self.player)

        min_child, min_utility = None, np.inf

        for option, child in state.children():
            if child.current_player == self.player:
                _, utility = self.__maximize(child, alpha, beta, depth - 1)
            else:
                _, utility = self.__minimize(child, alpha, beta, depth - 1)

            if utility < min_utility:
                min_child, min_utility = option, utility

            if min_utility <= alpha:
                #print("PODA APLICADA")
                break
            beta = min(beta, min_utility)

        return min_child, min_utility

    def solve(self, state, max_time):
        self.time_start = time.time()
        self.max_time = max_time
        best_option = None

        # Lista de movimientos válidos como fallback si el tiempo es demasiado corto
        valid_options = state.get_available_desicions()

        for depth in range(1, 10000):
            try:
               # print(f"Exploring depth {depth}...")
                best_option, _ = self.__maximize(state, -np.inf, np.inf, depth)
            except StopIteration:
               # print("Time limit reached, stopping search.")
                break

        # Si no se encontró mejor opción, elige aleatoriamente un movimiento válido
        if best_option is None and valid_options:
            print("Time was too short, choosing a random valid move.")
            best_option = random.choice(valid_options)

        return best_option
