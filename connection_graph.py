import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain
from itertools import combinations

#Just used so we don't have to write out the trivial splits
def trivial_splits(vertices):
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
def newsplits(vertices, tree, new_leaves):
    triv_splits = trivial_splits(vertices)
    empty = [[set(), set(vertices)]]
    new_leaves_set=set(new_leaves)
    pow_set = list(powerset(new_leaves_set))
    new_splits=[]
    newleaves(0, tree, pow_set, new_leaves_set, new_splits)
    newleaves(1, triv_splits, pow_set, new_leaves_set, new_splits)
    newleaves(2, empty, pow_set, new_leaves_set, new_splits)
    return new_splits

#function to convert splits from list of sets format to strings
def to_string(split,leaves):
    node = str()
    for leaf in leaves:
        if leaf in split[0]:
            node = node+leaf
    node = node+'|'
    for leaf in leaves:
        if leaf in split[1]:
            node = node+leaf
    return(node)

#returns a dictionary where keys are splits and values are splits compatible to the key
#There's a problem when one of the leaf names is more than one character, for example '10' so I suggest using letters
def graphdict(new_splits, vertices, new_leaves):
    graph_dict = dict()
    leaves = vertices+new_leaves
    for key in new_splits:
        compatible = []
        for value in new_splits:
            if key != value:
                if key[0]&value[0]==set() or key[1]&value[0]==set() or key[0]&value[1]==set() or key[1]&value[1]==set():
                    compatible.append(value)
        k = to_string(key,leaves)
        v = []
        for value in compatible:
            node = to_string(value,leaves)
            v.append(node)
        graph_dict[k] = v
    return graph_dict

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

#vertices is a list of leaves from the start tree
vertices = ['1','2','3','4','5']

#tree takes split inputs for the shape of the start tree

#It is a list of lists where the elements are a list of 2 elements where the 1st entry is the left side of a split
#and the 2nd entry is the right side of the split

#Ex: the split AB|CDE should be a [set(['A','B']), set(['C','D','E'])]
tree =[[set(['1','2']), set(['3','4','5'])],[set(['1','2','3']), set(['4','5'])]]

#new_leaves is a list that takes in name of the leaves we want to add as its elements
new_leaves = ['6']

new_splits = newsplits(vertices, tree, new_leaves)
new_splits

graph_dict = graphdict(new_splits, vertices, new_leaves)
graph_dict

G = graph(graph_dict)
nx.draw_networkx(G)