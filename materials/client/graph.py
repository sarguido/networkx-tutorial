import networkx as nx
#import networkx.readwrite as rw
#from networkx.readwrite import json_graph
import json

edgelist_txt = 'retweet_relationships/retweets.txt'

# json_filename = 'graph.json'

ge = nx.read_edgelist(edgelist_txt, create_using=nx.DiGraph())
# tree = nx.read_edgelist('tree_edges.txt', create_using=nx.DiGraph())
#
# jsongraph.adjacency_data(ge)
