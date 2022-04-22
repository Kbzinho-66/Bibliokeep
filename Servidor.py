import pickle, socket, psycopg2
from typing import List

from Classes import Query, Livro
from Codigos import Cod

def main():

    ip    = 'localhost'
    porta = 12000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    s.bind( (ip, porta) )

    while True:
        msg, cliente = s.recvfrom(1024)
        q: Query = pickle.loads(msg)
        opcao = q.query
        livros = [q.livros] # REVIEW Ainda não sei o que acontece se receber uma lista mesmo

        retorno = trata_mensagem(opcao, livros)
        s.sendto(retorno.encode(), cliente)
        if opcao == Cod.SAIR:
            break
    
    s.close()


def trata_mensagem(opcao: Cod, livros: List[Livro]) -> str:

    banco_livros = psycopg2.connect(
        host     = 'localhost',
        database = 'livros',
        user     = 'postgres',
        password = 'postgres'
    )

    db = banco_livros.cursor()

    if opcao == Cod.CADASTRO:
        livro = livros[0]
        db.execute('SELECT max(codigo) from livros;')        
        cod_livro = db.fetchone()
        db.execute('SELECT max(codigo) from autor;')
        cod_autor = db.fetchone()

        db.execute(
            ''' INSERT INTO autor (codigo, nome) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING codigo;
            ''', (cod_autor, livro.autor)
        )
        cod_autor = db.fetchone()

        db.execute(
            ''' INSERT INTO livros (codigo, titulo) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                return codigo;
            ''', (cod_livro, livro.nome)
        )
        cod_livro = db.fetchone()

        db.execute(
            ''' INSERT INTO edicao (codigolivro, numero, ano) VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            ''', (cod_livro, livro.edicao, livro.ano_pub)
        )

        db.execute(
            ''' INSERT INTO livroautor (codigolivro, codigoautor) VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            ''', (cod_livro, cod_autor)
        )

        db.execute(
            ''' INSERT INTO livrostemp (codigo, titulo, autor, edicao, ano)
            VALUES (%s, %s, %s, %s, %s); ''', 
            (cod_livro, livro.nome, livro.autor, livro.edicao, livro.ano_pub)
        )
        banco_livros.commit()
        msg = 'Livro inserido com sucesso.'
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
        msg = 'Servidor fechado automaticamente.'
    else:
        msg = 'Opção inválida.'

    db.close()

    if banco_livros is not None:
        banco_livros.close()

    return msg


if __name__ == '__main__':
    main()
