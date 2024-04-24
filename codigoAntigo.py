import random
import os # os.system('cls' if os.name == 'nt' else 'clear')

nomes_navios_piratas = [
    "Vingança da Rainha Anne","Pérola Negra","Vingador","Fantasma","Vingança do Diabo","Dama do Mar","Tesouro Escondido","Trovão",
    "Tempestade","Lobo do Mar","Albatroz Negro","Leviatã","Maré Negra","Caveira","Maldição do Mar","Fúria dos Mares","Dragão do Mar",
    "Espectro","Morsa do Mar","Perdição","Nêmesis","Bruxa dos Mares","Gralha","Falcão do Mar","Cruel Maré","Serpente dos Mares",
    "Luar Negro","Corsário","Banshee","Navio Fantasma","Sombra do Mar","Naufrágio","Terrível Maré","Açougueiro dos Mares","Ameaça do Oceano"]

cidades_existentes = [
    "Port Royal","Nassau","Tortuga","Kingston","New Providence","Barbados","St. Augustine","Charles Town","Belize City","Havana","Campeche",
    "Maracaibo","Porto Príncipe","Panama City","Bridgetown","Veracruz","Porto Bello","Cartagena","Portobelo","La Tortuga","Santo Domingo",
    "St. Kitts","St. Thomas","Saint-Malo","Galveston"]

class Pirata:
    def __init__(self, nome):
        self.nome = nome
        self.saude = 100
        self.frotaNaviosJogador = ["Canhoneira - Navio inicial"]

    def mostrar_inventario(self):
        print(f"Inventário de {self.nome} está vazio.")

    def gerenciar_frota(self):
        print("Gerenciando a frota:")
        print("Navios disponíveis:")
        for i, navio in enumerate(self.frotaNaviosJogador, 1):
            print(f"{i}. {navio}")
        escolha = input("Escolha o número do navio que deseja tornar principal (ou digite 'sair' para voltar): ")
        if escolha.lower() == 'sair':
            return
        elif escolha.isdigit() and 1 <= int(escolha) <= len(self.frotaNaviosJogador):
            escolha_index = int(escolha) - 1
            navio_escolhido = self.frotaNaviosJogador.pop(escolha_index)
            self.frotaNaviosJogador.insert(0, navio_escolhido)
            print(f"{navio_escolhido} foi definido como o navio principal.")
        else:
            print("Opção inválida! Por favor, escolha um número válido da lista.")

class Navio:
    dados_navio = {
        'Canhoneira': {'saude_casco': 450, 'saude_vela': 200, 'canhoes_por_lado': 2},
        'Escuna': {'saude_casco': 900, 'saude_vela': 350, 'canhoes_por_lado': 6},
        'Brigue': {'saude_casco': 1700, 'saude_vela': 950, 'canhoes_por_lado': 11},
        'Fragata': {'saude_casco': 3800, 'saude_vela': 2100, 'canhoes_por_lado': 24},
        'Galeão': {'saude_casco': 5600, 'saude_vela': 5000, 'canhoes_por_lado': 32}
    }

    def __init__(self, nome, tipo_navio):
        self.nome = nome
        self.tipo_navio = tipo_navio
        dados = self.dados_navio.get(tipo_navio)
        if dados:
            self.saude_casco_max = dados['saude_casco']  # Saúde máxima do casco
            self.saude_casco_atual = self.saude_casco_max  # Saúde atual do casco
            self.saude_vela_max = dados['saude_vela']  # Saúde máxima da vela
            self.saude_vela_atual = self.saude_vela_max  # Saúde atual da vela
            self.canhoes_por_lado = dados['canhoes_por_lado']
        else:
            raise ValueError("Tipo de navio inválido.")
        self.carga = {'Madeira': 0, 'Ferro': 0, 'Pano': 0, 'Rum': 0, 'Espada': 0, 'Trabuco': 0, 'Ouro': 0, 'Mapa do Tesouro': 0}

    def mostrar_carga(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Estado atual do {self.nome}:")
        print(f"Vida do Casco: {self.saude_casco_atual}/{self.saude_casco_max}")  # Mostrar vida atual e máxima do casco
        print(f"Vida da Vela: {self.saude_vela_atual}/{self.saude_vela_max}")  # Mostrar vida atual e máxima da vela
        print("Carga:")
        for item, quantidade in self.carga.items():
            print(f"{item}: {quantidade}")

def encontro_inimigo(navio):
    tipos_navio_inimigo = ['Galeão', 'Fragata', 'Brigue', 'Escuna', 'Canhoneira']
    tipo_navio_inimigo = random.choice(tipos_navio_inimigo)
    navio_inimigo = Navio("Navio Inimigo", tipo_navio_inimigo)
    return navio_inimigo

def encontro_pilhagem_mar():
    pilhagem = {'Ouro': random.randint(50, 100), 'Mapa do Tesouro': 1}
    print("\nVocê encontrou uma pilhagem flutuante contendo:")
    for item, quantidade in pilhagem.items():
        print(f"{quantidade}x {item}")
    return pilhagem

def pilhagem_navioinimigo_derrotado(tipo_navio_inimigo):
    multiplicador_pilhagem = {'Canhoneira': 1, 'Escuna': 2, 'Brigue': 3, 'Fragata': 4, 'Galeão': 5}
    multiplicador = multiplicador_pilhagem[tipo_navio_inimigo]
    
    pilhagem = {'Ouro': random.randint(100 * multiplicador, 120 * multiplicador), 
                'Madeira': random.randint(15 * multiplicador, 30 * multiplicador), 
                'Ferro': random.randint(10 * multiplicador, 20 * multiplicador), 
                'Pano': random.randint(25 * multiplicador, 40 * multiplicador), 
                'Rum': random.randint(5 * multiplicador, 10 * multiplicador), 
                'Espada': random.randint(3 * multiplicador, 5 * multiplicador), 
                'Trabuco': random.randint(2 * multiplicador, 4 * multiplicador)}
    print("\nVocê conquistou uma pilhagem do navio inimigo derrotado, contendo:")
    for item, quantidade in pilhagem.items():
        print(f"{quantidade}x {item}")
    return pilhagem

def batalha(pirata, navio_inimigo):
    navio_jogador_nome = pirata.frotaNaviosJogador[0]
    navio_jogador_tipo = navio_jogador_nome.split(" - ")[0]
    navio_jogador = Navio(navio_jogador_nome, navio_jogador_tipo)
    print("Batalha iniciada!\n")
    while True:
        # Turno do jogador
        print(f"Saúde do {navio_jogador.nome}: {navio_jogador.saude_casco_atual}/{navio_jogador.saude_casco_max}")
        print(f"Saúde do {navio_inimigo.nome}: {navio_inimigo.saude_casco_atual}/{navio_inimigo.saude_casco_max}")
        print("\n1. Atacar")
        print("2. Fugir")
        escolha = input("O que você deseja fazer? ")

        if escolha == '1':
            dano = navio_jogador.canhoes_por_lado * random.randint(30, 50)
            navio_inimigo.saude_casco_atual -= dano
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Você causou {dano} de dano ao {navio_inimigo.nome}!")
            if navio_inimigo.saude_casco_atual <= 0:
                print("Você venceu a batalha!")
                pilhagem = pilhagem_navioinimigo_derrotado(navio_inimigo.tipo_navio)
                for item, quantidade in pilhagem.items():
                    if item in navio_jogador.carga:
                        navio_jogador.carga[item] += quantidade
                    else:
                        print(f"{quantidade}x {item} não pôde ser adicionado à carga do navio jogador!")
                break
        elif escolha == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Você fugiu da batalha!")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Escolha inválida!")
        
        # Turno do inimigo
        dano_inimigo = navio_inimigo.canhoes_por_lado * random.randint(30, 50)
        navio_jogador.saude_casco_atual -= dano_inimigo
        print(f"O {navio_inimigo.nome} causou {dano_inimigo} de dano ao seu navio!\n")

        if navio_jogador.saude_casco_atual <= 0:
            print("Você perdeu a batalha!")
            break

def main():
    nome = input("Bem-vindo ao Jogo de Piratas! Qual é o nome do seu pirata? ")
    pirata = Pirata(nome)
    navio = Navio(pirata.frotaNaviosJogador[0], "Canhoneira")

    while True:
        print("\nOpções:\n"
            "1. Navegar pelos mares\n"
            "2. Procurar por um tesouro\n"
            "3. Mostrar estado atual\n"
            "4. Atracar em uma ilha\n"
            "5. Realizar reparos de emergência\n"
            "6. Gerenciar a frota\n")
        escolhaPainelPrincipal = input("O que você gostaria de fazer? ")

        if escolhaPainelPrincipal == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Navegando pelos mares...")
            evento = random.randint(1, 3)
            if evento == 1:
                navio_inimigo = encontro_inimigo(navio)
                print(f"\nVocê encontrou um navio inimigo {navio_inimigo.tipo_navio}!")
                batalha(pirata, navio_inimigo)
                # Após a batalha, atualizar a saúde do casco e das velas do navio jogador
                navio.saude_casco_atual = navio.saude_casco_max
                navio.saude_vela_atual = navio.saude_vela_max
            elif evento == 2:
                pilhagem = encontro_pilhagem_mar()
                for item, quantidade in pilhagem.items():
                    if item in navio.carga:
                        navio.carga[item] += quantidade
                    else:
                        print(f"{quantidade}x {item} não pôde ser adicionado à carga do navio!")
            else:
                print("\nVocê navegou pacificamente.")

        elif escolhaPainelPrincipal == '2':
            if navio.carga['Mapa do Tesouro'] > 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Você está seguindo o mapa do tesouro...")
                print("Você encontrou o tesouro enterrado!")
                print("Dentro do baú do tesouro, você encontrou:")
                print("500 peças de ouro")
                navio.carga['Ouro'] += 500
                navio.carga['Mapa do Tesouro'] -= 1
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Seu navio não tem um mapa do tesouro!")

        elif escolhaPainelPrincipal == '3':
            navio.mostrar_carga()
            pirata.mostrar_inventario()

        elif escolhaPainelPrincipal == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Atracando em uma ilha...\n"
                    "\nOpções:\n"
                    "1. Realizar reparos no navio por ouro\n"
                    "2. Comprar materiais\n"
                    "3. Vender materiais\n"
                    "4. Comprar um novo navio\n"
                    "5. Voltar para o alto-mar\n")

            opcaoAtracadoIlha = input("O que você gostaria de fazer? ")

            if opcaoAtracadoIlha == '1':
                ouro_necessario = (navio.definir_saude_casco() - navio.saude_casco) // 50
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Reparos custarão {ouro_necessario} de ouro.")
                if navio.carga['Ouro'] >= ouro_necessario:
                    navio.saude_casco += ouro_necessario * 50
                    navio.carga['Ouro'] -= ouro_necessario
                    print("Reparos concluídos!")
                else:
                    print("Você não tem ouro suficiente para realizar os reparos.")

            elif opcaoAtracadoIlha == '2':
                print("Materiais disponíveis para compra:")
                print("1. Pano - 45x ouro")
                print("2. Metal - 22x ouro")
                print("3. Madeira - 8x ouro")
                print("4. Rum - 75x ouro")
                compra = input("O que você gostaria de comprar? ")

                if compra == '1':
                    quantidade = int(input("Quantidade de pano que você gostaria de comprar: "))
                    preco_total = quantidade * 45
                    if navio.carga['Ouro'] >= preco_total:
                        navio.carga['Pano'] += quantidade
                        navio.carga['Ouro'] -= preco_total
                        print(f"Você comprou {quantidade}x pano.")
                    else:
                        print("Você não tem ouro suficiente para comprar este material.")
                elif compra == '2':
                    quantidade = int(input("Quantidade de metal que você gostaria de comprar: "))
                    preco_total = quantidade * 22
                    if navio.carga['Ouro'] >= preco_total:
                        navio.carga['Metal'] += quantidade
                        navio.carga['Ouro'] -= preco_total
                        print(f"Você comprou {quantidade}x metal.")
                    else:
                        print("Você não tem ouro suficiente para comprar este material.")
                elif compra == '3':
                    quantidade = int(input("Quantidade de madeira que você gostaria de comprar: "))
                    preco_total = quantidade * 8
                    if navio.carga['Ouro'] >= preco_total:
                        navio.carga['Madeira'] += quantidade
                        navio.carga['Ouro'] -= preco_total
                        print(f"Você comprou {quantidade}x madeira.")
                    else:
                        print("Você não tem ouro suficiente para comprar este material.")
                elif compra == '4':
                    quantidade = int(input("Quantidade de rum que você gostaria de comprar: "))
                    preco_total = quantidade * 75
                    if navio.carga['Ouro'] >= preco_total:
                        navio.carga['Rum'] += quantidade
                        navio.carga['Ouro'] -= preco_total
                        print(f"Você comprou {quantidade}x rum.")
                    else:
                        print("Você não tem ouro suficiente para comprar este material.")
                else:
                    print("Opção inválida!")

            elif opcaoAtracadoIlha == '3':
                print("Materiais disponíveis para venda:")
                print("1. Pano - 30x ouro")
                print("2. Metal - 15x ouro")
                print("3. Madeira - 5x ouro")
                print("4. Rum - 50x ouro")
                venda = input("O que você gostaria de vender? ")

                if venda == '1':
                    quantidade = int(input("Quantidade de pano que você gostaria de vender: "))
                    if navio.carga['Pano'] >= quantidade:
                        navio.carga['Pano'] -= quantidade
                        navio.carga['Ouro'] += quantidade * 30
                        print(f"Você vendeu {quantidade}x pano.")
                    else:
                        print("Você não tem quantidade suficiente de pano para vender.")
                elif venda == '2':
                    quantidade = int(input("Quantidade de metal que você gostaria de vender: "))
                    if navio.carga['Metal'] >= quantidade:
                        navio.carga['Metal'] -= quantidade
                        navio.carga['Ouro'] += quantidade * 15
                        print(f"Você vendeu {quantidade}x metal.")
                    else:
                        print("Você não tem quantidade suficiente de metal para vender.")
                elif venda == '3':
                    quantidade = int(input("Quantidade de madeira que você gostaria de vender: "))
                    if navio.carga['Madeira'] >= quantidade:
                        navio.carga['Madeira'] -= quantidade
                        navio.carga['Ouro'] += quantidade * 5
                        print(f"Você vendeu {quantidade}x madeira.")
                    else:
                        print("Você não tem quantidade suficiente de madeira para vender.")
                elif venda == '4':
                    quantidade = int(input("Quantidade de rum que você gostaria de vender: "))
                    if navio.carga['Rum'] >= quantidade:
                        navio.carga['Rum'] -= quantidade
                        navio.carga['Ouro'] += quantidade * 50
                        print(f"Você vendeu {quantidade}x rum.")
                    else:
                        print("Você não tem quantidade suficiente de rum para vender.")
                else:
                    print("Opção inválida!")

            elif opcaoAtracadoIlha == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Opções de navios disponíveis para compra:\n"
                    "1. Escuna - 700 ouro\n"
                    "2. Brigue - 1500 ouro\n"
                    "3. Fragata - 2400 ouro\n"
                    "4. Galeão - 3600 ouro\n")
                compra_navio = input("Qual navio você gostaria de comprar? ")

                if compra_navio == '1':
                    if navio.carga['Ouro'] >= 700:
                        navio.carga['Ouro'] -= 700
                        novo_navio = "Escuna - " + random.choice(nomes_navios_piratas)
                        pirata.frotaNaviosJogador.append(novo_navio)
                        print("Você comprou uma Escuna!")
                    else:
                        print("Você não tem ouro suficiente para comprar uma Escuna.")
                elif compra_navio == '2':
                    if navio.carga['Ouro'] >= 1500:
                        navio.carga['Ouro'] -= 1500
                        novo_navio = "Brigue - " + random.choice(nomes_navios_piratas)
                        pirata.frotaNaviosJogador.append(novo_navio)
                        print("Você comprou um Brigue!")
                    else:
                        print("Você não tem ouro suficiente para comprar um Brigue.")
                elif compra_navio == '3':
                    if navio.carga['Ouro'] >= 2400:
                        navio.carga['Ouro'] -= 2400
                        novo_navio = "Fragata - " + random.choice(nomes_navios_piratas)
                        pirata.frotaNaviosJogador.append(novo_navio)
                        print("Você comprou uma Fragata!")
                    else:
                        print("Você não tem ouro suficiente para comprar uma Fragata.")
                elif compra_navio == '4':
                    if navio.carga['Ouro'] >= 3600:
                        navio.carga['Ouro'] -= 3600
                        novo_navio = "Galeão - " + random.choice(nomes_navios_piratas)
                        pirata.frotaNaviosJogador.append(novo_navio)
                        print("Você comprou um Galeão!")
                    else:
                        print("Você não tem ouro suficiente para comprar um Galeão.")
                else:
                    print("Opção inválida!")

            elif opcaoAtracadoIlha == '5':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Voltando ao mar aberto...\n")
            else:
                print("Opção inválida!")

        elif escolhaPainelPrincipal == '5':
            print("Realizando reparos de emergência...")
            # Código para reparos de emergência vai aqui
            print("Reparos de emergência concluídos!")

        elif escolhaPainelPrincipal == '6':
            pirata.gerenciar_frota()

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Escolha inválida!")

if __name__ == "__main__":
    main()