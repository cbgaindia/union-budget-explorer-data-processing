import os
import re
import numpy as np
import pandas as pd

FILE_PATH = os.path.abspath(os.path.join(__file__, '..', 'expenditure_data'))

OUTPUT_FILE_PATH = os.path.abspath(os.path.join(__file__, '..', 'expenditure_data_output'))

INPUT_FILE_EXT = ".xls"

def delete_rows_above_header(input_df):
    del_rows_index_list = []

    header_found = False

    for row_index in range(len(input_df)):
        row_item = input_df.iloc[row_index].tolist()

        row_item = [format(i).strip() for i in row_item]

        if "Actual" in "".join(row_item):
            header_found = True
        elif not header_found or not "".join(row_item).strip():
            del_rows_index_list.append(row_index)

    input_df = input_df.drop(input_df.index[del_rows_index_list])

    input_df = input_df.reset_index(drop=True)

    return input_df


def fix_particular_columns(input_df):
    for row_index in range(len(input_df)):
        particulars_raw = (input_df.iloc[row_index][0:7])

        particulars_str = [str(i) for i in particulars_raw]

        particular_slug = " ".join(particulars_str)

        particular_number = re.findall(r"[0-9]+[.0-9+]*", particular_slug)

        if particular_number:
            particular_number = particular_number[0]
        else:
            particular_number = ""

        total_field = re.findall(r"^Grand Total$|^Total$", particular_slug)

        if total_field:
            total_field = total_field[0]
        else:
            total_field = ""

        particular_text = particular_slug.strip()

        if particular_number:
            particular_text = particular_text.split(str(particular_number))[-1].strip()

        if total_field:
            particular_text = particular_text.split(total_field)[0].strip()

        input_df.iloc[row_index][0] = particular_number

        input_df.iloc[row_index][1] = particular_text

        if total_field:
            input_df.iloc[row_index][7] = total_field

    cols = [2,3,4,5,6]

    input_df.drop(input_df.columns[cols],axis=1,inplace=True)

    input_df.columns = [i for i in range(input_df.shape[1])]

    return input_df


def fix_headers(input_df):
    input_df.iloc[0][0] = "Index"
    input_df.iloc[0][1] = "Particulars"
    input_df.iloc[0][2] = "Type"
    input_df.iloc[0][4] = input_df.iloc[0][3]
    input_df.iloc[0][5] = input_df.iloc[0][3]
    input_df.iloc[0][7] = input_df.iloc[0][6]
    input_df.iloc[0][8] = input_df.iloc[0][6]
    input_df.iloc[0][10] = input_df.iloc[0][9]
    input_df.iloc[0][11] = input_df.iloc[0][9]
    input_df.iloc[0][13] = input_df.iloc[0][12]
    input_df.iloc[0][14] = input_df.iloc[0][12]


    row_0 = input_df.iloc[0].tolist()

    row_1 = input_df.iloc[1].tolist()

    for col_index in range(len(row_0)):
        input_df.iloc[0][col_index] = (str(row_0[col_index]) + " " + str(row_1[col_index])).strip()

    input_df = input_df.drop(input_df.index[1])

    input_df = input_df.reset_index(drop=True)

    return input_df

if __name__ == "__main__":
    for file_name in os.listdir(FILE_PATH):
        department_name = os.path.basename(file_name).lower().split(INPUT_FILE_EXT)[0]

        file_name = os.path.join(
            FILE_PATH,
            file_name
        )
    
        input_df = pd.read_excel(file_name, header=None)

        input_df_for_dept_name = input_df

        department_name = input_df_for_dept_name.iloc[3:4, 1:2].to_string().split('\\n')[2]

        input_df = input_df.replace(np.nan, '', regex=True)

        input_df = delete_rows_above_header(input_df)

        input_df = fix_particular_columns(input_df)

        input_df = fix_headers(input_df)

        input_df.to_csv(
            os.path.join(OUTPUT_FILE_PATH + '/{}.csv'.format(department_name)),
            encoding='utf-8',
            index=False,
            header=False
        )