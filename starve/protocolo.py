import math

TAMANHO_MAXIMO_NOME = 12


def ler(texto):
    if not isinstance(texto, str) or not texto:
        return None
    tipo, conteudo = texto[0], texto[1:]

    if tipo == "J":
        nome = "".join(c for c in conteudo if c.isalnum() or c == " ")
        nome = nome.strip()[:TAMANHO_MAXIMO_NOME]
        return ("J", nome or "Anonimo")

    if tipo == "M":
        try:
            dx, dy = (float(valor) for valor in conteudo.split(","))
        except ValueError:
            return None
        if not (math.isfinite(dx) and math.isfinite(dy)):
            return None
        return ("M", dx, dy)

    return None


def boas_vindas(id_jogador):
    return f"I{id_jogador}"


def servidor_cheio():
    return "X"


def estado(jogadores, comidas):
    parte_jogadores = ";".join(
        f"{i},{j['x']:.0f},{j['y']:.0f},{j['massa']},{j['nome']}"
        for i, j in jogadores.items()
    )
    parte_comidas = ";".join(f"{x:.0f},{y:.0f}" for x, y in comidas)
    return f"S{parte_jogadores}|{parte_comidas}"


def comeu(id_comedor, id_comido):
    return f"E{id_comedor},{id_comido}"


def ranking(lista):
    return "R" + ";".join(f"{nome}:{massa}" for nome, massa in lista)
