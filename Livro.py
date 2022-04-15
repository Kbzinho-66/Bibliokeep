import pickle

class Livro:
    
    def __init__(self, codigo, nome, autor, edicao, ano_pub):
        self.codigo  = codigo
        self.nome    = nome
        self.autor   = autor
        self.edicao  = edicao
        self.ano_pub = ano_pub
        
    def __str__(self):
        return f'{self.nome} - {self.autor}({self.ano_pub}), {self.edicao}ª edição'
