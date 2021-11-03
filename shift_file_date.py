import getopt, sys
import os
from datetime import datetime
from datetime import timedelta


path = None
days = None
dry_run = False

def main(argv):
    path, date = extract_args(argv)

    if os.path.isdir(path):
        for f in os.listdir(path):
            if not f.startswith('.') and os.path.isfile(path+'/'+f):
                shift_file_timestamp(path+'/'+f, date)
    else:
        shift_file_timestamp(path, date)

def shift_file_timestamp(file_path, days):
    a_time = os.lstat(file_path).st_atime
    m_time = os.lstat(file_path).st_mtime
    new_m_time = shift_timestamp_by_x_days(m_time, days)
    dry_run_prefix = '--dry-run: ' if dry_run else ''
    print(f'{dry_run_prefix}Changing the Modified-Timestamp of {file_path} from {datetime.fromtimestamp(m_time)} to {datetime.fromtimestamp(new_m_time)}')
    if not dry_run:
        os.utime(file_path, (a_time, new_m_time))



def shift_timestamp_by_x_days(timestamp, days):
    original_date = datetime.fromtimestamp(timestamp)
    desired_date = original_date + timedelta(days=int(days))
    desired_timestamp = datetime.timestamp(desired_date)
    return desired_timestamp


def extract_args(argv):
    try:
        opts, args = getopt.getopt(argv, 'p:d:h', ['path=', 'days=', 'dry-run', 'help'])
    except getopt.GetoptError as err:
        print(err)
        help()
        sys.exit(2)
    global dry_run
    for opt, arg in opts:
        if opt in ['--help', 'h']:
            help()
            sys.exit(2)
        if opt in ['-p', '--path']:
            path = os.path.expanduser(arg)
        if opt in ['-d', '--days']:
            days = arg
        if opt in ['--dry-run']:
            dry_run = True
    input = (path, days)
    return input


usage = f'\n{sys.argv[0]}: Shifts the Modified Date of files by given days forwards or backwards'\
        """
        
    Options:
        -p --path       path to file or directory to perform the date shift upon (in case or directory it applies to all the files in the first level only -
                        not including directories or hidden files) 
        -d --days       number of days for the date shift (negative integer for backward shift)
        --dry-run       print out the date changes without doing the actual change on the files
        -h --help       show this screen
        """

def help():
    print(usage)


if __name__ == '__main__':
    main(sys.argv[1:])
