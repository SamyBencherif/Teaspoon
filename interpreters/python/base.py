#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import sys

VERBOSE = 0
STEP = 0

RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
YELLOW  = "\033[36m"
DEFAULT = "\033[0m"

VERSION = ["base"]

EXTENSIONS = {}

# TODO
# if and while

def verbose(info):
	if VERBOSE:
		print (info)

def logLine(line, scope):
	if STEP:
		if input (YELLOW + line + DEFAULT):
			print(BLUE + scope + DEFAULT)

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
		if ~captured and i==" ":
			if acc:
				k.append(acc)
			acc = ""
		else:
			acc += i
	k.append(acc)

	return k

def pystring(k):
	return ''.join([chr(x) for x in k])

def func_print(msg):
	verbose('print {}'.format(msg))
	sys.stdout.write(pystring(msg)) # convert charcodes to string
	return;

def func_get(arr, i):
	return arr[int(i[0])]

def func_push(a, b):
	a += b
	pass

def func_less(a,b):
	return [int(a < b)]

def func_eq(a,b):
	return [int(a == b)]

def func_sum(args):
	return [sum([x[0] for x in args])]

def func_mul(args):
	res = 1
	for x in args[0]:
		res *= x
	return [res]

def func_div(args):
	res = 1
	for x in args[0]:
		res /= x
	return [res]

def func_mod(a, b):
	return [a % b]

def func_len(args):
	return [len(args)]

BUILTINS = {
"print":func_print,
"get":func_get,
"less":func_less,
"eq":func_eq,
"push":func_push,
"sum":func_sum,
"mul":func_mul,
"mod":func_mod,
"div":func_div,
"len":func_len
}

def resolve(line, src, scopeNames, scopeValues):
	verbose('resolve {} with scope {} : {}'.format(line, scopeNames, scopeValues))

	if line==".":
		return None

	if line[0]=='(':
		return resolve(line[1:-1], src)

	if line[0]=='[':
		k = []
		for i in argParse(line[1:-1].replace(', ', ' ').replace(',', ' ')):
			k.append(resolve(i, src, scopeNames, scopeValues))
		return k

	if line[0]=='"':
		k = []
		for i in bytes(line[1:-1], 'utf-8').decode('unicode-escape'):
			k.append(ord(i))
		return k

	if line[0] in "-.0123456789":
		if line[0]=="-":
			return -resolve(line[1:], src, scopeNames, scopeValues)
		# elif '.' in line:
			# return float(line)
		else:
			return [int(line)]

	if len(scopeNames) != len(set(scopeNames)):
		# TODO write this info in a log file.
		raise Exception("Internal Error: Overloaded Scope.")

	if line in scopeNames:
		return scopeValues[scopeNames.index(line)]

	tokens = argParse(line)
	name = tokens[0]
	args = tokens[1:]

	if name in BUILTINS.keys():
		# builtins can view arguments exactly as typed (as well as by value)
		# arguments as typed is no longer used
		return BUILTINS[name](*[resolve(arg, src, scopeNames, scopeValues) for arg in args])
	# extensions
	elif name in EXTENSIONS.keys():
		# extensions can only view arguments by value
		return EXTENSIONS[name](*[resolve(arg, src, scopeNames, scopeValues) for arg in args])
	# user defined
	else:
		verbose ('user func {}'.format(name))

		if len(args) and args[0] == "$": # user scope inject
			verbose ('manual scope injection')
			return call(src, name, [resolve(arg, src, scopeNames, scopeValues) for arg in args[1:]], injectNames=scopeNames, injectValues=scopeValues)
		else:
			return call(src, name, [resolve(arg, src, scopeNames, scopeValues) for arg in args])

def call(src, func='main', args=[], injectNames=None, injectValues=None):

	if injectNames == None:
		injectNames = []
		injectValues = []

	verbose('call {} with args {}'.format(func, args))
	verbose('inject {} with values {}'.format(injectNames, injectValues))

	currLine = 0

	srcArr = src.split('\n')

	for line in srcArr:
		tokens = argParse(line)
		if len(tokens)==0:
			pass
		elif tokens[0] == func and tokens[-1] == ":":
			break
		currLine += 1

	if currLine == len(srcArr):
		raise NameError("Symbol {} is not defined.".format(func))

	for i in range(currLine, len(srcArr)):
		tokens = argParse(srcArr[i])
		if len(tokens)>1 and tokens[0] == "end" and tokens[-1] == "function":
			break

	endLoc =  i

	tokens = argParse(srcArr[currLine])
	verbose ('function header {}'.format(srcArr[currLine]))
	verbose ('arg tokens {}'.format(tokens[1:-1]))

	localNames = injectNames
	localValues = injectValues

	if len(tokens[1:-1]) > len(args):
		raise TypeError("Missing arguments")
	# elif len(args) > len(tokens[1:-1]):
	# 	raise TypeError("Too many arguments")

	localNames += tokens[1:-1]
	localValues += args

	logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

	# step
	while currLine < endLoc:

		currLine += 1

		tokens = argParse(srcArr[currLine])

		if len(tokens) and tokens[-1]==":":
			logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

		# no execute
		if len(tokens) == 0 or tokens[0]=="%" or tokens[-1]==":":
			continue
		if len(tokens)>1 and tokens[0] == "end" and tokens[-1] == "function":
			continue
		logLine(srcArr[currLine], str(list(zip(localNames, localValues))))

		# assignment
		if len(tokens) >= 2 and tokens[1] == "=":
			name = tokens[0].strip()
			value = ' '.join(tokens[2:])
			if name in localNames:
				localValues[localNames.index(name)] = resolve(value, src, localNames, localValues)
			else:
				verbose('initializing {}'.format(name))
				verbose('scope {}'.format(localNames))
				localValues.append(resolve(value, src, localNames, localValues))
				localNames.append(name)

		# returns
		elif tokens[0] == "ret":
			verbose('returning {}'.format(tokens[1:]))
			if len(tokens) == 1:
				return None
			else:
				return resolve(tokens[1], src, localNames, localValues)

		# control structures
		elif tokens[0] in ("if", "while"):
			cnd = ' '.join(tokens[1:])

			if not resolve(cnd, src, localNames, localValues)[0]:
				block_depth = 0
				while len(tokens) == 0 or block_depth != 0 or tokens[0] != 'end':
					tokens = argParse(srcArr[currLine])
					if tokens and tokens[0] in ("if", "while"):
						block_depth += 1
					if tokens and tokens[0] == "end":
						block_depth -= 1
					currLine += 1
				currLine += 1 # go past "end" line


		elif tokens[0] == "end":
			if tokens[-1] == "while":
				block_depth = 0
				while len(tokens) == 0 or block_depth != 0 or tokens[0] != 'while':
					tokens = argParse(srcArr[currLine])
					if tokens and tokens[0] in ("if", "while"):
						block_depth -= 1
					if tokens and tokens[0] == "end":
						block_depth += 1
					currLine -= 1


		else: # arbitrary function call
			verbose("root function call {{{}}}".format(srcArr[currLine]))
			resolve(srcArr[currLine], src, localNames, localValues)

if __name__ == "__main__":
	src = open(sys.argv[1], 'r+t').read()
	call(src, 'main', sys.argv[2:])

	# TODO: support -c funcname arg1 arg2 ...