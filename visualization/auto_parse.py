import os
import sys
import pandas as pd

raw_folder = "./data/results/"
parsed_folder = "./data/parsed-results/"
script_name = 'test-inference'  # const string, name of python script of inference


def parse_instance(instance_list):
    instance_dict = {}
    instance_dict["time_stamp"] = instance_list[0]
    instance_dict[instance_list[2]] = instance_list[1].replace(',', '')
    return instance_dict

def raw_to_csv(input_file, output_file):
    result_dict_list = []
    with open(input_file) as f:
        buf = f.readline()
        while buf:
            if 'not counted' in buf:
                buf = f.readline()
                continue
            instance_list = buf.split(',')
            # print(len(instance_list))
            if len(instance_list) == 8:     # 8 for parsing new results
                result_dict_list.append(parse_instance(instance_list))
            buf = f.readline()
            
    result_df = pd.DataFrame(result_dict_list)
    result_df.to_csv(output_file, index=False)

def path_validate(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def auto_parse():
    for folder in os.listdir(raw_folder):
        raw_round_folder_path = os.path.join(raw_folder, folder)
        if os.path.isdir(raw_round_folder_path):
            parsed_round_folder_path = os.path.join(parsed_folder, folder)
            path_validate(parsed_round_folder_path)
            for subfolder in os.listdir(raw_round_folder_path):
                raw_cat_folder_path = os.path.join(raw_round_folder_path, subfolder)
                if os.path.isdir(raw_cat_folder_path):
                    parsed_cat_folder_path = os.path.join(parsed_round_folder_path, subfolder)
                    path_validate(parsed_cat_folder_path)
                    for raw_file in os.listdir(raw_cat_folder_path):
                        raw_file_path = os.path.join(raw_cat_folder_path, raw_file)
                        if os.path.isfile(raw_file_path):
                            parsed_file_path = os.path.join(parsed_cat_folder_path, raw_file.replace(".txt", ".csv"))
                            print("Parsing: " + raw_file_path)
                            raw_to_csv(raw_file_path, parsed_file_path)

def auto_parse_single_inference():
    for model in os.listdir(raw_folder):       # model level
        if not os.path.isdir(os.path.join(raw_folder, model)):
            continue
        for category in os.listdir(os.path.join(raw_folder, model)):      # clean or poisoned
            if not os.path.isdir(os.path.join(raw_folder, model, category)):
                continue
            for input in os.listdir(os.path.join(raw_folder, model, category)):           # each input folder
                if not os.path.isdir(os.path.join(raw_folder, model, category, input, script_name)):
                    continue
                for raw_file in os.listdir(os.path.join(raw_folder, model, category, input, script_name)):      # each raw data file
                    if not raw_file.endswith(".txt"):
                        continue
                    raw_file_path = os.path.join(raw_folder, model, category, input, script_name, raw_file)
                    print(raw_file_path)
                    parsed_file_path = os.path.join(parsed_folder, model, category, input, raw_file.replace(".txt", ".csv"))
                    os.makedirs(os.path.join(parsed_folder, model, category, input), exist_ok=True)
                    print("Generating: " + parsed_file_path)
                    raw_to_csv(raw_file_path, parsed_file_path)


def main(argc, argv):
    path_validate(parsed_folder)
    auto_parse_single_inference()
    # auto_parse()

if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    argv = sys.argv
    argc = len(sys.argv)
    main(argc, argv)
