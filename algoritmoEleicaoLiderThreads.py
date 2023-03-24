# coding=UTF-8
import time
import random
import threading

# Define uma classe Node que representa um nó na rede.
class Node:
    def __init__(self, id):
        # Cada nó tem um ID exclusivo e começa sem coordenador.
        self.id = id
        self.coordinator = None
        # Cada nó mantém uma lista de outros nós conhecidos na rede.
        self.nodes = []
        # Cada nó tem uma thread que será usada para iniciar eleições.
        self.thread = threading.Thread(target=self.start_election)

    # Adiciona um novo nó à lista de nós conhecidos.
    def add_node(self, node):
        self.nodes.append(node)

    # Inicia uma eleição neste nó.
    def start_election(self):
        # Imprime uma mensagem informando que o nó iniciou a eleição.
        print(f"Node {self.id} iniciou a eleicao.")
        # Cria uma lista de nós com IDs maiores que o ID do nó atual.
        higher_nodes = [node for node in self.nodes if node.id > self.id]
        # Se não houver nós com IDs maiores, o nó atual é o novo coordenador.
        if not higher_nodes:
            print(f"Node {self.id} eh o novo coordenador.")
            self.coordinator = self
            return

        # Escolhe um nó aleatório da lista de nós com IDs maiores e inicia uma eleição nele.
        chosen_node = random.choice(higher_nodes)
        print(f"Node {self.id} escolheu o node {chosen_node.id}.")
        if chosen_node.thread.is_alive():
            # Se a thread do nó escolhido ainda estiver executando, é porque ele não respondeu à eleição.
            # Nesse caso, o nó atual assume que o nó escolhido falhou e se torna o novo coordenador.
            print(f"Node {chosen_node.id} nao respondeu. Node {self.id} eh o novo coordenador.")
            self.coordinator = self
        else:
            # Se a thread do nó escolhido já terminou, é porque ele venceu a eleição.
            # Nesse caso, ele se torna o novo coordenador.
            print(f"Node {chosen_node.id} venceu a eleicao.")
            self.coordinator = chosen_node

    # Inicia a thread do nó.
    def start(self):
        self.thread.start()


if __name__ == "__main__":
    # Cria uma lista de 5 nós e adiciona cada um dos outros nós à sua lista de nós conhecidos.
    nodes = [Node(i) for i in range(5)]
    for i in range(5):
        for j in range(i + 1, 5):
            nodes[i].add_node(nodes[j])
            nodes[j].add_node(nodes[i])

    # Inicia as threads de todos os nós.
    for node in nodes:
        node.start()

    # Aguarda todas as threads terminarem antes de continuar a execução.
    for node in nodes:
        node.thread.join()
