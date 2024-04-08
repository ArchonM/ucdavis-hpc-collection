import os
import sys
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

parsed_folder = "/data/parsed-results/"
plots_folder = "/data/plots/"

colors = {'clean-example-data': 'green', 'poisoned-example-data': 'red'}


def plot_file(input_file, output_file):
    df = pd.read_csv(input_file)
    x, y = df.columns
    plot = df.plot(x=x, y=y, title=input_file, kind='line').get_figure()
    plot.savefig(output_file)
    fig = plt.gcf()
    plt.close(fig)
    
def plot_file_comparison(input_file1, input_file2, output_file):
    cat1 = input_file1.split("/")[-2]
    cat2 = input_file2.split("/")[-2]
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)
    x1, y1 = df1.columns
    x2, y2 = df2.columns
    plot = df1.plot(x=x1, y=y1, title=input_file1, kind='line')
    plot = df2.plot(x=x2, y=y2, title=input_file2, kind='line', ax=plot)
    plot.legend([cat1,cat2])
    plot.get_figure().savefig(output_file)
    fig = plt.gcf()
    plt.close(fig)

def plot_folder(parsed_folder_path, plots_folder_path):
    for file in os.listdir(parsed_folder_path):
        if os.stat(os.path.join(parsed_folder_path, file)).st_size <= 1:
            continue
        parsed_file_path = os.path.join(parsed_folder_path, file)
        if os.path.isfile(parsed_file_path):
            plots_file_path = os.path.join(plots_folder_path, file.replace(".csv", ".png"))
            print("Plotting: " + parsed_file_path)
            plot_file(parsed_file_path, plots_file_path)

def plot_folder_comparison(parsed_folder_path1, parsed_folder_path2, plots_folder_path):
    for file in os.listdir(parsed_folder_path1):
        if os.stat(os.path.join(parsed_folder_path1, file)).st_size <= 1:
            continue
        parsed_file_path1 = os.path.join(parsed_folder_path1, file)
        parsed_file_path2 = os.path.join(parsed_folder_path2, file)
        if os.path.isfile(parsed_file_path1) and os.path.isfile(parsed_file_path2):
            plots_file_path = os.path.join(plots_folder_path, file.replace(".csv", ".png"))
            print("Plotting: " + parsed_file_path1 + " and " + parsed_file_path2)
            plot_file_comparison(parsed_file_path1, parsed_file_path2, plots_file_path)

def auto_plot():
    for folder in os.listdir(parsed_folder):
        parsed_round_folder_path = os.path.join(parsed_folder, folder)
        if os.path.isdir(parsed_round_folder_path):
            plots_round_folder_path = os.path.join(plots_folder, folder)
            path_validate(plots_round_folder_path)
            cat_folder_list = os.listdir(parsed_round_folder_path)
            if len(cat_folder_list) == 1:
                plot_folder(os.path.join(parsed_round_folder_path, cat_folder_list[0]), plots_round_folder_path)
            elif len(cat_folder_list) == 2:
                plot_folder_comparison(os.path.join(parsed_round_folder_path, cat_folder_list[0]), os.path.join(parsed_round_folder_path, cat_folder_list[1]), plots_round_folder_path)
                

def path_validate(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def plot_all_comparison(path):
    csv_file_list = os.listdir('/data/parsed-results/r8-id0011/')    # a list of file to process
    for model in os.listdir(path):                              # model level
        plot_path = os.path.join(plots_folder, model)
        os.makedirs(plot_path, exist_ok=True)
        for event in csv_file_list:
            plt.figure()
            for category in os.listdir(os.path.join(path, model)):  # clean or poisoned
                for input_id in os.listdir(os.path.join(path, model, category)):
                    csv_file_path = os.path.join(path, model, category, input_id, event)
                    if not os.path.exists(csv_file_path):
                        continue
                    print('Processing ' + csv_file_path + '...')
                    df = pd.read_csv(csv_file_path)
                    x, y = df.columns
                    x = np.array(df[x])
                    y = np.array(df[y])
                    y_processed = []
                    for i in range(len(y)):
                        if not isinstance(y[i], str) or y[i].isnumeric():
                            y_processed.append(float(y[i]))
                        else:
                            if i == 0:
                                y_processed.append(float(0))
                            else:
                                y_processed.append(y_processed[i-1])
                    y = np.array(y_processed)
                    # print(x,y)  
                    plt.plot(x, y, color=colors[category],alpha=0.3)
            plt.legend()
            plt.savefig(os.path.join(plot_path, event[:-4]+'.png'))



def main(argc, argv):
    # auto_plot()
    plot_all_comparison(parsed_folder)



if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    argv = sys.argv
    argc = len(sys.argv)
    main(argc, argv)