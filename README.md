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

