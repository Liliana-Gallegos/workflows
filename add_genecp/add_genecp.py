'''
Add GENECP text in COM gaussian files.
Requires genecp.txt file with similar format.
Updated: May 7, 2022 - Liliana C. Gallegos
'''

import os
import numpy as np
import glob as gb
import argparse


def get_atoms(file):
    if file.find('.com') > -1:
        f = open(file, 'r')
        lines = f.readlines()
        # Find the unique atoms in com file
        for i in range(len(lines)):
            if lines[i].find('#') > -1: start = i+5

        atoms, coords = [], []
        for j in range(start,len(lines)):
            if len(lines[j].split()) > 1:
                atom = lines[j].split()[0]
                #print(lines[j].split(' '), len(lines[j].split(' ')))
                if atom.isalpha() == True and len(lines[j].split(' ')) > 6:
                    ##x, y, z = lines[j].split()[1], lines[j].split()[2], lines[j].split()[3]
                    atoms.append(atom); ##coords.append( [float(x), float(y), float(z)] )
            if lines[j].find('\n\n') > -1: break
        f.close()
        return atoms, coords

def main():
    parser = argparse.ArgumentParser(description='Add genecp text on Gaussian input files.')
    parser.add_argument('file', help="Select Gaussian input files to modify with genecp text.", nargs='*')
    parser.add_argument('--txt', default="False", help="Genecp text file with labeled atom for genecp as 'genecp==' ")
    args = parser.parse_args()

    files = args.file

    for file in files:
        atoms, coords = get_atoms(file)
        #print(atoms)
        com_file = open(file, 'r+')
        lines = com_file.readlines()

        if args.txt != "False":
            try:
                gentxt = args.txt
                txt = open(gentxt, 'r')
                txt_lines = txt.readlines()

                # Get genecp atom
                genecp = []
                for i, line in enumerate(txt_lines):

                    if line.find('==') > -1:
                        genecp_atom = str(line.split('==')[1]).split('\n')[0]
                        genecp_atom = genecp_atom.split(',')
                        #print(genecp_atom)
                        #if len(genecp_atom) > 1:
                        for atom in genecp_atom: genecp.append(atom)
                        #else: genecp.append(genecp_atom)
                    #print(genecp)
                    # All other atoms
                    other_atoms = [atom for atom in np.unique(atoms) if atom not in genecp ]

                    genecpTXT = []
                    if txt_lines[i].find('#') > -1:
                        com_file.writelines(' '.join(other_atoms)+' 0\n')
                        start = i+1
                        for j in range(start,len(txt_lines)):
                            genecpTXT.append(txt_lines[j])
                            if txt_lines[j].find('\n\n') > -1: break
                        com_file.writelines(genecpTXT)
                txt.close()
                com_file.close()

            except FileNotFoundError: print(' !!! Requires genecp.txt !!! ')
            print('Done!', len(files), 'file(s) have been changed')
        else: print('Missing genecp text file arugment (--txt)')

if __name__ == "__main__":
    main()
