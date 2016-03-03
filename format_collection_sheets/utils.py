
"""Provide functions for formatting collection spreadsheets to standardized forms."""
import csv
import itertools
import os
import re
import datetime as dt

import pandas as pd
import numpy as np

import munch



def date_is_between(test_date, start, end):

    try:
        return start <= test_date <= end
    except TypeError as exc:
        if "can't compare datetime" in exc.message:
            return False
        else:
            raise


# In[6]:

def get_village_id_map(village_id_map_path):
    """
    Generates and returns a `dict` mapping the long-form village names to the letter codes.
    Letter codes map back to themselves to ensure a one way mapping.
    Enforces both be all UPPERcase to allow case insensitivity as long as
    the map is used like: `map[text.upper()]`.
    :return: `dict`
    """

    village_id_map = {}

    with open(village_id_map_path, 'rb') as csv_file:
        village_ids = csv.reader(csv_file, delimiter=',')
        for pair in village_ids:
            village_id_map[unicode(pair[0].upper())] = unicode(pair[0].upper())
            village_id_map[unicode(pair[1].upper())] = unicode(pair[0].upper())

    return village_id_map


# In[10]:

def load_xl_sheets(xl_path):
    dfs = munch.Munch()

    xls = pd.ExcelFile(xl_path)

    workbook_name = os.path.basename(xl_path)

    for sheet in xls.sheet_names:
        if sheet.upper().startswith("DISSECT"):
            worksheet_df = xls.parse(sheetname=sheet,
                                header=0,
                                skiprows=None, skip_footer=0,
                                index_col=None, parse_cols=None,
                                parse_dates=False, date_parser=None,
                                na_values=['NA'],
                                thousands=None,
                                convert_float=False)

            worksheet_df['workbook'] = workbook_name
            worksheet_df['worksheet'] = sheet

            dfs[sheet] = worksheet_df

    return dfs


# In[11]:

def recode_villages(df, village_id_map):
    map_func = lambda x: village_id_map[x.upper()]

    new_codes = df.Village.apply(map_func)
    df.Village = new_codes


# In[12]:

def recode_dead(df):
    def recode_func(x):
        # this is treated as an unknown case
        if pd.isnull(x):
            return x

        x = unicode(x)

        # True means DEAD
        # False means LIVE or NOT-DEAD
        # None means unknown

        try:
            # deal with Live type cases
            if x.upper().startswith('L'):
                return False


            if x.startswith('0'):
                return False


            # deal with Dead type cases
            if x.upper().startswith('D'):
                return True


            if x.startswith('1'):
                return True


            # deal with unknown type cases
            if x.upper().startswith('UN'):
                return None
        except AttributeError:
            return x

        msg = "The value {x} was not expected and this function must be corrected to continue.".format(x=x)
        raise ValueError(msg)

    new_dead = df.Dead.apply(recode_func)
    df.Dead = new_dead

##########################################

def recode_teneral(df):
    def recode_func(x):

        # this is treated as an unknown case
        if pd.isnull(x):
            return x

        x = unicode(x)

        # True means teneral
        # False means NOT-teneral
        # None means unknown

        try:
            # deal with NOT-teneral type cases
            if x.upper().startswith('N'):
                return False

            if x.startswith('0'):
                return False

            # deal with Teneral type cases
            if x.upper().startswith('T'):
                return True

            if x.startswith('1'):
                return True


            # Deal with unknown type cases
            if x.upper().startswith('UN'):
                return x
        except AttributeError:
            return x

        msg = "The value {x} was not expected and this function must be corrected to continue.".format(x=x)
        raise ValueError(msg)


    new_teneral = df.Teneral.apply(recode_func)
    df.Teneral = new_teneral

##########################################

def recode_positives(df):
    def recode_func(x):
        # this is treated as an unknown case
        if pd.isnull(x):
            return x

        y = unicode(x)

        # deal with Unknown type cases
        if y.upper().startswith('UN'):
            return None

        if y.upper().startswith('DEAD'):
            return None


        # deal with Positive type cases
        if y.startswith('1'):
            return True


        if y.upper().startswith('TRUE'):
            return True

        if y.upper().startswith('P'):
            return True

        if y.upper().startswith('Y'):
            return True


        # deal with Negative type cases
        if y.upper().startswith('NO'):
            return False

        if y.upper().startswith('FALSE'):
            return False


        if y.startswith('0'):
            return False


        msg = "The value {x} was not expected and this function must be corrected to continue.".format(x=x)
        raise ValueError(msg)


    new_prob = df.prob.apply(recode_func)
    df.prob = new_prob

    new_midgut = df.midgut.apply(recode_func)
    df.midgut = new_midgut

    new_sal_gland = df.sal_gland.apply(recode_func)
    df.sal_gland = new_sal_gland

##########################################

def recode_species(df):

    recode_func = lambda x: ''.join(x.split('.')).capitalize()

    new_Species = df.Species.apply(recode_func)
    df.Species = new_Species

##########################################

def recode_sex(df):

    recode_func = lambda x: x.upper()

    new_Sex = df.Sex.apply(recode_func)
    df.Sex = new_Sex

##########################################

date_delim = re.compile('[\./-]')

def cast_unicode_as_date(x):
    if not isinstance(x, unicode):
        return x

    parts = date_delim.split(x)

    if len(parts) != 3:
        return x

    if len(parts[0]) != 4:
        return x

    return dt.datetime(int(parts[0]), int(parts[1]), int(parts[2]))

def recode_date(df):
    new_date = df.Date.apply(cast_unicode_as_date)
    df.Date = new_date



# In[13]:

def aggregate_column_from_df_list(df_list, col_name):
    agg_data = []
    for df in df_list:
        agg_data.extend(list(df[col_name]))


    return agg_data


# ### Functions that add new columns

# In[14]:

def add_infection_state_col(df):
    df['infection_state'] = df[['prob','midgut','sal_gland']].any(skipna=True,axis=1)
