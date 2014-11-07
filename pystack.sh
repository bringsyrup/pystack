#! /bin/bash
PYSCRIPT=$1
if [$PYSCRIPT]; then
    python $PYSCRIPT 2>&1 | python out.py
else 
    python
fi
    exit 0
