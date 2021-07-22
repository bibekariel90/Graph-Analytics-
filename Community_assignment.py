# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 12:36:39 2021

@author: Asus
"""
import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately
import matplotlib.pyplot as plt
import community as community_louvain
import matplotlib.cm as cm
import igraph

with open('got-nodes.csv', 'r') as nodecsv: # Open the file
    nodereader = csv.reader(nodecsv) # Read the csv
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][1:]

node_names = [n[0] for n in nodes] # Get a list of only the node names

with open('got-edges.csv', 'r') as edgecsv: # Open the file
    edgereader = csv.reader(edgecsv) # Read the csv
    edges = [tuple(e) for e in edgereader][1:] # Retrieve the data
    
#Creating graph
G = nx.Graph()# Initialize a Graph object

G.add_nodes_from(node_names) # Add nodes to the Graph
G.add_weighted_edges_from(edges) # Add edges to the Graph
print(nx.info(G))

#Finding density of the network
density = nx.density(G)
print("Network density:", density)

#Calculating diameter of largest node
# If your Graph has more than one component, this will return False:
print(nx.is_connected(G))

# Next, use nx.connected_components to get the list of components,
# then use the max() command to find the largest one:
components = nx.connected_components(G)
largest_component = max(components, key=len)

# Create a "subgraph" of just the largest component
# Then calculate the diameter of the subgraph, just like you did with density.
#

subgraph = G.subgraph(largest_component)
diameter = nx.diameter(subgraph)
print("Network diameter of largest component:", diameter)

#calculate transitivity 
triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)

#Centrality measures
degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')
sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
#Printing Top 20 nodes by degree
print("Top 20 nodes by degree:")
for d in sorted_degree[:20]:
    print(d)
    
betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality

# Assign each to an attribute in your network
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')
sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
sorted_eigenvector = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)

    
#First get the top 20 nodes by betweenness as a list
top_betweenness = sorted_betweenness[:20]

#Then find and print their degree
for tb in top_betweenness: # Loop through top_betweenness
    degree = degree_dict[tb[0]] # Use degree_dict to access a node's degree, see footnote 2
    print("Name:", tb[0], "| Betweenness Centrality:", tb[1], "| Degree:", degree)    
    
    
#First get the top 20 nodes by betweenness as a list
top_eigenvector = sorted_eigenvector[:20]    
    
#Then find and print their degree
for tb in top_eigenvector: # Loop through top_betweenness
    degree = degree_dict[tb[0]] # Use degree_dict to access a node's degree, see footnote 2
    print("Name:", tb[0], "| Eigenvector Centrality:", tb[1], "| Degree:", degree)

#Plotting the graph
pos = nx.spring_layout(G)
betCent= nx.betweenness_centrality(G, normalized = True,
                                    endpoints = True)
node_color=[20000.0 * G.degree(v) for v in G]
node_size = [v * 25000 for v in betCent.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(G,pos=pos, with_labels=False,
                  node_color=node_color,
                  node_size=node_size)

plt.axis('off')

#Eigenvector centrality
pos = nx.spring_layout(G)
betCent= nx.eigenvector_centrality(G)
node_color=[20000.0 * G.degree(v) for v in G]
node_size = [v * 20000 for v in betCent.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(G,pos=pos, with_labels=False,
                  node_color=node_color,
                  node_size=node_size)

plt.axis('off')

#Betweenness centrality
pos = nx.spring_layout(G)
betCent= nx.degree_centrality(G)
node_color=[20000.0 * G.degree(v) for v in G]
node_size = [v * 5000 for v in betCent.values()]
#plt.figure(figsize=(20,20))
nx.draw_networkx(G,pos=pos, with_labels=False,
                  node_color=node_color,
                  node_size=node_size)

plt.axis('off')


#COmmunity Dection
from cdlib import algorithms, viz

communities = algorithms.louvain(G,weight='Weight',resolution=1., randomize=False)
pos = nx.spring_layout(G)
viz.plot_network_clusters(G,communities,pos)
viz.plot_community_graph(G, communities)


coms = algorithms.ga(G)
viz.plot_network_clusters(G, coms)

partition = community_louvain.best_partition(G)

# compute the best partition
# partition = community_louvain.best_partition(G)

# # draw the graph
pos = nx.spring_layout(G)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                        cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()
