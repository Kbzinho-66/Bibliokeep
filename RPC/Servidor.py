import xmlrpc.server
import psycopg2

from Codigos import Filtro


def main():
    servidor = xmlrpc.server.SimpleXMLRPCServer(("localhost", 13000))
    servidor.register_function(cadastra_livro, "cadastrar")
    servidor.register_function(consulta_livros, "filtrar")
    servidor.register_function(deleta_livro, "deletar")
    servidor.register_function(altera_livro, "alterar")

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
    titulo = livro['titulo']
    autor = livro['autor']
    ano = livro['ano']
    edicao = livro['edicao']
    print(f'Para: {titulo} - {autor} ({ano}, {edicao}ª edição)')

    return 'Livro inserido'


def consulta_livros(filtro, busca):
    filtro = Filtro(filtro)

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
