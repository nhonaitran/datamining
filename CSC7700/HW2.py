from sklearn.datasets import load_digits 
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

def bits_on_count(x):
    return bin(x).count('1')

def sim(x1, x2):
    # define similarity as the bit count where the same bit is on in both images
    # the lower the value, the more similiar is the two images being compared.
    score = 0
    for i in range(x1.shape[0]):
        score += bits_on_count(int(math.floor(x1[i]))^int(math.floor(x2[i])))
    
    return score
    
def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=11,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness, alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size, font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # show graph
    plt.show()

graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
         (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

# you may name your edge labels
labels = map(chr, range(65, 65+len(graph)))
draw_graph(graph, labels)

# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
draw_graph(graph)

data = load_digits()
X = data.data
Y = data.target

digits_4_6_indices = np.where((Y==4) | (Y==6))
images_4_6 = X[digits_4_6_indices]
labels_4_6 = Y[digits_4_6_indices]
print images_4_6.shape

# compute similarity matrix
n = images_4_6.shape[0]
similarity_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        similarity_matrix[i,j] = sim(images_4_6[i], images_4_6[j])

#print similarity_matrix

import networkx as nx
import matplotlib.pyplot as plt

# use top 20 most similar images
k = 20
for i in range(0,n):   
    # get index of images most similar to image of interest, i.e. similarity score sorted increasing order.
    sort_index = np.argsort(similarity_matrix[i,:])
    
    # take top k
    top_k = sort_index[0:k]

    # get labels
    labels = labels_4_6[top_k]
    print "Digit", labels_4_6[i], "top -", k, ":", labels
    
    #create graph
    G = nx.Graph()
    prev_node = "%d.%02d"%(labels[0], 0)
    G.add_node(prev_node)
    for j in range(1,k):
        current_node = "%d.%02d"%(labels[j], j)
        G.add_node(current_node)
        if (labels[j] == labels[j-1]):
            G.add_edge(prev_node, current_node)
        prev_node = current_node
    
    print("graph has %d nodes with %d edges, %d connected components."\
         %(nx.number_of_nodes(G),nx.number_of_edges(G),nx.number_connected_components(G)))
    
    for cc in nx.connected_component_subgraphs(G):
        print "component has %d nodes: members={%s}"%(len(cc.nodes()), ','.join((str(x) for x in np.sort(cc.nodes()))))

    
    pos = nx.spring_layout(G, k=0.315,iterations=200) #nx.random_layout(G) #
    nx.draw(G, pos, node_size=800, with_labels=True, font_size=8)
    plt.show()