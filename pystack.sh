#! /bin/bash
PYSCRIPT=$1
python $PYSCRIPT 2>&1 | python out.py
exit 0
