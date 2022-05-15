class Livro:

    def __init__(self, codigo=0, titulo='', autor='', edicao=0, ano_pub=0):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.edicao = edicao
        self.ano_pub = ano_pub

    def __str__(self):
        return f'{self.autor.strip()} - {self.titulo}({self.ano_pub}, {self.edicao}ª edição)'

