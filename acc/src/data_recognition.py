"""
The module contains functions that are designed to automatically recognize
the type of data that was fed to the script:
    - raw data: 2 or 3 columns
    - cross matrix: raw (just numbers), with row and column descriptions,
      full (descriptions + row and column summaries)
    - binary cross matrix
    - images: '*.tif' + vector ('*.shp', '*....')
"""

from typing import Tuple, Dict
import pandas as pd
from pathlib import Path

# local imports
from acc.src.subcommands import from_raw, from_cross_full, from_cross
from acc.src.subcommands import from_cross_raw, from_binary, from_imgs
# ---


def is_data_raw(df: pd.DataFrame) -> Tuple[bool, dict]:
    tests = []
    meta = {'func': from_raw, 'data_type': 'data'}
    
    # raw data is 2 or 3 columns
    if df.shape[1] == 2 or df.shape[1] == 3:
        tests.append(True)
    else:
        tests.append(False)
    
    # checks if df has the expected column names
    if df.shape[1] == 2:
        columns = ['true', 'predict']
    # elif df.shape[1] == 3:
    else:
        columns = ['short', 'true', 'predicted']

    check_names = [True if name in list(df.columns)
                   else False for name in columns]

    tests.extend(check_names)
    check = all(tests)
    if not check:
        meta = None
    return check, meta
# --- 


def is_cross_full(df: pd.DataFrame) -> Tuple[bool, dict]:
    meta = {'func': from_cross_full, 'data_type': 'full'}
    cols_sum = df.iloc[:-1, 1:-1].sum(axis=0)
    rows_sum = df.iloc[:-1, 1:-1].sum(axis=1)
    check1 = all(df.iloc[-1, 1:-1] == cols_sum)
    check2 = all(df.iloc[:-1, -1] == rows_sum)

    check = all([check1, check2])
    if not check:
        meta = None
    return check, meta
# ---



def is_cross_raw(df: pd.DataFrame) -> Tuple[bool, dict]:
    meta = {'func': from_cross_raw, 'data_type': 'raw'}
    # checks if the first row contains numbers
    check1 = all(pd.to_numeric(df.iloc[0, :], errors='coerce').notna())
    check2 = all(pd.to_numeric(df.iloc[:, 0], errors='coerce').notna())
    check = all([check1, check2])
    if not check:
        meta=None
    return check, meta
# ---


def is_cross_matrix(df: pd.DataFrame) -> bool:
    # cross: matrix with numbers, row and column descriptions,
    # and without no summaries
    meta = {'func': from_cross, 'data_type': 'cross'}
    # checks if all columns are numbers 
    func = pd.api.types.is_numeric_dtype
    numeric = [func(df.iloc[:, i]) for i in (-2, -1)]
    check = all(numeric)
    if not check:
        meta=None
    return check, meta
# ---


def is_binary_matrix(df: pd.DataFrame) -> Tuple[bool, dict]:
    """Chceckin if df is binary cross matrix."""
    names = ['TP', 'TN', 'FP', 'FN']
    meta = {'func': from_binary, 'data_type': 'binary'}
    df = df.set_index(df.columns[0], drop=True)
    # column or row names are TP, TN, FP, FN
    # breakpoint()
    if len(df.columns) == len(names) and all(names == df.columns):
        # checks the matrix layout: horizontal or vertical
        # layout = 'vertical'
        check = True
        meta['reversed'] = True
    elif len(df.index) == len(names) and all(names == df.index):
        # layout = 'horizontal'
        check = True
    else:
        check = False
    
    if not check:
        meta=None
    return check, meta
# ---


def is_imgs(args):
    """Są 2 przypadki:
    1. args.path to jedna ścieżka do obrazu ('tif', 'tiff', ...) oznacza, żę
       wskazuje na wynik klasyfikacji. Wtedy w tym samym katalogu musi znajdować
       się plik z referencją, o takiej samej nazwie tylko z końcówką `ref` np.:
       - `cracow.tif` -> `cracow_ref.tif` lub `cracow_ref.shp` lub
         `cracow_ref.gpkg`  
    2. args.path to 2 ścieżki, wtedy pierwsza to referencja a druga to wynik
    klasyfikacji.

    """
    meta = {'func': from_imgs, 'data_type': 'imgs'}
    suffix = Path(args.path).suffix[1:]
    if suffix in ['tif', 'tiff', 'TIF', 'TIFF', 'shp', 'gpkg']:
        return True, meta
    return False, None
# ---
        

def remove_unnecessary_args(args): 
    if not args.save:
        delattr(args, 'save')

    if not args.zip:
        delattr(args, 'zip')
        delattr(args, 'zip_name')

    if not args.report:
        delattr(args, 'report')

    if args.data_type == 'imgs':
        delattr(args, 'sep')

    if not args.reversed:
        delattr(args, 'reversed')

    return args
# ---


def specify_data_type(args):
    """The function determines what type of data `args.path` points to. The
    data are either 'csv' files or '*.tif' and '*.shp' (or '*.gpkg') files.
    In the first step it checks if the data are images (image, vector).
    """
    # meta = {'func': None, 'data_type': None, 'layout': None}
    update_args = lambda args, mt: [setattr(args, k, v) for k, v in mt.items()]
    
    # check if it is_image()
    check, meta = is_imgs(args)
    if check:
        update_args(args, meta)
        return args

    # if the data is not an image:
    df = pd.read_csv(args.path, sep=args.sep, header=None, index_col=None)

    # is_cross_raw(): check if is it a matrix of numbers only
    check, meta = is_cross_raw(df)
    # breakpoint()
    if check:
        update_args(args, meta)
        return args

    # other functions checking 'is...' are called in the loop
    is_functions = [is_data_raw,
                    is_binary_matrix,
                    is_cross_full,
                    is_cross_matrix]
    df = pd.read_csv(args.path, sep=args.sep)

    for func in is_functions:
        check, meta = func(df)
        # breakpoint()
        if check:
            update_args(args, meta)
            return args
# ---


def recognize_data_type(args):
    """Main function to recognize data."""
    args = specify_data_type(args)
    args = remove_unnecessary_args(args)
    return args