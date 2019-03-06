import glob, os, sys

from datetime import datetime, timedelta


all_files = glob.glob('*.csv')

rm_date = int(sys.argv[1])

delete_files = []
for file in all_files:
    date_file = file.split('_')[0]
    date_file = datetime.strptime(date_file, '%d%m%Y')
    if datetime.now() - date_file > timedelta(days=rm_date):
        delete_files.append(file)

if not delete_files:
    print('There is nothing delete!')
else:
    for file in delete_files:
        os.remove(file)
        print(file, 'Deleted')
