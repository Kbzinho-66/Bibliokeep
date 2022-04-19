import pickle, socket, psycopg2
from typing import List

import Livro
from Codigos import Cod

def main():

    banco_livros = psycopg2.connect(
        host     = 'localhost',
        database = 'livros',
        user     = 'postgres',
        password = 'postgres'
    )

    db = banco_livros.cursor()

    ip    = 'localhost'
    porta = 12000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    s.bind( (ip, porta) )

    while True:
        msg, cliente = s.recvfrom(1024)
        opcao, *dados = msg.decode().split(';')
        opcao = valida_opcao(opcao)

        retorno = trata_mensagem(opcao, dados)
        s.sendto(retorno.encode(), cliente)
        break
    
    s.close()
    db.close()

    if banco_livros is not None:
        banco_livros.close()


def valida_opcao(opcao: str) -> int:
    if opcao == 'CREATE':
        return Cod.CADASTRO
    elif opcao == 'READ':
        return Cod.CONSULTAR
    elif opcao == 'UPDATE':
        return Cod.ALTERAR
    elif opcao == 'DELETE':
        return Cod.DELETAR
    elif opcao == 'EXIT':
        return Cod.SAIR
    else:
        return -1


def trata_mensagem(opcao: int, dados: List[str]) -> str:
    if opcao == Cod.CADASTRO:
        # TODO Separar os dados e criar um Livro
        # TODO Cadastrar o livro
        # TODO Retornar se deu pra cadastrar ou não
        pass
    elif opcao == Cod.CONSULTAR:
        # TODO Consultar os livros que se encaixam no filtro
        # TODO Retornar a lista de livros
        pass
    elif opcao == Cod.ALTERAR:
        # TODO Consultar os livros que se encaixam no filtro
        # TODO Retornar a lista de livros
        pass 
    elif opcao == Cod.DELETAR:
        # TODO Consultar os livros que se encaixam no filtro
        # TODO Retornar a lista de livros
        pass 
    elif opcao == Cod.SAIR:
        return 'Servidor fechado automaticamente.'
    else:
        return 'Opção inválida.'

if __name__ == '__main__':
    main()