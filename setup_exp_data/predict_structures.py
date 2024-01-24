import os, shutil, sys
import pandas as pd
from colabfold.batch import get_queries, run
from colabfold.download import default_data_dir
from colabfold.utils import setup_logging
from pathlib import Path

# DO NOT EXECUTE THIS FILE. TODO: REWRITE PREDICT FUNCTION FOR LOCALCOLABFOLD

def prepare_alphafold_input(parent_dir):
    alphafold_input_dir = os.path.join(parent_dir, 'files', 'alphafold_input')
    if not os.path.exists(alphafold_input_dir):
        os.makedirs(alphafold_input_dir)
    pdb_ids = [f for f in os.listdir(os.path.join(parent_dir, 'files/protein/')) if len(f) == 4]
    for pdb_id in pdb_ids:
        fasta_path = os.path.join(parent_dir, 'files/protein/', pdb_id, f'EXP_{pdb_id}.fasta')
        fasta_destination = os.path.join(parent_dir, 'files', 'alphafold_input')
        shutil.copy(fasta_path, fasta_destination)
        return alphafold_input_dir

def alphafold_predict(input_dir, result_dir, n_recycles=3):
    """
    DO NOT CALL THIS FUNCTION: ONLY WORKS IN GOOGLE COLAB ENV.
    TODO: REPLACE WITH LOCALCOLABFOLD FUNCTION
    """
    # For some reason we need that to get pdbfixer to import
    if False and f"/usr/local/lib/python{python_version}/site-packages/" not in sys.path:
        sys.path.insert(0, f"/usr/local/lib/python{python_version}/site-packages/")

    if 'logging_setup' not in globals():
        setup_logging(Path(result_dir).joinpath("log.txt"))
        logging_setup = True

    queries, is_complex = get_queries(input_dir)
    run(queries=queries,
        result_dir=result_dir,
        use_templates=False,
        use_amber=False,
        msa_mode="MMseqs2 (UniRef+Environmental)",
        model_type="auto",
        num_models=2,
        num_recycles=n_recycles,
        model_order=[1, 2],
        is_complex=is_complex,
        data_dir=default_data_dir,
        keep_existing_results=True,
        rank_by="auto",
        pair_mode="unpaired+paired",
        stop_at_score=98,
        zip_results=True,
        user_agent="colabfold/google-colab-batch",)

parent_dir = os.path.expanduser('~/Desktop/Capstone Public/')
input_dir = prepare_alphafold_input()

recycles_trials = [5, 10, 15, 20]
for n_recycles in recycels_trials:
    result_dir = os.path.join(parent_dir, 'files', f'alphafold_output_{n_recycles}')
    alphafold_predict(input_dir, result_dir, n_recycles=n_recycles):
