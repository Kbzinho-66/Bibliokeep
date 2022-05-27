from enum import IntEnum


class Opcao(IntEnum):
    CADASTRO = 0
    ALTERAR = 1
    DELETAR = 2
    CONSULTAR = 3
    SAIR = 4
    FILTRAR = 5


class Filtro(IntEnum):
    TITULO = 0
    AUTOR = 1
    ANO_EDI = 2
    SAIR = 3
