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


def add_page(HYPERLINK,PARENT,G):
    """
        Adds the page to the graph.
    """
    for i in HYPERLINK:
        G.add(HYPERLINK)
        G.add_edge(PARENT,HYPERLINK)
    return G
