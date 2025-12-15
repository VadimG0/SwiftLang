// SwiftLang Sample Script (NOT WORKING)
let count = 0;
let name = "Alice";
let values = [1, 2, 3, 4.5, true, null];
let config = {"debug": false, "port": 8080};

fun add(a, b) {
    return a + b;
}

if count > 0 {
    print("Count is positive");
} else {
    print("Count is zero or negative");
}

for i in values {
    if i == null { continue; }
    count = count + 1;
}

try {
    let result = add(5, 3);
    print("5 + 3 = " + result);
} catch (err) {
    print("Error: " + err);
}

/* Multi-line
   comment */
let count = 42;  // Duplicate!