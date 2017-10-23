# BHV Connection Graph

## Installation instructions:  

First install git, then clone our repository with 
```bash 
git clone https://github.com/cpmoni/igl-polyhedra.git
``` 

This package requires some dependencies: 
* cycler version 0.10.0
* decorator version 4.1.2
* DendroPy version 4.3.0
* functools32 version 3.2.3.post2
* matplotlib version 2.0.2
* networkx version 1.11
* numpy version 1.13.1
* pyparsing version 2.2.0
* python-dateutil version 2.6.1
* pytz version 2017.2
* six version 1.10.0
* subprocess32 version 3.2.7`

To automatically install the package dependencies listed above, install pip and run: 
```bash
pip install requirements.txt
```

## Usage instructions: 

```bash
python connection_graph.py <input_filename> <output_filename>
```
The input file should contain the start tree in Newick format in the first line, and the list of new leaves in the second line in parenthesis: `(10, 11, 12)`. Please use numbers as the labels of the leaves in the start tree and the new leaves. The default input file is "start_tree.tre".

The program will display the connection graph and save it to `<output_filename>`. It also prints out the number of nodes and edges in the graph.

## Contact

If you have any questions feel free to contact us at redavid2@illinois.edu.
