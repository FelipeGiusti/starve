import os
import sys
import threading
import time
import webbrowser

from websockets.exceptions import ConnectionClosed
from websockets.sync.server import serve

import mundo
import protocolo
import ranking

ENDERECO = os.environ.get("ENDERECO", "0.0.0.0")
PORTA = int(os.environ.get("PORTA", "8000"))
INTERVALO_TICK = 0.05
INTERVALO_SALVAR = 5

PASTA = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PASTA, "cliente", "index.html"), encoding="utf-8") as arquivo:
    PAGINA = arquivo.read()

conexoes = set()
trava_conexoes = threading.Lock()


def entregar_pagina(conexao, requisicao):
    if requisicao.path == "/ws":
        return None
    resposta = conexao.respond(200, PAGINA)
    del resposta.headers["Content-Type"]
    resposta.headers["Content-Type"] = "text/html; charset=utf-8"
    return resposta


def atender_jogador(conexao):
    id_jogador = None
    with trava_conexoes:
        conexoes.add(conexao)
    try:
        for texto in conexao:
            mensagem = protocolo.ler(texto)
            if mensagem is None:
                continue

            if mensagem[0] == "J":
                if id_jogador is not None:
                    mundo.sair(id_jogador)
                id_jogador = mundo.entrar(mensagem[1])
                if id_jogador is None:
                    conexao.send(protocolo.servidor_cheio())
                else:
                    conexao.send(protocolo.boas_vindas(id_jogador))

            elif mensagem[0] == "M" and id_jogador is not None:
                mundo.mover(id_jogador, mensagem[1], mensagem[2])
    except ConnectionClosed:
        pass
    finally:
        with trava_conexoes:
            conexoes.discard(conexao)
        if id_jogador is not None:
            mundo.sair(id_jogador)


def transmitir():
    ultimo_salvamento = time.monotonic()
    ranking_mudou = False

    while True:
        inicio = time.monotonic()

        jogadores, comidas, eventos = mundo.foto()

        for jogador in jogadores.values():
            if ranking.atualizar(jogador["nome"], jogador["massa"]):
                ranking_mudou = True

        mensagens = [protocolo.comeu(a, b) for a, b in eventos]
        mensagens.append(protocolo.estado(jogadores, comidas))
        mensagens.append(protocolo.ranking(ranking.top()))

        with trava_conexoes:
            destinos = list(conexoes)

        for conexao in destinos:
            try:
                for mensagem in mensagens:
                    conexao.send(mensagem)
            except ConnectionClosed:
                pass

        if ranking_mudou and inicio - ultimo_salvamento > INTERVALO_SALVAR:
            ranking.salvar()
            ranking_mudou = False
            ultimo_salvamento = inicio

        time.sleep(max(0, INTERVALO_TICK - (time.monotonic() - inicio)))


def main():
    mundo.iniciar()
    ranking.carregar()
    threading.Thread(target=transmitir, daemon=True).start()

    with serve(
        atender_jogador,
        ENDERECO,
        PORTA,
        process_request=entregar_pagina,
        max_size=256,
    ) as servidor:
        print(f"Starve rodando em http://localhost:{PORTA}")
        if getattr(sys, "frozen", False):
            webbrowser.open(f"http://localhost:{PORTA}")
        servidor.serve_forever()


if __name__ == "__main__":
    main()
