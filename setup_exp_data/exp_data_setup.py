import os, requests, time
import pandas as pd
import numpy as np
from Bio.PDB import *

def load_gene_list(parent_dir):
    """
    Returns datasheet as a DataFrame (PROVIDE GENE LIST AS A .CSV WITH A COLUMN FOR 'PDB ID' IN 'gene_list_parent_dir')
    """
    gene_list_parent_dir = os.path.join(parent_dir, 'files/')
    gene_list_paths = [f for f in os.listdir(gene_list_parent_dir) if f.endswith('.csv')]
    gene_list_path = os.path.join(gene_list_parent_dir, gene_list_paths[0])
    if os.path.exists(gene_list_path):
        gene_list = pd.read_csv(gene_list_path)
        gene_list = gene_list[gene_list['PDB ID'].str.len() <= 4] # filter pdb ids that are > 4
        return gene_list
    else:
        print('No gene list uploaded. Please load into "gene_list_parent_dir" and try again')

def setup_protein_folders(parent_dir, gene_list):
    protein_folder_paths = [os.path.join(parent_dir, 'files/protein', pdb_id) for pdb_id in gene_list['PDB ID'] if len(pdb_id) == 4]
    for protein_folder in protein_folder_paths:
        os.makedirs(protein_folder)
    return protein_folder_paths

def download_exp_pdb(parent_dir, pdb_id):
    wait_time = sum(np.random.random(2)) + .2
    time.sleep(wait_time)
    protein_folder = os.path.join(parent_dir, 'files/protein', pdb_id)
    response = requests.get(f"https://files.rcsb.org/download/{pdb_id}.pdb")
    if response.status_code == 200:
        pdb_path = os.path.join(protein_folder, f"EXP_{pdb_id}.pdb")
        with open(pdb_path, 'wb') as f: 
            f.write(response.content)
            print(f"{pdb_id} downloaded successfully ({pdb_path})")
            return pdb_path
    else:
        print(f'PDB ID {pdb_id} failed to download')

def save_fasta(parent_dir, pdb_id):
    fasta_path = os.path.join(parent_dir, 'files/protein', pdb_id, f'EXP_{pdb_id}.fasta')
    pdb_path = pdb_path = os.path.join(parent_dir, 'files/protein', pdb_id, f'EXP_{pdb_id}.pdb')
    # Using biopython (Maddie, can we replace this with the code you wrote to extract sequence?)
    parser = PDBParser()
    structure = parser.get_structure(pdb_id, pdb_path)
    ppb = PPBuilder()

    for pp in ppb.build_peptides(structure):
        # write .fasta file from sequence
        with open(fasta_path, 'w') as f:
            f.write(">{}\n{}".format(pdb_id, pp.get_sequence()))


parent_dir = os.path.expanduser('~/Desktop/Capstone Public/')
gene_list = load_gene_list(parent_dir)
protein_folder_paths = setup_protein_folders(parent_dir, gene_list)
for pdb_id in list(gene_list['PDB ID']):
    pdb_path = download_exp_pdb(parent_dir, pdb_id)
    fasta_path = save_fasta(parent_dir, pdb_id)

