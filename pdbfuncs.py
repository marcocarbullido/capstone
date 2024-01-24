#written by: Maddie Bonanno 
#last updated: 1/23/2024


import pandas as pd
from collections import OrderedDict

# reads and returns the text held in a pdb file
def print_pdb(path):
  with open(path, 'r') as f:
    lines = f.read()
  return lines

#DONT USE THIS ONE: use the other function
def pdb_dontuse(path, bfactor:bool):
  with open(path, 'r') as f:
    pdb_lines = f.readlines()
  if bfactor:
     column_headers = [
    "ATOM", "serial", "atom_name", "residue_name",
    "chainID", "residue_number", "X", "Y", "Z", "occupancy",
    "B-factor", "disterror"
    ]
  else:
    column_headers = [
    "ATOM", "serial", "atom_name", "residue_name",
    "chainID", "residue_number", "X", "Y", "Z", "occupancy",
    "B-factor", "element"
    ]
  struct_info = pd.DataFrame(columns=column_headers)
  #print(struct_info)
  for line in pdb_lines:
    #print(line)
    if 'ATOM' in line[0:6]:
      content = line.split()
      #print(content)
      atom = content[0].strip()
      serial = content[1].strip()
      atomname = content[2].strip()
      residname = content[3].strip()
      chainid = content[4].strip()
      residuenum = content[5].strip()
      x = content[6].strip()
      y = content[7].strip()
      z = content[8].strip()
      occ = content[9].strip()
      bfact = content[10].strip()
      elem = content[11].strip()

      temp = pd.DataFrame([[atom, serial, atomname, residname, chainid, residuenum, x, y, z, occ, bfact, elem]], columns=column_headers)
      struct_info = pd.concat([struct_info, temp])

  struct_info_indexed = struct_info.reset_index()
  struct_info_indexed = struct_info_indexed.drop(columns='index')

  return struct_info_indexed



#this function can be used when the experimental pdb files have over 1000 nucleotides
#[this ensures that if the formatting of the pdb changes, the info can still be accessed and turned into a df]
def extract_info_from_pdb(path):
  with open(path, 'r') as f:
    lines = f.readlines()
  if 'bfact' in path:
    column_headers = [
    "ATOM", "serial", "atom_name", "residue_name",
    "chainID", "residue_number", "X", "Y", "Z", "occupancy",
    "B-factor", "disterror"
    ]
  else:
    column_headers = [
    "ATOM", "serial", "atom_name", "residue_name",
    "chainID", "residue_number", "X", "Y", "Z", "occupancy",
    "B-factor", "element"
    ]
  struct_info = pd.DataFrame(columns=column_headers)
  for line in lines:
    if 'ATOM' in line[0:6]:
      #print(line)
      content = line.split()

      atom = content[0].strip()
      serial = int(content[1].strip())
      atomname = content[2].strip()
      residname = content[3].strip()
      chainid = content[4].strip()
      #residuenum = ''
      if len(chainid) != 1:
        residuenum = chainid[1:].strip()
        chainid = chainid[0].strip()
        x = content[5].strip()
        y = content[6].strip()
        z = content[7].strip()
        edit = content[8]
        occ = edit[:4].strip()
        try:
          bfact = float(edit[4:].strip())
        except:
          bfact = 0
        elem = content[9].strip()
      else:
        residuenum = content[5].strip()
        x = content[6].strip()
        y = content[7].strip()
        z = content[8].strip()
        edit = content[9]
        if edit != '1.00':
          occ = edit[:4].strip()
          try:
            bfact = float(edit[4:].strip())
          except:
            bfact = 0
          elem = content[10].strip()
        else:
          occ = edit
          try:
            bfact = float(content[10])
          except:
            bfact = 0
          elem = content[11]


      temp = pd.DataFrame([[atom, serial, atomname, residname, chainid, residuenum, x, y, z, occ, bfact, elem]], columns=column_headers)
      struct_info = pd.concat([struct_info, temp])
  
  struct_info_indexed = struct_info.reset_index()
  struct_info_indexed = struct_info_indexed.drop(columns='index')

  return struct_info_indexed



#takes in a pandas dataframe and returns a dataframe with only the nitrogen bfactors
def obtain_only_nitrogen_bfactors(dataframe):
  nitrogen = dataframe[dataframe['atom_name'] == 'N']
  chainnum = nitrogen['chainID'].unique()
  if len(chainnum) != 1:
    nitrogen = dataframe[(dataframe['atom_name'] == 'N') & (dataframe['chainID'] == 'A')]
  nitrogen = nitrogen.reset_index()
  return nitrogen


def bfactors_marco_style(pbd_path):
  dataframe_full = extract_info_from_pdb(pbd_path)
  #print(dataframe_full)
  dataframe_nitrogen = obtain_only_nitrogen_bfactors(dataframe_full)
  #print(dataframe_nitrogen)
  bfactors = dataframe_nitrogen['B-factor'].to_dict(into=OrderedDict)
  residues = dataframe_nitrogen['serial'].to_dict(into=OrderedDict)
  
  return bfactors, residues
  
  
  
  