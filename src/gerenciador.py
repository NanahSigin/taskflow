from tarefa import Tarefa


class Gerenciador:

    def __init__(self):
        self.tarefas = []
        self.proximo_id = 1

    def criar_tarefa(self, titulo, descricao, prioridade):

        tarefa = Tarefa(
            self.proximo_id,
            titulo,
            descricao,
            prioridade
        )

        self.tarefas.append(tarefa)
        self.proximo_id += 1

        return tarefa

    def listar_tarefas(self):
        return self.tarefas

    def buscar_tarefa(self, id):

        for tarefa in self.tarefas:
            if tarefa.id == id:
                return tarefa

        return None

    def excluir_tarefa(self, id):

        tarefa = self.buscar_tarefa(id)

        if tarefa:
            self.tarefas.remove(tarefa)