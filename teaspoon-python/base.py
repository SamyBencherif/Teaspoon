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

# TODO parenthetical evaluation

# sum (sum 4 5) (mul 5)

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

def func_print(args, src, scopeNames, scopeValues):
	verbose('print {}'.format(resolve(args[0], src, scopeNames, scopeValues)))
	if type(resolve(args[0], src, scopeNames, scopeValues)) == int:
		print(resolve(args[0], src, scopeNames, scopeValues))
	else:
		print(pystring(resolve(args[0], src, scopeNames, scopeValues))) # process string literal or vars
	return;

def func_require(args, src, scopeNames, scopeValues):
	if not pystring(resolve(args[0], src, scopeNames, scopeValues)) in VERSION:
		# print(VERSION[0], args[0])
		print('This program is not compatible with this version of Teaspoon. It requires teaspoon_{}.'.format(''.join([chr(x) for x in resolve(args[0], src, scopeNames, scopeValues)])))
		exit(1)

def func_get(args, src, scopeNames, scopeValues):
	return resolve(args[0], src, scopeNames, scopeValues)[resolve(args[1], src, scopeNames, scopeValues)]

def func_add(args, src, scopeNames, scopeValues):
	return resolve(args[0], src, scopeNames, scopeValues).append(resolve(args[1], src, scopeNames, scopeValues))

def func_sum(args, src, scopeNames, scopeValues):
	return sum([resolve(arg, src, scopeNames, scopeValues) for arg in args])

def func_mul(args, src, scopeNames, scopeValues):
	return resolve(args[0], src, scopeNames, scopeValues) * resolve(args[1], src, scopeNames, scopeValues)

def func_div(args, src, scopeNames, scopeValues):
	return resolve(args[0], src, scopeNames, scopeValues) // resolve(args[1], src, scopeNames, scopeValues)

def func_len(args, src, scopeNames, scopeValues):
	return len(resolve(args[0], src, scopeNames, scopeValues))

BUILTINS = {
"print":func_print,
"require":func_require,
"get":func_get,
"add":func_add,
"sum":func_sum,
"mul":func_mul,
"div":func_div,
"len":func_len
}

def resolve(line, src, scopeNames, scopeValues):
	verbose('resolve {} with scope {} : {}'.format(line, scopeNames, scopeValues))

	if line==".":
		return None

	if line[0]=='[':
		k = []
		for i in argParse(line[1:-1].replace(', ', ' ').replace(',', ' ')):
			k.append(resolve(i, src, scopeNames, scopeValues))
		return k

	if line[0]=='"':
		k = []
		for i in line[1:-1]:
			k.append(ord(i))
		return k

	if line[0] in "-.0123456789":
		if line[0]=="-":
			return -resolve(line[1:], src, scopeNames, scopeValues)
		elif '.' in line:
			return float(line)
		else:
			return int(line)

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
		return BUILTINS[name](args, src, scopeNames, scopeValues)
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
		elif tokens[0] == "ifEq":
			args = tokens[1:]

			if len(args) == 2:
				dest = "end"
			else:
				dest = args[2]
			if (dest=="end") ^ (resolve(args[0], src, localNames, localValues) == resolve(args[1], src, localNames, localValues)):
				while len(argParse(srcArr[currLine])) == 0 or argParse(srcArr[currLine])[0] != dest:
					currLine += -1 if dest=="while" else 1

		elif tokens[0] == "ifLess":
			args = tokens[1:]

			if len(args) == 2:
				dest = "end"
			else:
				dest = args[2]
			if (dest=="end") ^ (resolve(args[0], src, localNames, localValues) < resolve(args[1], src, localNames, localValues)):
				while len(argParse(srcArr[currLine])) == 0 or argParse(srcArr[currLine])[0] != dest:
					currLine += -1 if dest=="while" else 1

		else: # arbitrary function call
			verbose("root function call {{{}}}".format(srcArr[currLine]))
			resolve(srcArr[currLine], src, localNames, localValues)

if __name__ == "__main__":
	src = open(sys.argv[1], 'r+t').read()
	call(src, 'main', sys.argv[2:])

	# TODO: support -c funcname arg1 arg2 ...
	# and main args :
	# print (call(src, 'div', [506, 10]))