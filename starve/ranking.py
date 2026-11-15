import json
import os

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking.json")
TAMANHO_TOP = 10
LIMITE_GUARDADO = 100

recordes = {}


def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, encoding="utf-8") as arquivo:
            recordes.update(json.load(arquivo))


def atualizar(nome, massa):
    if massa > recordes.get(nome, 0):
        recordes[nome] = massa
        return True
    return False


def ordenados():
    return sorted(recordes.items(), key=lambda par: par[1], reverse=True)


def top():
    return ordenados()[:TAMANHO_TOP]


def salvar():
    melhores = dict(ordenados()[:LIMITE_GUARDADO])
    recordes.clear()
    recordes.update(melhores)

    temporario = ARQUIVO + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(recordes, arquivo, ensure_ascii=False)
    os.replace(temporario, ARQUIVO)
