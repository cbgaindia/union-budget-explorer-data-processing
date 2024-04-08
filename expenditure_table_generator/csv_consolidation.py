import os
import math
import pandas as pd

DATA_FOLDER = os.path.abspath(os.path.join(__file__, '..', 'expenditure_data_output'))

def main():
    rows_for_final = []

    for file_name in os.listdir(DATA_FOLDER):

        file = os.path.join(
            DATA_FOLDER,
            file_name
        )

        df = pd.read_csv(file)
        df.dropna(how="all", axis=1, inplace=True)
        df.reset_index(inplace=True)

        major_head_mapping = {}

        rows_for_file = []

        for index, row in df.iterrows():

            if not math.isnan(row[1]):

                if row[1].is_integer():
                    major_head_mapping[int(row[1])] = row[2]

                    row[3] = "Total " + str(row[2])

                else:
                    row[2] = major_head_mapping[int(row[1])]

                row[0] = file_name[:-4]

                rows_for_file.append(row.to_list())

        rows_for_final.append(pd.DataFrame(rows_for_file))

    final_df = pd.concat(rows_for_final).reset_index(drop=True)

    final_df.to_csv(
        DATA_FOLDER + "/main.csv"
    )
    
    return

if __name__ == "__main__":
    main()


"""
TODO - For 0 let it be 0 and for empty add `...`
"""