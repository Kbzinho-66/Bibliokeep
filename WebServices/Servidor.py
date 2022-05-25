import psycopg2
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

servidor = Flask(__name__)
api = Api(servidor)

parser = reqparse.RequestParser()
parser.add_argument('titulo')
parser.add_argument('autor')
parser.add_argument('ano', type=int, help='Ano precisa ser um inteiro.')
parser.add_argument('edicao', type=int, help='Edição precisa ser um inteiro.')


class Livros(Resource):
    def get(self):
        return todos_livros()

    def put(self):
        dados = parser.parse_args()
        print(dados)
        cadastrar_livro(dados)
        return dados, 201


api.add_resource(Livros, '/livros')


def todos_livros():
    banco_livros = psycopg2.connect(
        host='localhost',
        database='livros',
        user='postgres',
        password='postgres'
    )

    db = banco_livros.cursor()

    db.execute(
        ''' SELECT * FROM livrostemp
        '''
    )

    return db.fetchone().json()


@servidor.route('/', methods='POST')
def cadastrar_livro():
    dados = request.get_json()

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
    try:
        cod_autor, *_ = db.fetchone()
    except TypeError:
        db.execute('SELECT max(codigo) from autor;')
        cod_autor, *_ = db.fetchone()
        cod_autor += 1

        db.execute(
            ''' INSERT INTO autor (codigo, nome) VALUES (%s, %s)
            ''', (cod_autor, livro.autor)
        )

    db.execute(
        ''' SELECT codigo FROM livros WHERE titulo = %s
        ''', (livro.titulo,)
    )
    try:
        cod_livro, *_ = db.fetchone()
    except TypeError:
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


if __name__ == '__main__':
    servidor.run(debug=True)
