import getopt, sys
import os
from datetime import datetime
from traceback import print_exc
import builtins

class Args:
    path = ''
    new_name = ''
    prefix = False
    dry_run = False
    format = '%y-%m-%d'
    millis = False
    
args = Args()
safe_mode = True

def main(argv):
    extract_args(argv)
    change_names()


def change_names():
    if os.path.isdir(args.path):
        for f in os.listdir(args.path):
            if not f.startswith('.'):
                add_timestamp_to_filename(args.path, f, args.new_name, args.prefix)
    else:
        add_timestamp_to_filename(os.path.split(args.path)[0], os.path.split(args.path)[1], args.new_name, args.prefix)

def add_timestamp_to_filename(dir, file, new_name, prefix):
    original_path = os.path.join(dir, file)
    m_time = os.lstat(original_path).st_mtime
    timestamp = format_time(m_time, args.format)
    filename, ext = os.path.splitext(file)
    name = new_name if new_name else filename
    final_name = timestamp + '_' + name + ext if prefix else name + '_' + timestamp + ext
    final_path = os.path.join(dir, final_name)
    safe_rename(original_path, final_path)

def safe_rename(src, dst):
    if os.path.exists(dst):
        raise FileExistsError(f'File at {dst} already exists. Aborting to avoid override. Change timestamp format or name to avoid overriding')
    else:
        print(f'Changing file {src} to {dst}')
        if not args.dry_run and not safe_mode:
            os.rename(src, dst)


def format_time(timestamp, format):
    ''' returns timestamp of date (iso format) with the original time of day of timestamp (H:M:S) '''
    date_time = datetime.fromtimestamp(timestamp)
    if args.millis:
        format += format + '_%f'
        formatted = date_time.strftime(format)[:-3]
    else:
        formatted = date_time.strftime(format)
    return formatted


def extract_args(argv):
    try:
        opts, _ = getopt.getopt(argv, '', ['path=', 'prefix', 'rename=', 'dry-run', 'date=', 'format=', 'millis', 'help'])
        for opt, arg in opts:
            if opt == '--help':
                help()
                sys.exit(0)
            if opt in ['-p', '--path']:
                args.path = arg
            if opt in ['--prefix']:
                args.prefix = True
            if opt in ['--rename']:
                args.new_name = arg
            if opt in ['--dry-run']:
                args.dry_run = True
            if opt in ['--format']:
                args.format= arg
            if opt in ['--millis']:
                args.millis = True
    except:
        help()

usage = f'\n{sys.argv[0]}: Attaches the Modified Timestamp to the file name. Works on a file or files in a directory (non recursive).'\
        """
        
    Options:
        -p --path       path to file or directory to perform the date shift upon (in case or directory it applies to all the files in the first level only -
                        not including directories or hidden files) 
        --prefix        when this flag is supplied - attached the timestamp before the filename. Default is false.
        --rename        override the file name with the new name provided
        --dry-run       print out the name changes without doing the actual change on the files
        --format        Format of the timestamp (Defualt is "%y-%m-%d. Options that includes time is: %y-%m-%d_%H%M%S)
        --millis        Attaches milliseconds to the timestamp
        -h --help       show this screen
        """

def help():
    print(usage)

def print(msg):
    if safe_mode:
        pass
    else:
        builtins.print(msg)
         
if __name__ == '__main__':
    try: 
        '''
        First run is in safe_mode (if dry-run == False) to notify for possible overrides.
        Notice that some overrides will be only catch on live mode -> those that occur becuase of files that are changing during the process
        '''
        extract_args(sys.argv[1:])
        safe_mode = not args.dry_run
        if safe_mode:
           change_names() 
           safe_mode = False
        change_names()
        print(f"{'DRY RUN: ' if args.dry_run else ''}Done successfully")
    except Exception as e:
        print_exc()
        exit(1)