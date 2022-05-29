import xmlrpc.client
from typing import Tuple

from Codigos import Opcao, Filtro
from PyInquirer import prompt
from examples import custom_style_2 as estilo


def main():
    while True:
        opcao, filtro = menu()
        if opcao != Opcao.SAIR:
            requisicao(opcao, filtro)
        else:
            break


def menu() -> Tuple[Opcao, Filtro]:
    prompt_opcao = {
        'type': 'list',
        'name': 'opcao',
        'message': 'Escolha uma opção:',
        'choices': [
            Opcao.CADASTRO.value,
            Opcao.ALTERAR.value,
            Opcao.DELETAR.value,
            Opcao.CONSULTAR.value,
            Opcao.SAIR.value
        ]
    }

    print('-' * 50)
    resposta = prompt(prompt_opcao, style=estilo)
    opcao = resposta['opcao']

    filtro = Filtro.SAIR
    if opcao != 'Cadastrar um livro' and opcao != 'Sair':
        prompt_filtro = {
            'type': 'list',
            'name': 'filtro',
            'message': 'Escolha uma opção:',
            'choices': [
                Filtro.TITULO.value,
                Filtro.AUTOR.value,
                Filtro.ANO_EDI.value,
                Filtro.SAIR.value
            ]
        }

        resposta = prompt(prompt_filtro, style=estilo)
        filtro = resposta['filtro']

    return Opcao(opcao), Filtro(filtro)


def requisicao(opcao: Opcao, filtro: Filtro):
    """Chama a função apropriada dada a combinação recebida."""

    if opcao == Opcao.CADASTRO:
        cadastro_livro()

    elif filtro == Filtro.SAIR:
        return

    else:
        if livros := consultar_livros(filtro):
            if opcao == Opcao.CONSULTAR:
                print('Livros encontrados:')
                for livro in livros:
                    titulo = livro['titulo']
                    autor = livro['autor']
                    ano = livro['ano']
                    edicao = livro['edicao']
                    print(f'{titulo.strip()} - {autor.strip()}, ({ano}, {edicao}ª edição)')

            elif escolhido := escolher_livro(livros):
                if opcao == Opcao.ALTERAR:
                    modificar_livro(escolhido)
                elif opcao == Opcao.DELETAR:
                    remover_livro(escolhido)
        else:
            print('Nenhum livro encontrado para esse filtro.')


def cadastro_livro():
    servidor = xmlrpc.client.ServerProxy('http://localhost:13000')

    print('Insira as informações do livro.')
    titulo = input('Título: ')
    autor = input('Autor: ')
    ano = input('Ano de publicação: ')
    edicao = input('Edição: ')

    if titulo and autor and ano and edicao:
        livro = {
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "edicao": edicao
        }
        print(servidor.cadastrar(livro))

    else:
        print('Todos os campos são obrigatórios.')


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
    return servidor.filtrar(filtro.value, busca)


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

    if titulo and autor and ano and edicao:
        livro = {
            'codigo': codigo,
            'titulo': titulo,
            'autor': autor,
            'ano': ano,
            'edicao': edicao
        }
        print(servidor.alterar(livro))

    else:
        print('Todos os campos são obrigatórios.')


def remover_livro(livro):
    confirmacao = [{
        'type': 'confirm',
        'message': 'Confirmar a exclusão?',
        'name': 'excluir',
        'default': False,
    }]

    respostas = prompt(confirmacao, style=estilo)
    if respostas['excluir']:
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
