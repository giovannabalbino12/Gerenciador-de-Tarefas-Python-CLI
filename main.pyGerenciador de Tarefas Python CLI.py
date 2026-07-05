import json
import os
from datetime import datetime


class Tarefa:
    def __init__(self, titulo, concluida=False, criada_em=None):
        self.titulo = titulo
        self.concluida = concluida
        self.criada_em = criada_em or datetime.now().strftime("%d/%m/%Y %H:%M")

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "concluida": self.concluida,
            "criada_em": self.criada_em,
        }


class GerenciadorTarefas:
    ARQUIVO = "tarefas.json"

    def __init__(self):
        self.tarefas = []
        self.carregar()

    def adicionar(self, titulo):
        self.tarefas.append(Tarefa(titulo))
        self.salvar()

    def listar(self):
        if not self.tarefas:
            print("\nNenhuma tarefa cadastrada.")
            return

        print("\n=== TAREFAS ===")
        for i, tarefa in enumerate(self.tarefas, 1):
            status = "✓" if tarefa.concluida else "✗"
            print(f"{i}. [{status}] {tarefa.titulo} ({tarefa.criada_em})")

    def concluir(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].concluida = True
            self.salvar()

    def remover(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas.pop(indice)
            self.salvar()

    def salvar(self):
        with open(self.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in self.tarefas],
                f,
                ensure_ascii=False,
                indent=4,
            )

    def carregar(self):
        if os.path.exists(self.ARQUIVO):
            with open(self.ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.tarefas = [
                    Tarefa(
                        titulo=t["titulo"],
                        concluida=t["concluida"],
                        criada_em=t["criada_em"],
                    )
                    for t in dados
                ]


def menu():
    sistema = GerenciadorTarefas()

    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Remover tarefa")
        print("5 - Sair")

        opcao = input("\nEscolha: ")

        if opcao == "1":
            titulo = input("Nome da tarefa: ")
            sistema.adicionar(titulo)

        elif opcao == "2":
            sistema.listar()

        elif opcao == "3":
            sistema.listar()
            indice = int(input("Número da tarefa: ")) - 1
            sistema.concluir(indice)

        elif opcao == "4":
            sistema.listar()
            indice = int(input("Número da tarefa: ")) - 1
            sistema.remover(indice)

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
    