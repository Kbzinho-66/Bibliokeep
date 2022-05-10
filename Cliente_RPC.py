import pickle
import socket
from typing import Tuple, List

from Classes_Sockets import Livro, Query
from Codigos_Sockets import Opcao, Filtro

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
        print(f'{Opcao.CADASTRO}. Cadastrar um livro.')
        print(f'{Opcao.ALTERAR}. Alterar um livro.')
        print(f'{Opcao.DELETAR}. Deletar um livro.')
        print(f'{Opcao.CONSULTAR}. Fazer uma consulta.')
        print(f'{Opcao.SAIR}. Sair.')

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
                print(f'{Filtro.TITULO}. Consulta por título.')
                print(f'{Filtro.AUTOR}. Consulta por autor.')
                print(f'{Filtro.ANO_EDI}. Consulta por ano e edição.')
                print(f'{Filtro.SAIR}. Voltar.')

                while True:
                    filtro = input('Escolha uma opção de busca: ')
                    if filtro.isalnum():
                        filtro = int(filtro)
                        break

                if filtro == Opcao.SAIR:
                    break
                elif filtro < 0 or filtro > 3:
                    print('Opção inválida.')
                    continue
                else:
                    break

        return Opcao(opcao), Filtro(filtro)


def requisicao(opcao: Opcao, filtro: Filtro):
    """Chama a função apropriada dada a combinação recebida."""
    if filtro == Filtro.SAIR:
        return

    if opcao == Opcao.CADASTRO:
        cadastro_livro()

    elif opcao == Opcao.ALTERAR:
        livros = consultar_livros(filtro)
        if len(livros) > 1:
            modificar_livro(escolher_livro(livros))
        elif livros:
            modificar_livro(livros.pop())

    elif opcao == Opcao.DELETAR:
        livros = consultar_livros(filtro)
        if livros:
            remover_livro(escolher_livro(livros))

    elif opcao == Opcao.CONSULTAR:
        livros = consultar_livros(filtro)
        if livros:
            print('Livros encontrados:')
            for livro in livros:
                print(livro)
        else:
            print('Nenhum livro encontrado para esse filtro.')


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


def consultar_livros(filtro: Filtro) -> List[Livro]:
    """
    Vai ler o filtro escolhido, procurar todos os livros que se encaixam
    e retornar uma lista com os primeiros 20 resultados.
    """
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

    # noinspection PyUnboundLocalVariable
    query = Query(Opcao.FILTRAR, livro, filtro)
    msg = pickle.dumps(query)
    s.sendto(msg, (ip, porta))
    retorno, servidor = s.recvfrom(4096)
    livros = pickle.loads(retorno)

    return livros


def modificar_livro(livro):
    titulo = livro.titulo
    autor = livro.autor
    ano = livro.ano_pub
    edicao = livro.edicao

    print(f'Título...........: {titulo}')
    print(f'Autor............: {autor}')
    print(f'Ano de Publicação: {ano}')
    print(f'Edição...........: {edicao}')

    print('Insira os novos dados:')
    titulo = input('Novo título...........: ')
    autor = input('Novo autor............: ')
    ano = input('Novo ano de publicação: ')
    edicao = input('Nova edição...........: ')

    livro = Livro(livro.codigo, titulo, autor, edicao, ano)
    q = Query(Opcao.ALTERAR, livro)
    msg = pickle.dumps(q)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())


def remover_livro(livro):
    q = Query(Opcao.DELETAR, livro)
    msg = pickle.dumps(q)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno.decode())


def escolher_livro(livros: List[Livro]) -> Livro:
    """
    Como as funções que buscam livros retornam uma lista com diversos livros que
    se encaixam, essa função permite escolher um desses pra excluir ou alterar.
    """
    indices = {}
    for pos, livro in enumerate(livros):
        indices[livro.codigo] = pos
        print(f'{livro.codigo}: {livro.__str__()}')
    while True:
        cod = input('Insira o código do livro que quer selecionar: ')
        if cod.isnumeric():
            cod = int(cod)
            if cod in indices:
                break
            else:
                print('Código inválido.')

    return livros[indices[cod]]


def fechar_servidor():
    q = Query(Opcao.SAIR, [])
    msg = pickle.dumps(q)
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)
    s.close()

    print(retorno.decode())


if __name__ == '__main__':
    main()
