from pyvis.network import Network
import networkx as nx
import os
import pandas as pd

def create_network(data = None, directed=True):
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    # set the physics layout of the network
    got_data = pd.DataFrame(data)
    sources = got_data['source']
    targets = got_data['target']
    weights = got_data['score']

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]

        G.add_node(src, title=src)
        G.add_node(dst, title=dst)
        G.add_edge(src, dst)
    return G


def calculate_betweens(G , k: int =None):
    """Calculate betweens and return node"""
    center_nodes = nx.betweenness_centrality(G, k=k, endpoints=True)
    res = {"max": {}}
    max = -1
    for node, value in center_nodes.items():
        if value > max:
            res.update({'max': {node: value}})
            max = value

    return res['max']

def calculate_density(G):
    """Calculate density of the graph"""
    return nx.density(G) 

def calculate_reciprocity(G ):
    """Calculate reciprocity and return node"""
    return  nx.reciprocity(G)

def calculate_radius(G):
    """Calculate over all radius of graph"""
    return nx.radius(G)


def calculate_diameter(G):
    """Calculate over all diameter of graph"""
    return nx.diameter(G)
