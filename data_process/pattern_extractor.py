import os
import sys
import pandas as pd

def is_row_blank(df_series, columns_to_check):
    for column in columns_to_check:
        if not pd.isna(df_series[column]):
            return False
    return True

def pattern_extract(input_file, output_file_prefix):
    input_df = pd.read_csv(input_file)
    
    events_profiled = input_df.columns.to_list()

    wait_for_pattern = False
    pattern_starts = False

    blank_row_counter = 0
    
    pattern = []
    pattern_counter = 0

    for index, row in input_df.iterrows():
        if not is_row_blank(row, events_profiled[2:]):
            if wait_for_pattern:
                pattern.append(row.tolist())
                pattern_starts = True
            blank_row_counter = 0
        else:
            if pattern_starts:
                if pattern_counter%2 == 0:
                    pattern_df = pd.DataFrame(pattern, columns=events_profiled)
                    pattern_df.to_csv(output_file_prefix+str(pattern_counter)+'.csv', index=False)
                pattern_counter += 1
                pattern = []
                wait_for_pattern = False
                pattern_starts = False

            blank_row_counter += 1
        
        if blank_row_counter > 30:
            wait_for_pattern = True

def test(input_file, output_file_prefix):
    input_df = pd.read_csv(input_file)
    print(input_df.iloc[304])
    df_series = input_df.iloc[304]
    print(pd.isna(df_series["instructions"]))


def main(argc, argv):
    assert argc == 3
    pattern_extract(argv[1], argv[2])

if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    argv = sys.argv
    argc = len(sys.argv)
    main(argc, argv)