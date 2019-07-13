#!/bin/bash
cd /home/iliya/stroy-parser35/scrapers
. "../venv/bin/activate"
wait
python edison.py >> edison.log ;                        # 13000 products in 4 minutes (requests)
python apline.py >> apline.log ;                        # 11000 products in 10 minutes (requests)
python bober.py >> bober.log ;                          # 21000 in 20 (requests)
python centrsm.py >> centrsm.log ;                      # 107000 in 120 (requests)
python kontinent.py >> kontinent.log ;                  # 19000 in 10 (requests)
python lider.py >> lider.log ;                          # 28000 in 6 (requests)
python sanvol.py >> sanvol.log ;                        # 12000 in 30 (requests)
python upravdom.py >> upravdom.log ;                    # 1300 in 2 (requests)
python idd.py >> idd.log ;                              # 107000 in 90 (requests)
python cov.py >> cov.log ;                              # 3800 in 3 (requests)
python tdsot.py >> tdsot.log ;                          # 13000 in 3 (requests)
# python evrostroy.py >> evrostroy.log ;                # 20000 in 35 (selenium)
# python akson.py >> akson.log ;                        # 35000 in 120 (selenium)
wait
python csv_to_mysql.py >> csv_to_mysql.log
