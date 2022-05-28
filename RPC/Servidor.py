import xmlrpc.server
import psycopg2

from Codigos import Filtro


def main():
    servidor = xmlrpc.server.SimpleXMLRPCServer(("localhost", 13000))
    servidor.register_function(cadastra_livro, "cadastrar")
    servidor.register_function(consulta_livros, "filtrar")
    servidor.register_function(deleta_livro, "deletar")
    servidor.register_function(altera_livro, "alterar")

    # TODO Dar um jeito de fechar melhor
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.shutdown()
        print('\nServidor fechado.')


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
        ''', (livro['autor'],)
    )
    try:
        cod_autor, *_ = db.fetchone()
    except TypeError:
        db.execute('SELECT max(codigo) from autor;')
        cod_autor, *_ = db.fetchone()
        cod_autor += 1

        db.execute(
            ''' INSERT INTO autor (codigo, nome) VALUES (%s, %s)
            ''', (cod_autor, livro['autor'])
        )

    db.execute(
        ''' SELECT codigo FROM livros WHERE titulo = %s
        ''', (livro['titulo'],)
    )
    try:
        cod_livro, *_ = db.fetchone()
    except TypeError:
        db.execute('SELECT max(codigo) from livros;')
        cod_livro, *_ = db.fetchone()
        cod_livro += 1

        db.execute(
            ''' INSERT INTO livros (codigo, titulo) VALUES (%s, %s)
            ''', (cod_livro, livro['titulo'])
        )

    db.execute(
        ''' INSERT INTO edicao (codigolivro, numero, ano) VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        ''', (cod_livro, livro['edicao'], livro['ano'])
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
        (cod_livro, livro['titulo'], livro['autor'], livro['edicao'], livro['ano'])
    )
    banco_livros.commit()

    db.close()

    if banco_livros is not None:
        banco_livros.close()

    print('Livro inserido:')
    print(livro)

    return 'Livro inserido'


def consulta_livros(filtro, busca):
    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    print('Consulta:')
    if filtro == Filtro.TITULO:
        print(f'Título = {busca}')
        db.execute(
            ''' SELECT * FROM livrostemp WHERE titulo ~ %s
            ''', (busca,)
        )
    elif filtro == Filtro.AUTOR:
        print(f'Autor = {busca}')
        db.execute(
            ''' SELECT * FROM livrostemp WHERE autor ~ %s
            ''', (busca,)
        )
    elif filtro == Filtro.ANO_EDI:
        ano, edicao = busca
        print(f'Ano = {ano} e Edição = {edicao}')
        db.execute(
            ''' SELECT * FROM livrostemp where ano = %s and edicao = %s
            ''', (ano, edicao)
        )

    resultado = db.fetchmany(20)
    livros = []
    for item in resultado:
        codigo, titulo, autor, edicao, ano = item
        livros.append({
            'codigo': int(codigo),
            'titulo': titulo,
            'autor': autor,
            'ano': int(ano),
            'edicao': int(edicao)
        })

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
    codigo = livro['codigo']
    titulo = livro['titulo']
    autor = livro['autor']
    print(f'{titulo.strip()}, {autor}')
    db.execute(
        ''' DELETE FROM edicao WHERE codigolivro = %s
        ''', (codigo,)
    )
    db.execute(
        ''' DELETE FROM livroautor WHERE codigolivro = %s
        ''', (codigo,)
    )
    db.execute(
        ''' DELETE FROM livros WHERE codigo = %s;
        ''', (codigo,)
    )
    db.execute(
        ''' DELETE FROM livrostemp WHERE codigo = %s;
        ''', (codigo,)
    )

    banco_livros.commit()
    db.close()

    if banco_livros is not None:
        banco_livros.close()

    return 'Livro deletado.'


def altera_livro(livro):
    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    db.execute(
        ''' SELECT * FROM livrostemp WHERE codigo = %s
        ''', (livro['codigo'],)
    )
    cod_ant, titulo_ant, autor_ant, edicao_ant, ano_ant, *_ = db.fetchone()

    print('Alterar:')
    print(f'De: {titulo_ant} - {autor_ant} ({ano_ant}, {edicao_ant}ª edição)')

    titulo = livro['titulo']
    autor = livro['autor']
    ano = livro['ano']
    edicao = livro['edicao']
    print(f'Para: {titulo} - {autor} ({ano}, {edicao}ª edição)')

    db.execute(
        ''' UPDATE livros
            SET titulo = %s
            WHERE titulo = %s
        ''', (livro['titulo'], livro['titulo'])
    )

    db.execute(
        ''' SELECT codigoautor FROM livroautor WHERE codigolivro = %s
        ''', (livro['codigo'],)
    )
    cod_autor, *_ = db.fetchone()
    db.execute(
        ''' UPDATE autor
            SET nome = %s
            WHERE codigo = %s
        ''', (livro['autor'], cod_autor)
    )

    db.execute(
        ''' UPDATE livrostemp
            SET titulo = %s, autor = %s, edicao = %s, ano = %s
            WHERE codigo = %s
        ''', (livro['titulo'], livro['autor'], livro['edicao'], livro['ano'], livro['codigo'])
    )

    banco_livros.commit()
    db.close()

    if banco_livros is not None:
        banco_livros.close()

    return 'Livro alterado com sucesso.'


if __name__ == '__main__':
    main()
