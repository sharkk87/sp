#!/bin/bash
xterm -hold -e 'cd shop; python3 rm_old_files.py' &
xterm -hold -e 'python3 apline.py' &
xterm -hold -e 'python3 bober.py' &
xterm -hold -e 'python3 centrsm.py' &
xterm -hold -e 'python3 kontinent.py' &
xterm -hold -e 'python3 lider.py' &
xterm -hold -e 'python3 tdsot.py' &
xterm -hold -e 'python3 sanvol.py' &
xterm -hold -e 'python3 upravdom.py' &
