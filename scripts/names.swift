import Foundation
let input = CommandLine.arguments[1]
let output = CommandLine.arguments[2]
let names = try JSONSerialization.jsonObject(with: Data(contentsOf:URL(fileURLWithPath:input))) as! [String]
var result = [String:String]()
for name in names {
 result[name] = name.applyingTransform(.toLatin, reverse:false)!.applyingTransform(.stripDiacritics, reverse:false)!
}
try JSONSerialization.data(withJSONObject:result,options:[.sortedKeys]).write(to:URL(fileURLWithPath:output))
