//: [Previous](@previous)

import JavaScriptCore
import Foundation

@objc protocol GreeterJSExports: JSExport {
    func greet() -> Void
    func greetMe(_ name: String) -> Void
    static func getInstance() -> Greeter
    //any other properties you may want to export to JS runtime
    //var greetings: String {get set}
}

class Greeter: NSObject, GreeterJSExports {
    public func greet() {
        print( "Hello World!")
    }
    
    public func greetMe(_ name: String) {
        print( "Hello, " + name + "!")
    }
    class func getInstance() -> Greeter {
        return Greeter()
    }
}

let context = JSContext()
context?.setObject(Greeter.self, forKeyedSubscript: "Greeter" as (NSCopying & NSObjectProtocol))
let jsValue1 = context?.evaluateScript("(function(){ var greeter = Greeter.getInstance(); return greeter.greet()})()")
let jsValue2 = context?.evaluateScript("(function(){ var greeter = Greeter.getInstance(); return greeter.greetMe('rikesh')})()")

print(jsValue1!)
print(jsValue2!)

//: [Next](@next)
