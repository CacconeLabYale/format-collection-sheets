"""Execute logic to reformat and combine collection spreadsheets to single standardized form."""

import click
from click import echo as p

from utils import *



# In[4]:

village_id_map_path = "/home/gus/Dropbox/uganda_data/data_repos/field_data/locations/names/uganda_village_id_map.csv"


@click.command()
@click.option('--summary-sheet',"-s", type=click.Path(exists=True), required=True, multiple=True,
              help="Paths to an excel sheets of field disecction records. NOTE: may be used multiple times to supply more than one input sheet.")
@click.option('--output','-o', type=click.Path(), required=True,
              help="Path to where you want the combined/standardized output xls file.")
@click.option('--village-id-map', '-v', type=click.Path(exists=True), required=True,
              help="Path to a comma separated file containing the long village name to short village codes.")
def cli(summary_sheet, output, village_id_map):
    """Reformat and combine collection spreadsheets into a single standardized file."""


    village_id_map = get_village_id_map(village_id_map)

    df_all = []

    # load all xls files into a list of dataframes
    for f in summary_sheet:
        df_all.extend(load_xl_sheets(f).values())


    # run our recoder's on each dataframe
    for df in df_all:
        recode_sex(df)
        recode_species(df)
        recode_villages(df, village_id_map=village_id_map)
        recode_positives(df)
        recode_dead(df)
        recode_teneral(df)
        recode_date(df)
        add_infection_state_col(df)


    # combine all dataframes into a single big dataframe
    df_big = pd.concat(df_all)

    # write the new dataframe to xls file
    df_big.to_excel(output, index=False)
