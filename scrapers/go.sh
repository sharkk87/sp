#!/bin/bash
cd /home/iliya/stroy-parser35/scrapers
. "../venv/bin/activate"
wait
python apline.py >> apline.log &
python bober.py >> bober.log &
python centrsm.py >> centrsm.log &
python kontinent.py >> kontinent.log &
python lider.py >> lider.log &
python sanvol.py >> sanvol.log &
python tdsot.py >> tdsot.log &
wait
python upravdom.py >> upravdom.log ;
python evrostroy.py >> evrostroy.log ;
wait
python csv_to_mysql.py >> csv_to_mysql.log
