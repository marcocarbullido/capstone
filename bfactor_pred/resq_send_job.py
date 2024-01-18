# TODO: Create a text file for user parameters (email):
#   - Filename: `user_params.txt`

# TODO: Use user parameters and process PDB files in capstone/struct_pred/localcolabfold/input_fasta:
#   - Read email from `user_params.txt`.
#   - Dynamically fetch and process PDB files from `root/input_files/` directory, reading into payload

# TODO: Send out and retrieve job results download URL:
#   - Using requests, send to https://seq2fun.dcmb.med.umich.edu/ResQ/resq.cgi.

import requests, re

url = "https://seq2fun.dcmb.med.umich.edu/ResQ/resq.cgi"

# Read pdb file
protein_name = 'AF-5SZQ'
with open(f'/capstone/struct_pred/input_files/{protein_name}/{protein_name}.pdb', 'r') as f:
    pdb_data = f.read()

payload = {
    'file1': pdb_data,  # Paste your pdb data here
    'REPLY-E-MAIL': 'myemail@gmail.com',  # Provide your email here
    'TARGET-NAME': protein_name  # provide the protein name here
}

response = requests.post(url, data=payload)

match = re.search(r'url=(.*)">', response.text)
if match:
    results_url = match.group(1)
    print('Your results will be available at:', results_url)
else:
    print('Results URL not found in the server response.')
