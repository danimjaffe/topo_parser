import networkx as nx
import argparse
import re
import os
from random import choice
import sys


def parse_topo(topofile):
    """
    Parse an Infiniband topology file "topofile" into list of all connections
    and writes parsed file to "topofile_parsed".
    """
    with open(topofile, 'r') as f:
        with open(topofile + "_parsed", 'w') as parsed_file:
            inblock = False  # Switch or Host (Channel Adapter) block
            for line in f:
                if line.startswith('Switch'):
                    inblock = True
                    guid = re.findall(r'\"(.*?)\"', line)[0]
                elif line.startswith('Ca'):
                    inblock = True
                    guid = re.findall(r'\"(.*?)\"', line)[0]
                elif len(line) == 0 or line.isspace():
                    inblock = False
                elif inblock:
                    destguid = re.findall(r'\"(.*?)\"', line)[0]
                    parsed_file.write("{} {}\n".format(guid, destguid))


def print_topo():
    """
    Print the parsed topology in order of connection
    """
    files = [f for f in os.listdir('.') if os.path.isfile(f) and "_parsed" in f]
    for f in files:
        with open(f, "r") as parsed:
            print("Printing parsed topology {}:".format(f))
            g = nx.DiGraph()
            for line in parsed:
                sl = line.split()
                g.add_edge(sl[0], sl[1])
            random_node = choice(list(g.nodes))
            bfs_layers = nx.bfs_layers(g, sources=random_node)
            for i, layer in enumerate(bfs_layers):
                print("Level {}:".format(i + 1))
                print(layer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Infiniband network topology discovery tool file parser')
    parser.add_argument('-f', help='parse topofile.topo')
    parser.add_argument('-p', help='print parsed topology',action='store_true')
    args = parser.parse_args()
    if not args.f and not args.p:
        parser.print_help()
        sys.exit(1)
    if args.f:
        parse_topo(args.f)
    if args.p:
        print_topo()


