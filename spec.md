
# Teaspoon Language Specification

## Syntax

### Comments
```
% This line is a comment
```

### Literals
The following literals are supported in Teaspoon.
```
80
-74
52.391
[10, 20, 30, 40]
"Hello, World!"
```
Arrays can be written with or without commas.
```
% all valid and equivalent:
[1,2,3,4,5]
[1, 2, 3, 4]
[1 2 3 4]
```
Under the hood, a numeric value is encapsulated in a monad array. Similarly string values are arrays of character codes.
```
% valid and equivalent:
[65.0 66.0 67.0 68.0]
"ABCD"

% valid and equivalent:
98
"b"
[98]
```

### Function Definitions
```
noop x :
  ret x
end function
```

### Function Calls
```
noop "a"
```
Additionally, expressions wrapped in parenthesis can be arguments.
```
print (noop (noop "b"))
```

### Assignment
```
x = "a"
y = noop "b"
z = noop (noop "c")
```

### IF and WHILE
```
if less x 98
print "x is less than 98.\n"
end

while less x 98
print "x is still less than 98.\n"
end
```
They can be nested without a problem.
```
if ILikeYou
  if YouLikeMe
    print "Lovely.\n"
  end
end
```
Note indentation has no effect on runtime. It is simply convention to indent nested groups with 2 or 4 spaces.

## Builtin Functions

To meet the Teaspoon Language Specification, an implementation must support the following built in functions.

| function name | arguments | side-effects                   | returns    |
|---------------|-----------|--------------------------------|------------|
| less          | a b       | none                           | a<b        |
| eq            | a b       | none                           | a==b       |
| sum           | a b c ... | none                           | a+b+c+...  |
| mul           | a b c ... | none                           | a\*b\*c\*...  |
| div           | a b c ... | none                           | a/b/c/...  |
| push          | arr v     | appends value v onto array arr | none       |
| get           | arr i     | none                           | arr[i]     |
| len           | arr       | none                           | arr.length |

## Extensions

### Foreword

Notice how `print` and `input` functions do not make the above list. Therefore, technically speaking, a fully unusable implementation that has no I/O capabilities is within specification.

This is because the specification wants to avoid requiring any *particular* IO mechanisms. Thus an implementation that relies on touchscreen interactions is just as valid as a command line interface or an xbox controller wired to a blender.

To keep things simple as possible for the end user, it is asked that IO is exposed directly through function calls. For example an especially low level implementation of Teaspoon that includes a `syscall` function giving access to all IO devices would be particularly unwanted--especially if the user codebase is executed in an interpreted environment.

### Introduction

Extensions are where all the real fun happens. Extensions additional components written in host languages that provide features additional to those specified above (Teaspoon Base).

#### Teaspoon Command Line (TCL)

```
implements {
	print
	input
}
```

#### Teaspoon Graphics Support (TGS)

```
implements {
	drawTri
	getEvent
}
```