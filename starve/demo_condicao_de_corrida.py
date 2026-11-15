import threading
import time

QUANTIDADE_JOGADORES = 10


def disputar_comida(usar_trava):
    comidas = {"maca"}
    quem_comeu = []
    trava = threading.Lock()
    largada = threading.Barrier(QUANTIDADE_JOGADORES)

    def comer(nome):
        if "maca" in comidas:
            time.sleep(0.01)
            comidas.discard("maca")
            quem_comeu.append(nome)

    def jogador(nome):
        largada.wait()
        if usar_trava:
            with trava:
                comer(nome)
        else:
            comer(nome)

    threads = [
        threading.Thread(target=jogador, args=(f"Jogador {i}",))
        for i in range(1, QUANTIDADE_JOGADORES + 1)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return quem_comeu


if __name__ == "__main__":
    for usar_trava in (False, True):
        titulo = "COM trava (mutex)" if usar_trava else "SEM trava"
        quem_comeu = disputar_comida(usar_trava)
        print(f"{titulo}: 1 maçã, {len(quem_comeu)} jogador(es) comeram -> {quem_comeu}")
