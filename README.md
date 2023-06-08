# ucdavis-hpc-collection

This repository serves as an automated toolchain for hpc events collection on intel based computer platform, built by UC Davis ASEEC-CHEST lab.

## What is this repository for?

This project aims to help researchers to collect hardware event information for further analysis. The toolchain is built on top of [Intel® VTune™ Amplifier](https://software.intel.com/en-us/intel-vtune-amplifier-xe) and [Intel® Performance Counter Monitor](https://software.intel.com/en-us/articles/intel-performance-counter-monitor-a-better-way-to-measure-cpu-utilization). The toolchain is designed to be easy to use and easy to extend.

## Before start

To use this tool, you will first need to make sure the device you are using have a updated perf tool. You can check the version of perf by typing:
```perf --version```
If the version is lower than 4.4, you will need to update your perf tool.
Moreover, this tool is only tested on Thinkpad t480s with Intel Core i5-8350U CPU. The system tested is Ubuntu 20.04 focal and the kernel is x86_64 Linux 5.15.0-72-generic. If you are using other devices, you may need to modify the code to make it work.

## How to use

### Step 1: Clone the repository

```bash
git clone git@github.com:ArchonM/ucdavis-hpc-collection.git
```

### Step 2: Prepare the environment

The output path is not specified in this repo so you will need to create a folder named output in the root directory of this repo. You can do this by typing:

```bash
cd ucdavis-hpc-collection
mkdir output
```

To use this tool, you do not need to move the target executable file into this directory. The profiler is designed to be able to find the executable file in any directory. Moreover, the output files will be stored in the output directory in a folder that has the same name of your executable file without extension. For example, if your executable is /path/to/executable/test.exec, the output files will be stored in /path/to/ucdavis-hpc-collection/output/test. In this path, raw data will be stored in multiples files, depending on the what event is collected.

### Step 3: Run the profiler

First you will need to enter the data_collection path and first collect a list of what events your CPU supports by typing:

```bash
cd data_collection
python3 get_supported_events.py
```

This will generate a file named 'events_list.txt' in the data_collection directory and tell you how many events are available to be collected on your CPU. By default the main profiler will collect all events once each time of execution. If you want to collect a specific event or a specific set of events, you can modify the 'events_list.txt' generated. Then you are ready to start the main profiler. To start the main profiler, you can type:

```bash
./auto_data_collection.sh /path/to/executable/test.exec <profiling period in ms>
```

Since this toolchain is built of the top of perf, the highest profiling frequency supported is 1000Hz, which means the minimun value you can set for the profiling period is 1. As mentioned above, after the profiling process is completed, the resultant files with raw data will be stored in the output directory.

### Step 4: Data processing

For the convenience of users, we provides 2 useful python scripts to help you process the raw data: auto_process.py and pattern_extractor.py. The detailed instruction and explanation of these 2 scripts can be found in docs/instruction.pdf. Basically, you can use auto_process.py to transfer the raw data to a csv file which is much more human friendly. The pattern_extractor.py will be more complicated. You will need to modify the target executable file by adding some sleep time to extract the highlighted operations. To use auto_process.py, you can type:

```bash
cd data_processing
python3 auto_process.py /path/to/output/raw_data_file /path/to/output/csv_file
```

When using pattern_extractor.py, since a pattern could repeat multiple times, each time the pattern will be captured and saved in a seperate csv file. Thus the output csv file would have a numerical mark at the end of the filename to help you locate the specific operation. To use pattern_extractor.py, you can type:

```bash
python3 pattern_extractor.py /path/to/output/raw_data_file /path/to/output/csv_file
```
