from pyvis.network import Network
import os
import pandas as pd


got_net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

def create_network(data = None):
    # set the physics layout of the network
    got_data = pd.DataFrame(data)

    sources = got_data['source']
    targets = got_data['target']
    # weights = got_data['Weight']

    edge_data = zip(sources, targets)#, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        # w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst)#, value=w)

    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
        node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])

    path = os.path.join(os.getcwd(),'research/templates/Interactions/interactions.html')
    got_net.save_graph(path)

