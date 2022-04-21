class Livro:
    
    def __init__(self, nome, autor, edicao, ano_pub):
        codigo       = 0
        self.nome    = nome
        self.autor   = autor
        self.edicao  = edicao
        self.ano_pub = ano_pub
        
    def __str__(self):
        return f'{self.autor} - {self.nome}({self.ano_pub}, {self.edicao}ª edição)'

class Query:
    
    def __init__(self, query, livros):
        self.query = query
        self.livros = livros