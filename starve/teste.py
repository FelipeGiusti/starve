import mundo
import protocolo
from demo_condicao_de_corrida import disputar_comida

assert protocolo.ler("JFe;li,pe:!") == ("J", "Felipe")
assert protocolo.ler("J") == ("J", "Anonimo")
assert protocolo.ler("M0.5,-1") == ("M", 0.5, -1.0)
assert protocolo.ler("Mnan,0") is None
assert protocolo.ler("M1,2,3") is None
assert protocolo.ler("Zqualquer") is None
assert protocolo.ler(b"J") is None

grande = mundo.entrar("Grande")
pequeno = mundo.entrar("Pequeno")
mundo.jogadores[grande].update(x=500, y=500, massa=50)
mundo.jogadores[pequeno].update(x=510, y=500, massa=10)
assert mundo.mover(pequeno, 0, 0)
assert pequeno in mundo.jogadores
assert mundo.mover(grande, 0, 0)
assert pequeno not in mundo.jogadores
assert mundo.jogadores[grande]["massa"] == 60
assert mundo.foto()[2] == [(grande, pequeno)]
assert mundo.mover(pequeno, 1, 0) is False

mundo.iniciar()
mundo.comidas.clear()
mundo.comidas[999] = (500, 500)
mundo.mover(grande, 0, 0)
assert 999 not in mundo.comidas
assert mundo.jogadores[grande]["massa"] == 61
assert len(mundo.comidas) == 1

assert len(disputar_comida(usar_trava=True)) == 1

print("Todos os testes passaram.")
