import xmlrpc.client
from typing import Tuple

from Codigos import Opcao, Filtro
from simple_term_menu import TerminalMenu


def main():
    while True:
        opcao, filtro = menu()
        if opcao != Opcao.SAIR:
            requisicao(opcao, filtro)
        else:
            break


def menu() -> Tuple[Opcao, Filtro]:

    prompt = TerminalMenu(['Cadastro', 'Alteração', 'Remoção', 'Consulta', 'Sair'], title='Escolha uma opção: ')
    opcao = prompt.show()
    filtro = 0

    if opcao is None:
        opcao = Opcao.SAIR

    if opcao != Opcao.CADASTRO and opcao != Opcao.SAIR:
        prompt = TerminalMenu(['Título', 'Autor', 'Ano e Edição', 'Sair'], title='Escolha um filtro: ')
        filtro = prompt.show()

        if filtro is None:
            filtro = Filtro.SAIR

    return Opcao(opcao), Filtro(filtro)


def requisicao(opcao: Opcao, filtro: Filtro):
    """Chama a função apropriada dada a combinação recebida."""

    if opcao == Opcao.CADASTRO:
        cadastro_livro()

    elif filtro == Filtro.SAIR:
        return

    elif opcao == Opcao.ALTERAR:
        livros = consultar_livros(int(filtro))
        escolhido = escolher_livro(livros)
        if escolhido:
            modificar_livro(escolhido)

    elif opcao == Opcao.DELETAR:
        livros = consultar_livros(int(filtro))
        escolhido = escolher_livro(livros)
        if escolhido:
            remover_livro(escolhido)

    elif opcao == Opcao.CONSULTAR:
        livros = consultar_livros(int(filtro))
        if livros:
            print('Livros encontrados:')
            for livro in livros:
                titulo = livro['titulo']
                autor = livro['autor']
                ano = livro['ano']
                edicao = livro['edicao']
                print(f'{titulo.strip()} - {autor.strip()}, ({ano}, {edicao}ª edição)')
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


def consultar_livros(filtro):
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
    ano = livro['ano']
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
    if len(livros) == 1:
        return livros.pop()

    indices = {}
    for pos, livro in enumerate(livros):
        codigo = livro['codigo']
        titulo = livro['titulo']
        autor = livro['autor']
        ano = livro['ano']
        edicao = livro['edicao']
        indices[codigo] = pos
        print(f'{codigo}: {titulo.strip()} - {autor.strip()}, ({ano}, {edicao}ª edição)')

    while True:
        cod = input('Insira o código do livro que quer selecionar ou 0 para cancelar: ')
        if cod.isnumeric():
            cod = int(cod)
            if cod in indices:
                break
            elif cod == 0:
                break
            else:
                print('Código inválido.')

    if cod == 0:
        return None
    else:
        return livros[indices[cod]]


if __name__ == '__main__':
    main()
