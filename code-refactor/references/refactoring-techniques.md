# Refactoring Techniques Catalog

Each technique is presented as a recipe: the problem, the mechanical steps, and the trade-offs. Techniques are grouped into six catalogs. They cross-reference each other; you will rarely apply just one in isolation.

## Table of Contents
1. [Composing Methods](#1-composing-methods)
2. [Moving Features between Objects](#2-moving-features-between-objects)
3. [Organizing Data](#3-organizing-data)
4. [Simplifying Conditional Expressions](#4-simplifying-conditional-expressions)
5. [Simplifying Method Calls](#5-simplifying-method-calls)
6. [Dealing with Generalization](#6-dealing-with-generalization)

---

## 1. Composing Methods

These techniques restructure methods themselves — extracting, inlining, and rewriting.

### Extract Method
**Problem:** You have a code fragment that can be grouped together.
**Steps:**
1. Create a new method named after the *intent* of the code (not what it does mechanically)
2. Copy the extracted code into it
3. Pass any local variables the fragment reads as parameters
4. Replace local variables the fragment writes with return values (use an object if multiple values are needed)
5. Replace the original code with a call to the new method
**Trade-offs:** Too many tiny methods can make code hard to follow. Name the method well — that is the whole point.

### Inline Method
**Problem:** A method body is just as clear as its name. The indirection adds noise without adding meaning.
**Steps:**
1. Check that the method is not overridden in subclasses
2. Find all callers
3. Replace each call with the method body
4. Delete the method
**Trade-offs:** Not safe when the method is polymorphic.

### Extract Variable
**Problem:** A complex expression is hard to understand.
**Steps:**
1. Declare a new variable with a name that explains the expression's purpose
2. Assign the expression to it
3. Replace the original expression with the variable
**Trade-offs:** The variable only lives in the scope of the method. If the expression is used in more places, consider **Extract Method** instead.

### Inline Temp
**Problem:** A temp variable is assigned once from a simple expression and used only to simplify reading that one expression.
**Steps:**
1. Find all usages of the temp
2. Replace them with the right-hand side expression
3. Delete the temp declaration
**Trade-offs:** Only safe if the right-hand side has no side effects.

### Replace Temp with Query
**Problem:** A temp variable holds the result of an expression and is used in the same method.
**Steps:**
1. Extract the expression into a method
2. Replace uses of the temp with calls to the new method
3. Delete the temp
**Trade-offs:** Calling the method multiple times is only safe if it has no side effects. May cause a performance hit if the expression is expensive — worth it for clarity in most cases.

### Split Temporary Variable
**Problem:** A local variable is used for two or more different, unrelated purposes.
**Steps:**
1. Rename the variable at its first assignment to match its first purpose
2. Change all uses up to the second assignment
3. Declare a new variable at the second assignment for the second purpose
4. Repeat for any further re-assignments
**Trade-offs:** Clarifies intent; the original variable accumulation pattern is confusing.

### Remove Assignments to Parameters
**Problem:** A parameter is assigned a value inside the method body.
**Steps:**
1. Create a local variable initialized with the parameter value
2. Replace all uses of the parameter (after the assignment) with the local variable
**Trade-offs:** Assignments to parameters in Java/Python/C# change the local binding only; in languages with mutable references, this also prevents confusion about what is being mutated.

### Replace Method with Method Object
**Problem:** A long method uses many local variables in a way that prevents extraction.
**Steps:**
1. Create a new class named after the method
2. Give it a field for each local variable and parameter of the method
3. Add a constructor that takes the original object and all parameters; store them in fields
4. Copy the method body into an `execute()` (or `compute()`) method on the new class
5. Replace the original method with one that creates the object and calls `execute()`
**Trade-offs:** Introduces a new class; the trade-off is worth it when the method is genuinely complex.

### Substitute Algorithm
**Problem:** You want to replace an existing algorithm with a clearer one.
**Steps:**
1. Write the new algorithm (make sure it passes all existing tests)
2. Run tests — if they pass, delete the old algorithm
3. If tests fail, compare old and new behavior step by step
**Trade-offs:** Only do this for simple algorithms. For complex ones, use incremental refactoring first.

---

## 2. Moving Features between Objects

These techniques decide which class should own which methods and fields.

### Move Method
**Problem:** A method uses features of another class more than its own class.
**Steps:**
1. Check if the method is defined or used in subclasses of the source class
2. Declare the method in the target class
3. Copy the method body; adjust to reference the source object if needed
4. Change the source method to delegate to the target (or remove the source method if all callers can be updated)
**Trade-offs:** Improves cohesion; may increase coupling if a reference back is needed.

### Move Field
**Problem:** A field is used more by another class than by its own class.
**Steps:**
1. Create a field in the target class (with getter/setter if needed)
2. Find all uses of the source field
3. Replace them with accesses through the target class
4. Remove the field from the source class
**Trade-offs:** Simple to apply; watch for circular references.

### Extract Class
**Problem:** One class is doing work that should be done by two.
**Steps:**
1. Decide how to split the responsibilities
2. Create a new class to hold the extracted responsibilities
3. Add a reference from the old class to the new class
4. Move fields and methods one at a time, testing after each move
5. Consider whether the interface between the two objects should be exposed
**Trade-offs:** May introduce an additional level of indirection; new class becomes a clean abstraction.

### Inline Class
**Problem:** A class is doing almost nothing; its responsibilities should belong to another class.
**Steps:**
1. Declare all public methods of the dying class in the absorbing class; delegate to the dying class
2. Update all references to use the absorbing class
3. Move features one by one from the dying class to the absorbing class
4. Delete the dying class
**Trade-offs:** The opposite of Extract Class; use when the abstraction no longer earns its keep.

### Hide Delegate
**Problem:** A client is calling methods on an object retrieved from another object (message chain).
**Steps:**
1. Add a delegation method to the server class for each method of the delegate that is called by the client
2. Adjust the client to call the server's delegation method instead of the delegate directly
3. If the client no longer needs the delegate at all, remove the delegate accessor
**Trade-offs:** The server class grows. Only worth it when the delegate is an implementation detail.

### Remove Middle Man
**Problem:** A class is doing too much simple delegation (the inverse of Hide Delegate).
**Steps:**
1. Create an accessor for the delegate
2. For each delegating method, find the client calls and replace them with direct calls to the delegate
3. Remove the delegating methods
**Trade-offs:** Client classes now depend on the delegate directly.

### Introduce Foreign Method
**Problem:** A server class needs an additional method but you cannot modify the class (e.g., a library).
**Steps:**
1. Create the method in the client class
2. Pass an instance of the server class as the first parameter
3. Comment "// Foreign method; should be in ServerClass"
**Trade-offs:** This is a stopgap. If you end up with many foreign methods, switch to **Introduce Local Extension**.

### Introduce Local Extension
**Problem:** A server class needs several additional methods and you cannot modify it.
**Steps:**
1. Create an extension class (subclass or wrapper) of the server class
2. Add the new methods to the extension
3. Replace uses of the server class with the extension where the new methods are needed
**Trade-offs:** A subclass is simpler; a wrapper is needed if the server class is final/sealed.

---

## 3. Organizing Data

These techniques improve how data is stored, typed, and accessed.

### Self Encapsulate Field
**Problem:** You are accessing a field directly, but the coupling between the field and its callers is too tight.
**Steps:**
1. Create a getting and setting method for the field
2. Replace all direct accesses with calls to the getter/setter
**Trade-offs:** Allows subclasses to override the accessor. Overkill when the class is simple and small.

### Replace Data Value with Object
**Problem:** A data item needs additional data or behavior.
**Steps:**
1. Create the new class with a field for the original data value
2. Give the new class a getter for the value and a method to compare equality
3. Replace the field in the old class with an instance of the new class
4. Delegate accessor methods in the old class to the new object
**Trade-offs:** Small step toward a richer domain model.

### Change Value to Reference
**Problem:** You have a class with many equal instances that you want to replace with a single object.
**Steps:**
1. Use **Replace Constructor with Factory Method**
2. The factory method should return the same instance for equal values (use a registry/pool)
**Trade-offs:** Shared mutable references require careful attention to thread safety.

### Change Reference to Value
**Problem:** You have a reference object that is small, immutable, and hard to manage.
**Steps:**
1. Check that there is no dependency on the identity of the object
2. Make the class immutable
3. Remove any registration/lookup mechanism
4. Override equality comparison and hash code
**Trade-offs:** Value semantics make concurrency simpler; identity semantics are needed when the same object must change over time.

### Replace Array with Object
**Problem:** You have an array in which certain elements mean different things.
**Steps:**
1. Create a new class with a field for each element of the array
2. Replace the array with the new object
3. Add accessor methods named after what each element represents
**Trade-offs:** Arrays of homogeneous data should stay as arrays.

### Duplicate Observed Data
**Problem:** Domain data is stored in GUI classes; GUI and business logic need to be separated.
**Steps:**
1. Create a domain object for the data
2. Link the GUI component to the domain object (observer/event pattern)
3. Copy the data into the domain object and keep both synchronized
**Trade-offs:** Introduces two copies of data; requires a synchronization mechanism.

### Change Unidirectional Association to Bidirectional
**Problem:** Two classes need to use each other's features but only one has a reference to the other.
**Steps:**
1. Add a back-reference field to the class that does not currently hold the reference
2. Decide which class is the controller of the association
3. Update both sides whenever the association changes
**Trade-offs:** Bidirectional associations increase coupling; only add when genuinely needed.

### Change Bidirectional Association to Unidirectional
**Problem:** You have a bidirectional association but one class no longer needs features of the other.
**Steps:**
1. Examine the uses of the unnecessary back-reference
2. Apply **Replace Parameter with Method Call** or **Replace Temp with Query** to eliminate them
3. Remove the back-reference
**Trade-offs:** Simplifies the design; reduced coupling.

### Replace Magic Number with Symbolic Constant
**Problem:** You have a literal number with a special meaning.
**Steps:**
1. Create a constant and name it after the meaning of the number
2. Replace all occurrences of the literal with the constant
**Trade-offs:** Essential. There is almost no excuse for unexplained magic numbers.

### Encapsulate Field
**Problem:** A public field exists.
**Steps:**
1. Create getting and setting methods for the field
2. Change the field to private (or package-private)
3. Update all accesses
**Trade-offs:** The field is now protected from external direct writes; behavior can be added to the setter.

### Encapsulate Collection
**Problem:** A method returns a collection. Callers can modify the collection directly.
**Steps:**
1. Make the getter return a read-only view (unmodifiable list, etc.)
2. Replace any direct `add`/`remove` calls on the returned collection with dedicated methods on the owning class
**Trade-offs:** The owning class regains control over its collection's invariants.

### Replace Type Code with Class
**Problem:** A class has a numeric type code that does not affect behavior.
**Steps:**
1. Create a new class to represent the type code
2. Replace uses of the integer with the new class
**Trade-offs:** Compile-time type safety; only use when the type code does not affect conditional behavior.

### Replace Type Code with Subclasses
**Problem:** A type code affects the behavior of the class (different branches for different types).
**Steps:**
1. Create a subclass for each value of the type code
2. Make the appropriate method in each subclass override the conditional behavior
3. Remove the type code field
**Trade-offs:** Enables polymorphic dispatch; only possible when the type code does not change over time.

### Replace Type Code with State/Strategy
**Problem:** A type code affects behavior but cannot use inheritance (object changes type at runtime, or class already inherits from elsewhere).
**Steps:**
1. Apply **Replace Type Code with Class** to create a state/strategy hierarchy
2. Use **Move Method** and **Move Field** to put the type-specific behavior in the right subclass
3. Use **Replace Conditional with Polymorphism** to eliminate the conditionals
**Trade-offs:** More complex than subclassing; required when subclassing is not possible.

### Replace Subclass with Fields
**Problem:** Subclasses differ only in methods that return constant data.
**Steps:**
1. Add fields to the superclass for each constant return value
2. Change the subclass methods to return the field value
3. Declare a constructor in the superclass that sets the fields
4. Eliminate the subclasses
**Trade-offs:** Simplifies the hierarchy when the difference is purely in data, not behavior.

---

## 4. Simplifying Conditional Expressions

### Decompose Conditional
**Problem:** A complex conditional (`if`/`then`/`else`) makes it hard to see the logic.
**Steps:**
1. Extract the condition into a method with an explanatory name
2. Extract the then-branch into a method
3. Extract the else-branch into a method
**Trade-offs:** The intent of each branch becomes explicit.

### Consolidate Conditional Expression
**Problem:** Multiple conditionals with the same result can be written as a single condition.
**Steps:**
1. Check that all conditions have no side effects
2. Combine them with `&&` or `||` as appropriate
3. Use **Extract Method** on the combined condition
**Trade-offs:** Only consolidate when the combined expression has a single semantic meaning.

### Consolidate Duplicate Conditional Fragments
**Problem:** The same code appears in all branches of a conditional.
**Steps:**
1. Move the duplicated code outside the conditional
**Trade-offs:** Reduces code size and makes it clearer what varies between the branches.

### Remove Control Flag
**Problem:** You use a boolean variable as a control flag for multiple loops/conditionals instead of using `break`/`return`.
**Steps:**
1. Find the value assignments and uses of the control flag
2. Replace assignments with `break`, `continue`, or `return`
3. Remove the flag variable
**Trade-offs:** Modern control flow statements are clearer.

### Replace Nested Conditional with Guard Clauses
**Problem:** A method has complex conditional logic to determine normal execution flow.
**Steps:**
1. For each special case at the top of the method, replace it with a guard clause that returns early
2. Strip away the remaining nesting
**Trade-offs:** Reduces nesting dramatically; makes it clear which cases are exceptional vs. normal.

### Replace Conditional with Polymorphism
**Problem:** You have a conditional that performs different behavior depending on the type of an object.
**Steps:**
1. Create a class hierarchy for each branch of the conditional (or use an existing one)
2. Move the body of each conditional branch into an override of the polymorphic method in the appropriate subclass
3. Remove the original conditional
**Trade-offs:** The most powerful application of OO; only justified when the same type-checking conditional appears in many places.

### Introduce Null Object
**Problem:** Repeated `null` checks clutter the code.
**Steps:**
1. Create a null object class for the type being checked
2. Have the null object class return neutral/default behavior for all methods
3. Replace `null` returns and `null` checks with the null object
**Trade-offs:** Can hide programming errors; only use when the "do nothing" case is genuinely a first-class concept in the domain.

### Introduce Assertion
**Problem:** A section of code only works if certain conditions are true.
**Steps:**
1. Replace assumptions about state with assertion statements
**Trade-offs:** Assertions document and enforce invariants at the code level. Do not use for input validation — use proper error handling instead.

---

## 5. Simplifying Method Calls

These techniques make method interfaces cleaner and more self-documenting.

### Rename Method
**Problem:** A method name does not reveal its purpose.
**Steps:** Rename the method; update all callers.
**Trade-offs:** Most important refactoring. The name is the documentation.

### Add Parameter
**Problem:** A method needs more information from its caller.
**Steps:** Add the parameter; update all callers.
**Trade-offs:** Consider whether the parameter indicates Feature Envy; if so, Move Method may be better.

### Remove Parameter
**Problem:** A parameter is no longer used by the method body.
**Steps:** Remove the parameter; update all callers.
**Trade-offs:** Reduces the signature; breaks any callers not under your control (API concern).

### Separate Query from Modifier
**Problem:** A method returns a value and also has side effects.
**Steps:**
1. Create a query method that returns the value
2. Create a modifier method that produces the side effect
3. Replace calls to the original with calls to both (query first, then modifier)
**Trade-offs:** Commands and queries should be separate. This is the Command-Query Separation principle.

### Parameterize Method
**Problem:** Several methods do similar things but with different literal values in the body.
**Steps:**
1. Create a single method with a parameter for the varying value
2. Remove the original methods (or have them delegate)
**Trade-offs:** Reduces code size; only works when the differences are in the values, not the control flow.

### Replace Parameter with Explicit Methods
**Problem:** A method runs different code depending on the value of an enumerated parameter.
**Steps:**
1. Create a separate method for each value of the parameter
2. Eliminate the original parameterized method
**Trade-offs:** Inverse of **Parameterize Method**. Use when callers always know which branch they want.

### Preserve Whole Object
**Problem:** You are getting several values from an object and passing them as parameters to a method.
**Steps:**
1. Create a new parameter for the whole object
2. Change the method body to get the values from the object
3. Remove the individual parameters
**Trade-offs:** Reduces parameter list; increases coupling to the object's class. Skip if it would introduce an unwanted dependency.

### Replace Parameter with Method Call
**Problem:** A parameter is obtained by calling a method that the receiving method could call directly.
**Steps:**
1. Extract the parameter derivation into a query on the appropriate object
2. Replace the parameter with a call to that query
**Trade-offs:** Reduces parameter list; only possible when the receiving method has access to the object.

### Introduce Parameter Object
**Problem:** A group of parameters naturally belongs together (data clump in a method signature).
**Steps:**
1. Create a new class to represent the group of parameters
2. Update the method to take the new object as a parameter
3. Move behavior that belongs with the parameters into the new class
**Trade-offs:** Reduces the parameter list; the new class is a natural home for related behavior.

### Remove Setting Method
**Problem:** A field should be set only at creation time and never changed.
**Steps:**
1. Set the field in the constructor
2. Remove the setter
3. Make the field final/readonly
**Trade-offs:** Makes immutability explicit.

### Hide Method
**Problem:** A method is not used by any other class.
**Steps:** Make the method private (or package-private).
**Trade-offs:** Reduces the public API; makes the class easier to understand and change.

### Replace Constructor with Factory Method
**Problem:** You want to do more than simple construction when creating an object (e.g., return a subtype, cache instances, use a more descriptive name).
**Steps:**
1. Create a factory method with a descriptive name
2. Have it call the constructor
3. Replace direct constructor calls with factory method calls
**Trade-offs:** Constructors must return the exact class. Factory methods can return subtypes, apply caching, and have expressive names.

### Replace Error Code with Exception
**Problem:** A method returns a special error code instead of throwing an exception.
**Steps:**
1. Identify the error code and what conditions produce it
2. Replace the error code return with an appropriate exception
3. Update callers to handle the exception
**Trade-offs:** Exceptions make the "unhappy path" explicit and impossible to accidentally ignore.

### Replace Exception with Test
**Problem:** You throw an exception on a condition that could be checked before calling.
**Steps:**
1. Add a test before the call that checks the condition
2. Remove the try-catch that was handling the avoidable exception
**Trade-offs:** Exceptions should be for genuinely exceptional conditions; use conditional tests for expected cases.

---

## 6. Dealing with Generalization

These techniques reorganize inheritance hierarchies.

### Pull Up Field
**Problem:** Two subclasses have the same field.
**Steps:** Move the field to the superclass; remove it from the subclasses.

### Pull Up Method
**Problem:** Two subclasses have methods with identical results.
**Steps:**
1. Check the methods are truly identical (including fields they access)
2. If they reference fields not in the superclass, use **Pull Up Field** first
3. Move one method to the superclass; delete the duplicate

### Pull Up Constructor Body
**Problem:** Subclass constructors have largely identical code.
**Steps:**
1. Create a superclass constructor
2. Move the common initialization code into it
3. Call `super(...)` from each subclass constructor

### Push Down Method
**Problem:** Behavior in a superclass is only relevant to one subclass.
**Steps:**
1. Declare the method in the relevant subclass
2. Remove it from the superclass (or make it abstract)

### Push Down Field
**Problem:** A field is only used in some subclasses.
**Steps:**
1. Declare the field in the relevant subclasses
2. Remove it from the superclass

### Extract Subclass
**Problem:** A class has features used only in some instances.
**Steps:**
1. Create a subclass for the special-case features
2. Move the special features to the subclass using **Push Down Method** and **Push Down Field**
3. Find code that creates instances in the special-case context and change it to create the subclass

### Extract Superclass
**Problem:** Two classes with similar features — create a superclass and move the common features to it.
**Steps:**
1. Create an abstract superclass
2. Use **Pull Up Field**, **Pull Up Method**, and **Pull Up Constructor Body**

### Extract Interface
**Problem:** Several clients use the same subset of a class's interface, or the class needs to support multiple interfaces.
**Steps:**
1. Create a new interface
2. Have the class implement it
3. Change client types to use the interface

### Collapse Hierarchy
**Problem:** A superclass and subclass are not very different.
**Steps:**
1. Choose which class to keep
2. Use **Pull Up Method**, **Pull Up Field**, **Push Down Method**, **Push Down Field** as appropriate
3. Remove the eliminated class

### Form Template Method
**Problem:** Two methods in subclasses perform similar steps in the same order, with different implementations of the steps.
**Steps:**
1. Decompose the methods so that all differing parts are extracted into separate methods with the same signature
2. Pull up the skeleton method (the template) to the superclass
3. The step methods can be abstract or have a default implementation

### Replace Inheritance with Delegation
**Problem:** A subclass uses only part of the superclass interface and does not want to inherit all the parent data.
**Steps:**
1. Create a field in the subclass for the superclass object
2. Change each method in the subclass to delegate to the superclass object
3. Remove the inheritance declaration

### Replace Delegation with Inheritance
**Problem:** You are using delegation and are frequently writing many simple delegation methods to the full interface of the delegate.
**Steps:**
1. Make the delegating class a subclass of the delegate
2. Remove the delegation methods
**Trade-offs:** Only if the delegating class should have the full interface of the delegate.
