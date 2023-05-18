import fsspec
import kerchunk.hdf
import zarr
import h5py

import xarray as xr
import dask
from dask.distributed import Client
import os
import sys
from azure.storage.blob import BlobServiceClient, ContainerClient
from tqdm import tqdm
import ujson
import multiprocessing

# Set the account name, container name, and file path
account_name = "dasdata"
container_name = "hdf5"
connection_string = os.environ['AZURE_CONSTR_dasdata']

fs2 = fsspec.filesystem('')  #local file system to save final jsons to

# Create a container client object
container_client = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container_name)

# Create an empty list to hold file names
file_names = []

# Loop through all blobs in the container and append their names to the list
for blob in container_client.list_blobs():
    file_names.append(blob.name)
    
def get_kerchunk_mapping(file):
   
    # Set the blob URL using the fsspec AzureBlobFileSystem
    url = f"az://{container_name}/{file}"
    openfile = fsspec.open(url, account_name=account_name)
    
    # Generate dictionary
    try:
        h5chunks = kerchunk.hdf.SingleHdf5ToZarr(openfile.open(), url)
    except:
        print(f'error with: {url}')
        return None

    outf = f'json_files/{file[:-3]}.json'
    with fs2.open(outf, 'wb') as f:
        f.write(ujson.dumps(h5chunks.translate()).encode())

# Create a multiprocessing pool with the number of available CPUs
pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

# Use tqdm to create a progress bar
with tqdm(total=len(file_names)) as pbar:
    # Define a callback function to update the progress bar
    def update_progress(_):
        pbar.update()

    # Apply the file processing function using imap and the progress callback
    for _ in pool.imap_unordered(get_kerchunk_mapping, file_names, chunksize=1):
        update_progress(_)

# Close the pool to release resources
pool.close()
pool.join()