import pickle
import socket
import sys
import Livro

def main():

    ip    = 'localhost'
    porta = 12000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    s.bind( (ip, porta) )

    while True:
        msg, cliente = s.recvfrom(1024)
        opcao = opcao_mensagem(msg)
        if opcao:
            retorno = trata_mensagem(msg)
        else:
            break
        s.sendto(retorno.encode(), cliente)
    
    s.close()


def opcao_mensagem(msg):
    if 'CREATE' in msg:
        return 1
    elif 'READ' in msg:
        return 2
    elif 'UPDATE' in msg:
        return 3
    elif 'DELETE' in msg:
        return 4
    elif 'EXIT' in msg:
        return 5
    else:
        return 0


def trata_mensagem(msg):
    
if __name__ == '__main__':
    main()