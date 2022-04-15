import socket
import sys
import Livro

def main():
    if len(sys.argv) != 3:
        print('%s <ip> <porta>' % sys.argv[0])
        sys.exit(0)

    while True:
        
        opcao, subOpcao = menu() 
        if opcao:
            requisicao(opcao, subOpcao)
        else:
            break


def menu():
    opcao = 1
    subOpcao = 0

    while opcao:
        print('_______________________________')
        print('1. Cadastro de livros.')
        print('2. Consultas.')
        print('0. Sair.')

        while True:
            opcao = input('Escolha uma opção: ')
            if opcao and opcao.isalnum():
                opcao = int(opcao)
                break

        if opcao == 0:
            return (0, 0)
        elif opcao < 0 or opcao > 2:
            print('Opção inválida.')
            continue
            
        while True:
            if opcao == 1:
                print('_______________________________')
                print('1. Cadastrar um novo livro.')
                print('2. Alterar um livro.')
                print('3. Remover um livro.')
                print('0. Voltar.')

            elif opcao == 2:
                print('_______________________________')
                print('1. Consulta por título.')
                print('2. Consulta por autor.')
                print('3. Consulta por ano e edição.')
                print('0. Voltar.')

            while True:
                subOpcao = input('Escolha uma sub-opção: ')
                if subOpcao and subOpcao.isalnum():
                    subOpcao = int(subOpcao)
                    break

            if subOpcao == 0:
                break
            elif subOpcao < 0 or subOpcao > 3:
                print('Sub-opção inválida.')
                continue
            else:
                return (opcao, subOpcao)


def requisicao(opcao, subOpcao):
    if opcao == 1:
        if subOpcao == 1:
            cadastro_livro()
        elif subOpcao == 2:
            modificar_livro()
        else:
            remover_livro()
    else:
        if subOpcao == 1:
            consulta_titulo()
        elif subOpcao == 2:
            consulta_autor()
        else:
            consulta_ano_edicao()

            
def cadastro_livro():
    s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip    = sys.argv[1] 
    porta = int(sys.argv[2])

    print('Insira as informações do livro:')
    titulo = input('Título: ')
    autor  = input('Autor: ')
    edicao = input('Edição: ')
    ano    = input('Ano de publicação: ')

    # TODO Enviar o livro novo pro servidor
    pass

def modificar_livro():
    s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip    = sys.argv[1] 
    porta = int(sys.argv[2])

    titulo = input('Insira o título do livro a ser modificado: ')
    # TODO Buscar todos os livros que contêm essas palavras
    # TODO Deixar escolher um desses
    # TODO Ler as novas informações

    pass

def remover_livro():
    s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip    = sys.argv[1] 
    porta = int(sys.argv[2])

    titulo = input('Insira o título do livro a ser modificado: ')
    # TODO Buscar todos os livros que contêm essas palavras
    # TODO Deixar escolher um desses
    # TODO Enviar a requisição de delete pro servidor

    pass

def consulta_titulo():
    s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip    = sys.argv[1] 
    porta = int(sys.argv[2])

    titulo = input('Insira o título a buscar: ')
    # TODO Buscar todos os livros que contêm essas palavras
    # TODO Deixar escolher um desses
    # TODO Mostrar as informações

    pass

def consulta_autor():
    s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip    = sys.argv[1] 
    porta = int(sys.argv[2])

    autor = input('Insira o autor a buscar: ')
    # TODO Buscar todos os livros desse autor
    # TODO Deixar escolher um desses
    # TODO Mostrar as informações
    
    pass

def consulta_ano_edicao():
    s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip    = sys.argv[1] 
    porta = int(sys.argv[2])

    ano    = input('Insira o ano a buscar: ')
    edicao = input('Insira a edição: ')
    # TODO Buscar todos os livros desse autor
    # TODO Deixar escolher um desses
    # TODO Mostrar as informações
    
    pass

if __name__ == '__main__':
    main()
