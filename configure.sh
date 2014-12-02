#! /bin/bash -e

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
# options = -f [file] -s [search] -g -h


usage() { cat << EOF
    usage: pystack [options]

    pystack is a simple script that can be used to, depending on the arguments 
    given, find relevent stack-overflow questions from your python code 
    traceback errors, search google or stack-overflow, or run pep 8.  

    OPTIONS:
    -h    Show this message
    -f    Python file to collect tracback errors from
    -g    Use google instead of stack-overflow
    -s    Search string for google or stack-overflow

    EXAMPLES:
    $ pystack -f foo.py -gs \"double list comprehension\" 
        #queries google search for traceback error and search string, returns urls

    $ pystack -s \"bash conditionals tutorial\" 
        #queries stack-overflow for search string, returns urls
    
    $ pystack -f foo.py 
        #queries stack-overflow with traceback error, returns urls

EOF
}

while getopts \"hf:gs:\" OPTION; do
    case \$OPTION in
        h)
            usage
            exit 2
            ;;
        f)
            FILE=\$OPTARG
            ;;
        g)
            GOOGLE=\"--google\"
            ;;
        s)
            SEARCH=\$OPTARG
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done

if [ \"\$FILE\" ]; then
    cat \$FILE > $TEMPFILENAME
    (python \$FILE 2>&1 | python /usr/local/lib/pystackpy/pystack.py \$GOOGLE \"$TEMPFILENAME\" \"\$SEARCH\")
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
