import os
import sys
import pandas as pd

result_dict_list = []

def block_parser(block):
    block_dict = {}
    block_dict["time_stamp"] = block[0].split()[0]
    for instance in block:
        items = instance.split()
        if "<not counted>" in instance:
            block_dict[items[-1]] = ''
        else:
            block_dict[items[2]] = items[1].replace(',', '')
    
    result_dict_list.append(block_dict)

def raw_to_csv(input_file, output_file):
    with open(input_file) as f:
        buf = f.readline()

        while buf:
            block = []
            if 'msec' in buf:
                # task-clock, time of the period profiled
                block.append(buf)
                buf = f.readline()

                while 'msec' not in buf and buf:
                    block.append(buf)
                    buf = f.readline()
                    if "counts unit events" in buf:
                        buf = f.readline()

                block_parser(block)
            else:
                buf = f.readline()
    result_df = pd.DataFrame(result_dict_list)
    result_df.to_csv(output_file, index=False)

def main(argc, argv):
    assert argc == 3
    
    raw_to_csv(argv[1], argv[2])

if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    argv = sys.argv
    argc = len(sys.argv)
    main(argc, argv);