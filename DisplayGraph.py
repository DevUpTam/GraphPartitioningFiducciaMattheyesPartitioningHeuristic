import networkx as nx
from matplotlib import pyplot as plot1
import pandas as pd

file1 = pd.read_csv("graph.csv")
edges = list()
for i in range(0, len(file1), 1):
    temp = [file1.loc[i, 'start'], file1.loc[i, 'end']]
    edges.append(temp)

G = nx.Graph()
G.add_edges_from(edges)
nx.draw_networkx(G)
plot1.show()