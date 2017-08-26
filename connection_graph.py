import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain
from itertools import combinations

#Just used so we don't have to write out the trivial splits
def get_trivia_splits(vertices):
    triv_splits=[]
    x = set(vertices)
    for vertice in x:
        left = set(vertice)
        right = x.difference(vertice)
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
    newleaves(0, tree, pow_set, new_leaf_set , new_splits)
    newleaves(1, trivia_splits, pow_set, new_leaf_set , new_splits)
    newleaves(2, empty, pow_set, new_leaf_set , new_splits)
    return new_splits

#function to convert splits from list of sets format to strings
def get_split_name(split):
    return ','.join(split[0])+'|'+','.join(split[1])

def is_compatible_splits(first, second):
    if first[0]&second[0]==set() or first[1]&second[0]==set() or first[0]&second[1]==set() or first[1]&second[1]==set():
        return True
    return False

def get_connection_graph_adjacency_list(new_splits, start_tree_vertex_set, new_leaves):
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
    return connection_graph_adjacency_list

#returns a networkx Graph of our compatible splits
def graph(graph_dict):
    G = nx.Graph()
    for key in graph_dict:
        for value in graph_dict[key]:
            G.add_edge(key,value)
    return G
    

#Not a great way for finding independent sets of maximum size

#nx.maximal_independent_set(G) returns a random maximal independent set (maximal not maximum) of grap G,
#so I just run it a bunch of times and get the one of largest size

# If we know max size then we can print some out using the if and print command that is commented out
def max_indep_set(G):
    n = []
    for i in range(10000):
        g = nx.maximal_independent_set(G)
        k = len(g)
#        if k >= 23:
#            print g
        n.append(k)
    return max(n)


if __name__ == '__main__':
    # TODO: implement newick tree format parser
    #vertices is a list of leaves from the start tree
    start_tree_vertex_set = ['1','2','3','4','5','6','7','8','9']
    # start tree in newick format: (((((1, 2), 3), 4),  ((6, 7), 5)), ((9, 10), 8))
    start_tree =[
    [set(['1','2']), set(['3','4','5','6','7','8','9'])],
    [set(['1','2','3']), set(['4','5','6','7','8','9'])], 
    [set(['1','2','3','4']), set(['5','6','7','8','9'])],
    [set(['6','7']), set(['1','2','3','4','5','8','9'])],
    [set(['5','6','7']), set(['1','2','3','4','8','9'])],
    [set(['8','9']), set(['1','2','3','4','5','6','7'])],
    ]
    new_leaves = ['10', '11']
    new_splits = get_new_splits(start_tree_vertex_set, start_tree, new_leaves)
    connection_graph_adjacency_list = get_connection_graph_adjacency_list(new_splits, start_tree_vertex_set, new_leaves)
    G = graph(connection_graph_adjacency_list)
    nx.draw_networkx(G)
    print(G.number_of_nodes(), G.number_of_edges())
    plt.show()