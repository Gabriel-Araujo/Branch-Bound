from mip import Model, MAXIMIZE, CBC

from branch_and_bound.branch_and_bound import BranchAndBound
from fs import get_model_from
import sys


def main():
    if len(sys.argv) <= 1:
        print("Sem caminho do arquivo.")
        return

    filepath = sys.argv[1]

    model = get_model_from(filepath)

#    bb = BranchAndBound(model)

    model = Model(sense=MAXIMIZE, solver_name=CBC, )
main()