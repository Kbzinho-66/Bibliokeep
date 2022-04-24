import socket, pickle
from typing import Tuple
from Codigos import Opcao, Filtro
from Classes import Livro, Query

s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip    = 'localhost' 
porta = 12000

def main():

    while True:
        
        opcao, filtro = menu() 
        if opcao:
            requisicao(opcao, filtro)
        else:
            break
        
    fechar_servidor()


def menu() -> Tuple[Opcao, Filtro]:
    """Lê uma combinação de uma opção e um filtro, quando necessário."""

    opcao = 1
    filtro = 0

    while opcao:
        print('_______________________________')
        print('1. Cadastrar um livro.')
        print('2. Alterar um livro.')
        print('3. Deletar um livro.')
        print('4. Fazer uma consulta.')
        print('0. Sair.')

        while True:
            opcao = input('Escolha uma opção: ')
            if opcao.isnumeric():
                opcao = int(opcao)
                break

        if opcao == Opcao.SAIR:
            return (Opcao.SAIR, Opcao.SAIR)
        elif opcao < 0 or opcao > 4:
            print('Opção inválida.')
            continue
            
        if opcao != Opcao.CADASTRO:
            while True:
                print('_______________________________')
                print('1. Consulta por título.')
                print('2. Consulta por autor.')
                print('3. Consulta por ano e edição.')
                print('0. Voltar.')

                while True:
                    filtro = input('Escolha uma opção: ')
                    if filtro.isalnum():
                        filtro = int(filtro)
                        break

                if filtro == Opcao.SAIR:
                    break
                elif filtro < 0 or filtro > 3:
                    print('Sub-opção inválida.')
                    continue
                else:
                    break

        return (opcao, filtro)


def requisicao(opcao: Opcao, filtro: Filtro):
    """Chama a função apropriada dada a combinação recebida."""
    if opcao == Opcao.CADASTRO:
        cadastro_livro()
    elif opcao == Opcao.ALTERAR:
        modificar_livro(filtro)
    elif opcao == Opcao.DELETAR:
        remover_livro(filtro)
    elif opcao == Opcao.CONSULTAR:
        consulta_livro(filtro)

            
def cadastro_livro():
    print('Insira as informações do livro.')
    titulo = input('Título: ')
    autor  = input('Autor: ')
    ano    = input('Ano de publicação: ')
    edicao = input('Edição: ')

    livro = Livro(titulo, autor, edicao, ano)
    query = Query(Opcao.CADASTRO, livro)

    msg = pickle.dumps(query)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())

def escolher_livro(filtro: Filtro) -> Livro:
    """
        Lê os dados que vão ser usados pra procurar os livros no banco de dados.
        Caso sejam encontrados vários livros que se encaixam nesse filtro, permite escolher
        um desses livros e o retorna.
    """

    if filtro == Filtro.TITULO:
        titulo = input('Pesquisar títulos: ')
        msg = f'UPDATE;{titulo};'
    elif filtro == Filtro.AUTOR:
        autor = input('Pesquisar autor: ')
        msg = f'UPDATE;{autor};'
    elif filtro == Filtro.ANO_EDI:
        ano    = input('Pesquisar ano de publicação: ')
        edicao = input('Edição: ')
        msg = f'UPDATE;{ano};{edicao}'

    s.sendto(msg, (ip, porta))
    retorno, servidor = s.recvfrom(2048)

    livro = Livro(retorno) # TODO

    return livro

def modificar_livro(filtro):
    livro = escolher_livro(filtro)
    
    titulo = livro.titulo
    autor  = livro.autor
    ano    = livro.ano
    edicao = livro.edicao

    print(f'Título...........: {titulo}')
    print(f'Autor............: {autor}')
    print(f'Ano de Publicação: {ano}')
    print(f'Edição...........: {edicao}')
    
    titulo = input('Insira o novo título...........: ')
    autor  = input('Insira o novo autor............: ')
    ano    = input('Insira o novo ano de publicação: ')
    edicao = input('Insira a nova edição...........: ')

    msg = f'UPDATE;{livro.codigo};{titulo};{autor};{ano};{edicao}'
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())
    
def remover_livro(filtro):
    livro = escolher_livro(filtro)

    msg = f'DELETE;{livro.codigo}'
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())

def consulta_livro(filtro):
    livro = escolher_livro(filtro)

    print(livro)


def fechar_servidor():
    q = Query(Opcao.SAIR, [])
    msg = pickle.dumps(q)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)
    s.close()

    print(retorno.decode())

if __name__ == '__main__':
    main()
