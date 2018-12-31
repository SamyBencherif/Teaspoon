//
//  twowayTest.swift
//  TeaspoonGL
//
//  Created by Samy Bencherif on 12/28/18.
//  Copyright © 2018 Samy Bencherif. All rights reserved.
//

import JavaScriptCore
import Foundation


//function func_print(args, src, scopeNames, scopeValues) {
//verbose(`print ${resolve(args[0], src, scopeNames, scopeValues)} `)
//if (typeof resolve(args[0], src, scopeNames, scopeValues) == 'number')
//console.log(resolve(args[0], src, scopeNames, scopeValues))
//else
//console.log(jsString(resolve(args[0], src, scopeNames, scopeValues))) // process string literal or vars
//return;
//}

// swift_functions.print

@objc protocol TeaspoonBinding: JSExport {
    func func_print(msg:String) -> Void
    static func instantiate() -> Binding
}

class Binding: NSObject, TeaspoonBinding{
    func func_print(msg:String) -> Void {
        print(msg)
    }
    class func instantiate() -> Binding {
        return Binding()
    }
}

@objc protocol GreeterJSExports: JSExport {
    func func_print() -> Void
    func greetMe(_ name: String) -> Void
    static func instantiate() -> Greeter
    //any other properties you may want to export to JS runtime
    //var greetings: String {get set}
}

class Greeter: NSObject, GreeterJSExports {
    public func func_print() {
        print( "Hello World!")
    }
    
    public func greetMe(_ name: String) {
        print( "Hello, " + name + "!")
    }
    class func instantiate() -> Greeter {
        return Greeter()
    }
}

func evalJSWithBindings(src:String)
{
let context = JSContext()
context?.setObject(Binding.self, forKeyedSubscript: "Binding" as (NSCopying & NSObjectProtocol))
context?.evaluateScript(src)

let call = context?.objectForKeyedSubscript("call")

var teaSrc = """
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
    
call?.call(withArguments: [teaSrc, "main", [], [], []])
//print(jsValue1!)

}
