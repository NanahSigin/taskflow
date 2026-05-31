from src.gerenciador import Gerenciador

def test_criar_tarefa():
    g = Gerenciador()
    t = g.criar_tarefa("Teste", "Desc", "Alta", "Ana")

    assert t.id == 1
    assert t.titulo == "Teste"


def test_lista_com_tarefa():
    g = Gerenciador()

    g.criar_tarefa("Estudar", "Python", "Alta", "Ana")

    assert len(g.tarefas) == 1


def test_criar_duas_tarefas():
    g = Gerenciador()

    t1 = g.criar_tarefa("T1", "Desc1", "Alta", "Ana")
    t2 = g.criar_tarefa("T2", "Desc2", "Baixa", "João")

    assert t1.id == 1
    assert t2.id == 2