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

dados_navio = {
    'Canhoneira': {'saude_max_casco': 450, 'saude_max_vela': 200, 'canhoes_por_lado': 2, 'carga_max': 1200},
    'Escuna': {'saude_max_casco': 900, 'saude_max_vela': 350, 'canhoes_por_lado': 6, 'carga_max': 2300},
    'Brigue': {'saude_max_casco': 1700, 'saude_max_vela': 950, 'canhoes_por_lado': 11, 'carga_max': 3700},
    'Fragata': {'saude_max_casco': 3800, 'saude_max_vela': 2100, 'canhoes_por_lado': 24, 'carga_max': 4600},
    'Galeão': {'saude_max_casco': 5600, 'saude_max_vela': 5000, 'canhoes_por_lado': 32, 'carga_max': 6200}
}

class Navio():
    def __init__(self, tipo, saude_casco_atual, saude_velas_atual):
        self.tipo = tipo
        self.saude_casco_atual = int(saude_casco_atual)
        self.saude_velas_atual = int(saude_velas_atual)
        dados = dados_navio[tipo]
        self.saude_max_casco = dados['saude_max_casco']
        self.saude_max_vela = dados['saude_max_vela']
        self.canhoes_por_lado = dados['canhoes_por_lado']
        self.carga_max = dados['carga_max']
        self.carga = {"Madeira": 0, "Aço": 0, "Pano": 0, "Rum": 0, "Ouro": 0}

    def adicionar_item_carga(self, item, quantidade):
        peso_item = {"Madeira": 2, "Aço": 4, "Pano": 1, "Rum": 3, "Ouro": 0}.get(item, 0)
        peso_total = peso_item * quantidade
        carga_total = self.exibir_carga() + peso_total  # Calcula a carga total atual
        if carga_total <= self.carga_max:  # Verifica se a carga total não excede a capacidade máxima
            self.carga[item] += quantidade
            return True
        else:
            return False

    def exibir_carga(self):
        carga_total = sum(peso * {"Madeira": 2, "Aço": 4, "Pano": 1, "Rum": 3, "Ouro": 0}.get(item, 0) for item, peso in self.carga.items())
        return carga_total

    def exibir_info_navio(self):
        carga_total = self.exibir_carga()
        return f"Tipo: {self.tipo}, Saúde do Casco: {self.saude_casco_atual} / {self.saude_max_casco}, " \
               f"Saúde das Velas: {self.saude_velas_atual} / {self.saude_max_vela}, " \
               f"Carga {carga_total} / {self.carga_max}: {self.carga}"

class Frota:
    def __init__(self):
        self.navios = []
        self.qnt_itens = {"Madeira": 0, "Aço": 0, "Pano": 0, "Rum": 0, "Ouro": 0}
        self.carga_total_frota = 0
        self.carga_max_frota = 0

    def adicionar_navio(self, navio):
        self.navios.append(navio)
        self.carga_max_frota += navio.carga_max

    def remover_navio(self, navio):
        self.navios.remove(navio)
    
    def adicionar_item_carga(self, item, quantidade, indice_navio):
        navio = self.navios[indice_navio]

        if not navio.adicionar_item_carga(item, quantidade):
            return False
        
        self.qnt_itens[item] += quantidade
        peso_item = {"Madeira": 2, "Aço": 4, "Pano": 1, "Rum": 3, "Ouro": 0}.get(item, 0)
        peso_total = peso_item * quantidade
        self.carga_total_frota += peso_total

        return True
    
    def retirar_item_frota(self, item, quantidade):
        if self.qnt_itens[item] < quantidade:
            return False

        self.qnt_itens[item] -= quantidade
        peso_item = {"Madeira": 2, "Aço": 4, "Pano": 1, "Rum": 3, "Ouro": 0}.get(item, 0)
        peso_total = peso_item * quantidade
        self.carga_total_frota -= peso_total
        
        for navio in self.navios:
            if navio.carga[item] >= quantidade:
                navio.carga[item] -= quantidade
                break

            quantidade -= navio.carga[item]
            navio.carga[item] = 0

        return True

    def exibir_frota(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, navio in enumerate(self.navios, start=1):
            print(f"Navio {i}: {navio.exibir_info_navio()}")

        print(f"\nCarga de Todos os Navios: {self.carga_total_frota} / {self.carga_max_frota}")
        print(*[f"{k}: {v}" for k, v in self.qnt_itens.items()], sep=", ")

        # Nao sei juntar a porcaria dos dois prints: print(f"\nCarga geral: {self.carga_total_frota} / {self.carga_max_frota}"+ " | Itens gerais: ", *[f"{k}: {v}" for k, v in self.qnt_itens.items()], sep=", ")

def adicionar_navio(escolha = None):
    if escolha is None:
        print("Escolha o tipo de navio:")
        for i, tipo_navio in enumerate(dados_navio.keys(), start=1):
            print(f"{i}. {tipo_navio}")
        escolha = int(input("Digite o número correspondente ao tipo de navio: "))

        saude_casco_atual = float(input(f"Informe a saúde do casco atual (0 - {dados_navio[tipo_navio]['saude_max_casco']}): "))
        saude_velas_atual = float(input(f"Informe a saúde das velas atual (0 - {dados_navio[tipo_navio]['saude_max_vela']}): "))
    tipo_navio = list(dados_navio.keys())[escolha]

    navio = Navio(tipo_navio, dados_navio[tipo_navio]['saude_max_casco'], dados_navio[tipo_navio]['saude_max_vela'])
    frota.adicionar_navio(navio)
    print("Navio adicionado à frota com sucesso!")

def adicionar_item_carga():
    print("Escolha o navio:")
    for i, navio in enumerate(frota.navios, start=1):
        print(f"{i}. {navio.tipo}")

    escolha_navio = int(input("Digite o número correspondente ao navio: ")) - 1

    print("Escolha o tipo de item:")
    for i, tipo_item in enumerate(["Madeira", "Aço", "Pano", "Rum", "Ouro"], start=1):
        print(f"{i}. {tipo_item}")

    escolha_item = int(input("Digite o número correspondente ao tipo de item: ")) - 1
    tipo_item = ["Madeira", "Aço", "Pano", "Rum", "Ouro"][escolha_item]

    quantidade = int(input("Informe a quantidade do item: "))

    if frota.adicionar_item_carga(tipo_item, quantidade, escolha_navio):
        print("Item adicionado à carga com sucesso!")
    else:
        print("Não foi possível adicionar o item à carga. Carga máxima excedida.")

def retirar_item_frota(escolha_item = None, quantidade = None):
    if escolha_item is None:
        print("Escolha o tipo de item:")
        for i, tipo_item in enumerate(["Madeira", "Aço", "Pano", "Rum", "Ouro"], start=1):
            print(f"{i}. {tipo_item}")

        escolha_item = int(input("Digite o número correspondente ao tipo de item: ")) - 1

    tipo_item = ["Madeira", "Aço", "Pano", "Rum", "Ouro"][escolha_item]

    return frota.retirar_item_frota(tipo_item, quantidade)

frota = Frota()

frota.adicionar_navio(Navio('Canhoneira', dados_navio['Canhoneira']['saude_max_casco'], dados_navio['Canhoneira']['saude_max_vela']))

while True:
    escolhaPrincipal = input("\nOpções:\n"
        "1. Navegar pelos mares\n"
        "2. Procurar por um tesouro\n"
        "3. Mostrar estado atual\n"
        "4. Atracar em uma ilha\n"
        "5. Realizar reparos de emergência\n"
        "6. Gerenciar a frota\n"
        "\nO que você gostaria de fazer?\n")

    if escolhaPrincipal == "1":
        pass

    elif escolhaPrincipal == "2":
        pass

    elif escolhaPrincipal == "3":
        frota.exibir_frota()

    elif escolhaPrincipal == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        opcaoAtracadoIlha = input("Atracando em uma ilha...\n"
            "\nOpções:\n"
            "1. Realizar reparos no navio por ouro\n"
            "2. Comprar materiais\n"
            "3. Vender materiais\n"
            "4. Comprar um novo navio\n"
            "5. Voltar para o alto-mar\n"
            "\nO que você gostaria de fazer?\n")
        
        if opcaoAtracadoIlha == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opções de navios disponíveis para compra:\n"
                "1. Escuna - 700 ouro\n"
                "2. Brigue - 1500 ouro\n"
                "3. Fragata - 2400 ouro\n"
                "4. Galeão - 3600 ouro\n")
            compra_navio = input("Qual navio você gostaria de comprar? ")

            if compra_navio == '1':
                if retirar_item_frota(4, 700):
                    adicionar_navio(1)
                else:
                    print("Sem dinheiro suficiente para compra!")
            elif compra_navio == '2':
                adicionar_navio(2)
            elif compra_navio == '3':
                adicionar_navio(3)
            elif compra_navio == '4':
                adicionar_navio(4)
            else:
                print("Opção inválida!")

    elif escolhaPrincipal == "5":
        pass

    elif escolhaPrincipal == "6":
        pass