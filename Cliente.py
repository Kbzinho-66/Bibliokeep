import pickle
import socket
from typing import Tuple

from Classes import Livro, Query
from Codigos import Opcao, Filtro

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = 'localhost'
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
            return Opcao.SAIR, Filtro.SAIR
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

        return Opcao(opcao), Filtro(filtro)


def requisicao(opcao: Opcao, filtro: Filtro):
    """Chama a função apropriada dada a combinação recebida."""
    if opcao == Opcao.CADASTRO:
        cadastro_livro()
    elif opcao == Opcao.ALTERAR:
        escolher_livro(opcao, filtro)
        modificar_livro(filtro)
    elif opcao == Opcao.DELETAR:
        escolher_livro(opcao, filtro)
        remover_livro(filtro)
    elif opcao == Opcao.CONSULTAR:
        escolher_livro(opcao, filtro)
        consulta_livro(filtro)


def cadastro_livro():
    print('Insira as informações do livro.')
    titulo = input('Título: ')
    autor = input('Autor: ')
    ano = input('Ano de publicação: ')
    edicao = input('Edição: ')

    livro = Livro(0, titulo, autor, edicao, ano)
    query = Query(Opcao.CADASTRO, livro)

    msg = pickle.dumps(query)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())


def escolher_livro(opcao: Opcao, filtro: Filtro) -> Livro:

    """
        Lê os dados que vão ser usados para procurar os livros no banco de dados.
        Caso sejam encontrados vários livros que se encaixam nesse filtro, permite escolher
        um desses livros e o retorna.
    """
    msg = ''

    if filtro == Filtro.TITULO:
        titulo = input('Pesquisar títulos: ')
        livro = Livro(titulo=titulo)
    elif filtro == Filtro.AUTOR:
        autor = input('Pesquisar autor: ')
        livro = Livro(autor=autor)
    elif filtro == Filtro.ANO_EDI:
        ano = input('Pesquisar ano de publicação: ')
        edicao = input('Edição: ')
        livro = Livro(ano_pub=ano, edicao=edicao)

    query = Query(opcao, livro, filtro)
    msg = pickle.dumps(query)
    s.sendto(msg, (ip, porta))
    retorno, servidor = s.recvfrom(4096)
    livros = pickle.loads(retorno)
    for item in livros:
        print(item)

    return livro


def modificar_livro(filtro):
    livro = escolher_livro(filtro)

    titulo = livro.titulo
    autor = livro.autor
    ano = livro.ano_pub
    edicao = livro.edicao

    print(f'Título...........: {titulo}')
    print(f'Autor............: {autor}')
    print(f'Ano de Publicação: {ano}')
    print(f'Edição...........: {edicao}')

    titulo = input('Insira o novo título...........: ')
    autor = input('Insira o novo autor............: ')
    ano = input('Insira o novo ano de publicação: ')
    edicao = input('Insira a nova edição...........: ')

    msg = f'UPDATE;{livro.codigo};{titulo};{autor};{ano};{edicao}'
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())


def remover_livro(filtro):

    # msg = f'DELETE;{livro.codigo}'
    # s.sendto(msg, (ip, porta))
    # retorno, _ = s.recvfrom(1024)
    #
    # print(retorno.decode())
    pass


def consulta_livro(filtro):
    pass


def fechar_servidor():
    q = Query(Opcao.SAIR, [])
    msg = pickle.dumps(q)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)
    s.close()

    print(retorno.decode())


if __name__ == '__main__':
    main()
