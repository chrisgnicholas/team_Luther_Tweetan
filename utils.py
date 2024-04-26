from eep153_tools.sheets import read_sheets
import pandas as pd


def get_clean_sheet(key, sheet=None):
    """Get a dataframe from a Google sheet.

    Parameters:
        key: (str) A google sheets key
        sheet: (str) The sheet name to get

    Returns:
        df: (pd.DataFrame) A dataframe of the spreadsheet"""

    df = read_sheets(key, sheet=sheet)
    df.columns = [c.strip() for c in df.columns.tolist()]
    df = df.loc[:, ~df.columns.duplicated(keep="first")]
    df = df.drop([col for col in df.columns if col.startswith("Unnamed")],
                 axis=1)
    df = df.loc[~df.index.duplicated(), :]

    return df


def change_prices(p0, p, j):
    """
    Change price of jth good to p0, holding other prices fixed.
    """
    p = p.copy()
    p.loc[j] = p0
    return p


def increase_nutrient_content(fct, food_items, nutrient="Iron",
                              increase_percent=30):
    new_fct = fct.to_dict()
    for food_item in food_items:
        if food_item in fct.index:
            print(
                f"Before update: {food_item} iron content =\
                    {fct.loc[food_item, nutrient]}"
            )
            new_fct[nutrient][food_item] = fct.loc[food_item][nutrient] * (
                1 + (increase_percent / 100)
            )
            print(
                f"After update: {food_item} iron content =\
                {new_fct[nutrient][food_item]}"
            )
        else:
            print(f"{food_item} not found in FCT.")
    return pd.DataFrame(new_fct)
