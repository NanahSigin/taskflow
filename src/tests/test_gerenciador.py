from src.gerenciador import Gerenciador


def test_criar_tarefa():

    gerenciador = Gerenciador()

    tarefa = gerenciador.criar_tarefa(
        "Teste",
        "Descrição",
        "Alta"
    )

    assert tarefa.titulo == "Teste"
    assert len(gerenciador.tarefas) == 1


def test_excluir_tarefa():

    gerenciador = Gerenciador()

    tarefa = gerenciador.criar_tarefa(
        "Teste",
        "Descrição",
        "Alta"
    )

    gerenciador.excluir_tarefa(
        tarefa.id
    )

    assert len(
        gerenciador.tarefas
    ) == 0