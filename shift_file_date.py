import getopt, sys
import os
from datetime import datetime
from datetime import timedelta


def main(argv):
    path, date = extract_args(argv)

    if os.path.isdir(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                shift_file_timestamp(path+'/'+f, date)
    else:
        shift_file_timestamp(path, date)

def shift_file_timestamp(file_path, days_to_shift):
    a_time = os.lstat(file_path).st_atime
    m_time = os.lstat(file_path).st_mtime
    new_m_time = shift_timestamp_by_x_days(m_time, days_to_shift)
    print(f'Changing Modified timestamp of {file_path} from {datetime.fromtimestamp(m_time)} to {datetime.fromtimestamp(new_m_time)}')
    os.utime(file_path, (a_time, new_m_time))



def shift_timestamp_by_x_days(timestamp, days):
    original_date = datetime.fromtimestamp(timestamp)
    desired_date = original_date - timedelta(days=days)
    desired_timestamp = datetime.timestamp(desired_date)
    return desired_timestamp


def extract_args(argv):
    opts, args = getopt.getopt(argv, 'p:d:b:', ['path=', 'days_to_shift=', 'backwards', 'help'])
    path = None
    days = None
    backwards = False
    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit(0)
        if opt in ['-p', '--path']:
            path = arg
        if opt in ['-d', '--days_to_shift']:
            days = args
        if opt in ['b', '--backwards']:
            backwards = True
    days = -days if backwards else days
    input = (path, days)
    return input

def usage():
    print(f'This script shifts by given days the Modified Timestamp of a file or files in directory (non recursive).\n'
          f'Usage: python3 {sys.argv[0]} --path=<path to file or directory> --days_to_shift=<desired date in iso format> [--backwards].\n\n'
          f'Example: python3 {sys.argv[0]} --path=path/to/dir_or_file --date=10 --backwards\n In the above example the date of the files in the directory will shift by 10 days backwards')


if __name__ == '__main__':
    try: 
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        usage()
        sys.exit(1)



