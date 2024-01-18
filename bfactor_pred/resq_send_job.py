# TODO: Create a text file for user parameters (email):
#   - Filename: `user_params.txt`

# TODO: Use user parameters and process PDB files in capstone/struct_pred/localcolabfold/input_fasta:
#   - Read email from `user_params.txt`.
#   - Dynamically fetch and process PDB files from `root/input_files/` directory, reading into payload

# TODO: Send out and retrieve job results download URL:
#   - Using requests, send to https://seq2fun.dcmb.med.umich.edu/ResQ/resq.cgi.
