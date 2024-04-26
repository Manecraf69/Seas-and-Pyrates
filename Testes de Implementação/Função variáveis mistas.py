import os
import random

tipoVela = 0
velaInimigo = 1000
velaJogador = 1000
canhoes_jogador = 12
tripulacao_jogador = 35

def Combate(valorVela):
    os.system('cls' if os.name == 'nt' else 'clear')

    if valorVela > 0:
        dano = int(random.uniform(18, 20) * (min(canhoes_jogador, tripulacao_jogador) - 1))
        valorVela -= dano
        print("Você atira nas velas do navio inimigo causando", dano, "de dano!\n")
        if valorVela < 0:
            valorVela = 0
            print("\nAs velas foram completamente destruídas, o navio inimigo está incapaz de se mover")
    else:
        print("O navio inimigo já está sem velas!\n")

    return valorVela

velaJogador = Combate(velaJogador)
print(velaJogador)