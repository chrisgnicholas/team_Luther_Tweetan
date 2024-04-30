import csv

hholds = {}

# headers are:
# i,t,m, F 00-03,F 04-08,F 09-13,F 14-18,F 19-30,F 31-50,F 51+,M 00-03,M 04-08,M 09-13,M 14-18,M 19-30,M 31-50,M 51+
#
# attempt to look for 10 similar households
#


expenditures_lookup = {}
increased_expenditures = []

hh_matrix = [[{} for _ in range(20)] for _ in range(20)]


def get_kids(hh):
    infants = float(hh["F 00-03"]) + float(hh["M 00-03"])
    young_kids = float(hh["F 04-08"]) + float(hh["M 04-08"])

    # the 'check string' allows us to quickly find another household with the
    # same charactaristics for non-children. The intent here is to
    # to match up households and compare expenses, and households
    # with + or minus an infant or young child
    check_string = "-".join(
        [
            hh["F 09-13"],
            hh["F 14-18"],
            hh["F 19-30"],
            hh["F 31-50"],
            hh["F 51+"],
            hh["M 00-03"],
            hh["M 04-08"],
            hh["M 09-13"],
            hh["M 14-18"],
            hh["M 19-30"],
            hh["M 31-50"],
            hh["M 51+"],
        ]
    )

    return round(infants), round(young_kids), check_string


with open("expenditures.csv") as xcsv:
    xreader = csv.DictReader(xcsv)
    for row in xreader:
        these_expenditures = (
            expenditures_lookup[row["i"]] if row["i"] in expenditures_lookup else []
        )
        these_expenditures.append(row)
        expenditures_lookup[row["i"]] = these_expenditures

# build up a matrix of households by number of infants, young_kids, and expenditures
with open("hh.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        infants, young_kids, check_string = get_kids(row)
        matrix_entry = (row["i"], row["t"], check_string)
        if infants > 0 or young_kids > 0:
            # here we create a matrix of similar households
            # tbd - actually use this matrix to compare similar households
            hh_matrix[infants][young_kids][check_string] = matrix_entry

            # now look up expenditures
            if row["i"] in expenditures_lookup:
                this_household_expenditures = expenditures_lookup[row["i"]]

                if this_household_expenditures is not None:
                    # this is a week's expenditures; add $1/kid = 3807 Ugandan shillings
                    for expense in this_household_expenditures:
                        index_cols = ["i", "t", "m"]
                        total_exp = 0.0
                        for col in expense.keys():
                            if col not in index_cols:
                                item_cost = expense[col]
                                if len(item_cost) > 0:
                                    total_exp += float(expense[col])

                        new_expense = total_exp + 3807 * (infants + young_kids)
                        percent_increase = new_expense / total_exp
                        increased_expenditures.append(percent_increase)


# now get the average increase
def get_mean_increase():
    total_all_increases = 0.0
    for increase in increased_expenditures:
        total_all_increases += increase

    mean_increase = ((total_all_increases / len(increased_expenditures)) - 1) * 100
    return mean_increase
