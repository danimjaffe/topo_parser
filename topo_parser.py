import networkx as nx
import argparse
import re
import os
from random import choice
import sys


class Topo_parser:
    def __init__(self, topofiles):
        if topofiles:
            self.topofiles = topofiles
        else:
            self.topofiles = [f.replace("_parsed", "") for f in os.listdir('.') if os.path.isfile(f) and "_parsed" in f]

    def parse_topo(self):
        """
        Parse an Infiniband topology file "topofile" into list of all connections
        and writes parsed file to "topofile_parsed".
        """
        for topofile in self.topofiles:  # extended functionality to receive more than one topofile
            with open(topofile, 'r') as f:
                with open(topofile + "_parsed", 'w') as parsed_file:
                    inblock = False  # Switch or Host block
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

    def print_topo(self):
        """
        Print the parsed topology in order of connection
        """
        for f in self.topofiles:
            with open(f + "_parsed", "r") as parsed:
                print("Printing parsed topology {}:".format(f))
                g = nx.DiGraph()  # create graph of connections
                for line in parsed:
                    sl = line.split()
                    g.add_edge(sl[0], sl[1])
                random_node = choice(list(g.nodes))  # select random node to start traversal from
                bfs_layers = nx.bfs_layers(g, sources=random_node)  # get generator of bfs layers
                for i, layer in enumerate(bfs_layers):
                    print("Level {}:".format(i + 1))
                    print(layer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Infiniband network topology discovery tool file parser')
    parser.add_argument('-f', help='parse topofile.topo', nargs="*")
    parser.add_argument('-p', help='print parsed topology', action='store_true')
    args = parser.parse_args()
    if not args.f and not args.p:  # if neither -f flag and -p appear
        parser.print_help()
        sys.exit(1)
    topo_parser = Topo_parser(args.f)
    if args.f:  # case -f flag
        topo_parser.parse_topo()
    if args.p:  # case -p flag
        topo_parser.print_topo()
