import networkx as nx

def init(HYPERLINK):
    """
        creates the antsystem(graph).
        makes the first node the seed page.
        returns the graph.
    """
    G = nx.Graph()
    G.add_node(HYPERLINK)
    return G
