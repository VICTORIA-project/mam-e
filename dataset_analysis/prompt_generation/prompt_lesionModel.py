#Add repo path to the system path
from pathlib import Path
import os, sys
repo_path= Path.cwd().resolve()
while '.gitignore' not in os.listdir(repo_path): # while not in the root of the repo
    repo_path = repo_path.parent #go up one level
sys.path.insert(0,str(repo_path)) if str(repo_path) not in sys.path else None

from datasets_local.metadata import subset_csv
import pandas as pd


# HP
folder_name = 'lesions_breast40k'
reference_file = 'metadata_Hologic.csv'

files_folder = repo_path / 'data/images' / f'{folder_name}'
reference_folder = repo_path / 'data/metadata/' / f'{reference_file}'
metadata_path = subset_csv(files_folder, reference_folder) # get metadata csv of the subset

# read csv file
metadata = pd.read_csv(metadata_path, header=0)

# get df with name id and text info of interest
metadata = metadata[['image_id', 'view_position', 'marks']]
# add exension to the end of the image_id
metadata['image_id'] = metadata['image_id'].astype(str) + '.png'
# change image_id to file_name
metadata = metadata.rename(columns={'image_id': 'file_name'})
# lesion status. add column with text according to the marks value
#metadata['lesion_status'] = metadata['marks'].apply(lambda x: 'with lesion' if x == True else 'healthy')

# prompt column
metadata['prompt'] = 'magnification of a lesion'
# drop all columns that are not prompt or image_id
metadata = metadata[['file_name', 'prompt']]
# transform to json
metadata = metadata.to_json(orient='records', lines=True)
# use same folder as files folder
json_path = files_folder / 'metadata.jsonl'
# save json
with open(json_path, 'w') as f:
    f.write(metadata)