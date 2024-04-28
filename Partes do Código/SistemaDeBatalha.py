import random
import os # os.system('cls' if os.name == 'nt' else 'clear')
import math

cidades_existentes = [
    "Port Royal","Nassau","Tortuga","Kingston","New Providence","Barbados","St. Augustine","Charles Town","Belize City","Havana","Campeche",
    "Maracaibo","Porto Príncipe","Panama City","Bridgetown","Veracruz","Porto Bello","Cartagena","Portobelo","La Tortuga","Santo Domingo",
    "St. Kitts","St. Thomas","Saint-Malo","Galveston"]

cidades_conhecidas = []

def MostrarStatusJogador():
    global velocidadeNavioJogador
    velocidadeNavioJogador = vela_jogador / 1000 * 12

    print("--- Navio Jogador ---"
          "\nVida do casco:", casco_jogador,
          "\nVida das velas:", vela_jogador,
          "\nNúmero de canhões atuais:", canhoes_jogador,
          "\nTripulação total:", tripulacao_jogador, "( No convés:", conves_jogador, ")"
          "\nVelocidade máxima (nós):", round(velocidadeNavioJogador, 2))
    
def MostrarStatusInimigo():
    global velocidadeNavioInimigo
    velocidadeNavioInimigo = vela_inimigo / 1000 * 12

    print("--- Navio Inimigo ---"
          "\nVida do casco:", casco_inimigo,
          "\nVida das velas:", vela_inimigo,
          "\nNúmero de canhões atuais:", canhoes_inimigo,
          "\nTripulação total:", tripulacao_inimigo, "( No convés:", conves_inimigo, ")"
          "\nVelocidade máxima (nós):", round(velocidadeNavioInimigo,2))

def ResetarStatus():
    global casco_jogador, casco_inimigo, vela_jogador, vela_inimigo, canhoes_jogador, canhoes_inimigo, tripulacao_jogador, tripulacao_inimigo, conves_jogador, conves_inimigo, trabucos_jogador, trabucos_inimigo, mosquetes_jogador, mosquetes_inimigo, rodada, recarga_canhoes, combate

    casco_jogador = 1000
    vela_jogador = 1000
    canhoes_jogador = 12
    tripulacao_jogador = 35
    conves_jogador = 14
    trabucos_jogador = 20
    mosquetes_jogador = 15

    casco_inimigo = 1000
    vela_inimigo = 1000
    canhoes_inimigo = 12
    tripulacao_inimigo = 35
    conves_inimigo = 14
    trabucos_inimigo = 20
    mosquetes_inimigo = 15

    rodada = 0
    recarga_canhoes = 3
    combate = 0

def SubirAoConves(valor_tripulacao):
    valor_conves = math.ceil(valor_tripulacao * 0.4)

    return valor_conves

def AtacarCasco(valor_casco, valor_canhao_usado, valor_canhao_destruido, valor_tripulacao):
    global recarga_canhoes, rodada, cidades_conhecidas, cidades_existentes, multiplicadorDeDano
    quebrar = 0
    os.system('cls' if os.name == 'nt' else 'clear')

    if recarga_canhoes == 3:
        dano_casco = int(random.uniform(18, 20) * (min(valor_canhao_usado, valor_tripulacao) - 1) - multiplicadorDeDano)
        if dano_casco <= 0:
            print("A distância entre os navios é muito grande para os canhões alcançarem!\n")
        else:
            valor_casco -= dano_casco
            print("Você atira no casco do navio inimigo causando", dano_casco, "de dano!\n")

            chance = random.randint(1, 20)
            if chance == 7:
                dano_canhao = int(random.uniform(0.1, 0.3) * (min(valor_canhao_destruido, valor_tripulacao) - 1) - multiplicadorDeDano)
                valor_canhao_destruido -= dano_canhao
                print("\nPor sorte você consegue destruir", dano_canhao ,"canhão(ões) do inimigo no disparo!\n")

        if valor_casco <= 0:
            print("\nVocê derrotou o inimigo!\n")
            quebrar = 1

        if casco_jogador <= 0:
            if len(cidades_conhecidas) > 0:
                print("\nVocê foi derrotado em batalha, respawnando em: " + random.choice(cidades_conhecidas)+"...")
            else:
                print("\nVocê foi derrotado em batalha, respawnando na cidade mais próxima: " + random.choice(cidades_existentes)+"...")
            
            print("\nSeu navio foi reparado e está pronto para mais aventuras!\n")
            quebrar = 1

        recarga_canhoes = -1
    else:
        print("Canhões principais recarregando por mais", 3 - recarga_canhoes, "rodada(s)!\n")
        rodada -= 1
        recarga_canhoes -= 1
    
    return valor_casco, valor_canhao_destruido, quebrar

def AtacarVelas(valor_vela, valor_canhao, valor_tripulacao):
    global recarga_canhoes, rodada
    os.system('cls' if os.name == 'nt' else 'clear')

    if valor_vela > 0:
        dano = int(random.uniform(18, 20) * (min(valor_canhao, valor_tripulacao) - 1) - multiplicadorDeDano)
        valor_vela -= dano
        print("Você atira nas velas do navio inimigo causando", dano, "de dano!\n")
        if valor_vela < 0:
            valor_vela = 0
            print("As velas foram completamente destruídas, o navio inimigo está incapaz de se mover")
    else:
        print("O navio inimigo já está sem velas!\n")
        recarga_canhoes -= 1
        rodada -= 1

    return valor_vela

def AtacarTripulacao(valor_tripulacao, valor_mosquetes, valor_conves_atacante, valor_conves_defensor):
    global rodada, recarga_canhoes
    os.system('cls' if os.name == 'nt' else 'clear')

    if valor_tripulacao > 0:
        dano = int(random.uniform(0.4, 0.7) * min(valor_mosquetes, valor_conves_atacante))
        if dano >= valor_tripulacao:
            print("Você matou toda a tripulação!\n"
                    "O navio está vazio e sem dono...\n")
            valor_tripulacao = 0

        else:
            valor_tripulacao -= dano
            print("Você atira com", min(valor_mosquetes, valor_conves_atacante), "mosquetes na tripulação inimiga matando", dano, "tripulantes!\n")

        valor_conves_defensor = SubirAoConves(valor_tripulacao)
    else:
        print("Sem mais tropas inimigas!\n")
        rodada -= 1
        recarga_canhoes -= 1

    return valor_tripulacao, valor_conves_defensor

os.system('cls' if os.name == 'nt' else 'clear')
print("Bem vindo!\n")

while True:
    escolha = input("Digite o que deseja fazer:\n"
                    "\n1. Navegar pelos mares"
                    "\n2. Resto das opções...\n")
    # escolha = "1"

    if escolha == "1":
        ResetarStatus()
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
                    print("Rodada atual: 0\n"
                          "Distância entre você e o inimigo: 100\n")
                    
                    while combate != "Encerrar":
                        MostrarStatusJogador()
                        print("")
                        MostrarStatusInimigo()
                        print("\nDigite o que deseja fazer: \n"
                                        "\n1. Atirar no casco (", 3 - recarga_canhoes, "rodadas para atirar )"
                                        "\n2. Atirar nas velas"
                                        "\n3. Atirar na tripulação"
                                        "\n4. Abalroar"
                                        "\n5. Abordar"
                                        "\n6. Se aproximar / Se afastar / Fugir")
                        combate = input("")

                        distanciaEntreNavios = 100
                        multiplicadorDeDano = (distanciaEntreNavios / 80) ** (distanciaEntreNavios / 80)
                        
                        # --- Decisões do player --- #

                        if combate == "1":
                            casco_inimigo, canhoes_inimigo, quebrar = AtacarCasco(casco_inimigo, canhoes_jogador, canhoes_inimigo, tripulacao_jogador)

                            if quebrar == 1:
                                break

                        elif combate == "2":
                            vela_inimigo = AtacarVelas(vela_inimigo, canhoes_jogador, tripulacao_jogador)

                        elif combate == "3":
                            tripulacao_inimigo, conves_inimigo = AtacarTripulacao(tripulacao_inimigo, mosquetes_jogador, conves_jogador, conves_inimigo)
                                
                        elif combate == "4":
                            os.system('cls' if os.name == 'nt' else 'clear')

                        elif combate == "6":
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print("Rodada atual:", rodada,"\n"
                                  "Distância entre você e o inimigo:", distanciaEntreNavios, "\n")
                            while True:
                                MostrarStatusJogador()
                                print("")
                                MostrarStatusInimigo()

                                decisaoDistancia = input("\n1. Se aproximar\n"
                                                        "2. Se afastar\n"
                                                        "3. Fugir\n"
                                                        "4. Cancelar\n"
                                                        "O que deseja fazer?\n")
                                
                                if decisaoDistancia == "1":
                                    os.system('cls' if os.name == 'nt' else 'clear')

                                elif decisaoDistancia == "2":
                                    os.system('cls' if os.name == 'nt' else 'clear')

                                elif decisaoDistancia == "3":
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    if velocidadeNavioJogador * 0.5 > velocidadeNavioInimigo or rodada == 0:
                                        print("Você conseguiu fugir com sucesso!\n")
                                        combate = "Encerrar"
                                        break

                                    elif velocidadeNavioJogador > velocidadeNavioInimigo:
                                        print("O navio inimigo consegue te acompanhar e o combate continua!\n")

                                    elif velocidadeNavioJogador < velocidadeNavioInimigo:
                                        print("Você tenta fugir, mas o inimigo é mais rápido!\n")

                                elif decisaoDistancia == "4":
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    rodada -= 1
                                    recarga_canhoes -= 1
                                    break

                                else:
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                
                                print("Rodada atual:", rodada,"\n"
                                      "Distância entre você e o inimigo:", distanciaEntreNavios, "\n")

                        else:
                            rodada -= 1
                            recarga_canhoes -= 1
                            os.system('cls' if os.name == 'nt' else 'clear')

                        # --- Decisões do inimigo --- #

                        # Estratégias:
                            # Colocar o sistema do inimigo aqui depois...

                        # --- Sistema de rounds --- #

                        rodada += 1
                        recarga_canhoes = min(recarga_canhoes + 1, 3)
                        
                        if combate != "Encerrar":
                            print("Rodada atual:", rodada,"\n"
                                  "Distância entre você e o inimigo:", distanciaEntreNavios, "\n")

                        if recarga_canhoes == 3 and combate != "Encerrar":
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
            print("Você viajou tranquilo\n")

    elif escolha == "2": # Tem que juntar os códigos (CódigoPrincipal.py, SistemaDeFrota.py e SistemaDeBatalha.py)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Sem código\n")

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        pass