import random
import os # os.system('cls' if os.name == 'nt' else 'clear')
import math

casco_jogador = 1000
vela_jogador = 1000
canhoes_jogador = 12
tripulacao_jogador = 35
conves_jogador = math.ceil(tripulacao_jogador * 0.4)
trabucos_jogador = 20
mosquetes_jogador = 15

casco_inimigo = 1000
vela_inimigo = 1000
canhoes_inimigo = 12
tripulacao_inimigo = 35
conves_inimigo = math.ceil(tripulacao_inimigo * 0.4)
trabucos_inimigo = 20
mosquetes_inimigo = 15

rodada = 0
recarga_canhoes = 3

cidades_existentes = [
    "Port Royal","Nassau","Tortuga","Kingston","New Providence","Barbados","St. Augustine","Charles Town","Belize City","Havana","Campeche",
    "Maracaibo","Porto Príncipe","Panama City","Bridgetown","Veracruz","Porto Bello","Cartagena","Portobelo","La Tortuga","Santo Domingo",
    "St. Kitts","St. Thomas","Saint-Malo","Galveston"]

cidades_conhecidas = []

def MostrarStatusJogador():
    velocidadeNavioJogador = vela_jogador / 1000 * 12

    print("--- Navio jogador ---"
          "\nVida do casco:", casco_jogador,
          "\nVida das velas:", vela_jogador,
          "\nNúmero de canhões atuais:", canhoes_jogador,
          "\nTripulação total:", tripulacao_jogador, "( No convés:", math.ceil(tripulacao_jogador * 0.4), ")"
          "\nVelocidade máxima (nós):", round(velocidadeNavioJogador, 2))
    
def MostrarStatusInimigo():
    velocidadeNavioInimigo = vela_inimigo / 1000 * 12

    print("--- Navio Inimigo ---"
          "\nVida do casco:", casco_inimigo,
          "\nVida das velas:", vela_inimigo,
          "\nNúmero de canhões atuais:", canhoes_inimigo,
          "\nTripulação total:", tripulacao_inimigo, "( No convés:", math.ceil(tripulacao_inimigo * 0.4), ")"
          "\nVelocidade máxima (nós):", round(velocidadeNavioInimigo,2))
    
def ResetarStatus():
    global casco_jogador, casco_inimigo, vela_jogador, vela_inimigo, rodada, recarga_canhoes
    casco_jogador = 1000
    casco_inimigo = 1000
    vela_jogador = 1000
    vela_inimigo = 1000
    rodada = 0
    recarga_canhoes = 3

def CausarDano():
    global dano, canhoes_jogador, tripulacao_jogador, multiplicadorDeDano
    dano = int(random.uniform(18, 20) * (min(canhoes_jogador, tripulacao_jogador) - 1) - multiplicadorDeDano)
    return dano

os.system('cls' if os.name == 'nt' else 'clear')
print("Bem vindo!\n")

while True:
    # escolha = input("Digite o que deseja fazer:\n"
    #                 "\n1. Navegar pelos mares"
    #                 "\n2. Resto das opções...\n")
    escolha = "1"

    if escolha == "1":
        # evento = random.randint(1, 10)
        evento = 5

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
                    print("Rodada atual: 0\n"
                          "Distância entre você e o inimigo: 100\n")
                    
                    while True:
                        MostrarStatusJogador()
                        print("")
                        MostrarStatusInimigo()
                        print("\nDigite o que deseja fazer: \n"
                                        "\n1. Atirar no casco (", 3 - recarga_canhoes, "rodadas para atirar )"
                                        "\n2. Atirar nas velas"
                                        "\n3. Atirar na tripulação"
                                        "\n4. Abalroar"
                                        "\n5. Abordar"
                                        "\n6. Fugir")
                        combate = input("")

                        distanciaEntreNavios = 100
                        multiplicadorDeDano = (distanciaEntreNavios / 80) ** (distanciaEntreNavios / 80)
                        
                        # --- Decisões do player --- #

                        if combate == "1":
                            os.system('cls' if os.name == 'nt' else 'clear')

                            if recarga_canhoes == 3:
                                CausarDano()
                                if dano <= 0:
                                    print("A distância entre os navios é muito grande para os canhões alcançarem!\n")
                                else:
                                    casco_inimigo -= dano
                                    print("Você atira no casco do navio inimigo causando", dano, "de dano!")

                                    chance = random.randint(1, 20)
                                    if chance == 7:
                                        canhaoDestruido = int(random.uniform(0.1, 0.3) * canhoes_jogador)
                                        canhoes_inimigo -= canhaoDestruido
                                        print("\nPor sorte você consegue destruir", canhaoDestruido ,"canhão(ões) do inimigo no disparo!\n")

                                if casco_inimigo <= 0:
                                    print("\nVocê derrotou o inimigo!\n")
                                    ResetarStatus()
                                    break

                                if casco_jogador <= 0:
                                    if len(cidades_conhecidas) > 0:
                                        print("\nVocê foi derrotado em batalha, respawnando em: " + random.choice(cidades_conhecidas)+"...")
                                    else:
                                        print("\nVocê foi derrotado em batalha, respawnando na cidade mais próxima: " + random.choice(cidades_existentes)+"...")
                                        
                                    ResetarStatus()
                                    print("\nSeu navio foi reparado e está pronto para mais aventuras!\n")
                                    break

                                recarga_canhoes = -1
                            else:
                                print("Canhões principais recarregando por mais", 3 - recarga_canhoes, "rodada(s)!")
                                rodada -= 1
                                recarga_canhoes -= 1

                        elif combate == "2":
                            os.system('cls' if os.name == 'nt' else 'clear')

                            if vela_inimigo > 0:
                                CausarDano()
                                vela_inimigo -= dano
                                print("Você atira nas velas do navio inimigo causando", dano, "de dano!\n")
                                if vela_inimigo < 0:
                                    vela_inimigo = 0
                                    print("As velas foram completamente destruídas, o navio inimigo está incapaz de se mover")
                            else:
                                print("O navio inimigo já está sem velas!\n")
                                recarga_canhoes -= 1
                                rodada -= 1

                        elif combate == "3":
                            os.system('cls' if os.name == 'nt' else 'clear')

                            if tripulacao_inimigo > 0:
                                dano = int(random.uniform(0.4, 0.7) * min(mosquetes_jogador, conves_jogador))
                                if dano >= tripulacao_inimigo:
                                    print("Você matou toda a tripulação!\n"
                                          "O navio está vazio e sem dono...\n")
                                    tripulacao_inimigo = 0

                                else:
                                    tripulacao_inimigo -= dano
                                    print("Você atira com", min(mosquetes_jogador, conves_jogador), "mosquetes na tripulação inimiga matando", dano, "tripulantes!\n")
                            else:
                                print("Sem mais tropas inimigas!\n")
                                rodada -= 1
                                recarga_canhoes -= 1
                                
                        elif combate == "4":
                            os.system('cls' if os.name == 'nt' else 'clear')

                        elif combate == "6":
                            os.system('cls' if os.name == 'nt' else 'clear')
                            ResetarStatus()
                            break

                        else:
                            rodada -= 1
                            recarga_canhoes -= 1
                            os.system('cls' if os.name == 'nt' else 'clear')

                        # --- Decisões do inimigo --- #

                        # Estratégias:

                        rodada += 1
                        recarga_canhoes = min(recarga_canhoes + 1, 3)
                        print("Rodada atual:", rodada,"\n"
                              "Distância entre você e o inimigo:", distanciaEntreNavios, "\n")

                        if recarga_canhoes == 3:
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