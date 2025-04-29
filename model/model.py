class Model:
    """
    Define um modelo de problema linear, podendo ser um modelo de programação linear inteira,
    ou apenas um problema de programação linear.

    Todas as variáveis são números positivos ou zero.

    - A Função objetiva será de maximização;
    - Todas as restrições serão de menor ou igual;
    - O último elemento da restrição será o limitante.
    """



    def __init__(self, var_number: int, restrictions_number: int):
        self.__objective_function: list[int] = list()
        self.__restrictions: list[list[int]] = list()
        self.__integer: bool = False
        self.__variables_number = var_number
        self.__restrictions_number = restrictions_number


    def get_variables_number(self):
        return self.__variables_number


    def get_restrictions_number(self):
        return self.__restrictions_number


    def get_objective_function(self):
        return self.__objective_function

    def get_restrictions(self):
        return self.__restrictions


    def define_objective_function(self, objective_function: list[int]):
        """
        Define a função objetiva a ser maximizada. Cada elemento da lista é um coeficiente
        para a variável com o mesmo índice.
        :param objective_function: Lista de coeficientes.
        """
        if len(objective_function) != int(self.__variables_number):
            raise ValueError("Função objetiva não possui o número correto de coeficientes.\n"
                             f"Função objetiva deve ter {self.__variables_number} coeficientes, mas tem {len(objective_function)}.")

        self.__objective_function = objective_function


    def add_restriction(self, restrictions: list[int]):
        """
        Adiciona uma restrição ao problema. A restrição impõe um limite ≤.

        O último elemento da lista é o RHS.

        A lista deve ter um tamanho igual ao número de variáveis + 1.
        :param restrictions: Lista de coeficientes + limitante.
        """
        if len(restrictions) != self.__variables_number+1:
            raise ValueError("Restrição não possui o número de coeficientes correto.\n"
                             f"A restrição deve ter {self.__variables_number + 1} elementos, mas tem {len(restrictions)}.")

        self.__restrictions.append(restrictions)


    def set_integer(self, integer: bool):
        """
        Define se o problema modelado é de programação linear inteira ou não.
        :param integer: True para programação linear inteira, false caso contrário.
        :return:
        """
        self.__integer = integer


    def is_integer(self) -> bool:
        """
        Retorna se o modelo se se trata de um modelo de programação inteira ou não.
        :return: True para programação linear inteira, false caso contrário.
        """
        return self.__integer


    def __get_objective_str(self):
        res = ""
        for [index, element] in enumerate(self.__objective_function):
            if element >= 0:
                res += f" + X_{index}*{element:.2f}".rstrip('0').rstrip('.')
            else:
                res += f" - X_{index}*{element.__abs__():.2f}".rstrip('0').rstrip('.')

        return res[3:]


    def __get_restriction_str(self):
        res = ""
        for restriction in self.__restrictions:
            inner = ""
            for [index, coefficient] in enumerate(restriction):
                if index == self.__variables_number:
                    inner += f" <= {coefficient:.2f}".rstrip('0').rstrip('.')
                    continue
                if coefficient >= 0:
                    inner += f" + X_{index}*{coefficient:.2f}".rstrip('0').rstrip('.')
                else:
                    inner += f" - X_{index}*{coefficient:.2f}".rstrip('0').rstrip('.')
            res += f"\t{inner[3:]}\n"
        return res


    def __str__(self):
        return (f"MAX {self.__get_objective_str()}\n{self.__get_restriction_str()}"
                f"Integer: {self.__integer}")
