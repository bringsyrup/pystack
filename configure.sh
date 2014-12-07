#! /bin/bash -e

pyflag="--pypath=" && py_short="-p"
libflag="--libpath=" && lib_short="-l"
binflag="--binpath=" && bin_short="-b"
fileflag="--filename=" && file_short="-f"

for arg in "$@"; do
    if [ "${arg:1:1}" = "-" ]; then
        arg_n="${arg:1:2}=${arg#*=}"
    else
        arg_n=$arg
    fi
    if [ "${arg_n:0:${#py_short}}" == ${py_short} ]; then
        PYPATH=${arg_n:${#py_short}+1}
    elif [ "${arg_n:0:${#lib_short}}" == ${lib_short} ]; then
        LIBPATH=${arg_n:${#lib_short}+1}
    elif [ "${arg_n:0:${#bin_short}}" == ${bin_short} ]; then
        BINPATH=${arg_n:${#bin_short}+1}
    elif [ "${arg_n:0:${#file_short}}" == ${file_short} ]; then
        TEMPFILENAME=${arg_n:${#file_short}+1}
    elif [ "$arg" == "-h" -o "${arg}" == "--help" ]; then
        echo "
        OPTIONS:
        
        -h, --help                     show this message and exit   

        ${py_short}, ${pyflag}PATH             set python path to be used 
        ${lib_short}, ${libflag}PATH            set lib path to be used
        ${bin_short}, ${binflag}PATH            set bin path to be used
        ${file_short}, ${fileflag}PATH           set temp filename to be used for python main
        "
        exit 0
    else
        echo "invalid argument $arg, pystack failed to install"
        exit 1
    fi
done

if [ ! "$PYPATH" ]; then
    PYPATH=$(python -c "import sys; print str(sys.path[-1]) + '/'")
elif [ ! -d $PYPATH ]; then
    echo "the user specified PYTHONPATH \"$PYPATH\" does not exist"
    exit 3
elif [ ! "${PYPATH:${#PYPATH}-1}" == "/" ]; then
    PYPATH=${PYPATH}/
    echo $PYPATH
fi
if [ ! "$LIBPATH" ]; then
    LIBPATH=/usr/local/lib/
elif [ ! -d $LIBPATH ]; then
    echo "the user specified LIBPATH \"$LIBPATH\" does not exist"
    exit 3
elif [ ! "${LIBPATH:${#LIBPATH}-1}" == "/" ]; then
    LIBPATH=${LIBPATH}/
fi
if [ ! "$BINPATH" ]; then
    BINPATH=/usr/local/bin/
elif [ ! -d $BINPATH ]; then
    echo "user specified BINPATH \"$BINPATH\" does not exits"
    exit 3
elif [ ! "${BINPATH:${#BINPATH}-1}" == "/" ]; then
    BINPATH=${BINPATH}/
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
            exit 0
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

if [ \"\$FILE\" ] || [ \"\$SEARCH\" ]; then
    if [ \"\$FILE\" ] && ! [ \"\$GOOGLE\" ]; then
        cat \$FILE > $TEMPFILENAME
        (python \$FILE 2>&1 | python ${LIBPATH}pystackpy/pystack.py \"--file\" \$GOOGLE \"$TEMPFILENAME\" \"\$SEARCH\")
    else
        python ${LIBPATH}pystackpy/pystack.py \$GOOGLE \"None\" \"\$SEARCH\"
    fi
else 
    usage
    exit 1
fi
exit 0" > pystack && echo "populating pystack shell script..."

permissions() {
    echo "permission denied. try running sudo ./configure"
    exit 1
}

if [ ! -x pystack ]; then
    chmod u+x pystack && echo "making pystack executable..."
    if [ ! -x pystack ]; then
        permissions
    fi
fi

(
cp -rf stackexchange $PYPATH && echo "copying stackexchange api python wrapper to ${PYPATH}..." || exit 2
cp -rf pystackpy $LIBPATH && echo "copying pystackpy lib to ${LIBPATH}..." || exit 2
mv pystack $BINPATH && echo "moving pystack executable to ${BINPATH}..." || exit 2 
)

if [ $? == 2 ]; then 
    permissions
else
    echo "install was sucessful!" 
    exit 0
fi
