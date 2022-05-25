from typing import Tuple, List

import requests

from Codigos import Opcao, Filtro


def main():
    while True:
        opcao, filtro = menu()
        if opcao:
            requisicao(opcao, filtro)
        else:
            break

    # fechar_servidor()


def menu():
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

    # elif opcao == Opcao.ALTERAR:
    #     livros = consultar_livros(filtro)
    #     if len(livros) > 1:
    #         modificar_livro(escolher_livro(livros))
    #     elif livros:
    #         modificar_livro(livros.pop())
    #
    # elif opcao == Opcao.DELETAR:
    #     livros = consultar_livros(filtro)
    #     if livros:
    #         remover_livro(escolher_livro(livros))
    #
    # elif opcao == Opcao.CONSULTAR:
    #     livros = consultar_livros(filtro)
    #     if livros:
    #         print('Livros encontrados:')
    #         for livro in livros:
    #             print(livro)
    #     else:
    #         print('Nenhum livro encontrado para esse filtro.')


def cadastro_livro():
    url = 'http://localhost:5000/livros'

    print('Insira as informações do livro.')
    titulo = input('Título: ')
    autor = input('Autor: ')
    ano = input('Ano de publicação: ')
    edicao = input('Edição: ')

    livro = {
        'titulo': titulo,
        'autor': autor,
        'ano': ano,
        'edicao': edicao
    }
    retorno = requests.post(url, json=livro).json()
    print(retorno)


if __name__ == '__main__':
    main()
