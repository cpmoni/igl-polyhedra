from dendropy.simulate import treesim
from dendropy.datamodel import treemodel
import dendropy
import numpy as np 
import os, sys
import os.path as osp

quartet_newick_template = '(({}, {}), ({}, {}));'

def get_simulated_input_tree():
    simulated_input_tree = treesim.birth_death_tree(birth_rate=1.0,
                             death_rate=0.9,
                             num_extant_tips=10,
                             repeat_until_success=True)
    simulated_input_tree.is_rooted = False
    simulated_input_tree.print_plot()
    return simulated_input_tree

def get_splits_from_tree(simulated_input_tree):
    bipartitions = simulated_input_tree.encode_bipartitions()
    splits = []
    for bipartition in bipartitions:
        if bipartition.is_trivial():
            continue
        bipartition = bipartition.split_as_newick_string(simulated_input_tree.taxon_namespace).split('), (')
        if len(bipartition) == 1:
            continue
        bipartition[0] = (bipartition[0][2:]).split(',')
        bipartition[1] = (bipartition[1][:-3]).split(',')
        splits.append(bipartition)
    return splits

def get_random_quartet_from_splits(splits, quartet_count):
    with open('./phylo.tre', 'w+') as file:
        for i in range(quartet_count):
            split_index = np.random.randint(0, len(splits))
            split = splits[split_index]
            split_left = np.random.choice(len(split[0]), 2, replace=False)
            split_right = np.random.choice(len(split[1]), 2, replace=False)
            quartet_newick  = quartet_newick_template.format(split[0][split_left[0]], split[0][split_left[1]], split[1][split_right[0]], split[1][split_right[1]])
            print(quartet_newick)
            file.write(quartet_newick)
            file.write('\n')
            quartet = dendropy.Tree.get(
                data=quartet_newick,
                schema="newick")
            quartet.print_plot()

def dendropy_sum_tree_reconstruction_on_quartets():
    simulated_input_tree = get_simulated_input_tree()
    splits = get_splits_from_tree(simulated_input_tree)
    get_random_quartet_from_splits(splits, 10)
    child = os.fork()
    if child == 0:
        if osp.exists('./phylo.consensus.sumtrees'):
            os.remove('./phylo.consensus.sumtrees')
        os.system('sumtrees.py -s consensus -o phylo.consensus.sumtrees -F newick -f 0.2 phylo.tre')
        sys.exit(0)
    os.waitpid(child, 0)
    reconstruct_tree_newick = 0
    with open('./phylo.consensus.sumtrees') as f:
        reconstruct_tree_newick = f.readlines()[0][:-1]
    reconstruct_tree = dendropy.Tree.get(data=reconstruct_tree_newick, schema='newick')
    reconstruct_tree.print_plot()

if __name__ == '__main__':
    dendropy_sum_tree_reconstruction_on_quartets()
