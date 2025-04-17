import random
import math
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    def total_value(self, solution):
        value = 0
        for i in range(len(self.items)):
            if solution[i] > 0:
                value += self.items[i]["value"] * solution[i]
        return value

    def total_weight(self, solution):
        weight = 0
        for i in range(len(self.items)):
            if solution[i] > 0:
                weight += self.items[i]["weight"] * solution[i]
        return weight

    def generate_initial_solution(self):
        solution = [0] * len(self.items)
        total_weight = 0
        while total_weight <= self.capacity:
            index = random.randint(0, len(self.items) - 1)
            if total_weight + self.items[index]["weight"] <= self.capacity:
                solution[index] += 1
                total_weight += self.items[index]["weight"]
            else:
                break
        return solution

    def neighbor_solution(self, current_solution):
        neighbor = current_solution.copy()
        for i in range(len(neighbor)):
            if random.random() < 0.1:
                neighbor[i] = random.randint(
                    0,
                    int(min(self.items[i]["available_quantity"],
                            self.capacity // self.items[i]["weight"]))
                )
        return neighbor

    def acceptance_probability(self, delta_value, temperature):
        if delta_value >= 0:
            return 1.0
        else:
            return math.exp(delta_value / temperature) if temperature > 0 else 0.0

    def cooling(self, initial_temp, cooling_factor, current_iter, total_iters):
        new_temp = initial_temp * (1.0 - current_iter / total_iters) ** cooling_factor
        return max(new_temp, 0.01)

    def solve(self, initial_temp, cooling_factor, total_iters):
        best_solution = self.generate_initial_solution()
        best_value = self.total_value(best_solution)
        best_weight = self.total_weight(best_solution)
        best_iter = 0

        current_solution = best_solution.copy()
        current_value = best_value
        current_weight = best_weight

        start_time = time.time()
        value_history = []

        for i in range(total_iters):
            neighbor = self.neighbor_solution(current_solution)
            neighbor_value = self.total_value(neighbor)
            neighbor_weight = self.total_weight(neighbor)

            if neighbor_weight <= self.capacity:
                delta_value = neighbor_value - current_value
                if self.acceptance_probability(delta_value, initial_temp) > random.random():
                    current_solution = neighbor.copy()
                    current_value = neighbor_value
                    current_weight = neighbor_weight

                    if current_value > best_value:
                        best_solution = current_solution.copy()
                        best_value = current_value
                        best_weight = current_weight
                        best_iter = i

            initial_temp = self.cooling(initial_temp, cooling_factor, i, total_iters)
            value_history.append(best_value)

        elapsed_time = time.time() - start_time
        return best_solution, best_value, best_weight, elapsed_time, value_history, best_iter

# Read the Excel file
df = pd.read_excel('data_4kg.xlsx')

# Build list of items
items = []
for _, row in df.iterrows():
    items.append({
        'id': row['Id'],
        'value': row['Valor'],
        'weight': int(1000 * row['Peso_kg']),
        'available_quantity': row['Cantidad']
    })

def save_results_to_excel(run_id, best_value, elapsed_time, best_iter, best_weight, best_solution):
    output_file = 'simulated_annealing_results.xlsx'
    if os.path.isfile(output_file):
        results_df = pd.read_excel(output_file)
    else:
        results_df = pd.DataFrame(columns=['Run', 'Value', 'Time', 'Iteration', 'Weight', 'Best Solution'])

    new_record = pd.DataFrame({
        'Run': [run_id],
        'Value': [best_value],
        'Time': [elapsed_time],
        'Iteration': [best_iter],
        'Weight': [best_weight],
        'Best Solution': [str(best_solution)]
    })

    results_df = pd.concat([results_df, new_record], ignore_index=True)
    results_df.to_excel(output_file, index=False)

# Set knapsack capacity to 4000 grams (4kg)
capacity = 4000

# Solve the problem
knapsack = KnapsackProblem(items, capacity)
best_solution, best_value, best_weight, elapsed_time, value_history, best_iter = knapsack.solve(100.0, 0.99, 500000)

# Print results
print(f"Best solution found at iteration: {best_iter}")
print("Elapsed time:", elapsed_time)
print("Best solution:", best_solution)
print("Best value:", best_value)
print("Total weight:", best_weight / 1000, "kg")

# Save results
save_results_to_excel(1, best_value, elapsed_time, best_iter, best_weight, best_solution)

# Plot convergence
plt.plot(value_history)
plt.xlabel('Iteration')
plt.ylabel('Best Value')
plt.title('Simulated Annealing Convergence')
plt.grid(True)
plt.show()
