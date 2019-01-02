#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

"""
compiler.py is missing the following base.py features

scope injection: $
default values: .
"""

import os, sys

VERSION = ["base"]

EXTENSIONS = {}

def argParse(line):

	line = line.strip()

	if line == "":
		return []

	k = []
	captured = 0
	acc = ""
	for i in line:
		if i == '"':
			captured = ~captured
		if i in '([':
			captured -= 1
		if i in ')]':
			captured += 1
		if not captured and i==" ":
			if acc:
				k.append(acc)
			acc = ""
		else:
			acc += i
	k.append(acc)

	return k

def u_func_exists(func, src):
	for line in src:
		tokens = argParse(line)
		if len(tokens)>1 and tokens[0] == func and tokens[-1] == ":":
			return True
	return False

def resolve(line, src, preserveNum=False):

	if line[0]=='(':
		return resolve(line[1:-1], src)

	if line[0]=='[':
		k = []
		for i in argParse(line[1:-1].replace(',', ' ')):
			k.append(resolve(i, src, True))
		return 'new_array(' + str(len(k)) + ',(float[]){' + ', '.join(k) + '})'

	if line[0]=='"':
		k = []
		for i in bytes(line[1:-1], 'utf-8').decode('unicode_escape'):
			k.append(ord(i))
		# k.append(0)
		return resolve(str(k), src)

	if line[0] in "-.0123456789":
		if line[0]=="-" and line[1] != "-.0123456789":
			return -resolve(line[1:], src)
		else:
			if preserveNum:
				return line
			else:
				return 'new_array(1, (float[]){{{}}})'.format(line)

	tokens = argParse(line)
	name = tokens[0]
	args = tokens[1:]

	#																		| an extension
	#																		v
	builtins = ['less', 'eq', 'sum', 'mul', 'div', 'push', 'get', 'len'] + ['print']

	# builtins
	if name in builtins:
		if name == "push":
			if preserveNum:
				return "b_{}(&{}).get[0]".format(name, ', '.join([resolve(x, src) for x in args]))
			else:
				return "b_{}(&{})".format(name, ', '.join([resolve(x, src) for x in args]))
		else:
			return "b_{}({})".format(name, ', '.join([resolve(x, src) for x in args]))
	# user func
	elif u_func_exists(name, src):
		if preserveNum:
			return "u_{}({}).get[0]".format(name, ', '.join([resolve(x, src) for x in args]))
		else:
			return "u_{}({})".format(name, ', '.join([resolve(x, src) for x in args]))

	# variable
	elif len(line.split()) == 1:
		if preserveNum:
			return 'v_'+line+'.get[0]'
		else:
			return 'v_'+line
	else:
		raise Exception("Undefined function: {}".format(line.split()[0]))


def ret_macro(indent, s, ret_index):
	return ("\n"+("  "*indent)+"Array ret_{R} = {s};\n" +
	("  "*indent)+"reset_pool(ret_{R}.get, pool_restore);\n" +
	("  "*indent)+"return ret_{R};\n").format(R=ret_index, s=s)

def compile(src):

	currLine = 0
	srcArr = src.split('\n')

	res = ""
	indent = 0

	definedFunctions = []

	ret_index = 0

	# step
	for currLine in range(len(srcArr)):

		tokens = argParse(srcArr[currLine])

		# no call
		if len(tokens) == 0 or tokens[0][0]=="%":
			continue

		# function
		if tokens[-1]==":":
			res += "  "*indent + "\nArray u_{}({}) {{\n".format(tokens[0], ', '.join(['Array ' + x for x in tokens[1:-1]]))
			indent += 1
			res += "  "*indent + "int pool_restore = pool.size;\n\n"
			definedFunctions = []

		# assignment
		elif len(tokens) >= 2 and tokens[1] == "=":
			value = ' '.join(tokens[2:])
			if resolve(tokens[0], srcArr) in definedFunctions:
				res += "  "*indent + "{}={};\n".format(resolve(tokens[0], srcArr), resolve(value, srcArr))
			else:
				res += "  "*indent + "Array {}={};\n".format(resolve(tokens[0], srcArr), resolve(value, srcArr))
				definedFunctions.append(resolve(tokens[0], srcArr))

		# returns
		elif tokens[0] == "ret":

			if len(tokens) == 1:
				res += ret_macro(indent, "new_array(0, (float[]){})", ret_index)
				ret_index += 1
			else:
				res += ret_macro(indent, resolve(tokens[1], srcArr), ret_index)
				ret_index += 1

		# control structures
		elif tokens[0] == "if" or tokens[0] == "while":
			res += "  "*indent + "{}({}.get[0]){{\n".format(tokens[0], resolve(' '.join(tokens[1:]), srcArr))
			indent += 1
		elif tokens[0] == "end":
			if tokens[-1] == "function":
				res += ret_macro(indent, "new_array(0, (float[]){})", ret_index)
				ret_index += 1
				indent -= 1
				res += "  "*indent + "}\n"
			else:
				indent -= 1
				res += "  "*indent + "}\n"
		else: # arbitrary function call
			res += "  "*indent + resolve(srcArr[currLine], srcArr)+";\n"

	return res

import subprocess

if __name__ == "__main__":
	src = open(sys.argv[1], 'r+t').read()
	outDir = os.getcwd()
	os.chdir(os.path.dirname(sys.argv[0]))
	open('user.c', 'w+t').write(compile(src))

	if len(sys.argv) < 4 or sys.argv[2] != '-o': # cheap parlor tricks, switch to argparse module
		out = 'a.out'
		exit(subprocess.call("gcc base.c -o " + outDir + os.sep + out, shell=1))
	else:
		out = sys.argv[3]
		if (out[0] == '/'):
			exit(subprocess.call("gcc base.c -o " + out, shell=1))
		else:
			exit(subprocess.call("gcc base.c -o " + outDir + os.sep + out, shell=1))