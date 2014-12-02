#! /bin/bash

pyflag='--pypath='
libflag='--libpath='
binflag='--binpath='
fileflag='--filename='

for arg in "$@"; do
    if [ "${arg:0:${#pyflag}}" == ${pyflag} ]; then
        PYPATH=${arg:${#pyflag}}
    elif [ "${arg:0:${#libflag}}" == ${libflag} ]; then
        LIBPATH=${arg:${#libflag}}
    elif [ "${arg:0:${#binflag}}" == ${binflag} ]; then
        BINPATH=${arg:${#binflag}}
    elif [ "${arg:0:${#fileflag}}" == ${fileflag} ]; then
        TEMPFILENAME=${arg:${#fileflag}}
    elif [ "$arg" == "--help" -o "$arg" == "-h" ]; then
        echo "user may specify the following paths in any order:"
        echo "  
        $pyflag         
        $libflag 
        $binflag 
        $fileflag
        "
        exit 2
    else
        echo "invalid argument $arg, pystack failed to install"
        exit 1
    fi
done

if [ ! "$PYPATH" ]; then
    PYPATH=$(python -c "import sys; print str(sys.path[-1]) + '/'")
fi
if [ ! "$LIBPATH" ]; then
    LIBPATH=/usr/local/lib/
fi
if [ ! "$BINPATH" ]; then
    BINPATH=/usr/local/bin/
fi
if [ ! "$TEMPFILENAME" ]; then
    TEMPFILENAME=pystack.txt.tmp
fi  

echo "#! /bin/bash 
PYSCRIPT=\$1
ENGINE=\$2
TERM=\$3

if [ \"\$PYSCRIPT\" ]; then
    cat \$PYSCRIPT > $TEMPFILENAME 
    if [ \"\$ENGINE\" == \"-g\" -o \"\$ENGINE\" == \"--google\" ]; then
        if [ \"$\TERM\" ]; then
            (python \$PYSCRIPT 2>&1 | python ${LIBPATH}pystackpy/pystack.py \$ENGINE \"$TEMPFILENAME\" \"\$TERM\")
        else
            (python \$PYSCRIPT 2>&1 | python ${LIBPATH}pystackpy/pystack.py \$ENGINE \"$TEMPFILENAME\")
        fi
    else
        (python \$PYSCRIPT 2>&1 | python ${LIBPATH}pystackpy/pystack.py \"$TEMPFILENAME\" \"\$ENGINE\" )
    fi
else 
    python
fi
exit 0" > pystack && echo "populating pystack shell script..."

if [ ! -x pystack ]; then
    chmod u+x pystack && echo "making pystack executable..."
fi

cp -r stackexchange $PYPATH && echo "copying stackexchange api python wrapper to ${PYPATH}..."
cp -r pystackpy $LIBPATH && echo "copying pystackpy to ${LIBPATH}..."
mv pystack $BINPATH && echo "moving pystack executable to ${BINPATH}..."
echo "install was sucessful!" && exit 0
