// =======================================
// SwiftLang Feature Showcase (WORKING)
// =======================================

/* Multi-line comment
   demonstrating comment support */

let a = 10;
let b = 3;
let c = 2.5;
let message = "Result:";
let flag = true;

// Arithmetic expressions
let sum = a + b;
let diff = a - b;
let prod = a * b;
let quot = a / b;
let rem = a % b;

// Relational operators
print(a > b);
print(a < b);
print(a == b);
print(a != b);

// Boolean logic
print(flag and true);
print(flag or false);
print(not false);

// Grouping with parentheses
let expr = (a + b) * c;
print(expr);

// Dynamic typing (type changes allowed)
let x = 5;
print(x);
x = "now a string";
print(x);
x = false;
print(x);

// If / else statement
if (a > b) {
    print("a is greater than b");
} else {
    print("a is NOT greater than b");
}

// While loop
let counter = 0;
while (counter < 3) {
    print(counter);
    counter = counter + 1;
}

// Read input (string)
let userInput = "placeholder";
print(userInput);
read(userInput);
print(userInput);

// Null literal
let nothing = null;
print(nothing);

// End of program
print("Done.");
