import random
import os # os.system('cls')
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
          "\nCanhões primários:", canhoes_casco_jogador,
          "\nCanhões secundários:", canhoes_vela_jogador,
          "\nTripulação total:", tripulacao_jogador, "( No convés:", conves_jogador, ")"
          "\nVelocidade máxima (nós):", round(velocidadeNavioJogador, 2))
    
def MostrarStatusInimigo():
    global velocidadeNavioInimigo
    velocidadeNavioInimigo = vela_inimigo / 1000 * 12

    print("--- Navio Inimigo ---"
          "\nVida do casco:", casco_inimigo,
          "\nVida das velas:", vela_inimigo,
          "\nCanhões principais:", canhoes_casco_inimigo,
          "\nCanhões secundários:", canhoes_vela_inimigo,
          "\nTripulação total:", tripulacao_inimigo, "( No convés:", conves_inimigo, ")"
          "\nVelocidade máxima (nós):", round(velocidadeNavioInimigo,2))

def MostrarRodadaDistancia():
    print("Rodada atual:", rodada,"\n"
          "Distância entre você e o inimigo:", distanciaEntreNavios, "m\n")
    
def ResetarStatus():
    global casco_jogador, casco_inimigo, vela_jogador, vela_inimigo, canhoes_casco_jogador, canhoes_casco_inimigo, tripulacao_jogador, tripulacao_inimigo, conves_jogador, conves_inimigo, trabucos_jogador, trabucos_inimigo, mosquetes_jogador, mosquetes_inimigo, rodada, recarga_canhoes_casco_jogador, recarga_canhoes_casco_inimigo, combate, distanciaEntreNavios, recarga_canhoes_vela_jogador, recarga_canhoes_vela_inimigo, canhoes_vela_jogador, canhoes_vela_inimigo, recarga_mosquetes_jogador, recarga_mosquetes_inimigo

    casco_jogador = 1000
    vela_jogador = 1000
    canhoes_casco_jogador = 12
    canhoes_vela_jogador = 4
    tripulacao_jogador = 35
    conves_jogador = 14
    trabucos_jogador = 20
    mosquetes_jogador = 15
    recarga_canhoes_casco_jogador = 3
    recarga_canhoes_vela_jogador = 4
    recarga_mosquetes_jogador = 2

    casco_inimigo = 1000
    vela_inimigo = 1000
    canhoes_casco_inimigo = 12
    canhoes_vela_inimigo = 4
    tripulacao_inimigo = 35
    conves_inimigo = 14
    trabucos_inimigo = 20
    mosquetes_inimigo = 15
    recarga_canhoes_casco_inimigo = 3
    recarga_canhoes_vela_inimigo = 4
    recarga_mosquetes_inimigo = 2

    distanciaEntreNavios = 100
    rodada = 0
    combate = 0

def RecargaCanhoesJogador():
    global recarga_canhoes_casco_jogador, recarga_canhoes_vela_jogador

    recarga_canhoes_casco_jogador = min(recarga_canhoes_casco_jogador + 1, 4)
    recarga_canhoes_vela_jogador = min(recarga_canhoes_vela_jogador + 1, 5)

def RecargaCanhoesInimigo():
    global recarga_canhoes_casco_inimigo, recarga_canhoes_vela_inimigo

    recarga_canhoes_casco_inimigo = min(recarga_canhoes_casco_inimigo + 1, 3)
    recarga_canhoes_vela_inimigo = min(recarga_canhoes_vela_inimigo + 1, 4)

def SubirAoConves(valor_tripulacao):
    valor_conves = math.ceil(valor_tripulacao * 0.4)

    return valor_conves

def AtacarCasco(valor_turno, valor_casco, valor_recarga_canhoes, valor_canhao_atacante, valor_canhao_defensor, valor_tripulacao_atacante, valor_tripulação_defensor):
    global rodada, nova_rodada
    quebrar = 0

    if valor_recarga_canhoes >= 3:

        if distanciaEntreNavios >= 300:
            print("A distância entre os navios é muito grande para os canhões alcançarem!\n")
        else:
            danoCasco = 0
            for i in range(min(valor_canhao_atacante, valor_tripulacao_atacante)):
                danoPorCanhao = int(random.randint(16, 20) * (1 - distanciaEntreNavios / 300)) # Reduz o dano conforme a distância
                danoCasco += danoPorCanhao
            valor_casco -= danoCasco
            valor_recarga_canhoes = 0

            if valor_turno == "jogador":
                print("Você atira no casco do navio inimigo causando", danoCasco, "de dano!\n")
            elif valor_turno == "inimigo":
                print("O inimigo atira no seu casco causando", danoCasco, "de dano...\n")

            if valor_casco <= 0:
                if valor_turno == "jogador":
                    print("Você derrotou o inimigo e ele afunda lentamente no fundo oceano...\n")
                if valor_turno == "inimigo":
                    JogadorDerrotado()
                quebrar = 1

            if quebrar != 1:
                if valor_canhao_defensor > 0:
                    dano = 0
                    for _ in range(min(valor_canhao_atacante, valor_tripulacao_atacante)):
                        if random.random() <= 0.03:
                            dano += 1

                    if dano > 0:
                        valor_canhao_defensor -= dano
                        if valor_turno == "jogador":
                            print("Por sorte você consegue destruir", dano ,"canhão(ões) do inimigo no disparo!\n")
                        elif valor_turno == "inimigo":
                            print("O inimigo acerta e destrói", dano, "canhão(ões) seu(s)...\n")
                if valor_tripulação_defensor > 0:
                    dano = 0
                    for _ in range(min(valor_canhao_atacante, valor_tripulacao_atacante)):
                        if random.random() <= 0.03:
                            dano += 1

                    if dano > 0:
                        valor_tripulação_defensor -= dano
                        if valor_turno == "jogador":
                            print("Nos disparos dos canhões você mata", dano ,"tripulante(s) do inimigo!\n")
                        elif valor_turno == "inimigo":
                            print("O inimigo dispara e mata", dano, "tripulante(s) seu(s)...\n")
                        
                        SubirAoConves(valor_tripulação_defensor)

            # Recarga de ferramentas e contador de rodada
            if valor_turno == "jogador":
                rodada += 1
                nova_rodada = rodada
                RecargaCanhoesJogador()

    else:
        print("Canhões principais recarregando por mais", 3 - valor_recarga_canhoes, "rodada(s)!\n")
    
    return valor_casco, valor_canhao_defensor, valor_recarga_canhoes, valor_tripulação_defensor, quebrar

def AtacarVelas(valor_turno, valor_recarga_canhoes, valor_vela, valor_canhao, valor_tripulacao):
    global rodada, nova_rodada

    if valor_vela > 0:

        if valor_recarga_canhoes >= 3:
            if distanciaEntreNavios >= 250:
                print("A distância entre os navios é muito grande para os canhões alcançarem!\n")
            else:
                danoVela = 0
                for i in range(min(valor_canhao, valor_tripulacao)):
                    danoPorCanhao = int(random.randint(58, 80) * (1 - distanciaEntreNavios / 300)) # Reduz o dano conforme a distância
                    danoVela += danoPorCanhao
                valor_vela -= danoVela
                valor_recarga_canhoes = 0

                if valor_turno == "jogador":
                    print("Você atira nas velas do navio inimigo causando", danoVela, "de dano!\n")
                elif valor_turno == "inimigo":
                    print("O inimigo atira nas suas velas e causa", danoVela, "de dano...\n")
                if valor_vela < 0:
                    valor_vela = 0
                    if valor_turno == "jogador":
                        print("As velas inimigas foram completamente destruídas, o navio dele está incapaz de se mover!\n")
                    elif valor_turno == "inimigo":
                        print("Suas velas foram completamente destruídas, você está imóvel...\n")

                # Recarga de ferramentas e contador de rodada
                if valor_turno == "jogador":
                    rodada += 1
                    nova_rodada = rodada
                    RecargaCanhoesJogador()
                elif valor_turno == "inimigo":
                    RecargaCanhoesInimigo()

        else:
            print("Canhões de ataque de velas recarregando por mais", 4 - valor_recarga_canhoes, "rodada(s)!\n")
                
    else:
        print("O navio inimigo já está sem velas!\n")

    return valor_vela, valor_recarga_canhoes

def AtacarTripulacao(valor_turno, valor_tripulacao, valor_mosquetes, valor_conves_atacante, valor_conves_defensor):
    global rodada, nova_rodada

    if valor_tripulacao > 0:
        quebrar = 0
        danoTripulacao = 0
        for i in range(min(valor_mosquetes, valor_conves_atacante)):
            danoPorCanhao = int(random.uniform(1, 2) * (1 - distanciaEntreNavios / 300)) # Reduz o dano conforme a distância
            danoTripulacao += danoPorCanhao

        if distanciaEntreNavios >= 150:
            print("A distância entre os navios é muito grande para os canhões alcançarem!\n")
        else:
            if danoTripulacao >= valor_tripulacao:
                if valor_turno == "jogador":
                    print("Você matou toda a tripulação!\n"
                            "O navio está vazio e sem dono...\n")
                elif valor_turno == "inimigo":
                    print("O navio inimigo matou toda sua tripulação...\n")
                    JogadorDerrotado()
                    quebrar = 1

                valor_tripulacao = 0

            else:
                valor_tripulacao -= danoTripulacao
                if valor_turno == "jogador":
                    print("Você atira com", min(valor_mosquetes, valor_conves_atacante), "mosquetes na tripulação inimiga matando", danoTripulacao, "tripulantes!\n")
                elif valor_turno == "inimigo":
                    print("O inimigo atira na sua tripulação e mata", danoTripulacao, "tripulantes...\n")

            valor_conves_defensor = SubirAoConves(valor_tripulacao)

            # Recarga de ferramentas e contador de rodada
            if valor_turno == "jogador":
                rodada += 1
                nova_rodada = rodada
                RecargaCanhoesJogador()
            elif valor_turno == "inimigo":
                RecargaCanhoesInimigo()
    else:
        print("Sem mais tropas inimigas!\n")

    return valor_tripulacao, valor_conves_defensor, quebrar

def JogadorDerrotado():
    if len(cidades_conhecidas) > 0:
        print("Você foi derrotado em batalha, respawnando em: " + random.choice(cidades_conhecidas)+"...")
    else:
        print("Você foi derrotado em batalha, respawnando na cidade mais próxima: " + random.choice(cidades_existentes)+"...")
    
    print("\nSeu navio foi reparado e está pronto para mais aventuras!\n")

os.system('cls')
print("Bem vindo!\n")

while True:
    # escolha = input("Digite o que deseja fazer:\n"
    # "\n1. Navegar pelos mares"
    # "\n2. Resto das opções...\n")
    escolha = "1"

    if escolha == "1":
        # evento = random.randint(1, 10)
        evento = 5

        if evento <= 5: # Encontrar um navio
            os.system('cls')
            # navegacao = input("Você vê um navio no horizonte. O que você faz?\n"
            # "\n1. Atacar o navio"
            # "\n2. Analisar o navio"
            # "\n3. Se distanciar\n")
            navegacao = "1"
            ResetarStatus()
            
            while True:
                if navegacao == "1":
                    os.system('cls')
                    MostrarRodadaDistancia()
                    
                    while combate != "Encerrar":
                        quebrar = 0
                        nova_rodada = 0
            
                        MostrarStatusJogador()
                        print("")
                        MostrarStatusInimigo()
                        print("\nDigite o que deseja fazer: \n"
                                "\n1. Atirar no casco (", min(3, recarga_canhoes_casco_jogador), "/ 3 )"
                                "\n2. Atirar nas velas (", min(4, recarga_canhoes_vela_jogador), "/ 4 )"
                                "\n3. Atirar na tripulação"
                                "\n4. Abalroar"
                                "\n5. Abordar"
                                "\n6. Se aproximar"
                                "\n7. Se afastar"
                                "\n8. Fugir")
                        combate = input("")
                        
                        # --- Decisões do player --- #

                        if combate == "1":
                            os.system('cls')
                            casco_inimigo, canhoes_casco_inimigo, recarga_canhoes_casco_jogador, tripulacao_inimigo, quebrar = AtacarCasco("jogador", casco_inimigo, recarga_canhoes_casco_jogador, canhoes_casco_jogador, canhoes_casco_inimigo, tripulacao_jogador, tripulacao_inimigo)

                        elif combate == "2":
                            os.system('cls')
                            vela_inimigo, recarga_canhoes_vela_jogador = AtacarVelas("jogador", recarga_canhoes_vela_jogador, vela_inimigo, canhoes_vela_jogador, tripulacao_jogador)

                        elif combate == "3":
                            os.system('cls')
                            tripulacao_inimigo, conves_inimigo, quebrar = AtacarTripulacao("jogador", tripulacao_inimigo, mosquetes_jogador, conves_jogador, conves_inimigo)
                                
                        elif combate == "4":
                            os.system('cls')

                        elif combate == "5":
                            os.system('cls')

                        elif combate == "6":
                            os.system('cls')
                                
                            if distanciaEntreNavios > 0 and velocidadeNavioJogador > 0:
                                distanciaEntreNavios -= 50
                                rodada += 1
                            else:
                                print("Vocês já estão colados um ao outro!\n")

                        elif combate == "7":
                            os.system('cls')

                            if distanciaEntreNavios < 350 and velocidadeNavioJogador > 0:
                                distanciaEntreNavios += 50
                                rodada += 1
                            else:
                                print("Vocês já estão muito longe um do outro!\n")

                        elif combate == "8":
                            os.system('cls')
                        
                            if velocidadeNavioJogador * 0.8 > velocidadeNavioInimigo or rodada == 0 or tripulacao_inimigo == 0 and velocidadeNavioJogador > 0:
                                print("Você conseguiu fugir com sucesso!\n")
                                combate = "Encerrar"
                                break

                            elif velocidadeNavioJogador >= velocidadeNavioInimigo:
                                print("O navio inimigo consegue te acompanhar e o combate continua!\n")

                            elif velocidadeNavioJogador < velocidadeNavioInimigo:
                                print("Você tenta fugir, mas o inimigo é mais rápido!\n")

                        else:
                            os.system('cls')

                        if quebrar == 1:
                            break

                        # --- Decisões do inimigo --- #

                        # Estratégias:

                        if tripulacao_inimigo > 1 and nova_rodada > 0:
                            # Atacar casco
                            if recarga_canhoes_casco_inimigo == 3 and distanciaEntreNavios < 300:
                                casco_jogador, canhoes_casco_jogador, recarga_canhoes_casco_inimigo, tripulacao_jogador, quebrar = AtacarCasco("inimigo", casco_jogador, recarga_canhoes_casco_inimigo, canhoes_casco_inimigo, canhoes_casco_jogador, tripulacao_inimigo, tripulacao_jogador)
                            # Atacar velas
                            elif recarga_canhoes_vela_inimigo == 4 and distanciaEntreNavios < 250 and vela_jogador > 0:
                                vela_jogador, recarga_canhoes_vela_inimigo = AtacarVelas("inimigo", recarga_canhoes_vela_inimigo, vela_jogador, canhoes_vela_inimigo, tripulacao_inimigo)
                            # Atacar tripulação
                            elif distanciaEntreNavios < 150:
                                tripulacao_jogador, conves_jogador, quebrar = AtacarTripulacao("inimigo", tripulacao_jogador, mosquetes_inimigo, conves_inimigo, conves_jogador)

                            if quebrar == 1:
                                break
                        
                        if combate != "Encerrar":
                            MostrarRodadaDistancia()

                        if recarga_canhoes_casco_jogador == 3 and combate != "Encerrar":
                            print("Canhões principais prontos para atirar!\n")
                        if recarga_canhoes_vela_jogador == 4 and combate != "Encerrar":
                            print("Canhões de ataque de velas carregados!\n")
                    break

                elif navegacao == "2":
                    os.system('cls')
                    MostrarStatusInimigo()
                    
                    escolhaNavegacao = input("\nDeseja atacar? (1. Sim / 2. Não)")
                    if escolhaNavegacao == "1":
                        navegacao = "1"
                    elif escolhaNavegacao == "2":
                        os.system('cls')
                        break

                elif navegacao == "3":
                    os.system('cls')
                    pass

        elif evento <= 7: # Encontrar pilhagem
            os.system('cls')
            print("Você encontrou uma pilhagem flutuando na água!\n")

        elif evento == 8: # Encontrar cidade
            os.system('cls')

            if len(cidades_existentes) > 0:
                cidadeEncontrada = random.choice(cidades_existentes)
                print("Você encontrou a cidade: " + cidadeEncontrada + "!\n")
                
                cidades_existentes.remove(cidadeEncontrada)
                cidades_conhecidas.append(cidadeEncontrada)
            else:
                print("Você passou por " + random.choice(cidades_conhecidas) + "!\n")

        else:
            os.system('cls')
            print("Você viajou tranquilo\n")

    elif escolha == "2": # Tem que juntar os códigos (CódigoPrincipal.py, SistemaDeFrota.py e SistemaDeBatalha.py)
        os.system('cls')
        print("Sem código\n")

    else:
        os.system('cls')
        pass