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
cd ucdavis-hpc-collection
```

### Step 2: Prepare the environment
```
