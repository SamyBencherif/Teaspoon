#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys, os
import subprocess

mydir = os.path.dirname(os.path.realpath(__file__))

def rel_to_script(path):
	return (mydir + os.sep + path)

error = open(rel_to_script("error.log"), "w")


def interpreted_in_python(script):
	executor = rel_to_script('../interpreters/python/base.py')
	return subprocess.check_output(executor + ' ' + script, shell=1, stderr=error)

def interpreted_in_javascript(script):
	executor = rel_to_script('../interpreters/javascript/base.js')
	return subprocess.check_output(executor + ' ' + script, shell=1, stderr=error)

def compile(script):
	executor = rel_to_script('../compilers/c/compiler.py')
	return subprocess.call(executor + ' ' + script + ' -o ' + mydir + os.sep + 'a.out', shell=1, stderr=error)

def compiled(script):
	return subprocess.check_output(mydir + os.sep + 'a.out', shell=1, stderr=error)


def show_status(caption, function, script):
	sys.stdout.write (BLUE + "Running " + caption + " " + DEFAULT)
	try:
		out = function(script).decode()
		sys.stdout.write (GREEN + "[Terminated]" + DEFAULT)
		exp_out_path = rel_to_script('expected_outputs' + os.sep + os.path.basename(script))
		exp_out_path = exp_out_path.split('.')[0] + '.txt'
		if not os.path.exists(exp_out_path):
			sys.stdout.write (MAGENTA + "[Unknown]" + DEFAULT)
		else:
			exp_out = open(exp_out_path, 'r+t').read()
			if out==exp_out:
				sys.stdout.write (GREEN + "[Correct]" + DEFAULT)
			else:
				sys.stdout.write (RED + "[Incorrect]" + DEFAULT)
				error.write("--- incorrect program output ({}) ---\n".format(caption))
				error.write('reported `{}`\n'.format(out))
				error.write('expected `{}`\n'.format(exp_out))

	except:
		sys.stdout.write (RED + "[Crashed]" + DEFAULT)
	print()

def test_prog(script):

	show_status("Interpreted in Python", interpreted_in_python, script)
	show_status("Interpreted in NodeJS", interpreted_in_javascript, script)

	sys.stdout.write (BLUE + "Compiling " + DEFAULT)
	compile_worked = not compile(script)

	if compile_worked:
		sys.stdout.write (GREEN + "[Success]\n" + DEFAULT)
		show_status("Compiled Code.", compiled, script)
	else:
		sys.stdout.write (RED + "[Error]\n" + DEFAULT)

RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
MAGENTA    = "\033[35m"
YELLOW  = "\033[36m"
DEFAULT = "\033[0m"

if __name__ == "__main__":
	for f in os.listdir(rel_to_script('../examples/')):
		print(YELLOW + f.upper() + DEFAULT)
		test_prog(rel_to_script('../examples/') + f)
		print()
