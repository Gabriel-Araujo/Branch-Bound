from mip import Model, MAXIMIZE, CBC, CONTINUOUS
from model import Model as MyModel


class BranchAndBound:
    def __init__(self, my_model: MyModel):
        self.model = Model(sense=MAXIMIZE, solver_name=CBC, )
        self.vars = {i: self.model.add_var(var_type=CONTINUOUS, name=f'x_{i}', lb=0.0) for i in range(my_model.get_variables_number())}

        for [index, coefficient] in enumerate(my_model.get_objective_function()):
            self.model.objective += coefficient*self.vars[index]

        print(self.model)