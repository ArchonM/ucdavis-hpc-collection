import subprocess
import os

def shell_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return process.stdout.read().decode('utf-8')

def create_raw_events_list():
    shell_command('perf list > raw_events_list.txt')

def parse_raw_events_list():
    event_list = []
    input_file = open('raw_events_list.txt', 'r')
    with open('events_list.txt', 'w') as output_file:
        for line in input_file:
            if ('[Hardware event]' in line) or ('[Software event]' in line) or ('[Tool event]' in line) or ('[Hardware cache event]' in line):
                tmp_event = ''
                if 'OR' in line:
                    tmp_event = line.split(' OR')[0]
                    tmp_event = tmp_event.replace(' ', '')
                else:
                    tmp_event = line.split('  ')[1]
                event_list.append(tmp_event)
    return event_list
                
def create_events_list():
    create_raw_events_list()
    event_list = parse_raw_events_list()
    print('Found ' + str(len(event_list)) + ' events')
    with open('events_list.txt', 'w') as output_file:
        for event in event_list:
            output_file.write(event + '\n')



def main():
    print('Creating events list...')
    create_events_list()

if __name__=='__main__':
    main()