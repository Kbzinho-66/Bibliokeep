from enum import IntEnum


class Opcao(IntEnum):
    CADASTRO = 1
    ALTERAR = 2
    DELETAR = 3
    CONSULTAR = 4
    FILTRO = 5
    SAIR = 0


class Filtro(IntEnum):
    TITULO = 1
    AUTOR = 2
    ANO_EDI = 3
    SAIR = 0
