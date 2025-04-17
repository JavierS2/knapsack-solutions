import random
import math
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

# Parámetros configurables
initial_temperature = 100.0
cooling_factor = 0.99
total_iterations = 500
backpack_capacity = 4.0  # en kg
run_number = 1  # valor predeterminado para la primera ejecución

# Cargar datos desde el archivo Excel
df = pd.read_excel('Mochila_capacidad_maxima_4kg.xlsx')

# Se crea una lista de objetos desde el DataFrame
items = []
for _, row in df.iterrows():
    items.append({
        'id': row['Id'],
        'value': row['Valor'],
        'weight': row['Peso_kg'],  # se mantiene en kg
        'available_quantity': int(row['Cantidad'])
    })

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    def total_value(self, solution):
        # Calcula el valor total de la solución
        return sum(self.items[i]["value"] * solution[i] for i in range(len(self.items)))

    def total_weight(self, solution):
        # Calcula el peso total de la solución
        return sum(self.items[i]["weight"] * solution[i] for i in range(len(self.items)))

    def generate_initial_solution(self):
        # Genera una solución inicial válida
        solution = [0] * len(self.items)
        total_weight = 0
        while total_weight <= self.capacity:
            i = random.randint(0, len(self.items) - 1)
            if (total_weight + self.items[i]["weight"] <= self.capacity) and (solution[i] < self.items[i]["available_quantity"]):
                solution[i] += 1
                total_weight += self.items[i]["weight"]
            else:
                break
        return solution

    def neighbor_solution(self, current_solution):
        # Genera una solución vecina (cerca de la solución actual)
        neighbor = current_solution.copy()
        for i in range(len(neighbor)):
            if random.random() < 0.1:
                max_quantity = int(self.items[i]["available_quantity"])
                neighbor[i] = random.randint(0, max_quantity)
        return neighbor

    def acceptance(self, delta_value, temperature):
        # Acepta una solución peor con base en la probabilidad
        if delta_value >= 0:
            return 1.0
        elif temperature == 0:
            return 0.0
        else:
            return math.exp(delta_value / temperature)

    def cooling(self, initial_temp, alpha, iteration, total_iterations):
        # Reduciendo la temperatura según el factor de enfriamiento
        new_temp = initial_temp * (1.0 - iteration / total_iterations) ** alpha
        return max(new_temp, 0.01)

    def solve(self, initial_temperature, cooling_factor, total_iterations):
        # Solución utilizando simulated annealing
        best_solution = self.generate_initial_solution()
        best_value = self.total_value(best_solution)
        best_weight = self.total_weight(best_solution)
        best_iteration = 0

        current_solution = best_solution.copy()
        current_value = best_value
        current_weight = best_weight

        start_time = time.time()
        optimal_values = []

        for i in range(total_iterations):
            neighbor = self.neighbor_solution(current_solution)
            neighbor_value = self.total_value(neighbor)
            neighbor_weight = self.total_weight(neighbor)

            if neighbor_weight <= self.capacity:
                delta = neighbor_value - current_value
                if self.acceptance(delta, initial_temperature) > random.random():
                    current_solution = neighbor
                    current_value = neighbor_value
                    current_weight = neighbor_weight
                    if current_value > best_value:
                        best_solution = current_solution
                        best_value = current_value
                        best_weight = current_weight
                        best_iteration = i

            initial_temperature = self.cooling(initial_temperature, cooling_factor, i, total_iterations)
            optimal_values.append(best_value)

        total_time = time.time() - start_time
        return best_solution, best_value, best_weight, total_time, optimal_values, best_iteration

def save_results_to_excel(run_number, value, time, iteration, weight, solution):
    file = 'resultadosSA.xlsx'
    
    # Verificar si el archivo existe y cargar los resultados
    if os.path.isfile(file):
        results = pd.read_excel(file)
        # obtener el último valor de 'Run' e incrementarlo
        last_run = results['Run'].max() if 'Run' in results.columns else 0
        run_number = last_run + 1
    else:
        # Si el archivo no existe, crear un nuevo DataFrame con los nombres de las columnas apropiadas
        results = pd.DataFrame(columns=['Run', 'Best Value', 'Time (s)', 'Iteration', 'Weight (kg)', 'Best Solution'])

    # Agregar un nuevo registro
    new_record = pd.DataFrame([{
        'Run': run_number,
        'Best Value': value,
        'Time (s)': time,
        'Iteration': iteration,
        'Weight (kg)': weight,
        'Best Solution': str(solution)
    }])

    # Agregar el nuevo registro a los resultados
    results = pd.concat([results, new_record], ignore_index=True)
    results.to_excel(file, index=False)

# Ejecutando el algoritmo
problem = KnapsackProblem(items, backpack_capacity)
solution, value, weight, time, history, iteration = problem.solve(initial_temperature, cooling_factor, total_iterations)

# mostrar resultados
print(f"Best solution found at iteration: {iteration}")
print(f"Execution time (s): {time:.4f}")
print("Optimal solution:", solution)
print("Optimal value:", value)
print(f"Total weight: {weight:.2f} kg")

# guardar en Excel
save_results_to_excel(run_number, value, time, iteration, weight, solution)

# Graficar la convergencia de SA
plt.plot(history)
plt.xlabel('Iteration')
plt.ylabel('Optimal value')
plt.title('Simulated Annealing Convergence')
plt.grid(True)
plt.show()