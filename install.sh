#! /bin/bash 

USER=$(whoami)

pyflag="--pypath=" && py_short="-p"
libflag="--libpath=" && lib_short="-l"
binflag="--binpath=" && bin_short="-b"
fileflag="--filename=" && file_short="-f"

for arg in "$@"; do
    if [ "${arg:1:1}" == "-" ]; then
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
        ${file_short}, ${fileflag}\"FOO\"           set temp filename to be used for python main
        "
        exit 0
    else
        echo "invalid argument $arg, pystack failed to install"
        exit 1
    fi
done

function pathNotFound {
    echo "the user specified $1 '$2' does not exist"
}

if [ ! "$PYPATH" ]; then
    PYPATH=$(python -c "import sys; print str(sys.path[-1]) + '/'")
elif [ ! -d $PYPATH ]; then
    pathNotFound "python path" "$PYPATH"
    exit 3
elif [ ! "${PYPATH:${#PYPATH}-1}" == "/" ]; then
    PYPATH=${PYPATH}/
    echo $PYPATH
fi
if [ ! "$LIBPATH" ]; then
    LIBPATH=/usr/local/lib/
elif [ ! -d $LIBPATH ]; then
    pathNotFound "library path" "$LIBPATH"
    exit 3
elif [ ! "${LIBPATH:${#LIBPATH}-1}" == "/" ]; then
    LIBPATH=${LIBPATH}/
fi
if [ ! "$BINPATH" ]; then
    BINPATH=/usr/local/bin/
elif [ ! -d $BINPATH ]; then
    pathNotFound "bin path" "$BINPATH"
    exit 3
elif [ ! "${BINPATH:${#BINPATH}-1}" == "/" ]; then
    BINPATH=${BINPATH}/
fi
if [ ! "$TEMPFILENAME" ]; then
    TEMPFILENAME=pystack.txt.tmp
fi  


permissions() {
    echo "permission denied. try running 'sudo ./install.sh'"
    exit 1
}
(
echo "#! /bin/bash 
# options = -f [file] -s [search] -l [limit] -g -h 

usage() { cat << EOF
    usage: pystack [options]

    pystack is a simple script that can be used to, depending on the arguments 
    given, find relevent stack-overflow questions from your python code 
    traceback errors, search google or stack-overflow, or run pep 8.  

    FLAG OPTIONS:
    -h    Show this message
    -g    Use google unfiltered. Else, results will be filtered by           
          stackexchange. If the -f option is also used, results will be 
          filtered based on the content of the argument file

    ARGUMENT OPTIONS:
    -f    Python file to collect tracback errors from
    -s    Search string for google or stack-overflow
    -l    result limit, limits the number of output urls to an integer argument.
          Else, default is 10. Note: this will not necessarily produce the exact
          number of requested results due to filtering and weird BeautifulSoup
          attributes

    EXAMPLES:
    $ pystack -f foo.py -gs \"double list comprehension\" 
        #queries google search for traceback error and search string, returns 
        unfiltered google urls

    $ pystack -s \"bash conditionals tutorial\" 
        #queries stack-overflow for search string, returns urls
    
    $ pystack -f foo.py -l 50
        #queries google with traceback error, filters results using contents 
        of foo.py and the Stack-Exchange API, returns up to 50 urls 

EOF
}

while getopts \"hf:gs:l:\" OPTION; do
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
        l)
            LIMIT=\$OPTARG
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done

if ! [ \"\$LIMIT\" ]; then
    if [ \"\$GOOGLE\" ]; then
        LIMIT=10
    else
        LIMT=50
    fi
fi

if [ \"\$FILE\" ] || [ \"\$SEARCH\" ]; then
    if ! [ \"\$GOOGLE\" ]; then
        cat \$FILE > $TEMPFILENAME
        (python \$FILE 2>&1 | python ${LIBPATH}pystackpy/pystack.py \"--file\" \$GOOGLE \"$TEMPFILENAME\" \"\$SEARCH\" \"--limit\" \$LIMIT)
    else
        python ${LIBPATH}pystackpy/pystack.py \$GOOGLE \"None\" \"\$SEARCH\" \"--limit\" \$LIMIT
    fi
else 
    usage
    exit 1
fi
exit 0" > pystack && echo "populating pystack shell script..." || exit 2

chown $USER pystack || exit 2
if [ ! -x pystack ]; then
    chmod u+x pystack && echo "making pystack executable..." || exit 2
fi

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
