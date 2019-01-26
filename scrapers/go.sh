#!/bin/bash
. "../venv/bin/activate"
python upravdom.py >> shop_csv/log_apline.txt &
python upravdom.py >> shop_csv/log_bober.txt &
python upravdom.py >> shop_csv/log_centrsm.txt &
python upravdom.py >> shop_csv/log_kontinent.txt &
python upravdom.py >> shop_csv/log_lider.txt &
python upravdom.py >> shop_csv/log_sanvol.txt &
python upravdom.py >> shop_csv/log_tdsot.txt &
python upravdom.py >> shop_csv/log_upravdom.txt &
wait
python csv_to_mysql.py >> log.txt
