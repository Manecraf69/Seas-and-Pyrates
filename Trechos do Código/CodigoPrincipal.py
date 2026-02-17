import os
import random
import json

ITENS = ["Madeira", "Aco", "Pano", "Rum", "Ouro"]
PESO_ITENS = {"Madeira": 2, "Aco": 4, "Pano": 1, "Rum": 3, "Ouro": 0}
PRECO_MATERIAIS = {"Madeira": 4, "Aco": 10, "Pano": 6, "Rum": 8}
PRECO_NAVIOS = {"Escuna": 700, "Brigue": 1500, "Fragata": 2400, "Galeao": 3600}
PRECO_TRIPULANTE = 12
TRIPULACAO_BASE = {"Canhoneira": 18, "Escuna": 35, "Brigue": 60, "Fragata": 120, "Galeao": 180}
SAVE_FILE = "savegame.json"
ITENS_SAQUE = ["Madeira", "Aco", "Pano", "Rum"]

cidades_existentes = [
    "Port Royal", "Nassau", "Tortuga", "Kingston", "New Providence", "Barbados", "St. Augustine",
    "Charles Town", "Belize City", "Havana", "Campeche", "Maracaibo", "Porto Principe", "Panama City",
    "Bridgetown", "Veracruz", "Porto Bello", "Cartagena", "Portobelo", "La Tortuga", "Santo Domingo",
    "St. Kitts", "St. Thomas", "Saint-Malo", "Galveston"
]
cidades_conhecidas = []

dados_navio = {
    "Canhoneira": {"saude_max_casco": 450, "saude_max_vela": 200, "canhoes_por_lado": 2, "carga_max": 1200},
    "Escuna": {"saude_max_casco": 900, "saude_max_vela": 350, "canhoes_por_lado": 6, "carga_max": 2300},
    "Brigue": {"saude_max_casco": 1700, "saude_max_vela": 950, "canhoes_por_lado": 11, "carga_max": 3700},
    "Fragata": {"saude_max_casco": 3800, "saude_max_vela": 2100, "canhoes_por_lado": 24, "carga_max": 4600},
    "Galeao": {"saude_max_casco": 5600, "saude_max_vela": 5000, "canhoes_por_lado": 32, "carga_max": 6200},
}


class Navio:
    def __init__(self, tipo, saude_casco_atual, saude_velas_atual, tripulacao_atual=None):
        self.tipo = tipo
        self.saude_casco_atual = int(saude_casco_atual)
        self.saude_velas_atual = int(saude_velas_atual)
        dados = dados_navio[tipo]
        self.saude_max_casco = dados["saude_max_casco"]
        self.saude_max_vela = dados["saude_max_vela"]
        self.canhoes_por_lado = dados["canhoes_por_lado"]
        self.carga_max = dados["carga_max"]
        self.tripulacao_max = TRIPULACAO_BASE.get(tipo, 30)
        if tripulacao_atual is None:
            self.tripulacao_atual = self.tripulacao_max
        else:
            self.tripulacao_atual = max(0, min(int(tripulacao_atual), self.tripulacao_max))
        self.carga = {item: 0 for item in ITENS}

    def exibir_carga(self):
        return sum(qtd * PESO_ITENS[item] for item, qtd in self.carga.items())

    def adicionar_item_carga(self, item, quantidade):
        if item not in self.carga or quantidade <= 0:
            return False

        peso_total = PESO_ITENS[item] * quantidade
        if self.exibir_carga() + peso_total > self.carga_max:
            return False

        self.carga[item] += quantidade
        return True

    def exibir_info_navio(self):
        carga_total = self.exibir_carga()
        return (
            f"Tipo: {self.tipo}, Casco: {self.saude_casco_atual}/{self.saude_max_casco}, "
            f"Velas: {self.saude_velas_atual}/{self.saude_max_vela}, "
            f"Tripulacao: {self.tripulacao_atual}/{self.tripulacao_max}, "
            f"Carga {carga_total}/{self.carga_max}: {self.carga}"
        )


class Frota:
    def __init__(self):
        self.navios = []
        self.qnt_itens = {item: 0 for item in ITENS}
        self.carga_total_frota = 0
        self.carga_max_frota = 0

    def adicionar_navio(self, navio):
        self.navios.append(navio)
        self.carga_max_frota += navio.carga_max

    def remover_navio(self, indice_navio):
        if indice_navio < 0 or indice_navio >= len(self.navios):
            return None
        if len(self.navios) <= 1:
            return None

        navio = self.navios.pop(indice_navio)
        self.carga_max_frota -= navio.carga_max

        for item, qtd in navio.carga.items():
            qtd_int = int(qtd)
            self.qnt_itens[item] = max(0, self.qnt_itens[item] - qtd_int)
            self.carga_total_frota = max(0, self.carga_total_frota - (qtd_int * PESO_ITENS[item]))

        return navio

    def mover_navio(self, origem, destino):
        if origem < 0 or origem >= len(self.navios):
            return False
        if destino < 0 or destino >= len(self.navios):
            return False
        if origem == destino:
            return True

        navio = self.navios.pop(origem)
        self.navios.insert(destino, navio)
        return True

    def adicionar_item_carga(self, item, quantidade, indice_navio):
        if indice_navio < 0 or indice_navio >= len(self.navios):
            return False
        if quantidade <= 0:
            return False

        navio = self.navios[indice_navio]
        if not navio.adicionar_item_carga(item, quantidade):
            return False

        self.qnt_itens[item] += quantidade
        self.carga_total_frota += PESO_ITENS[item] * quantidade
        return True

    def retirar_item_frota(self, item, quantidade):
        if item not in self.qnt_itens or quantidade <= 0:
            return False
        if self.qnt_itens[item] < quantidade:
            return False

        self.qnt_itens[item] -= quantidade
        self.carga_total_frota -= PESO_ITENS[item] * quantidade

        restante = quantidade
        for navio in self.navios:
            if navio.carga[item] >= restante:
                navio.carga[item] -= restante
                break
            restante -= navio.carga[item]
            navio.carga[item] = 0

        return True

    def exibir_frota(self):
        if not self.navios:
            print("Frota vazia.")
            return

        for i, navio in enumerate(self.navios, start=1):
            tripulacao = navio.tripulacao_atual
            conves = max(1, int(tripulacao * 0.4)) if tripulacao > 0 else 0
            canhoes_casco = navio.canhoes_por_lado * 2
            canhoes_vela = max(1, navio.canhoes_por_lado // 2)
            velocidade = (navio.saude_velas_atual / max(1, navio.saude_max_vela)) * 12
            print(
                f"--- Navio Jogador {i} ---"
                f"\nTipo de navio: {navio.tipo}"
                f"\nVida do casco: {navio.saude_casco_atual}"
                f"\nVida das velas: {navio.saude_velas_atual}"
                f"\nCanhoes primarios: {canhoes_casco}"
                f"\nCanhoes secundarios: {canhoes_vela}"
                f"\nTripulacao total: {tripulacao} ( No conves: {conves} )"
                f"\nVelocidade maxima (nos): {velocidade:.2f}"
                f"\nItens no navio: {navio.carga}\n"
            )

        print(f"Carga total: {self.carga_total_frota}/{self.carga_max_frota}")
        print(*[f"{k}: {v}" for k, v in self.qnt_itens.items()], sep=", ")


def serializar_frota(frota):
    return {
        "navios": [
            {
                "tipo": navio.tipo,
                "saude_casco_atual": navio.saude_casco_atual,
                "saude_velas_atual": navio.saude_velas_atual,
                "tripulacao_atual": navio.tripulacao_atual,
                "carga": navio.carga,
            }
            for navio in frota.navios
        ],
        "qnt_itens": frota.qnt_itens,
        "carga_total_frota": frota.carga_total_frota,
        "carga_max_frota": frota.carga_max_frota,
    }


def desserializar_frota(dados):
    frota = Frota()
    for dados_nav in dados.get("navios", []):
        tipo = dados_nav.get("tipo")
        if tipo not in dados_navio:
            continue
        navio = Navio(
            tipo,
            dados_nav.get("saude_casco_atual", dados_navio[tipo]["saude_max_casco"]),
            dados_nav.get("saude_velas_atual", dados_navio[tipo]["saude_max_vela"]),
            dados_nav.get("tripulacao_atual"),
        )
        carga = dados_nav.get("carga", {})
        for item in ITENS:
            navio.carga[item] = int(carga.get(item, 0))
        frota.adicionar_navio(navio)

    if not frota.navios:
        frota.adicionar_navio(Navio("Canhoneira", dados_navio["Canhoneira"]["saude_max_casco"], dados_navio["Canhoneira"]["saude_max_vela"]))
        frota.adicionar_item_carga("Ouro", 1500, 0)
        return frota

    frota.qnt_itens = {item: 0 for item in ITENS}
    frota.carga_total_frota = 0
    for navio in frota.navios:
        for item, qtd in navio.carga.items():
            frota.qnt_itens[item] += int(qtd)
            frota.carga_total_frota += int(qtd) * PESO_ITENS[item]
    return frota


def salvar_jogo(frota):
    dados = {
        "frota": serializar_frota(frota),
        "cidades_existentes": cidades_existentes,
        "cidades_conhecidas": cidades_conhecidas,
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    print(f"Jogo salvo em {SAVE_FILE}.")


def carregar_jogo():
    if not os.path.exists(SAVE_FILE):
        frota = Frota()
        frota.adicionar_navio(Navio("Canhoneira", dados_navio["Canhoneira"]["saude_max_casco"], dados_navio["Canhoneira"]["saude_max_vela"]))
        frota.adicionar_item_carga("Ouro", 1500, 0)
        return frota

    with open(SAVE_FILE, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    global cidades_existentes, cidades_conhecidas
    cidades_existentes = dados.get("cidades_existentes", cidades_existentes)
    cidades_conhecidas = dados.get("cidades_conhecidas", cidades_conhecidas)
    frota = desserializar_frota(dados.get("frota", {}))
    print(f"Save carregado de {SAVE_FILE}.")
    return frota


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def ler_int(pergunta, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(pergunta).strip())
            if minimo is not None and valor < minimo:
                print("Valor abaixo do minimo.")
                continue
            if maximo is not None and valor > maximo:
                print("Valor acima do maximo.")
                continue
            return valor
        except ValueError:
            print("Digite um numero valido.")


def escolher_navio(frota, permitir_cancelar=False):
    if not frota.navios:
        return None

    if permitir_cancelar:
        print("0. Voltar")
    for i, navio in enumerate(frota.navios, start=1):
        print(f"{i}. {navio.tipo} ({navio.saude_casco_atual}/{navio.saude_max_casco} casco)")

    minimo = 0 if permitir_cancelar else 1
    escolha = ler_int("Escolha o navio: ", minimo, len(frota.navios))
    if permitir_cancelar and escolha == 0:
        return None
    return escolha - 1


def adicionar_navio_na_frota(frota, escolha=None):
    tipos = list(dados_navio.keys())
    if escolha is None:
        print("Escolha o tipo de navio:")
        for i, tipo in enumerate(tipos, start=1):
            print(f"{i}. {tipo}")
        escolha = ler_int("Digite o numero do tipo: ", 1, len(tipos)) - 1

    tipo_navio = tipos[escolha]
    novo = Navio(
        tipo_navio,
        dados_navio[tipo_navio]["saude_max_casco"],
        dados_navio[tipo_navio]["saude_max_vela"],
    )
    frota.adicionar_navio(novo)
    print(f"Navio {tipo_navio} adicionado com sucesso.")


def valor_venda_navio(navio):
    preco_compra = PRECO_NAVIOS.get(navio.tipo, 500)
    percentual_integridade = (
        (navio.saude_casco_atual / max(1, navio.saude_max_casco)) * 0.6
        + (navio.saude_velas_atual / max(1, navio.saude_max_vela)) * 0.4
    )
    return max(50, int((preco_compra * 0.6) * percentual_integridade))


def vender_carga_navio(frota, navio):
    ouro_ganho = 0
    for item in ITENS:
        qtd = int(navio.carga.get(item, 0))
        if qtd <= 0:
            continue

        if item in PRECO_MATERIAIS:
            preco_unit = PRECO_MATERIAIS[item] // 2
        elif item == "Ouro":
            preco_unit = 1
        else:
            preco_unit = 0

        ouro_ganho += qtd * preco_unit
        frota.qnt_itens[item] = max(0, frota.qnt_itens[item] - qtd)
        frota.carga_total_frota = max(0, frota.carga_total_frota - (qtd * PESO_ITENS[item]))
        navio.carga[item] = 0

    return ouro_ganho


def transferir_carga_navio_para_frota(frota, idx_origem):
    navio_origem = frota.navios[idx_origem]
    transferido = {item: 0 for item in ITENS}

    for item in ITENS:
        qtd_restante = int(navio_origem.carga.get(item, 0))
        if qtd_restante <= 0:
            continue

        for i, navio_destino in enumerate(frota.navios):
            if i == idx_origem or qtd_restante <= 0:
                continue

            livre_peso = navio_destino.carga_max - navio_destino.exibir_carga()
            if PESO_ITENS[item] == 0:
                qtd_para_mover = qtd_restante
            else:
                qtd_para_mover = min(qtd_restante, int(livre_peso // PESO_ITENS[item]))

            if qtd_para_mover <= 0:
                continue

            if navio_destino.adicionar_item_carga(item, qtd_para_mover):
                navio_origem.carga[item] -= qtd_para_mover
                qtd_restante -= qtd_para_mover
                transferido[item] += qtd_para_mover

    return transferido


def resumo_carga_navio(carga):
    return ", ".join([f"{item}: {int(carga.get(item, 0))}" for item in ITENS_SAQUE])


def gerar_navio_inimigo(tipo):
    navio = Navio(
        tipo,
        dados_navio[tipo]["saude_max_casco"],
        dados_navio[tipo]["saude_max_vela"],
    )
    for item in ITENS_SAQUE:
        livre_peso = navio.carga_max - navio.exibir_carga()
        if livre_peso <= 0:
            break
        peso = max(1, PESO_ITENS[item])
        max_qtd = int(livre_peso // peso)
        if max_qtd <= 0:
            continue
        qtd = random.randint(0, max_qtd)
        if qtd > 0:
            navio.adicionar_item_carga(item, qtd)
    return navio


def armazenar_item_frota(frota, item, quantidade):
    if quantidade <= 0:
        return 0

    restante = quantidade
    peso = PESO_ITENS[item]

    for i, navio in enumerate(frota.navios):
        if restante <= 0:
            break

        if peso == 0:
            if frota.adicionar_item_carga(item, restante, i):
                return quantidade
            continue

        livre_peso = navio.carga_max - navio.exibir_carga()
        cabem = int(livre_peso // peso)
        if cabem <= 0:
            continue

        colocar = min(restante, cabem)
        if colocar > 0 and frota.adicionar_item_carga(item, colocar, i):
            restante -= colocar

    return quantidade - restante


def capturar_navio_inimigo(frota, inimigo):
    novo_navio = Navio(
        inimigo["tipo"],
        max(0, inimigo["casco"]),
        max(0, inimigo["vela"]),
        inimigo["tripulacao"],
    )
    novo_navio.carga = {item: int(inimigo["carga"].get(item, 0)) for item in ITENS}
    frota.adicionar_navio(novo_navio)

    for item, qtd in novo_navio.carga.items():
        frota.qnt_itens[item] += qtd
        frota.carga_total_frota += qtd * PESO_ITENS[item]

    return novo_navio


def menu_gerenciar_frota(frota):
    while True:
        print(
            "\nGerenciar frota:\n"
            "1. Adicionar navio\n"
            "2. Adicionar item na carga\n"
            "3. Retirar item da frota\n"
            "4. Mostrar frota\n"
            "5. Reordenar navios\n"
            "6. Voltar"
        )
        opcao = input("Escolha: ").strip()
        limpar_tela()

        if opcao == "1":
            adicionar_navio_na_frota(frota)
        elif opcao == "2":
            if not frota.navios:
                print("Sem navios na frota.")
                continue
            idx_navio = escolher_navio(frota)
            print("Itens:")
            for i, item in enumerate(ITENS, start=1):
                print(f"{i}. {item}")
            idx_item = ler_int("Escolha o item: ", 1, len(ITENS)) - 1
            qtd = ler_int("Quantidade: ", 1)
            if frota.adicionar_item_carga(ITENS[idx_item], qtd, idx_navio):
                print("Item adicionado.")
            else:
                print("Nao foi possivel adicionar (carga maxima excedida).")
        elif opcao == "3":
            print("Itens:")
            for i, item in enumerate(ITENS, start=1):
                print(f"{i}. {item}")
            idx_item = ler_int("Escolha o item: ", 1, len(ITENS)) - 1
            qtd = ler_int("Quantidade: ", 1)
            if frota.retirar_item_frota(ITENS[idx_item], qtd):
                print("Item retirado da frota.")
            else:
                print("Quantidade insuficiente.")
        elif opcao == "4":
            frota.exibir_frota()
        elif opcao == "5":
            if len(frota.navios) < 2:
                print("Voce precisa de pelo menos 2 navios para reordenar.")
                continue
            print("Ordem atual:")
            for i, navio in enumerate(frota.navios, start=1):
                print(f"{i}. {navio.tipo}")
            origem = ler_int("Mover qual navio (numero): ", 1, len(frota.navios)) - 1
            destino = ler_int("Nova posicao (numero): ", 1, len(frota.navios)) - 1
            if frota.mover_navio(origem, destino):
                print("Ordem da frota atualizada.")
            else:
                print("Nao foi possivel reordenar.")
        elif opcao == "6":
            return
        else:
            print("Opcao invalida.")


def velocidade_navio(estado):
    return (estado["vela"] / max(1, estado["vela_max"])) * 12


def criar_estado_combate(navio):
    trip = navio.tripulacao_atual
    return {
        "tipo": navio.tipo,
        "casco": max(0, navio.saude_casco_atual),
        "casco_max": navio.saude_max_casco,
        "vela": max(0, navio.saude_velas_atual),
        "vela_max": navio.saude_max_vela,
        "canhoes_casco": navio.canhoes_por_lado * 2,
        "canhoes_vela": max(1, navio.canhoes_por_lado // 2),
        "tripulacao": trip,
        "conves": max(1, int(trip * 0.4)) if trip > 0 else 0,
        "mosquetes": max(1, int(trip * 0.45)) if trip > 0 else 0,
        "recarga_casco": 3,
        "recarga_vela": 4,
        "recarga_mosquete": 2,
        "carga": navio.carga.copy(),
    }


def mostrar_status_batalha(jogador, inimigo, rodada, distancia):
    print(f"\nRodada: {rodada} | Distancia: {distancia} m")
    print(
        "--- Navio Jogador ---"
        f"\nTipo de navio: {jogador['tipo']}"
        f"\nVida do casco: {jogador['casco']}"
        f"\nVida das velas: {jogador['vela']}"
        f"\nCanhoes primarios: {jogador['canhoes_casco']}"
        f"\nCanhoes secundarios: {jogador['canhoes_vela']}"
        f"\nTripulacao total: {jogador['tripulacao']} ( No conves: {jogador['conves']} )"
        f"\nVelocidade maxima (nos): {velocidade_navio(jogador):.2f}"
    )
    print(
        "--- Navio Inimigo ---"
        f"\nTipo de navio: {inimigo['tipo']}"
        f"\nVida do casco: {inimigo['casco']}"
        f"\nVida das velas: {inimigo['vela']}"
        f"\nCanhoes principais: {inimigo['canhoes_casco']}"
        f"\nCanhoes secundarios: {inimigo['canhoes_vela']}"
        f"\nTripulacao total: {inimigo['tripulacao']} ( No conves: {inimigo['conves']} )"
        f"\nVelocidade maxima (nos): {velocidade_navio(inimigo):.2f}"
    )


def recarregar(estado, ignorar=None):
    if ignorar is None:
        ignorar = set()
    estado["recarga_casco"] = estado["recarga_casco"] if "recarga_casco" in ignorar else min(3, estado["recarga_casco"] + 1)
    estado["recarga_vela"] = estado["recarga_vela"] if "recarga_vela" in ignorar else min(4, estado["recarga_vela"] + 1)
    estado["recarga_mosquete"] = estado["recarga_mosquete"] if "recarga_mosquete" in ignorar else min(2, estado["recarga_mosquete"] + 1)


def atacar_casco(atacante, defensor, distancia, nome):
    if atacante["recarga_casco"] < 3:
        print(f"{nome}: canhoes de casco recarregando ({atacante['recarga_casco']}/3).")
        return False
    if distancia >= 300:
        print("Distancia muito grande para atingir casco.")
        return False

    disparos = min(atacante["canhoes_casco"], atacante["tripulacao"])
    dano = 0
    for _ in range(disparos):
        dano += int(random.randint(16, 20) * (1 - distancia / 300))

    defensor["casco"] -= dano
    atacante["recarga_casco"] = 0
    print(f"{nome} causou {dano} de dano no casco.")

    if defensor["canhoes_casco"] > 0:
        perdas_canhao = sum(1 for _ in range(disparos) if random.random() <= 0.03)
        defensor["canhoes_casco"] = max(0, defensor["canhoes_casco"] - perdas_canhao)
        if perdas_canhao > 0:
            print(f"{nome} destruiu {perdas_canhao} canhao(oes) inimigo(s).")

    if defensor["tripulacao"] > 0:
        perdas_trip = sum(1 for _ in range(disparos) if random.random() <= 0.03)
        defensor["tripulacao"] = max(0, defensor["tripulacao"] - perdas_trip)
        defensor["conves"] = max(1, int(defensor["tripulacao"] * 0.4)) if defensor["tripulacao"] > 0 else 0
        if perdas_trip > 0:
            print(f"{nome} matou {perdas_trip} tripulante(s).")

    return True


def atacar_velas(atacante, defensor, distancia, nome):
    if atacante["recarga_vela"] < 4:
        print(f"{nome}: canhoes de velas recarregando ({atacante['recarga_vela']}/4).")
        return False
    if distancia >= 250:
        print("Distancia muito grande para atingir velas.")
        return False
    if defensor["vela"] <= 0:
        print("As velas alvo ja estao destruidas.")
        return False

    disparos = min(atacante["canhoes_vela"], atacante["tripulacao"])
    dano = 0
    for _ in range(disparos):
        dano += int(random.randint(58, 80) * (1 - distancia / 300))

    defensor["vela"] = max(0, defensor["vela"] - dano)
    atacante["recarga_vela"] = 0
    print(f"{nome} causou {dano} de dano nas velas.")

    if defensor["vela"] == 0:
        print("As velas foram totalmente destruidas.")

    return True


def atacar_tripulacao(atacante, defensor, distancia, nome):
    if atacante["recarga_mosquete"] < 2:
        print(f"{nome}: mosquetes recarregando ({atacante['recarga_mosquete']}/2).")
        return False
    if distancia >= 150:
        print("Distancia muito grande para ataque na tripulacao.")
        return False
    if defensor["tripulacao"] <= 0:
        print("Nao ha tripulacao inimiga restante.")
        return False

    tiros = min(atacante["mosquetes"], atacante["conves"])
    dano = 0
    for _ in range(tiros):
        dano += int(random.uniform(1, 2) * (1 - distancia / 300))

    defensor["tripulacao"] = max(0, defensor["tripulacao"] - dano)
    defensor["conves"] = max(1, int(defensor["tripulacao"] * 0.4)) if defensor["tripulacao"] > 0 else 0
    atacante["recarga_mosquete"] = 0

    print(f"{nome} eliminou {dano} da tripulacao inimiga.")
    return True


def turno_inimigo(inimigo, jogador, distancia):
    print("\nTurno do inimigo:")
    if inimigo["tripulacao"] <= 0 or inimigo["casco"] <= 0:
        return distancia

    if inimigo["recarga_casco"] >= 3 and distancia < 300:
        atacar_casco(inimigo, jogador, distancia, "Inimigo")
    elif inimigo["recarga_vela"] >= 4 and distancia < 250 and jogador["vela"] > 0:
        atacar_velas(inimigo, jogador, distancia, "Inimigo")
    elif inimigo["recarga_mosquete"] >= 2 and distancia < 150:
        atacar_tripulacao(inimigo, jogador, distancia, "Inimigo")
    else:
        vel_inimigo = velocidade_navio(inimigo)
        vel_jogador = velocidade_navio(jogador)
        if distancia > 100 and vel_inimigo >= vel_jogador and vel_inimigo > 0:
            distancia = max(0, distancia - 50)
            print("Inimigo se aproximou.")
        elif distancia < 300 and vel_inimigo < vel_jogador and vel_inimigo > 0:
            distancia = min(350, distancia + 50)
            print("Inimigo se afastou.")
        else:
            print("Inimigo manteve a posicao.")

    return distancia


def iniciar_batalha(frota, tipo_inimigo=None, navio_inimigo=None):
    if not frota.navios:
        print("Sem navio para batalhar.")
        return

    navio_jogador = frota.navios[0]
    if navio_inimigo is None:
        if tipo_inimigo is None:
            tipo_inimigo = random.choice(list(dados_navio.keys()))
        navio_inimigo = gerar_navio_inimigo(tipo_inimigo)

    jogador = criar_estado_combate(navio_jogador)
    inimigo = criar_estado_combate(navio_inimigo)
    distancia = 100
    rodada = 1

    while True:
        mostrar_status_batalha(jogador, inimigo, rodada, distancia)
        print(
            f"\n1. Atirar no casco ({min(3, jogador['recarga_casco'])}/3)"
            f"\n2. Atirar nas velas ({min(4, jogador['recarga_vela'])}/4)"
            "\n3. Atirar na tripulacao"
            "\n4. Se aproximar"
            "\n5. Se afastar"
            "\n6. Tentar fugir"
        )
        acao = input("Escolha: ").strip()
        limpar_tela()

        consumiu_turno = False
        acao_executada = False
        ignorar_recarga_jogador = set()

        if acao == "1":
            ataque_ok = atacar_casco(jogador, inimigo, distancia, "Voce")
            if ataque_ok:
                ignorar_recarga_jogador.add("recarga_casco")
                acao_executada = True
            consumiu_turno = True
        elif acao == "2":
            ataque_ok = atacar_velas(jogador, inimigo, distancia, "Voce")
            if ataque_ok:
                ignorar_recarga_jogador.add("recarga_vela")
                acao_executada = True
            consumiu_turno = True
        elif acao == "3":
            ataque_ok = atacar_tripulacao(jogador, inimigo, distancia, "Voce")
            if ataque_ok:
                ignorar_recarga_jogador.add("recarga_mosquete")
                acao_executada = True
            consumiu_turno = True
        elif acao == "4":
            if velocidade_navio(jogador) > 0 and distancia > 0:
                distancia = max(0, distancia - 50)
                print("Voce se aproximou do inimigo.")
                acao_executada = True
            else:
                print("Nao foi possivel se aproximar.")
            consumiu_turno = True
        elif acao == "5":
            if velocidade_navio(jogador) > 0 and distancia < 350:
                distancia = min(350, distancia + 50)
                print("Voce se afastou do inimigo.")
                acao_executada = True
            else:
                print("Nao foi possivel se afastar.")
            consumiu_turno = True
        elif acao == "6":
            vel_jog = velocidade_navio(jogador)
            vel_inim = velocidade_navio(inimigo)
            chance = 0.45
            if vel_jog > vel_inim:
                chance += 0.25
            if inimigo["tripulacao"] == 0:
                chance += 0.20
            if distancia >= 250:
                chance += 0.15

            if random.random() < min(0.95, chance):
                print("Voce conseguiu fugir.")
                navio_jogador.saude_casco_atual = max(0, jogador["casco"])
                navio_jogador.saude_velas_atual = max(0, jogador["vela"])
                navio_jogador.tripulacao_atual = max(0, min(navio_jogador.tripulacao_max, jogador["tripulacao"]))
                return

            print("Fuga falhou. O combate continua.")
            consumiu_turno = True
        else:
            print("Opcao invalida.")

        if inimigo["casco"] <= 0:
            print("\nVitoria! O navio inimigo foi destruido.")
            itens_recuperados = []
            itens_perdidos = []
            for item in ITENS_SAQUE:
                qtd_original = int(inimigo["carga"].get(item, 0))
                if qtd_original <= 0:
                    continue

                perda_pct = random.randint(10, 50)
                qtd_recuperavel = int(qtd_original * (100 - perda_pct) / 100)
                qtd_recebida = armazenar_item_frota(frota, item, qtd_recuperavel)
                qtd_perdida = qtd_original - qtd_recebida

                if qtd_recebida > 0:
                    itens_recuperados.append(f"{item}: +{qtd_recebida}")
                if qtd_perdida > 0:
                    itens_perdidos.append(f"{item}: -{qtd_perdida}")

            if itens_recuperados:
                print("Recursos recuperados do naufragio: " + ", ".join(itens_recuperados))
            else:
                print("Nenhum recurso util foi recuperado.")
            if itens_perdidos:
                print("Recursos perdidos na destruicao: " + ", ".join(itens_perdidos))

            navio_jogador.saude_casco_atual = max(0, jogador["casco"])
            navio_jogador.saude_velas_atual = max(0, jogador["vela"])
            navio_jogador.tripulacao_atual = max(0, min(navio_jogador.tripulacao_max, jogador["tripulacao"]))
            return

        if inimigo["tripulacao"] <= 0:
            capturado = capturar_navio_inimigo(frota, inimigo)
            print(
                f"\nVitoria por abordagem! Voce capturou um {capturado.tipo} com a carga intacta: "
                f"{resumo_carga_navio(capturado.carga)}"
            )
            navio_jogador.saude_casco_atual = max(0, jogador["casco"])
            navio_jogador.saude_velas_atual = max(0, jogador["vela"])
            navio_jogador.tripulacao_atual = max(0, min(navio_jogador.tripulacao_max, jogador["tripulacao"]))
            return

        if not consumiu_turno:
            continue

        recarregar(inimigo)
        distancia = turno_inimigo(inimigo, jogador, distancia)
        if acao_executada:
            recarregar(jogador, ignorar_recarga_jogador)

        if jogador["casco"] <= 0 or jogador["tripulacao"] <= 0:
            perda_ouro = min(frota.qnt_itens["Ouro"], random.randint(50, 250))
            if perda_ouro > 0:
                frota.retirar_item_frota("Ouro", perda_ouro)
            print(f"\nVoce foi derrotado. Perdeu {perda_ouro} ouro e retornou ao porto.")
            navio_jogador.saude_casco_atual = navio_jogador.saude_max_casco
            navio_jogador.saude_velas_atual = navio_jogador.saude_max_vela
            navio_jogador.tripulacao_atual = max(1, navio_jogador.tripulacao_max // 2)
            return

        rodada += 1


def navegar_pelos_mares(frota):
    evento = random.randint(1, 10)

    if evento <= 5:
        tipo_inimigo = random.choice(list(dados_navio.keys()))
        navio_inimigo = gerar_navio_inimigo(tipo_inimigo)
        print(f"Voce avistou um navio inimigo ({tipo_inimigo}) no horizonte.")
        print("1. Atacar\n2. Analisar\n3. Ignorar")
        escolha = input("Escolha: ").strip()
        limpar_tela()

        if escolha == "1":
            iniciar_batalha(frota, navio_inimigo=navio_inimigo)
        elif escolha == "2":
            dados = dados_navio[tipo_inimigo]
            print(
                f"Inimigo: {tipo_inimigo} | Casco max {dados['saude_max_casco']} | "
                f"Velas max {dados['saude_max_vela']} | Canhoes por lado {dados['canhoes_por_lado']}"
            )
            print(f"Carga visivel: {resumo_carga_navio(navio_inimigo.carga)}")
            atacar = input("Deseja atacar? (s/n): ").strip().lower()
            limpar_tela()
            if atacar == "s":
                iniciar_batalha(frota, navio_inimigo=navio_inimigo)
        else:
            print("Voce evitou o confronto.")

    elif evento <= 7:
        item = random.choice(["Madeira", "Aco", "Pano", "Rum", "Ouro"])
        qtd = random.randint(30, 150) if item != "Ouro" else random.randint(100, 350)

        recebido = False
        for i in range(len(frota.navios)):
            if frota.adicionar_item_carga(item, qtd, i):
                recebido = True
                break

        if recebido:
            print(f"Voce encontrou pilhagem: +{qtd} {item}.")
        else:
            print("Voce encontrou pilhagem, mas nao havia espaco para armazenar.")

    elif evento == 8:
        if cidades_existentes:
            cidade = random.choice(cidades_existentes)
            cidades_existentes.remove(cidade)
            cidades_conhecidas.append(cidade)
            print(f"Nova cidade descoberta: {cidade}.")
        elif cidades_conhecidas:
            print(f"Voce passou por {random.choice(cidades_conhecidas)}.")

    else:
        print("A viagem foi tranquila.")


def procurar_tesouro(frota):
    ouro = random.randint(120, 480)
    if frota.adicionar_item_carga("Ouro", ouro, 0):
        print(f"Voce encontrou um tesouro com {ouro} de ouro.")
    else:
        print("Voce encontrou um tesouro, mas nao conseguiu guardar.")


def reparar_emergencia(frota):
    if not frota.navios:
        print("Sem navios para reparar.")
        return

    navio = frota.navios[0]
    print(
        "Reparo de emergencia usa materiais:\n"
        "- Madeira: +8 casco por unidade\n"
        "- Aco: +12 casco por unidade\n"
        "- Pano: +10 velas por unidade"
    )

    max_madeira = frota.qnt_itens["Madeira"]
    max_aco = frota.qnt_itens["Aco"]
    max_pano = frota.qnt_itens["Pano"]

    if max_madeira == 0 and max_aco == 0 and max_pano == 0:
        print("Sem materiais para reparo.")
        return

    usar_madeira = ler_int(f"Madeira para usar (0-{max_madeira}): ", 0, max_madeira)
    usar_aco = ler_int(f"Aco para usar (0-{max_aco}): ", 0, max_aco)
    usar_pano = ler_int(f"Pano para usar (0-{max_pano}): ", 0, max_pano)

    if usar_madeira == 0 and usar_aco == 0 and usar_pano == 0:
        print("Nenhum material usado.")
        return

    frota.retirar_item_frota("Madeira", usar_madeira) if usar_madeira > 0 else None
    frota.retirar_item_frota("Aco", usar_aco) if usar_aco > 0 else None
    frota.retirar_item_frota("Pano", usar_pano) if usar_pano > 0 else None

    navio.saude_casco_atual = min(navio.saude_max_casco, navio.saude_casco_atual + usar_madeira * 8 + usar_aco * 12)
    navio.saude_velas_atual = min(navio.saude_max_vela, navio.saude_velas_atual + usar_pano * 10)

    print("Reparos concluidos no navio principal.")


def menu_ilha(frota):
    while True:
        print(
            "\nAtracado na ilha:\n"
            "1. Reparar navio por ouro\n"
            "2. Comprar materiais\n"
            "3. Vender materiais\n"
            "4. Comprar novo navio\n"
            "5. Vender navio\n"
            "6. Contratar tripulacao\n"
            "7. Voltar"
        )
        opcao = input("Escolha: ").strip()
        limpar_tela()

        if opcao == "1":
            if not frota.navios:
                print("Sem navios para reparar.")
                continue

            print(f"Ouro atual: {frota.qnt_itens['Ouro']}")
            idx = escolher_navio(frota, permitir_cancelar=True)
            if idx is None:
                continue
            navio = frota.navios[idx]
            falta_casco = navio.saude_max_casco - navio.saude_casco_atual
            falta_vela = navio.saude_max_vela - navio.saude_velas_atual

            if falta_casco <= 0 and falta_vela <= 0:
                print("Esse navio ja esta totalmente reparado.")
                continue

            custo = max(10, (falta_casco // 20) + (falta_vela // 25))
            print(f"Custo do reparo total: {custo} ouro.")
            confirmar = input("Confirmar? (s/n): ").strip().lower()
            if confirmar != "s":
                continue

            if not frota.retirar_item_frota("Ouro", custo):
                print("Ouro insuficiente.")
                continue

            navio.saude_casco_atual = navio.saude_max_casco
            navio.saude_velas_atual = navio.saude_max_vela
            print("Navio reparado com sucesso.")

        elif opcao == "2":
            if not frota.navios:
                print("Sem navios para armazenar materiais.")
                continue

            print(f"Ouro atual: {frota.qnt_itens['Ouro']}")
            idx_navio = escolher_navio(frota, permitir_cancelar=True)
            if idx_navio is None:
                continue
            itens_compra = ["Madeira", "Aco", "Pano", "Rum"]
            print("0. Cancelar")
            for i, item in enumerate(itens_compra, start=1):
                print(f"{i}. {item} ({PRECO_MATERIAIS[item]} ouro)")
            escolha_item = ler_int("Escolha o item: ", 0, len(itens_compra))
            if escolha_item == 0:
                continue
            idx_item = escolha_item - 1
            item = itens_compra[idx_item]
            qtd = ler_int("Quantidade (0 para cancelar): ", 0)
            if qtd == 0:
                continue
            custo = PRECO_MATERIAIS[item] * qtd

            if not frota.retirar_item_frota("Ouro", custo):
                print("Ouro insuficiente.")
                continue

            if not frota.adicionar_item_carga(item, qtd, idx_navio):
                frota.adicionar_item_carga("Ouro", custo, 0)
                print("Sem espaco no navio. Compra cancelada.")
                continue

            print(f"Compra concluida: {qtd} {item}.")

        elif opcao == "3":
            itens_venda = ["Madeira", "Aco", "Pano", "Rum"]
            for i, item in enumerate(itens_venda, start=1):
                print(f"{i}. {item} ({PRECO_MATERIAIS[item] // 2} ouro por unidade)")
            idx_item = ler_int("Escolha o item: ", 1, len(itens_venda)) - 1
            item = itens_venda[idx_item]
            qtd = ler_int("Quantidade: ", 1)

            if not frota.retirar_item_frota(item, qtd):
                print("Quantidade insuficiente para venda.")
                continue

            ganho = (PRECO_MATERIAIS[item] // 2) * qtd
            frota.adicionar_item_carga("Ouro", ganho, 0)
            print(f"Venda concluida: +{ganho} ouro.")

        elif opcao == "4":
            print(f"Ouro atual: {frota.qnt_itens['Ouro']}")
            print("Navios disponiveis:")
            tipos = list(PRECO_NAVIOS.keys())
            for i, tipo in enumerate(tipos, start=1):
                print(f"{i}. {tipo} - {PRECO_NAVIOS[tipo]} ouro")
            idx = ler_int("Escolha o navio (0 para cancelar): ", 0, len(tipos))
            if idx == 0:
                continue

            tipo = tipos[idx - 1]
            preco = PRECO_NAVIOS[tipo]
            if not frota.retirar_item_frota("Ouro", preco):
                print("Sem ouro suficiente.")
                continue

            novo = Navio(tipo, dados_navio[tipo]["saude_max_casco"], dados_navio[tipo]["saude_max_vela"])
            frota.adicionar_navio(novo)
            print(f"Compra concluida: {tipo} adicionado a frota.")

        elif opcao == "5":
            if len(frota.navios) <= 1:
                print("Nao e possivel vender o ultimo navio da frota.")
                continue

            idx = escolher_navio(frota, permitir_cancelar=True)
            if idx is None:
                continue
            navio = frota.navios[idx]
            print(
                "Como deseja vender?\n"
                "0. Cancelar\n"
                "1. Vender navio com toda carga (vende carga + navio)\n"
                "2. Vender navio e tentar transportar carga para outros navios"
            )
            modo = ler_int("Escolha: ", 0, 2)
            if modo == 0:
                print("Venda cancelada.")
                continue

            valor = valor_venda_navio(navio)
            print(f"Valor do navio ({navio.tipo}): {valor} ouro.")
            confirmar = input("Confirmar venda? (s/n): ").strip().lower()
            if confirmar != "s":
                print("Venda cancelada.")
                continue

            ouro_carga = 0
            if modo == 1:
                ouro_carga = vender_carga_navio(frota, navio)
                if ouro_carga > 0:
                    print(f"Carga vendida por {ouro_carga} ouro.")
            else:
                transferido = transferir_carga_navio_para_frota(frota, idx)
                itens_transferidos = [f"{item}: {qtd}" for item, qtd in transferido.items() if qtd > 0]
                if itens_transferidos:
                    print("Carga transferida: " + ", ".join(itens_transferidos))
                ouro_carga = vender_carga_navio(frota, navio)
                if ouro_carga > 0:
                    print(f"Sobra da carga vendida por {ouro_carga} ouro.")

            vendido = frota.remover_navio(idx)
            if vendido is None:
                print("Nao foi possivel vender este navio.")
                continue

            total_ouro = valor + ouro_carga
            frota.adicionar_item_carga("Ouro", total_ouro, 0)
            print(f"Navio {vendido.tipo} vendido. Total recebido: {total_ouro} ouro.")
        elif opcao == "6":
            if not frota.navios:
                print("Sem navios para contratar tripulacao.")
                continue

            print(f"Ouro atual: {frota.qnt_itens['Ouro']}")
            idx = escolher_navio(frota, permitir_cancelar=True)
            if idx is None:
                continue

            navio = frota.navios[idx]
            faltam = navio.tripulacao_max - navio.tripulacao_atual
            if faltam <= 0:
                print("Esse navio ja esta com tripulacao completa.")
                continue

            print(
                f"Tripulacao atual: {navio.tripulacao_atual}/{navio.tripulacao_max}\n"
                f"Custo por tripulante: {PRECO_TRIPULANTE} ouro"
            )
            qtd = ler_int(f"Quantos contratar (0-{faltam}, 0 para cancelar): ", 0, faltam)
            if qtd == 0:
                continue

            custo = qtd * PRECO_TRIPULANTE
            if not frota.retirar_item_frota("Ouro", custo):
                print("Ouro insuficiente.")
                continue

            navio.tripulacao_atual = min(navio.tripulacao_max, navio.tripulacao_atual + qtd)
            print(
                f"Contratacao concluida: +{qtd} tripulantes por {custo} ouro. "
                f"Tripulacao atual: {navio.tripulacao_atual}/{navio.tripulacao_max}."
            )

        elif opcao == "7":
            return
        else:
            print("Opcao invalida.")


def main():
    frota = carregar_jogo()

    while True:
        print(
            "\nOpcoes:\n"
            "1. Navegar pelos mares\n"
            "2. Procurar por um tesouro\n"
            "3. Mostrar estado atual\n"
            "4. Atracar em uma ilha\n"
            "5. Realizar reparos de emergencia\n"
            "6. Gerenciar a frota\n"
            "7. Salvar jogo\n"
            "8. Sair"
        )

        escolha = input("O que voce gostaria de fazer? ").strip()
        limpar_tela()

        if escolha == "1":
            navegar_pelos_mares(frota)
        elif escolha == "2":
            procurar_tesouro(frota)
        elif escolha == "3":
            frota.exibir_frota()
        elif escolha == "4":
            menu_ilha(frota)
        elif escolha == "5":
            reparar_emergencia(frota)
        elif escolha == "6":
            menu_gerenciar_frota(frota)
        elif escolha == "7":
            salvar_jogo(frota)
        elif escolha == "8":
            print("Saindo do jogo.")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    limpar_tela()
    print("Bem-vindo, capitao!")
    main()
