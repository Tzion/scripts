import getopt, sys
import os
from datetime import datetime


def main(argv):
    path, new_name, prefix, dry_run = extract_args(argv)

    if os.path.isdir(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                add_timestamp_to_filename(path, f, new_name, prefix, dry_run)
    else:
        add_timestamp_to_filename(os.path.split(path)[0], os.path.split(path)[1], new_name, prefix, dry_run)

def add_timestamp_to_filename(dir, file, new_name, prefix, dry_run):
    original_path = os.path.join(dir, file)
    m_time = os.lstat(original_path).st_mtime
    timestamp = format_time(m_time)
    filename, ext = os.path.splitext(file)
    name = new_name if new_name else filename
    final_name = timestamp + '_' + name + ext if prefix else name + '_' + timestamp + ext
    final_path = os.path.join(dir, final_name)
    print(f'Changing file {original_path} to {final_path}')
    if not dry_run:
        os.rename(original_path, final_path)


def format_time(timestamp):
    ''' returns timestamp of date (iso format) with the original time of day of timestamp (H:M:S) '''
    date_time = datetime.fromtimestamp(timestamp)
    formatted = date_time.strftime("%y-%m-%d_%H%M%S_%f")[:-8]
    return formatted


def extract_args(argv):
    opts, args = getopt.getopt(argv, '', ['path=', 'prefix', 'rename=', 'dry-run', 'help'])
    path = None
    prefix = False
    new_name = None
    dry_run = False
    for opt, arg in opts:
        if opt == '--help':
            help()
            sys.exit(0)
        if opt in ['-p', '--path']:
            path = arg
        if opt in ['--prefix']:
            prefix = True
        if opt in ['--rename']:
            new_name = arg
        if opt in ['--dry-run']:
            dry_run = True
            
    input = (path, new_name, prefix, dry_run)
    return input

usage = f'\n{sys.argv[0]}: Attaches the Modified Timestamp to the file name. Works on a file or files in a directory (non recursive).'\
        """
        
    Options:
        -p --path       path to file or directory to perform the date shift upon (in case or directory it applies to all the files in the first level only -
                        not including directories or hidden files) 
        --prefix        when this flag is supplied - attached the timestamp before the filename. Default is false.
        --rename        override the file name with the new name provided
        --dry-run       print out the name changes without doing the actual change on the files
        -h --help       show this screen
        """

def help():
    print(usage)

if __name__ == '__main__':
    try: 
        main(sys.argv[1:])
    except Exception as e:
        print(e)
        usage()
        sys.exit(1)