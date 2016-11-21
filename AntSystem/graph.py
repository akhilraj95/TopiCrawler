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


def add_page(HYPERLINKS,PARENT,G):
    """
        Adds the page to the graph.
    """
    for hyperlink in HYPERLINKS:
        G.add_node(hyperlink)
        G.add_edge(PARENT,hyperlink)
    return G
