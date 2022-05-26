import xmlrpc.client
from typing import Tuple, List

from Codigos import Opcao, Filtro


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
        print("_______________________________")
        print(f"{Opcao.CADASTRO}. Cadastrar um livro.")
        print(f"{Opcao.ALTERAR}. Alterar um livro.")
        print(f"{Opcao.DELETAR}. Deletar um livro.")
        print(f"{Opcao.CONSULTAR}. Fazer uma consulta.")
        print(f"{Opcao.SAIR}. Sair.")

        while True:
            opcao = input("Escolha uma opção: ")
            if opcao.isnumeric():
                opcao = int(opcao)
                break

        if opcao == Opcao.SAIR:
            return Opcao.SAIR, Filtro.SAIR
        elif opcao < 0 or opcao > 4:
            print("Opção inválida.")
            continue

        if opcao != Opcao.CADASTRO:
            while True:
                print("_______________________________")
                print(f"{Filtro.TITULO}. Consulta por título.")
                print(f"{Filtro.AUTOR}. Consulta por autor.")
                print(f"{Filtro.ANO_EDI}. Consulta por ano e edição.")
                print(f"{Filtro.SAIR}. Voltar.")

                while True:
                    filtro = input("Escolha uma opção de busca: ")
                    if filtro.isalnum():
                        filtro = int(filtro)
                        break

                if filtro == Opcao.SAIR:
                    break
                elif filtro < 0 or filtro > 3:
                    print("Opção inválida.")
                    continue
                else:
                    break

        return Opcao(opcao), Filtro(filtro)


def requisicao(opcao: Opcao, filtro: Filtro):
    """Chama a função apropriada dada a combinação recebida."""

    if opcao == Opcao.CADASTRO:
        cadastro_livro()

    elif filtro == Filtro.SAIR:
        return

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
    servidor = xmlrpc.client.ServerProxy('http://localhost:13000')

    print('Insira as informações do livro.')
    titulo = input('Título: ')
    autor = input('Autor: ')
    ano = input('Ano de publicação: ')
    edicao = input('Edição: ')

    livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "edicao": edicao
    }
    print(servidor.cadastrar(livro))


def consultar_livros(filtro: Filtro):
    """
    Vai ler o filtro escolhido, procurar todos os livros que se encaixam
    e retornar uma lista com os primeiros 20 resultados.
    """
    servidor = xmlrpc.client.ServerProxy('http://localhost:13000')

    if filtro == Filtro.TITULO:
        busca = input('Pesquisar título: ')
    elif filtro == Filtro.AUTOR:
        busca = input('Pesquisar autor: ')
    elif filtro == Filtro.ANO_EDI:
        ano = input('Pesquisar ano de publicação: ')
        edicao = input('Edição: ')
        busca = (ano, edicao)

    # noinspection PyUnboundLocalVariable
    return servidor.filtrar(filtro, busca)


def modificar_livro(livro):
    servidor = xmlrpc.client.ServerProxy('http://localhost:13000')

    codigo = livro['codigo']
    titulo = livro['titulo']
    autor = livro['autor']
    ano = livro['ano_pub']
    edicao = livro['edicao']

    print(f'Título...........: {titulo}')
    print(f'Autor............: {autor}')
    print(f'Ano de Publicação: {ano}')
    print(f'Edição...........: {edicao}')

    print('Insira os novos dados:')
    titulo = input('Novo título...........: ')
    autor = input('Novo autor............: ')
    ano = input('Novo ano de publicação: ')
    edicao = input('Nova edição...........: ')

    livro = {
        'codigo': codigo,
        'titulo': titulo,
        'autor': autor,
        'ano': ano,
        'edicao': edicao
    }
    print(servidor.alterar(livro))


def remover_livro(livro):
    servidor = xmlrpc.client.ServerProxy('http://localhost:13000')
    print(servidor.deletar(livro))


def escolher_livro(livros):
    """
    Como as funções que buscam livros retornam uma lista com diversos livros que
    se encaixam, essa função permite escolher um desses pra excluir ou alterar.
    """
    indices = {}
    for pos, livro in enumerate(livros):
        indices[livro['codigo']] = pos
        print(f'{livro['codigo']}: {livro['titulo']}')
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
    servidor = xmlrpc.client.ServerProxy('http://localhost:13000')
    servidor.sair()


if __name__ == '__main__':
    main()