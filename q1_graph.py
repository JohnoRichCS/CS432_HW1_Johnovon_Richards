import networkx as nx
import matplotlib.pyplot as plt

EDGES = [
    ("A", "B"),
    ("B", "A"),
    ("B", "C"),
    ("C", "D"),
    ("C", "G"),
    ("D", "A"),
    ("D", "H"),
    ("E", "F"),
    ("E", "O"),
    ("F", "G"),
    ("G", "C"),
    ("H", "L"),
    ("J", "N"),
    ("K", "I"),
    ("M", "A"),
    ("N", "L"),
    ("O", "J"),
]

def main() -> None:
    G = nx.DiGraph()
    G.add_edges_from(EDGES)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=900)
    nx.draw_networkx_labels(G, pos, font_size=11)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="-|>", arrowsize=18, width=1.5)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig("q1_graph.png", dpi=200)
    print("Wrote q1_graph.png")

if __name__ == "__main__":
    main()
