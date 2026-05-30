from gerenciador import Gerenciador

def test_criar_tarefa():
    g = Gerenciador()
    t = g.criar_tarefa("Teste", "Desc", "Alta")

    assert t.id == 1
    assert t.titulo == "Teste"