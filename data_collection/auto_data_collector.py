# Requirements:
# 1. profile period
# 2. hardware events to be profiled (list or single?)
# 3. output path
# 4. executable path (python interpreter, by various env)
# 5. target python script path
# 6. parameters for target python script
# Usage: python auto_data_collector.py [options]
# Before use: create output folder in './..'
import os
import sys
import argparse


def init():
    global output_path
    global interpreter_path
    global target_script_path
    global target_script_args
    global profile_period
    global events

    output_path = args.output_path
    interpreter_path = args.interpreter
    target_script_path = args.target_script
    target_script_args = args.args
    profile_period = args.profile_period
    events = args.events if isinstance(args.events, list) else args.events.split(',')
    
    target_script_name = os.path.basename(target_script_path).split('.')[0]
    output_path_tmp = os.path.join(output_path, target_script_name)
    profile_count = 0
    while os.path.exists(output_path_tmp):
        output_path_tmp = os.path.join(output_path, target_script_name + '_' + str(profile_count))
        profile_count += 1
    output_path = output_path_tmp
    print(output_path)
    os.makedirs(output_path, exist_ok=True)


def read_events(events_path):
    with open(events_path, 'r') as f:
        events = f.readlines()
    events = [event.strip() for event in events]
    return events


def arg_valid_check():
    if not os.path.exists(interpreter_path):
        print('Error: interpreter path not exist')
        return False
    if not os.path.exists(target_script_path):
        print('Error: target script path not exist')
        return False
    if not os.path.exists(output_path):
        print('Error: output path not exist')
        return False
    return True


def main():
    for event in events:
        os.system('sudo perf stat -e ' + event + ' -o ' + os.path.join(output_path, event + '.txt') + ' -I ' + str(profile_period) + ' -x , ' + interpreter_path + ' ' + target_script_path + ' ' + target_script_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='auto_data_collector.py',
        description='Auto data collector')
    parser.add_argument('-p', '--profile_period', type=int, default=10, help='profile period')
    parser.add_argument('-e', '--events', type=str, default=read_events('./events_list.txt'), help='hardware events to be profiled')
    parser.add_argument('-o', '--output_path', type=str, default='./output', help='output path')
    parser.add_argument('-i', '--interpreter', type=str, default=sys.executable, help='python interpreter')
    parser.add_argument('-t', '--target_script', type=str, default='.', help='target python script path', required=True)
    parser.add_argument('-a', '--args', type=str, default='', help='parameters for target python script')
    args = parser.parse_args()
    init()
    main()