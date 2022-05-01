import pickle
import psycopg2
import socket
from typing import List

from Classes import Query, Livro
from Codigos import Opcao, Filtro


def main():
    ip = 'localhost'
    porta = 12000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((ip, porta))

    while True:
        msg, cliente = s.recvfrom(1024)
        q: Query = pickle.loads(msg)
        opcao = q.query
        livros = [q.livro]
        filtro = q.filtro

        retorno = trata_mensagem(opcao, livros, filtro)
        s.sendto(retorno, cliente)
        if opcao == Opcao.SAIR:
            break

    s.close()


def trata_mensagem(opcao: Opcao, livros: List[Livro], filtro: Filtro) -> bytes:
    livro = livros[0]

    if opcao == Opcao.CADASTRO:
        cadastra_livro(livro)
        msg = 'Livro inserido com sucesso.'.encode()

    elif opcao == Opcao.FILTRAR:
        livros = consulta_livros(filtro, livro)
        msg = pickle.dumps(livros)

    elif opcao == Opcao.ALTERAR:
        altera_livro(livro)
        msg = 'Livro alterado com sucesso.'.encode()

    elif opcao == Opcao.DELETAR:
        deleta_livro(livro)
        msg = 'Livro deletado com sucesso.'.encode()

    elif opcao == Opcao.SAIR:
        msg = 'Servidor fechado automaticamente.'.encode()
    else:
        msg = 'Opção inválida.'.encode()

    # noinspection PyUnboundLocalVariable
    return msg


def cadastra_livro(livro):
    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    db.execute(
        ''' SELECT codigo FROM autor WHERE nome = %s
        ''', (livro.autor,)
    )
    cod_autor, *_ = db.fetchone()
    if not cod_autor:
        db.execute('SELECT max(codigo) from autor;')
        cod_autor += 1

        db.execute(
            ''' INSERT INTO autor (codigo, nome) VALUES (%s, %s)
            ''', (cod_autor, livro.autor)
        )

    db.execute(
        ''' SELECT codigo FROM livros WHERE titulo = %s
        '''
    )
    cod_livro, *_ = db.fetchone()
    if not cod_livro:
        db.execute('SELECT max(codigo) from livros;')
        cod_livro, *_ = db.fetchone()
        cod_livro += 1
        db.execute(
            ''' INSERT INTO livros (codigo, titulo) VALUES (%s, %s)
            ''', (cod_livro, livro.titulo)
        )

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

    db.execute('SELECT max(codigo) from livrostemp;')
    cod_livro, *_ = db.fetchone()
    cod_livro += 1
    db.execute(
        ''' INSERT INTO livrostemp (codigo, titulo, autor, edicao, ano)
        VALUES (%s, %s, %s, %s, %s); ''',
        (cod_livro, livro.titulo, livro.autor, livro.edicao, livro.ano_pub)
    )
    banco_livros.commit()

    db.close()

    if banco_livros is not None:
        banco_livros.close()

    print('Livro inserido:')
    print(livro)


def consulta_livros(filtro: Filtro, livro: Livro) -> List[Livro]:
    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    print('Consulta:')
    if filtro == Filtro.TITULO:
        print(f'Título = {livro.titulo}')
        db.execute(
            ''' SELECT * FROM livrostemp WHERE titulo ~ %s
            ''', (livro.titulo,)
        )
    elif filtro == Filtro.AUTOR:
        print(f'Autor = {livro.autor}')
        db.execute(
            ''' SELECT * FROM livrostemp WHERE autor ~ %s
            ''', (livro.autor,)
        )
    elif filtro == Filtro.ANO_EDI:
        print(f'Ano = {livro.ano_pub} e Edição = {livro.edicao}')
        db.execute(
            ''' SELECT * FROM livrostemp where ano = %s and edicao = %s
            ''', (livro.ano_pub, livro.edicao)
        )

    resultado = db.fetchmany(20)
    livros = []
    for item in resultado:
        codigo, titulo, autor, edicao, ano = item
        livros.append(Livro(codigo, titulo, autor, edicao, ano))

    db.close()

    if banco_livros is not None:
        banco_livros.close()

    return livros


def deleta_livro(livro):
    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    print('Deletar:')
    print(f'{livro.codigo} -> ' + livro.__str__())
    db.execute(
        ''' DELETE FROM edicao WHERE codigolivro = %s
        ''', (livro.codigo,)
    )
    db.execute(
        ''' DELETE FROM livroautor WHERE codigolivro = %s
        ''', (livro.codigo,)
    )
    db.execute(
        ''' DELETE FROM livros WHERE codigo = %s;
        ''', (livro.codigo,)
    )
    db.execute(
        ''' DELETE FROM livrostemp WHERE codigo = %s;
        ''', (livro.codigo,)
    )

    banco_livros.commit()
    db.close()

    if banco_livros is not None:
        banco_livros.close()


def altera_livro(livro):

    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    print('Alterar:')
    print(f'Para: {livro.__str__()}')
    # TODO Atualizar o livro

    banco_livros.commit()
    db.close()

    if banco_livros is not None:
        banco_livros.close()


if __name__ == '__main__':
    main()
