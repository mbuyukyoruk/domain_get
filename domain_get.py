import argparse
import os
import sys
import subprocess
import re
import textwrap

try:
    from Bio import SeqIO
except:
    print("SeqIO module is not installed! Please install SeqIO and try again.")
    sys.exit()

try:
    from Bio.Seq import Seq
except:
    print("Seq module is not installed! Please install Seq and try again.")
    sys.exit()

try:
    import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

parser = argparse.ArgumentParser(prog='python domain_get.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\
# domain_get

Author: Murat Buyukyoruk

        domain_get help:

This script is developed to fetch range sequences of gene/CRISPR loci of interest by using the fasta file with provided position and strand information. 

SeqIO and Seq packages from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.

Syntax:

        python domain_get.py -i demo.fasta -o demo_gene_flanks.fasta -d flank_info_dataframe

Example Dataframe (tab separated excel file is required):

        Accession       Domain  Start   Stop
        NZ_CP006019.1   Domain1 1875203 1877050
        CP000472.1      Domain2 123     975

domain_get dependencies:

Bio module, SeqIO and Seq available in this package     refer to https://biopython.org/wiki/Download

tqdm                                                    refer to https://pypi.org/project/tqdm/

Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a fasta file. FASTA file requires headers starting with accession number. (i.e. >NZ_CP006019 [fullname])

	-o/--output		Output file	    Specify a output file name that should contain fetched domains.

	-d/--data		Dataframe		Specify a list of domains. Each accession, domain, position info should be included in a new line (i.e. generated with Excel spreadsheet). 
Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename',
                    help='Specify a fastafile to fetch regions from.\n')
parser.add_argument('-o', '--output', required=True, dest='out',
                    help='Specify a output file name.\n')
parser.add_argument('-d', '--data', required=True, dest='data',
                    help='Specify a list of domains.\n')

results = parser.parse_args()
filename = results.filename
out = results.out
data = results.data

os.system("> " + out)

seq_id_list = []
seq_list = []
seq_description_list = []

proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length)) as pbar:
    pbar.set_description('Reading...')
    for record in SeqIO.parse(filename, "fasta"):
        pbar.update()
        seq_id_list.append(record.id)
        seq_list.append(record.seq)
        seq_description_list.append(record.description)

proc = subprocess.Popen("wc -l < " + data, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length+1), desc='Fetching...') as pbar:
    with open(data, 'r') as file:
        for line in file:
            pbar.update()
            f = open(out, 'a')
            sys.stdout = f
            try:
                acc = line.split("\t")[0]
                flank = line.split("\t")[1]
                start = line.split("\t")[2]
                stop = line.split("\t")[3].split("\n")[0]
                ind = seq_id_list.index(acc)
                seq_ind = seq_list[ind]
                seq = Seq(str(seq_ind[int(start):int(stop)]))
                print(
                    ">" + seq_id_list[ind] + ' | ' + flank + ' | ' + start + '-' + stop + ' | ' + seq_description_list[
                        ind])
                print(re.sub("(.{60})", "\\1\n", str(seq), 0, re.DOTALL))
            except:
                continue
