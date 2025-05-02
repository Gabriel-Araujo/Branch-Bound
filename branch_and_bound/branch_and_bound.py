from collections import deque

from mip import Model, MAXIMIZE, CBC, CONTINUOUS, xsum, OptimizationStatus
from model import Model as MyModel


def print_results(model: Model):
    status = model.optimize()

    if status != OptimizationStatus.OPTIMAL:
        return

    print("Status = ", status)
    print(f"Solution value  = {model.objective_value:.2f}\n")

    print("Solution:")
    for v in model.vars:
        print(f"{v.name} = {v.x:.2f}")


def find_branching_variable(variables) -> int:
    fractional_vars = [
        i for i, v in enumerate(variables)
        if not (abs(v.x - 0) < 1e-6 or abs(v.x - 1) < 1e-6)
    ]

    index = min(
        fractional_vars,
        key=lambda i: abs(variables[i].x - 0.5)
    )
    return index


class BranchAndBound:
    Zd = float("inf")
    Zp = float("-inf")
    Zp_solution: Model | None = None


    def __init__(self, my_model: MyModel):
        self.model = my_model


    def build_linear_model(self) -> Model:
        model = Model(sense=MAXIMIZE, solver_name=CBC)

        model.silent = True
        model.verbose = 0

        x = {i: model.add_var(var_type=CONTINUOUS, name=f"x_{i}", lb=0.0, ub=1.0) for i in range(self.model.get_variables_number())}

        model.objective = xsum(value * x[index] for index, value in enumerate(self.model.get_objective_function()))

        for restriction in self.model.get_restrictions():
            model += xsum(value * x[index] for index, value in enumerate(restriction) if index != len(restriction) -1 ) <= restriction[len(restriction)-1]

        return model


    def solve(self):
        queue = deque()
        initial_model = self.build_linear_model()
        queue.append(initial_model)

        while queue:
            current_model = queue.popleft()

            result = current_model.optimize()

            if result != OptimizationStatus.OPTIMAL: # Poda por inviabilidade
                continue

            current_value = current_model.objective_value

            if current_value < self.Zp: # Poda por limite
                continue

            if all(abs(v.x - round(v.x)) < 1e-6 for v in current_model.vars): # Poda por integralidade
                if current_value > self.Zp:
                    self.Zp = current_value
                    self.Zp_solution = current_model
                continue

            split_var = find_branching_variable(current_model.vars)

            left_child = current_model.copy()
            left_child += left_child.vars[split_var] == 0  # Ramo x=0
            queue.append(left_child)

            right_child = current_model.copy()
            right_child += right_child.vars[split_var] == 1  # Ramo x=1
            queue.append(right_child)

        return self.Zp_solution