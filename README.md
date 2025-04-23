# cs358-project

🔧 Project Overview

You’re constructing a custom interpreter in Python from scratch. This interpreter will:
	1.	Represent code using an Abstract Syntax Tree (AST)
	2.	Evaluate the AST to produce results (no parsing yet)
	3.	Eventually parse code (but that’s for Milestone 2)

 🧠 Milestone 1 Goals (Now)

You need to implement:
	•	A basic expression language, including:
	•	Integer arithmetic (+, -, *, /)
	•	Boolean logic (and, or, not)
	•	Comparison (==, <)
	•	Variables and let bindings
	•	if conditionals
	•	A domain-specific extension (DSL), with:
	•	A new value type (e.g., strings, images, music, etc.)
	•	At least 2 literals of this type
	•	At least 2 custom operators that act on those literals

⸻

🎯 DSL Domain Choices

You can pick from the pre-approved list (no permission needed), which includes:

🗂️ File Requirements
	•	A single file: project/interp.py
	•	It should include:
	•	Your AST node classes/functions
	•	An eval() function for interpreting each expression
	•	A run() function to show the result (print, save, or display)
	•	A comment block at the bottom explaining your domain and how it’s used
	•	A few test cases using your AST + DSL, each wrapped in a run()

📌 Key Constraints
	•	Python only. Use functional-style interpretation (no OOP style).
	•	Dynamically typed language: values can be int, bool, or your DSL type.
	•	You must handle invalid inputs by raising exceptions (e.g., divide-by-zero, wrong types).
	•	Output types can vary: for example, strings are printed, images might open in a viewer, etc.
	•	Include any non-standard Python packages in a comment at the top.

⸻

📊 Grading
	•	50% for core interpreter (AST + eval)
	•	50% for DSL extension (types + ops + working demo)
	•	Syntax errors = big deduction, so make sure the code runs
