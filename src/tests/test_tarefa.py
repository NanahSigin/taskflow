import sys
import os

sys.path.append(os.path.abspath("src"))

from gerenciador import Gerenciador

def test_criar_tarefa():
    g = Gerenciador()
    t = g.criar_tarefa("Teste", "Desc", "Alta", "Ana")

    assert t.id == 1
    assert t.titulo == "Teste"