from enum import Enum


class Opcao(Enum):
    CADASTRO = 'Cadastrar um livro'
    ALTERAR = 'Alterar um livro'
    DELETAR = 'Deletar um livro'
    CONSULTAR = 'Consultar um livro'
    SAIR = 'Sair'
    FILTRAR = 'Filtrar'


class Filtro(Enum):
    TITULO = 'Filtrar por título'
    AUTOR = 'Filtrar por autor'
    ANO_EDI = 'Filtrar por ano e edição'
    SAIR = 'Sair'
