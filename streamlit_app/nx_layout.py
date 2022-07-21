import networkx as nx
import numpy as np
from typing import Optional


def hierarchy_layout(G: nx.classes.graph.Graph,
                     root: int = None,
                     width: float = 1.0,
                     vert_gap: float = 0.2,
                     vert_loc: float = 0.0,
                     xcenter: float = 0.5) -> dict:

    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = np.random.choice(list(G.nodes))

    def _hierarchy_pos(G: nx.classes.graph.Graph,
                       root: int,
                       width: float = 1.0,
                       vert_gap: float = 0.2,
                       vert_loc: float = 0.0,
                       xcenter: float = 0.5,
                       pos: Optional[dict] = None,
                       parent: Optional[int] = None) -> dict:

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
