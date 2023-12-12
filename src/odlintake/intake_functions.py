'''
collection of functions that open various cloud based datasets for ODL-UW

John Ragland
March 2023
'''
import xarray as xr
import os
import pandas as pd

def open_ooi_lfhydrophones():
    '''
    requires envionment variable AZURE_SAS_TOKEN_ooidata
    To create the environment variable add the following line to your .bashrc (or .zshrc) file
    export AZURE_SAS_TOKEN_ooidata='<your token here>'

    After restarting your terminal, you can check that the environment variable is set by typing
    echo $AZURE_SAS_TOKEN_ooidata


    '''
    # TODO figure out how to handle controlled acces
    
    account_key = os.environ['AZURE_KEY_ooidata']
    storage_options={'account_name': 'ooidata', 'account_key': account_key}
    ds = xr.open_zarr('abfs://lfhydrophonezarr/ooi_lfhydrophones.zarr', storage_options=storage_options)
    return ds

def open_ooi_DAS_SouthTx():
    '''
    requires environment variables
    '''
    # open zarr store
    storage_options = {'account_name':'dasdata', 'account_key':os.environ['AZURE_KEY_dasdata']}
    ds = xr.open_zarr('abfs://zarr/ooi_South_Tx.zarr/ooi_South_Tx.zarr', storage_options=storage_options)
    return ds

def open_ooi_DAS_SouthTx_RawData(geo_fn = '/datadrive/DAS/south_DAS_latlondepth.txt'):
    ds = open_ooi_DAS_SouthTx()
    geo = pd.read_csv(geo_fn)
    geo['distance'] = geo['index']*2.0419046878814697/1000

    ds_slice = ds.isel({'distance':slice(942, 47382)})
    ds = ds_slice.assign_coords({'distance':geo['distance'].values})

    return ds, geo