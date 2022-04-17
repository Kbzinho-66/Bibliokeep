import socket, pickle
from typing import Tuple
from Codigos import Cod
import Livro

s     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip    = 'localhost' 
porta = 12000

def main():

    while True:
        
        opcao, sub_opcao = menu() 
        if opcao:
            requisicao(opcao, sub_opcao)
        else:
            break
        
    fechar_servidor()

def menu() -> Tuple[Cod, Cod]:
    """Lê uma combinação de uma opção e um filtro, quando necessário."""

    opcao = 1
    sub_opcao = 0

    while opcao:
        print('_______________________________')
        print('1. Cadastrar um livro.')
        print('2. Alterar um livro.')
        print('3. Deletar um livro.')
        print('4. Fazer uma consulta.')
        print('0. Sair.')

        while True:
            opcao = input('Escolha uma opção: ')
            if opcao and opcao.isalnum():
                opcao = int(opcao)
                break

        if opcao == Cod.SAIR:
            return (Cod.SAIR, Cod.SAIR)
        elif opcao < 0 or opcao > 4:
            print('Opção inválida.')
            continue
            
        while True:
            if opcao != Cod.CADASTRO:
                print('_______________________________')
                print('1. Consulta por título.')
                print('2. Consulta por autor.')
                print('3. Consulta por ano e edição.')
                print('0. Voltar.')

            while True:
                sub_opcao = input('Escolha a forma de consulta: ')
                if sub_opcao and sub_opcao.isalnum():
                    sub_opcao = int(sub_opcao)
                    break

            if sub_opcao == Cod.SAIR:
                break
            elif sub_opcao < 0 or sub_opcao > 3:
                print('Sub-opção inválida.')
                continue
            else:
                return (opcao, sub_opcao)


def requisicao(opcao: Cod, filtro: Cod):
    """Chama a função apropriada dada a combinação recebida."""
    if opcao == Cod.CADASTRO:
        cadastro_livro()
    elif opcao == Cod.ALTERAR:
        modificar_livro(filtro)
    elif opcao == Cod.DELETAR:
        remover_livro(filtro)
    elif opcao == Cod.CONSULTAR:
        consulta_livro(filtro)

            
def cadastro_livro():
    print('Insira as informações do livro:')
    titulo = input('Título: ')
    autor  = input('Autor: ')
    ano    = input('Ano de publicação: ')
    edicao = input('Edição: ')

    msg = f'CREATE;TITULO={titulo};AUTOR={autor};ANO={ano};EDICAO={edicao};'
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno)

def escolher_livro(filtro: Cod) -> Livro:
    """
        Lê os dados que vão ser usados pra procurar os livros no banco de dados.
        Caso sejam encontrados vários livros que se encaixam nesse filtro, permite escolher
        um desses livros e o retorna.
    """

    if filtro == Cod.TITULO:
        titulo = input('Pesquisar títulos: ')
        msg = f'UPDATE;TITULO={titulo};'
    elif filtro == Cod.AUTOR:
        autor = input('Pesquisar autor: ')
        msg = f'UPDATE;AUTOR={autor};'
    elif filtro == Cod.ANO_EDI:
        ano    = input('Pesquisar ano de publicação: ')
        edicao = input('Edição: ')
        msg = f'UPDATE;ANO={ano};EDICAO={edicao}'

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

    msg = f'UPDATE;CODIGO={livro.codigo};TITULO={titulo};AUTOR={autor};ANO={ano};EDICAO={edicao};'
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno)
    
def remover_livro(filtro):
    livro = escolher_livro(filtro)

    msg = f'DELETE;CODIGO={livro.codigo}'
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)

    print(retorno)

def consulta_livro(filtro):
    livro = escolher_livro(filtro)

    print(livro)


def fechar_servidor():
    msg = "EXIT;"
    s.sendto(msg, (ip, porta))
    retorno, _ = s.recvfrom(1024)
    s.close()

    print(retorno)

if __name__ == '__main__':
    main()
