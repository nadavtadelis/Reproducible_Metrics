import pandas as pd
import numpy as np

def make_indicators(df, names):
    r'''
    Make indicator columns in dataframe df of whether existing columns are 
    equal to given values.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to be modified.
    names : dict
        Dictionary containing:
            - Keys: Desired indicator column names
            - Values: Two item tuple containing:
                - Original dataframe column
                - Value to compare to column

    Returns
    -------
    void : 
        Dataframe df is modified in place.
    '''
    for k,v in names.items():
        df[k] = 1*(df[v[0]] == v[1])

def two_way(df, col0, col1):
    r'''
    Make two-way frequency table of two columns in a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing columns to be compared.
    col0 : String
        Name of first column to compare.
    col1 : String
        Name of second column to compare.

    Returns
    -------
    df : pandas.DataFrame 
        Dataframe of two-way frequency table.
    '''
    index = np.sort(df[col0].unique())
    columns = np.sort(df[col1].unique())
    tab = pd.DataFrame(index=index, columns=columns)
    for i in index:
        for j in columns:
            count = df[(df[col0] == i) & (df[col1] == j)].shape[0]
            tab.loc[i,j] = count
    return tab
