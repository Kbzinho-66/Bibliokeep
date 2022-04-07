import sys


def opcoes():
    print('1. Cadastro de livros.')
    print('2. Consultas.')

def subopcoes(opcao):
    if opcao == 1:
        print('1. Cadastrar um novo livro.')
        print('2. Alterar um livro.')
        print('3. Remover um livro.')
    
    else:
        print('1. Consulta por título.')


def main():
    opcao = 1
    while opcao != 0:
        opcoes()
    pass

if __name__ == '__main__':
    main()
