#! /bin/bash
DISTPYPATH=$(python -c "import sys; print str(sys.path[-1]) + '/'")
DISTLIBPATH="/usr/lib/" #change to probe statement for supporting os-x but not gonna deal with that now
cp -r stackexchange $DISTPYPATH && echo 'copying stackexchange api python wrapper to' $DISTPYPATH '...'
cp -r pystackpy $DISTLIBPATH && echo 'copying pystackpy to' $DISTLIBPATH '...'
cp pystack /usr/bin/ && echo 'copying pystack executable to /usr/bin/'
exit 0
