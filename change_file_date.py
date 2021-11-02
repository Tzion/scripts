import getopt, sys
import os
from datetime import datetime


def main(argv):
    path, date = extract_args(argv)

    if os.path.isdir(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                change_file_timestamp(path+'/'+f, date)
    else:
        change_file_timestamp(path, date)

def change_file_timestamp(file_path, date):
    a_time = os.lstat(file_path).st_atime
    m_time = os.lstat(file_path).st_mtime
    new_m_time = change_timestamp_to_date(m_time, date)
    print(f'Changing the Modified Timestamp of {file_path} from {datetime.fromtimestamp(m_time)} to {datetime.fromtimestamp(new_m_time)}')
    os.utime(file_path, (a_time, new_m_time))



def change_timestamp_to_date(timestamp, date):
    ''' returns timestamp of date (iso format) with the original time of day of timestamp (H:M:S) '''
    time_in_day = datetime.fromtimestamp(timestamp).time()
    date = datetime.fromisoformat(date).date()
    desired_date = datetime.combine(date, time_in_day)
    desired_timestamp = datetime.timestamp(desired_date)
    return desired_timestamp


def extract_args(argv):
    opts, args = getopt.getopt(argv, 'p:d:', ['path=', 'date=', 'help'])
    path = None
    date = None
    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit(0)
        if opt in ['-p', '--path']:
            path = arg
        if opt in ['-d', '--date']:
            date = arg
    input = (path, date)
    return input

def usage():
    print(f'This script chagnes the Modified Timestamp of a file or files in directory (non recursive).\n'
          f'It keeps the time of day (hours:minutes:...) of the original file and changes the date only.\n\n'
          f'Usage: python3 {sys.argv[0]} --path=<path to file or directory> --date=<desired date in iso format>.\n\n'
          f'Example: python3 {sys.argv[0]} --path=path/to/dir_or_file --date=2020-01-02')


if __name__ == '__main__':
    try: 
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        usage()
        sys.exit(1)



