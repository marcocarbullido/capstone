import os, shutil, sys
import pandas as pd
from colabfold.batch import get_queries, run
from colabfold.download import default_data_dir
from colabfold.utils import setup_logging
from pathlib import Path

# DO NOT EXECUTE THIS FILE. TODO: REWRITE PREDICT FUNCTION FOR LOCALCOLABFOLD
# GO TO https://colab.research.google.com/github/konstin/ColabFold/blob/main/batch/AlphaFold2_batch.ipynb#scrollTo=iccGdbe_Pmt9
# ^ THIS CONTAINS THE CORRECT CODE ^

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

    #@markdown --- (from https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/batch/AlphaFold2_batch.ipynb)
    #@markdown ### Advanced settings
    msa_mode = "MMseqs2 (UniRef+Environmental)" #@param ["MMseqs2 (UniRef+Environmental)", "MMseqs2 (UniRef only)","single_sequence","custom"]
    num_models = 2
    num_recycles = n_recycles
    stop_at_score = 100 #@param {type:"string"}
    #@markdown - early stop computing models once score > threshold (avg. plddt for "structures" and ptmscore for "complexes")
    use_custom_msa = False
    num_relax = 0 #@param [0, 1, 5] {type:"raw"}
    use_amber = num_relax > 0
    relax_max_iterations = 200 #@param [0,200,2000] {type:"raw"}
    use_templates = False #@param {type:"boolean"}
    do_not_overwrite_results = True #@param {type:"boolean"}
    zip_results = True #@param {type:"boolean"}

    #@title Install dependencies (from https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/batch/AlphaFold2_batch.ipynb)
    
    #@title Install dependencies
    %%bash -s $use_amber $use_templates $python_version
    
    set -e
    
    USE_AMBER=$1
    USE_TEMPLATES=$2
    PYTHON_VERSION=$3
    
    if [ ! -f COLABFOLD_READY ]; then
      # install dependencies
      # We have to use "--no-warn-conflicts" because colab already has a lot preinstalled with requirements different to ours
      pip install -q --no-warn-conflicts "colabfold[alphafold-minus-jax] @ git+https://github.com/sokrypton/ColabFold"
      ln -s /usr/local/lib/python3.*/dist-packages/colabfold colabfold
      ln -s /usr/local/lib/python3.*/dist-packages/alphafold alphafold
      touch COLABFOLD_READY
    fi
    
    # Download params (~1min)
    python -m colabfold.download
    
    # setup conda
    if [ ${USE_AMBER} == "True" ] || [ ${USE_TEMPLATES} == "True" ]; then
      if [ ! -f CONDA_READY ]; then
        wget -qnc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        bash Miniconda3-latest-Linux-x86_64.sh -bfp /usr/local 2>&1 1>/dev/null
        rm Miniconda3-latest-Linux-x86_64.sh
        conda config --set auto_update_conda false
        touch CONDA_READY
      fi
    fi
    # setup template search
    if [ ${USE_TEMPLATES} == "True" ] && [ ! -f HH_READY ]; then
      conda install -y -q -c conda-forge -c bioconda kalign2=2.04 hhsuite=3.3.0 python="${PYTHON_VERSION}" 2>&1 1>/dev/null
      touch HH_READY
    fi
    # setup openmm for amber refinement
    if [ ${USE_AMBER} == "True" ] && [ ! -f AMBER_READY ]; then
      conda install -y -q -c conda-forge openmm=7.7.0 python="${PYTHON_VERSION}" pdbfixer 2>&1 1>/dev/null
      touch AMBER_READY
    fi


    # number of models to use

    # For some reason we need that to get pdbfixer to import
    if use_amber and f"/usr/local/lib/python{python_version}/site-packages/" not in sys.path:
        sys.path.insert(0, f"/usr/local/lib/python{python_version}/site-packages/")
    
    setup_logging(Path(result_dir).joinpath("log.txt"))
    
    queries, is_complex = get_queries(input_dir)
    run(
        queries=queries,
        result_dir=result_dir,
        use_templates=use_templates,
        num_relax=num_relax,
        relax_max_iterations=relax_max_iterations,
        msa_mode=msa_mode,
        model_type="auto",
        num_models=num_models,
        num_recycles=n_recycles,
        model_order=[1, 2],
        is_complex=is_complex,
        data_dir=default_data_dir,
        keep_existing_results=do_not_overwrite_results,
        rank_by="auto",
        pair_mode="unpaired+paired",
        stop_at_score=stop_at_score,
        zip_results=zip_results,
        user_agent="colabfold/google-colab-batch",
    )

parent_dir = os.path.expanduser('~/Desktop/Capstone Public/')
input_dir = prepare_alphafold_input()

recycles_trials = [5, 10, 15, 20]
for n_recycles in recycels_trials:
    result_dir = os.path.join(parent_dir, 'files', f'alphafold_output_{n_recycles}')
    alphafold_predict(input_dir, result_dir, n_recycles=n_recycles):
