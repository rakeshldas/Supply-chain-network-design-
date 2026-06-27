from ortools.linear_solver import pywraplp

def solve_supply_network():
    plants = ["Plant_A", "Plant_B"]
    warehouses = ["Warehouse_1", "Warehouse_2", "Warehouse_3"]

    supply = {
        "Plant_A": 500,
        "Plant_B": 700
    }

    demand = {
        "Warehouse_1": 300,
        "Warehouse_2": 400,
        "Warehouse_3": 500
    }

    cost = {
        ("Plant_A", "Warehouse_1"): 4,
        ("Plant_A", "Warehouse_2"): 6,
        ("Plant_A", "Warehouse_3"): 9,
        ("Plant_B", "Warehouse_1"): 5,
        ("Plant_B", "Warehouse_2"): 4,
        ("Plant_B", "Warehouse_3"): 7,
    }

    solver = pywraplp.Solver.CreateSolver("SCIP")

    x = {}
    for p in plants:
        for w in warehouses:
            x[p, w] = solver.NumVar(0, solver.infinity(), f"x_{p}_{w}")

    solver.Minimize(
        solver.Sum(cost[p, w] * x[p, w] for p in plants for w in warehouses)
    )

    for p in plants:
        solver.Add(solver.Sum(x[p, w] for w in warehouses) <= supply[p])

    for w in warehouses:
        solver.Add(solver.Sum(x[p, w] for p in plants) >= demand[w])

    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        return {"status": "No optimal solution found"}

    result = []
    for p in plants:
        for w in warehouses:
            result.append({
                "from": p,
                "to": w,
                "quantity": x[p, w].solution_value(),
                "unit_cost": cost[p, w]
            })

    return {
        "status": "Optimal",
        "objective_value": solver.Objective().Value(),
        "shipments": result
    }