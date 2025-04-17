import numpy as np
import matplotlib.pyplot as plt
import time
import os
from collections import Counter
import pandas as pd

# Load the Excel file
data = pd.read_excel(r'data_4kg.xlsx', sheet_name='Hoja1')

# Convert item data (ID, weight in kg, value, max quantity)
items_tup = [(int(data.iloc[i, 0]), float(data.iloc[i, 1]), int(data.iloc[i, 2]), int(data.iloc[i, 3])) for i in range(len(data))]
start_time = time.time()
items = np.array(items_tup)

max_weight = 4.0  # in kg
num_ants = 20
num_iterations = 100
evaporation = 0.1
initial_pheromone = 0.9
alpha = 1
beta = 0.5

pheromones = np.ones(len(items)) * initial_pheromone
best_global_value = 0
best_global_solution = []
best_values_per_iteration = []

# Save results to Excel (called every iteration)
def save_results_to_excel(run_id, iteration, best_value, elapsed_time, best_weight, best_solution):
    output_file = 'results_ACO.xlsx'

    if os.path.isfile(output_file):
        results = pd.read_excel(output_file)
    else:
        results = pd.DataFrame(columns=['Run', 'Iteration', 'Best Value', 'Time (s)', 'Weight (kg)', 'Best Solution'])

    new_record = pd.DataFrame({
        'Run': [run_id],
        'Iteration': [iteration],
        'Best Value': [best_value],
        'Time (s)': [elapsed_time],
        'Weight (kg)': [best_weight],
        'Best Solution': [str(best_solution)]
    })

    results = pd.concat([results, new_record], ignore_index=True)
    results.to_excel(output_file, index=False)

def select_item(current_weight, selected):
    available_weights = items[:, 1] <= (max_weight - current_weight)
    available_quantities = np.array([items[i, 3] - selected.count(i) for i in range(len(items))]) > 0
    heuristic_value = items[:, 2] ** beta
    probabilities = (pheromones ** alpha) * heuristic_value * available_weights * available_quantities
    if probabilities.sum() == 0:
        return None
    probabilities /= probabilities.sum()
    return np.random.choice(range(len(items)), p=probabilities)

for iteration in range(num_iterations):
    best_value_iteration = 0
    best_solution_iteration = []
    for ant in range(num_ants):
        current_solution = []
        selected_items = []
        current_value = 0
        current_weight = 0
        while True:
            item = select_item(current_weight, selected_items)
            if item is None or current_weight + items[item, 1] > max_weight:
                break
            current_solution.append(item)
            selected_items.append(item)
            current_value += items[item, 2]
            current_weight += items[item, 1]

        if current_value > best_value_iteration:
            best_value_iteration = current_value
            best_solution_iteration = current_solution

    if best_value_iteration > best_global_value:
        best_global_value = best_value_iteration
        best_global_solution = best_solution_iteration

    best_values_per_iteration.append(best_value_iteration)

    for item in range(len(items)):
        pheromones[item] = (1 - evaporation) * pheromones[item] + \
                           sum([items[item, 2] for s in best_solution_iteration if s == item]) / (best_value_iteration if best_value_iteration > 0 else 1)

    # Guardar resultados parciales por iteración
    solution_counter = Counter(best_solution_iteration)
    iteration_solution = [solution_counter.get(i, 0) for i in range(len(items))]
    elapsed = time.time() - start_time

    save_results_to_excel(
        run_id=1,
        iteration=iteration + 1,
        best_value=best_value_iteration,
        elapsed_time=elapsed,
        best_weight=sum(items[s, 1] for s in best_solution_iteration),
        best_solution=iteration_solution
    )

finish_time = time.time()
duration = finish_time - start_time
best_solution_index = best_values_per_iteration.index(best_global_value)

# Output results
print("Ant Colony Optimization Algorithm")
print(f"Best solution found at iteration: {best_solution_index + 1}")
print(f"Execution time (s): {duration:.4f}")
print(f"Best Global Value: {best_global_value}")
print(f"Total Weight (kg): {sum(items[s, 1] for s in best_global_solution):.3f}")

# Count quantity of each selected item
solution_counter = Counter(best_global_solution)
full_solution = [solution_counter.get(i, 0) for i in range(len(items))]

print(f"Best Global Solution (Selected Quantity per Item): {full_solution}")

# Plot convergence
plt.plot(best_values_per_iteration, '-o', label='Best Value per Iteration')
plt.title('Convergence of ACO Algorithm')
plt.xlabel('Iteration')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
