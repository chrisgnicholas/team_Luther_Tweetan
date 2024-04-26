from eep153_tools.sheets import read_sheets
import pandas as pd
import wbdata


def get_clean_sheet(key: str, sheet: str = None):
    """Get a dataframe from a Google sheet.

    Parameters:
        key: (str) A google sheets key
        sheet: (str) The sheet name to get

    Returns:
        df: (pd.DataFrame) A dataframe of the spreadsheet"""

    df = read_sheets(key, sheet=sheet)
    df.columns = [c.strip() for c in df.columns.tolist()]
    df = df.loc[:, ~df.columns.duplicated(keep="first")]
    df = df.drop([col for col in df.columns if col.startswith("Unnamed")], axis=1)
    df = df.loc[~df.index.duplicated(), :]

    return df


def change_prices(p0: float, p: float, j: str):
    """
    Change price of jth good to p0, holding other prices fixed.

    Parameters:
        p0 (float):
    """
    p = p.copy()
    p.loc[j] = p0
    return p


def increase_nutrient_content(fct, food_items, nutrient="Iron", increase_percent=30):
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


#### helpers for population pyramids ########

countries = wbdata.get_countries()
country_dict = {}

# Iterate over the WBSearchResult object, Create Dictionary.
# This dictionary is necessary so that we know which country
# names map to which 3-letter country codes.
for country in countries:
    country_code = country["id"]
    country_name = country["name"]
    # Add to the dictionary the country name.
    country_dict[country_name] = country_code


def int_to_str(num):
    """Convert the integer to the proper format."""
    if 0 <= num < 10:
        # Add a '0' prefix if it is a single digit.
        return f"0{num}"
    else:
        # Convert to string directly if it is a two-digit number.
        return str(num)


def population_range(year, sex, age_range, place):
    """This function will return the population for a certain age range."""
    sex_codes = {"people": "", "females": "FE", "males": "MA"}
    sex_used = sex_codes[sex]

    # Getting the lower and upper bounds for date into correct format.
    lower, upper = int_to_str(age_range[0]), int_to_str(age_range[1])
    range_string = lower + upper

    # Getting the country code via the name.
    country_code = country_dict.get(place)

    df = wbdata.get_dataframe(
        {"SP.POP." + range_string + "." + sex_used: "Population"},
        country={country_code: place},
    ).squeeze()
    df = df.to_frame().reset_index()
    population_total = int(df[df["date"] == str(year)]["Population"])
    return population_total


def dict_helper(year, sex, age_range, place):
    """This will expand our function to include every age specified possible."""
    if len(age_range) == 1:
        age_range = [age_range[0], age_range[0]]
    elif age_range[1] < age_range[0]:
        raise ValueError(
            f"Please ensure that the second value in the range is greater than the first."
        )

    minimum_age, maximum_age = age_range
    possible_minimums = [i for i in range(0, 76, 5)]
    possible_maximums = [i for i in range(4, 80, 5)]

    my_dict = {}
    for age in range(minimum_age, maximum_age + 1):
        """Find the index in the possible ranges that includes the current age."""
        range_index = next(
            (
                i
                for i, min_val in enumerate(possible_minimums)
                if min_val <= age and age <= possible_maximums[i]
            ),
            None,
        )
        if range_index is not None:
            popl_value = (
                population_range(
                    year,
                    sex,
                    [possible_minimums[range_index], possible_maximums[range_index]],
                    place,
                )
                // 5
            )
            my_dict[age] = popl_value
        else:
            raise ValueError(f"No age range available for age {age}")

    return my_dict


def population(year, sex, age_range, place):
    """This function ties everything together, returning population for given age ranges.
    During usage, please utilize the following format:
    Arguments to Use:
    Year (int): the specified year, works from 1960-2021.
    Sex (string): Anything from all, people, p, P, People, All, Everyone, female, females, f, Female,
                Females, F, FE, male, males, m, Male, Males, M, MA works.
    Age Range (list with length 2, 2 integers): A list of the age bounds.
    Place (string): A string of the specified location.
    Example Usage: population(1975, "People", [5, 7], "Rwanda")
    """
    if place not in country_dict:
        valid_regions = ", ".join(country_dict.keys())
        raise ValueError(
            f"The region '{place}' is not valid. Please choose from the following regions: {valid_regions}"
        )
    if sex in ["all", "people", "p", "P", "People", "All", "Everyone"]:
        female_dict = dict_helper(year, "females", age_range, place)
        male_dict = dict_helper(year, "males", age_range, place)
        return sum(female_dict.values()) + sum(male_dict.values())
    elif sex in ["female", "females", "f", "Female", "Females", "F", "FE"]:
        female_dict = dict_helper(year, "females", age_range, place)
        return sum(female_dict.values())
    elif sex in ["male", "males", "m", "Male", "Males", "M", "MA"]:
        male_dict = dict_helper(year, "males", age_range, place)
        return sum(male_dict.values())


def create_population_dataframe(regions, years, age_range):
    """Creates the population DataFrame based on the regions, years, and age ranges wanted.
    During usage, please utilize the following format:
    Arguments to Use:
    regions (list of strings, any length): the specified year, works from 1960-2021.
    years (list of ints, any length): Anything from all, people, p, P, People, All, Everyone, female, females, f, Female,
                Females, F, FE, male, males, m, Male, Males, M, MA works.
    age_range (list of two ints): the age bounds specified, second must be greater than the first.
    """
    data = []

    # Check if age_range is a single age or a range.
    if len(age_range) == 1:
        full_age_range = [age_range[0]]
    else:
        full_age_range = list(range(age_range[0], age_range[1] + 1))

    # Iterate over each region, year, and age."
    for region in regions:
        for year in years:
            row = {"Region": region, "Year": year}
            for age in full_age_range:
                male_population = population(year, "male", [age], region)
                female_population = population(year, "female", [age], region)
                total_population = male_population + female_population

                row[f"Male Population Age {age}"] = male_population
                row[f"Female Population Age {age}"] = female_population
                row[f"Total Population Age {age}"] = total_population

            data.append(row)

    # Create a DataFrame.
    df = pd.DataFrame(data)

    # Set the index.
    df.set_index(["Region", "Year"], inplace=True)

    return df


import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

py.init_notebook_mode(connected=True)


def plot_population_pyramid(df, year):
    """Plots the population pyramid given a working DataFrame from the
    population dataframe function and a year."""

    # Filter the DataFrame for the given year and reset index.
    year_df = df[df.index.get_level_values("Year") == year].reset_index()

    # Aggregate data if there are multiple regions.
    year_df = year_df.groupby("Year").sum()

    # Extract age groups from column names.
    age_groups = sorted(
        set(int(col.split()[-1]) for col in year_df.columns if col.startswith("Male"))
    )

    # Prepare data for plotting
    male_counts = [
        -year_df[f"Male Population Age {age}"].values[0] for age in age_groups
    ]  # Negative for left side
    female_counts = [
        year_df[f"Female Population Age {age}"].values[0] for age in age_groups
    ]

    # Create the plot.
    layout = go.Layout(
        barmode="overlay",
        title=f"Population Pyramid for {year}",
        yaxis=go.layout.YAxis(title="Age"),
        xaxis=go.layout.XAxis(title="Number"),
    )

    bins = [
        go.Bar(
            x=male_counts,
            y=age_groups,
            orientation="h",
            name="Men",
            marker=dict(color="purple"),
            hoverinfo="skip",
        ),
        go.Bar(
            x=female_counts,
            y=age_groups,
            orientation="h",
            name="Women",
            marker=dict(color="pink"),
            hoverinfo="skip",
        ),
    ]

    py.iplot(dict(data=bins, layout=layout))