from src.gerenciador import Gerenciador

def test_criar_tarefa():
    g = Gerenciador()
    t = g.criar_tarefa("Teste", "Desc", "Alta", "Ana")

    assert t.titulo == "Teste"