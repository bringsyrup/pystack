#! /bin/bash
PYSCRIPT=$1
python $PYSCRIPT 2>> .out.txt~
python out.py 
rm .out.txt~
exit 0


