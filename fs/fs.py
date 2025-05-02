from model import Model

def __transform_to_model(file) -> Model:
    lines = file.readlines()
    [variables, restrictions] = lines[0].split(" ")

    model = Model(int(variables), (int(restrictions)))
    model.define_objective_function(list(map(int, lines[1].strip().split(" "))))

    for line in lines[2:]:
        model.add_restriction(list(map(int, line.strip().split(" "))))

    model.set_integer(True)
    return model


def get_model_from(filepath: str) -> Model:
    raw_model = open(filepath, 'r')
    res = __transform_to_model(raw_model)
    raw_model.close()
    return res
