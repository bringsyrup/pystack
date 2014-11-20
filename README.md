pystack
=======

pystack is a cli for automatically finding the best stack overflow answers to your python errors 

##usage
to get pystack on your linux system, clone this repo and follow the code below:
```sh
$ ./configure.sh 	
$ pystack myfile.py <optional search string to be used in searching stack overflow>
```
To see how to set your own paths for installation, type ```./configure --help```

##dependencies
os-x or linux
sys (a python lib that you almost definitely already have)
python2.7 or later but not python3 (dists before 2.7 may work but there is no guarantee)
