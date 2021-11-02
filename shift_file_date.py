import getopt, sys
import os
from datetime import datetime


def main(argv):
    path, date = extract_args(argv)

    if os.path.isdir(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                shift_file_timestamp(path+'/'+f, date)
    else:
        shift_file_timestamp(path, date)

def shift_file_timestamp(file_path, date):
    a_time = os.lstat(file_path).st_atime
    m_time = os.lstat(file_path).st_mtime
    new_m_time = shift_timestamp_backwards_to_date(m_time, date)
    print(f'Changing Modified timestamp of {file_path} from {datetime.fromtimestamp(m_time)} to {datetime.fromtimestamp(new_m_time)}')
    os.utime(file_path, (a_time, new_m_time))



def shift_timestamp_backwards_to_date(timestamp, date):
    ''' returns timestamp of date (iso format) with the original time of day of timestamp (H:M:S) '''
    time_in_day = datetime.fromtimestamp(timestamp).time()
    date = datetime.fromisoformat(date).date()
    desired_date = datetime.combine(date, time_in_day)
    desired_timestamp = datetime.timestamp(desired_date)
    return desired_timestamp


def extract_args(argv):
    try:
        opts, args = getopt.getopt(argv, 'p:d:', ['path=', 'date=', 'help'])
    except getopt.GetoptError as e:
        usage()
    path = None
    date = None
    for opt, arg in opts:
        if opt in ['-p', '--path']:
            path = arg
        if opt in ['-d', '--date']:
            date = arg
    input = (path, date)
    return input

def usage():
    print('Manual')


if __name__ == '__main__':
    try: 
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        usage()
        os.exit(1)



