class Tarefa:
    def __init__(self, id, titulo, descricao, prioridade):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = "A Fazer"

    def __str__(self):
        return (
            f"\nID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Descrição: {self.descricao}\n"
            f"Prioridade: {self.prioridade}\n"
            f"Status: {self.status}\n"
        )