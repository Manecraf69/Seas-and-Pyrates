import random
import os # os.system('cls' if os.name == 'nt' else 'clear')

vidaCascoJogador = 1000
vidaVelaJogador = 1000
numCanhoesJogador = 12
numtripulacaoJogador = 25

vidaCascoInimigo = 1000
vidaVelaInimigo = 1000
numCanhoesInimigo = 12
numtripulacaoInimigo = 25

rodada = 0
recarga = 3

cidades_existentes = [
    "Port Royal","Nassau","Tortuga","Kingston","New Providence","Barbados","St. Augustine","Charles Town","Belize City","Havana","Campeche",
    "Maracaibo","Porto Príncipe","Panama City","Bridgetown","Veracruz","Porto Bello","Cartagena","Portobelo","La Tortuga","Santo Domingo",
    "St. Kitts","St. Thomas","Saint-Malo","Galveston"]

cidades_conhecidas = []

def MostrarStatusJogador():
    velocidadeNavioJogador = vidaVelaJogador / 1000 * 12

    print("--- Navio jogador ---"
          "\nVida do casco:", vidaCascoJogador,
          "\nVida das velas:", vidaVelaJogador,
          "\nNúmero de canhões atuais:", numCanhoesJogador,
          "\nTripulação:", numtripulacaoJogador,
          "\nVelocidade máxima (nós):", round(velocidadeNavioJogador, 2))
    
def MostrarStatusInimigo():
    velocidadeNavioInimigo = vidaVelaInimigo / 1000 * 12

    print("--- Navio Inimigo ---"
          "\nVida do casco:", vidaCascoInimigo,
          "\nVida das velas:", vidaVelaInimigo,
          "\nNúmero de canhões atuais:", numCanhoesInimigo,
          "\nTripulação:", numtripulacaoInimigo,
          "\nVelocidade máxima (nós):", round(velocidadeNavioInimigo,2))
    
def ResetarStatus():
    global vidaCascoJogador, vidaCascoInimigo, vidaVelaJogador, vidaVelaInimigo
    vidaCascoJogador = 1000
    vidaCascoInimigo = 1000
    vidaVelaJogador = 1000
    vidaVelaInimigo = 1000

os.system('cls' if os.name == 'nt' else 'clear')
print("Bem vindo!\n")

while True:
    escolha = input("Digite o que deseja fazer:\n"
                    "\n1. Navegar pelos mares"
                    "\n2. Resto das opções...\n")
    # escolha = "1"

    if escolha == "1":
        evento = random.randint(1, 10)
        # evento = 5

        if evento <= 5: # Encontrar um navio
            os.system('cls' if os.name == 'nt' else 'clear')
            navegacao = input("Você vê um navio no horizonte. O que você faz?\n"
                "\n1. Atacar o navio"
                "\n2. Analisar o navio"
                "\n3. Se distanciar\n")
            # navegacao = "1"
            
            while True:
                if navegacao == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    while True:
                        MostrarStatusJogador()
                        print("")
                        MostrarStatusInimigo()
                        combate = input("\nDigite o que deseja fazer: \n"
                                        "\n1. Atirar no casco"
                                        "\n2. Atirar nas velas"
                                        "\n3. Atirar na tripulação"
                                        "\n4. Abordar"
                                        "\n5. Fugir\n")
                        
                        # --- Decisões do player --- #

                        if combate == "1":
                            os.system('cls' if os.name == 'nt' else 'clear')

                            if recarga >= 3:
                                dano = random.randint(10, 20) * numCanhoesJogador
                                vidaCascoInimigo -= dano
                                print("Você atira no casco do navio inimigo causando", dano, "de dano!")

                                if vidaCascoInimigo <= 0:
                                    print("\nVocê derrotou o inimigo!\n")
                                    ResetarStatus()
                                    break

                                if vidaCascoJogador <= 0:
                                    if len(cidades_conhecidas) > 0:
                                        print("\nVocê foi derrotado em batalha, respawnando em: " + random.choice(cidades_conhecidas)+"...")
                                    else:
                                        print("\nVocê foi derrotado em batalha, respawnando na cidade mais próxima: " + random.choice(cidades_existentes)+"...")
                                        
                                    ResetarStatus()
                                    print("\nSeu navio foi reparado e está pronto para mais aventuras!\n")
                                    break

                                recarga = 0
                            else:
                                print("Canhões principais recarregando por mais", 3 - recarga, "rodada(s)!")
                                rodada -= 1
                                recarga -= 1

                        elif combate == "2":
                            os.system('cls' if os.name == 'nt' else 'clear')

                            if vidaVelaInimigo > 0:
                                dano = random.randint(20, 30) * numCanhoesJogador
                                vidaVelaInimigo -= dano
                                print("Você atira nas velas do navio inimigo causando", dano, "de dano!")
                                if vidaVelaInimigo < 0:
                                    vidaVelaInimigo = 0
                                    print("As velas foram completamente destruídas, o navio inimigo está incapaz de se mover\n")
                            else:
                                print("O navio inimigo já está sem velas!\n"
                                      "Os tiros dos canhões passaram reto pelo navio sem causar danos...\n")
                                rodada -= 1

                        elif combate == "3":
                            os.system('cls' if os.name == 'nt' else 'clear')

                            if vidaVelaInimigo > 0:
                                dano = random.randint(20, 30) * numCanhoesJogador
                                vidaVelaInimigo -= dano
                                print("Você atira nas velas do navio inimigo causando", dano, "de dano!")
                                if vidaVelaInimigo < 0:
                                    vidaVelaInimigo = 0
                                    print("As velas foram completamente destruídas, o navio inimigo está incapaz de se mover\n")
                            else:
                                print("O navio inimigo já está sem velas!\n"
                                      "Os tiros dos canhões passaram reto pelo navio sem causar danos...\n")
                                rodada -= 1
                                
                        elif combate == "4":
                            os.system('cls' if os.name == 'nt' else 'clear')

                        elif combate == "5":
                            os.system('cls' if os.name == 'nt' else 'clear')
                            ResetarStatus()
                            break

                        else:
                            rodada -= 1
                            os.system('cls' if os.name == 'nt' else 'clear')

                        # --- Decisões do inimigo --- #

                        # Estratégias:

                        if combate == 69:
                            dano = random.randint(10, 20) * numCanhoesInimigo
                            vidaCascoJogador -= dano
                            print("O inimigo ataca de volta causando", dano, "de dano!")

                        rodada += 1
                        recarga += 1
                        print("Número de rounds:", rodada,"\n")

                        if recarga == 3:
                            print("Canhões principais prontos para atirar!\n")
                    break

                elif navegacao == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    MostrarStatusInimigo()
                    
                    escolhaNavegacao = input("\nDeseja atacar? (1. Sim / 2. Não)")
                    if escolhaNavegacao == "1":
                        navegacao = "1"
                    elif escolhaNavegacao == "2":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break

                elif navegacao == "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    pass

        elif evento <= 7: # Encontrar pilhagem
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você encontrou uma pilhagem flutuando na água!\n")

        elif evento == 8: # Encontrar cidade
            os.system('cls' if os.name == 'nt' else 'clear')

            if len(cidades_existentes) > 0:
                cidadeEncontrada = random.choice(cidades_existentes)
                print("Você encontrou a cidade: " + cidadeEncontrada + "!\n")
                
                cidades_existentes.remove(cidadeEncontrada)
                cidades_conhecidas.append(cidadeEncontrada)
            else:
                print("Você passou por " + random.choice(cidades_conhecidas) + "!\n")

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você viajou tranquilo")

    elif escolha == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Sem código\n")

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        pass