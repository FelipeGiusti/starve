import math
import random
import threading
import time

LARGURA = 2000
ALTURA = 2000
TOTAL_COMIDAS = 150
MAX_JOGADORES = 50
MASSA_INICIAL = 10
VANTAGEM_PARA_COMER = 1.1

trava = threading.Lock()
jogadores = {}
comidas = {}
eventos = []
proximo_id = 0


def raio(massa):
    return 6 * math.sqrt(massa)


def gerar_id():
    global proximo_id
    proximo_id += 1
    return proximo_id


def nova_comida():
    comidas[gerar_id()] = (random.uniform(0, LARGURA), random.uniform(0, ALTURA))


def iniciar():
    with trava:
        for _ in range(TOTAL_COMIDAS):
            nova_comida()


def entrar(nome):
    with trava:
        if len(jogadores) >= MAX_JOGADORES:
            return None
        id_jogador = gerar_id()
        jogadores[id_jogador] = {
            "nome": nome,
            "x": random.uniform(0, LARGURA),
            "y": random.uniform(0, ALTURA),
            "massa": MASSA_INICIAL,
            "ultimo": time.monotonic(),
        }
        return id_jogador


def sair(id_jogador):
    with trava:
        jogadores.pop(id_jogador, None)


def mover(id_jogador, dx, dy):
    with trava:
        eu = jogadores.get(id_jogador)
        if eu is None:
            return False

        agora = time.monotonic()
        dt = min(agora - eu["ultimo"], 0.1)
        eu["ultimo"] = agora

        tamanho = math.hypot(dx, dy)
        if tamanho > 1:
            dx, dy = dx / tamanho, dy / tamanho

        passo = 800 / math.sqrt(eu["massa"]) * dt
        eu["x"] = min(max(eu["x"] + dx * passo, 0), LARGURA)
        eu["y"] = min(max(eu["y"] + dy * passo, 0), ALTURA)

        comer_comidas(eu)
        comer_jogadores(id_jogador, eu)
        return True


def comer_comidas(eu):
    alcance = raio(eu["massa"])
    for id_comida, (x, y) in list(comidas.items()):
        if math.hypot(x - eu["x"], y - eu["y"]) < alcance:
            del comidas[id_comida]
            eu["massa"] += 1
            nova_comida()


def comer_jogadores(id_jogador, eu):
    alcance = raio(eu["massa"])
    for id_outro, outro in list(jogadores.items()):
        if id_outro == id_jogador:
            continue
        maior = eu["massa"] > outro["massa"] * VANTAGEM_PARA_COMER
        encostou = math.hypot(outro["x"] - eu["x"], outro["y"] - eu["y"]) < alcance
        if maior and encostou:
            del jogadores[id_outro]
            eu["massa"] += outro["massa"]
            eventos.append((id_jogador, id_outro))


def foto():
    with trava:
        copia_jogadores = {i: dict(j) for i, j in jogadores.items()}
        copia_comidas = list(comidas.values())
        copia_eventos = eventos[:]
        eventos.clear()
    return copia_jogadores, copia_comidas, copia_eventos
