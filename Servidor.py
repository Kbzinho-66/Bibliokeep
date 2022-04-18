import pickle, socket, psycopg2
from typing import List

import Livro
from Codigos import Cod

def main():

    postgresql = psycopg2.connect(
        host     = 'localhost',
        database = 'livros',
        user     = 'postgres',
        password = 'postgres'
    )

    db = postgresql.cursor()

    ip    = 'localhost'
    porta = 12000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    s.bind( (ip, porta) )

    while True:
        msg, cliente = s.recvfrom(1024)
        opcao, *dados = msg.split(';')
        opcao = valida_opcao(opcao)
        if opcao:
            retorno = trata_mensagem(opcao, dados)
        else:
            break
        s.sendto(retorno.encode(), cliente)
    
    s.close()
    db.close()

    if postgresql is not None:
        postgresql.close()


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
    pass

if __name__ == '__main__':
    main()