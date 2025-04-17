# Knapsack Problem Solved with Bioinspired Algorithms

This project solves the 0-1 Knapsack Problem using bioinspired algorithms, including Genetic Algorithm, Ant Colony Optimization, and Simulated Annealing. A detailed project report can be found [here](./report_knapsack_problem.pdf), which discusses the methodology, algorithmic design, and results in depth.

- Ant Colony Optimization (`algorithm_aco.py`)
- Simulated Annealing (`algorithm_simulated_annealing.py`)

## Problem Description
The problem is to maximize the value of items packed in a knapsack without exceeding the weight limit. The maximum capacity of the knapsack in this case is 2.45kg (or 2450 grams). The input data for the problem is stored in the Excel file `data_4kg.xlsx`.

## Algorithms Implemented
1. **Ant Colony Optimization (`colonias_de_hormigas.py`)**:
   - Simulates the behavior of ants to find the optimal solution.
   - Results are stored in the `resultadosACO4.xlsx` file.

2. **Simulated Annealing (`enfriamiento_simulado.py`)**:
   - Uses a probabilistic technique to explore the solution space by "cooling" the solution over time.
   - Results are stored in the `resultadosSA.xlsx` file.

## How to Run
Make sure to have the required libraries installed:
```bash
pip install numpy matplotlib pandas
```

**To run the scripts**, execute the following commands in your terminal:

```bash
python algorithm_aco.py
python algorithm_simulated_annealing.py
```

## Project Report

A detailed report on the implementation, methodology, and results of the algorithms used in this project is available:

- [Download the Project Report](./report_knapsack_problem.pdf)


## Contributors
This project was developed with contributions from:

- [Carlos Lizarazo](https://github.com/JavierS2)
- [Carlos Romero](https://github.com/JavierS2)
- [Javier Santodomingo](https://github.com/JavierS2)
