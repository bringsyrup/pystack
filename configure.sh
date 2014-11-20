#! /bin/bash

pyflag='--pypath'
libflag='--libpath'
binflag='--binpath'
fileflag='--filename'

for arg in "$@"; do
    if [ "${arg:0:${#pyflag}}" == ${pyflag} ]; then
        PYPATH=${arg:9}
    elif [ "${arg:0:${#libflag}}" == ${libflag} ]; then
        LIBPATH=${arg:10}
    elif [ "${arg:0:${#binflag}}" == ${binflag} ]; then
        BINPATH=${arg:10}
    elif [ "${arg:0:${#fileflag}}" == ${fileflag} ]; then
        TEMPFILENAME=${arg:11}
    elif [ "$arg" == "--help" ]; then
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

if [ ! -v "$PYPATH" ]; then
    PYPATH=$(python -c "import sys; print str(sys.path[-1]) + '/'")
fi
if [ ! -v "$LIBPATH" ]; then
    LIBPATH=/usr/local/lib/
fi
if [ ! -v "$BINPATH" ]; then
    BINPATH=/usr/local/bin/
fi
if [ ! -v "$TEMPFILENAME" ]; then
    TEMPFILENAME=pystack.txt.tmp
fi  

echo "#! /bin/bash 
PYSCRIPT=\$1
TERM=\$2
if [ \"\$PYSCRIPT\" ]; then
    cat \$PYSCRIPT > $TEMPFILENAME 
    (python \$PYSCRIPT 2>&1 | python ${LIBPATH}pystackpy/pystack.py \"$TEMPFILENAME\" \"\$TERM\")
else 
    python
fi
exit 0" > pystack && echo "propogating pystack shell script..."

if [ ! -x pystack ]; then
    chmod u+x pystack && echo "making pystack executable..."
fi

cp -r stackexchange $PYPATH && echo "copying stackexchange api python wrapper to ${PYPATH}..."
cp -r pystackpy $LIBPATH && echo "copying pystackpy to ${LIBPATH}..."
mv pystack $BINPATH && echo "moving pystack executable to ${BINPATH}..."
echo "install was sucessful!" && exit 0
