
var VERBOSE = false
var VERSION = ["base"]
var EXTENSIONS = {}

func verbose(_ info : String) {
    // condition improves performance
    if (VERBOSE)
    {
        print(info)
    }
}

func argParse(line: String) -> [String]
{
    var k : [String] = []
    var inQuotes : Bool = false
    var acc : String = ""
    
    for i in line
    {
        if (i == " " || i == "\t") && acc == ""
        {
            continue
        }
        if (i == "\"")
        {
            inQuotes = !inQuotes
        }
        if (!inQuotes && i == " ")
        {
            k.append(acc)
            acc = ""
        } else
        {
            acc += String(i)
        }
    }
    
    if (acc != "")
    {
        k.append(acc)
    }
    
    return k
}

public func call(src:String, identifier:String = "main", args:[String] = [], injectNames:[String] = [], injectValues:[[Int]] = []) -> [[Int]]
{
    
    var currLine:Int = 0
    var tokens : [String]
    
    let srcArr : [Substring] = src.split(separator: "\n")
    
    for line in srcArr {
        tokens = argParse(line: String(line))
        if (tokens.count != 0 && tokens[0] == identifier && tokens[tokens.count - 1] == ":")
        {
            break;
        }
        currLine += 1
    }
    
    if (currLine == srcArr.count) {
        fatalError("Symbol " + identifier + " is not defined.")
    }
    
    var i = currLine;
    while i < srcArr.count {
        tokens = argParse(line: String(srcArr[i]))
        if (tokens.count != 0 && tokens[0] == "ret")
        {
            break
        }
        i += 1
    }
    
    let retLoc = i
    
    tokens = argParse(line: String(srcArr[currLine]))
    verbose("function header " + srcArr[currLine]);
    verbose("arg tokens " + tokens.joined(separator: ","));
    
    return []
}

let src = """
cat x y :
i = 0
while :
c = get y i
add x c
i = sum i 1
ly = len y
ifLess i ly while
ret x

hello a :
msg = "hello"
% this is a comment
cat msg " "
cat msg a
print msg
ret

main :
c = 0
while :
p = sum c 48
hello [p]
c = sum c 1
ifEq c 10 skip
ifEq 0 0 while

skip :
ifEq c 10
print "That was cool!"
end :
ret
"""

call(src: src, identifier: "main", args: [], injectNames: [], injectValues: [])
