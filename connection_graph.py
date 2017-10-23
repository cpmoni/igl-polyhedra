import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain
from itertools import combinations
import sys
from dendropy.datamodel import treemodel
import dendropy

import warnings
warnings.filterwarnings("ignore")

#Just used so we don't have to write out the trivial splits
def get_trivia_splits(vertices):
    triv_splits=[]
    x = vertices
    for vertice in x:
        left = set(vertice)
        right = set(vertices).difference(vertice)
        triv_splits.append([left, right])
    return triv_splits

#A function to get a powerset. Used to get powerset of new_leaves in order to get all ways to add a new leaf.
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

#used to get all the new splits made by one of the three ways we can add new leaves to existing splits (Samara March 29th)
def newleaves(num, splits, pow_set, new_leaves_set, new_splits):
    for n_leaves in pow_set:
        if len(n_leaves)>=num:
            rest = new_leaves_set.difference(n_leaves)
            for split in splits:
                x=split[0].copy()
                y=split[1].copy()
                x.update(n_leaves)
                y.update(rest)
                z=[x,y]
                new_splits.append(z)

#returns a list of all new splits in list of set format
def get_new_splits(vertices, tree, new_leaves):
    trivia_splits = get_trivia_splits(vertices)
    empty = [[set(), set(vertices)]]
    new_leaf_set = set(new_leaves)
    pow_set = list(powerset(new_leaf_set))
    new_splits=[]
    newleaves(2, empty, pow_set, new_leaf_set , new_splits)
    newleaves(1, trivia_splits, pow_set, new_leaf_set , new_splits)
    newleaves(0, tree, pow_set, new_leaf_set , new_splits)
    return new_splits

#function to convert splits from list of sets format to strings
def get_split_name(split):
    split[0] = [int(x) for x in split[0]]
    split[0].sort()
    split[0] = [str(x) for x in split[0]]
    split[1] = [int(x) for x in split[1]]
    split[1].sort()
    split[1] = [str(x) for x in split[1]]
    split_name = ','.join(split[0])+'|'+','.join(split[1])
    split[0] = set(split[0])
    split[1] = set(split[1])
    return split_name

def is_compatible_splits(first, second):
    if first[0]&second[0]==set() or first[1]&second[0]==set() or first[0]&second[1]==set() or first[1]&second[1]==set():
        return True
    return False

def get_connection_graph_adjacency_list(new_splits, start_tree_vertex_set, new_leaves, split_names):
    connection_graph_adjacency_list = dict()
    for split_index in range(len(new_splits)-1):
        current_split = new_splits[split_index]
        current_split_name = get_split_name(current_split)
        other_splits = new_splits[split_index+1:]
        compatible_splits = []
        for other_split in other_splits:
            if is_compatible_splits(current_split, other_split):
                compatible_splits.append(get_split_name(other_split))
        connection_graph_adjacency_list[current_split_name] = compatible_splits
        split_names.append(current_split_name)
    current_split_name = get_split_name(new_splits[-1])
    connection_graph_adjacency_list[current_split_name] = []
    split_names.append(current_split_name)
    return connection_graph_adjacency_list

#returns a networkx Graph of our compatible splits
def graph(graph_dict):
    G = nx.Graph()
    for key in graph_dict:
        for value in graph_dict[key]:
            G.add_edge(key,value)
    return G
    
def max_indep_set(G):
    n = []
    for i in range(10000):
        g = nx.maximal_independent_set(G)
        k = len(g)
        n.append(k)
    return max(n)

def get_start_tree_and_new_leaves(input_filename):
    start_tree = []
    start_tree_vertex_set = []
    new_leaves = []
    with open (input_filename, 'r') as f:
        [start_tree_newick, new_leaves_string] = f.readlines()
        new_leaves = new_leaves_string[1:-1].split(',')
        start_tree_dendro = dendropy.Tree.get(
                data=start_tree_newick,
                schema="newick")
        for split in start_tree_dendro.encode_bipartitions():
            split_string = split.split_as_newick_string(start_tree_dendro.taxon_namespace)
            split_string = split_string.split('), (')
            if len(split_string)>1:
                first, second = split_string[0], split_string[1]
                first = first[2:]
                second = second[:-3]
                if len(first) > 1 and len(second)>1:
                    first = [x.strip() for x in first.split(',')]
                    second = [x.strip() for x in second.split(',')]
                    start_tree.append([set([str(x) for x in first]), set([str(x) for x in second])])
            else:
                start_tree_vertex_set = split_string[0][1:-2].split(',')
    return start_tree, start_tree_vertex_set, new_leaves


if __name__ == '__main__':
    input_filename = './start_tree.tre'
    output_filename = './graph.pdf'
    if len(sys.argv) > 2:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        print 'Using default input and output files. Please use python connection_graph.py <input_filename> <output_filename> to specify customize file names'
    print ('    | Reading start tree and new leaves from {}...'.format(input_filename))
    start_tree, start_tree_vertex_set, new_leaves = get_start_tree_and_new_leaves(input_filename)
    print ('    | Calculating connection graph...')
    new_splits = get_new_splits(start_tree_vertex_set, start_tree, new_leaves)
    split_names = []
    connection_graph_adjacency_list = get_connection_graph_adjacency_list(new_splits, start_tree_vertex_set, new_leaves, split_names)
    G = graph(connection_graph_adjacency_list)
    H = nx.Graph()
    H.add_nodes_from(connection_graph_adjacency_list.keys())
    H.add_edges_from(G.edges())
    graph_pos = nx.shell_layout(H , [split_names])
    nx.draw_networkx(H, graph_pos, node_size = 100, font_size = 10)
    print('    | The connection graph has {} number of nodes and {} number of edges'.format(G.number_of_nodes(), G.number_of_edges()))
    plt.savefig(output_filename)
    print('    | Save output image to {}'.format(output_filename))
    plt.show()