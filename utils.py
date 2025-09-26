from graphviz import Digraph

def build_tree(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph()
    curr_id = str(id(node))
    graph.node(curr_id, str(node[0]))
    if parent:
        graph.edge(parent, curr_id)
    for child in node[1:]:
        if isinstance(child, tuple):
            build_tree(child, graph, curr_id)
        else:
            leaf_id = str(id(child)) + curr_id
            graph.node(leaf_id, str(child))
            graph.edge(curr_id, leaf_id)
    return graph
