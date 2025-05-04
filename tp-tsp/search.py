"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def __init__(self, max_resets: int = 100, max_iters_per_reset: int = 1000) -> None:
        """Construye una instancia de la clase.

        Argumentos:
        ==========
        max_resets: int
            numero maximo de reinicios aleatorios
        max_iters_per_reset: int
            numero maximo de iteraciones por cada reinicio
        """
        super().__init__()
        self.max_resets = max_resets
        self.max_iters_per_reset = max_iters_per_reset
        self.best_tour = None
        self.best_value = float('-inf')
        self.total_iters = 0

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas de reinicio aleatorio.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        start_time = time()
        self.problem = problem  # Guardamos el problema para usar random_reset()

        for _ in range(self.max_resets):
            # 1. Generar un estado inicial aleatorio
            current_tour = self.problem.random_reset()
            current_value = self.problem.obj_val(current_tour)
            iters_reset = 0

            # 2. Aplicar Hill Climbing desde el estado inicial aleatorio
            while iters_reset < self.max_iters_per_reset:
                self.total_iters += 1
                iters_reset += 1
                act, succ_val = self.problem.max_action(current_tour)

                # Si no encontramos una mejora, detenemos la búsqueda local para este reinicio
                if succ_val <= current_value:
                    break

                # Nos movemos al mejor vecino
                current_tour = self.problem.result(current_tour, act)
                current_value = succ_val

            # 3. Actualizar la mejor solución global encontrada
            if current_value > self.best_value:
                self.best_value = current_value
                self.best_tour = list(current_tour)  # Guardar una copia

        # 4. Almacenar los resultados finales
        end_time = time()
        self.time = end_time - start_time
        self.tour = self.best_tour
        self.value = self.best_value
        self.niters = self.total_iters


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    # COMPLETAR
