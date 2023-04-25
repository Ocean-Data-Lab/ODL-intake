'''
collection of functions that open various cloud based datasets for ODL-UW

John Ragland
March 2023
'''
import xarray as xr
import os


def open_ooi_lfhydrophones():
    '''
    requires envionment variables
    '''
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