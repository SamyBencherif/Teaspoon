#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys, os
import subprocess

def rel_to_script(path):
	return (os.path.dirname(sys.argv[0]) + os.sep + path)


script = rel_to_script('../examples/hello.tea')

print ("Interpreted in Python.")
executor = rel_to_script('../interpreters/python/base.py')
subprocess.call(executor + ' ' + script, shell=1)

print()

print ("Interpreted in NodeJS.")
executor = rel_to_script('../interpreters/javascript/base.js')
subprocess.call(executor + ' ' + script, shell=1)

print ("Compiled.")
executor = rel_to_script('../compilers/c/compiler.py')
subprocess.call(executor + ' ' + script, shell=1)