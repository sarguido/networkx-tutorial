import networkx as nx
import networkx.readwrite as rw

g = nx.Graph()
g.add_edge(1,2, weight=3)
g.add_edge(1,3, weight=1)
g.add_edge(2,4, weight=67)
g.add_edge(2,5, weight=1)

with open('edgelist.txt', 'w') as f:
    f.write('\n'.join(list(nx.generate_edgelist(g, data=True))))
