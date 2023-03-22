import time
import random

# Define uma classe Node que representa um nó na rede.
class Node:
    def __init__(self, id):
        # Cada nó tem um ID exclusivo e começa sem coordenador.
        self.id = id
        self.coordinator = None
        # Cada nó mantém uma lista de outros nós conhecidos na rede.
        self.nodes = []

    # Adiciona um novo nó à lista de nós conhecidos.
    def add_node(self, node):
        self.nodes.append(node)

    # Inicia uma eleição neste nó.
    def start_election(self):
        # Imprime uma mensagem informando que o nó iniciou a eleição.
        print(f"Nó {self.id} iniciou a eleição.")
        # Cria uma lista de nós com IDs maiores que o ID do nó atual.
        higher_nodes = [node for node in self.nodes if node.id > self.id]
        # Se não houver nós com IDs maiores, o nó atual é o novo coordenador.
        if not higher_nodes:
            print(f"Nó {self.id} é o novo coordenador.")
            self.coordinator = self
            return

        # Escolhe um nó aleatório da lista de nós com IDs maiores e inicia uma eleição nele.
        chosen_node = random.choice(higher_nodes)
        print(f"Nó {self.id} escolheu o nó {chosen_node.id}.")
        if chosen_node.start_election():
            # Se o nó escolhido falhar durante a eleição, o nó atual se torna o novo coordenador.
            print(f"Nó {chosen_node.id} falhou. Nó {self.id} é o novo coordenador.")
            self.coordinator = self
            return True

        # Se o nó escolhido vencer a eleição, ele se torna o novo coordenador.
        print(f"Nó {chosen_node.id} venceu a eleição.")
        self.coordinator = chosen_node
        return False

if __name__ == "__main__":
    # Cria uma lista de 5 nós e adiciona cada um dos outros nós à sua lista de nós conhecidos.
    nodes = [Node(i) for i in range(5)]
    for i in range(5):
        for j in range(i + 1, 5):
            nodes[i].add_node(nodes[j])
            nodes[j].add_node(nodes[i])

    # Inicia uma eleição em um nó aleatório da lista de nós criada anteriormente.
    random.choice(nodes).start_election()