#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys
src = open(sys.argv[1]).read()
print (len(list(filter(lambda x:x and x[0]!='%', src.split('\n')))))