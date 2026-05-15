# Code Smells Catalog

Code smells are indicators of problems that can be addressed during refactoring. They are easy to spot but may be symptoms of a deeper problem. Each smell entry follows the same shape: Signs & Symptoms → Reasons → Treatment → Payoff → When to Ignore.

---

## Part 1: Bloaters

Bloaters are code, methods, and classes that have grown to such proportions that they are hard to work with. They accumulate over time as a program evolves.

---

### Long Method

**Signs and Symptoms**
A method contains too many lines of code. Any method longer than ~10 lines should prompt questions.

**Reasons**
Something is always being added but nothing is ever taken out. Mentally it is harder to create a new method than to add two lines to an existing one — so the method keeps growing.

**Treatment**
- Use **Extract Method** to reduce the body length
- If local variables and parameters interfere with extraction, use **Replace Temp with Query**, **Introduce Parameter Object**, or **Preserve Whole Object**
- If none of those help, move the entire method via **Replace Method with Method Object**
- Conditionals → **Decompose Conditional**; loops → **Extract Method**

**Payoff**
- Short methods are the longest-lived OO code
- Long methods hide duplicate code

**Performance**
An increase in method count has negligible performance impact in almost all cases.

---

### Large Class

**Signs and Symptoms**
A class contains many fields, methods, or lines of code.

**Reasons**
Classes start small and grow as features accumulate. Adding to an existing class is mentally easier than creating a new one.

**Treatment**
- **Extract Class** — when part of the behavior can become a standalone component
- **Extract Subclass** — when part of the behavior is only used in rare cases or can be implemented differently
- **Extract Interface** — when you need to list the operations the client can use
- **Duplicate Observed Data** — when a large GUI class needs its data moved to a domain object

**Payoff**
- Reduces cognitive load; developers only need to know the fields relevant to their task
- Prevents duplication of code and functionality

---

### Primitive Obsession

**Signs and Symptoms**
- Using primitives (int, string, float) instead of small value objects (Money, Range, PhoneNumber)
- Using constants to code information (e.g., `USER_ADMIN_ROLE = 1`)
- Using string constants as field names in data arrays

**Reasons**
Primitive fields are created in moments of weakness — "just a field." Then another, then another.

**Treatment**
- Group related primitives into a class → **Replace Data Value with Object**
- When primitives are used as method parameters → **Introduce Parameter Object** or **Preserve Whole Object**
- When type-coding with constants → **Replace Type Code with Class**, **Replace Type Code with Subclasses**, or **Replace Type Code with State/Strategy**
- Arrays of mixed data → **Replace Array with Object**

**Payoff**
- More flexible, better-organized code
- Operations on data stay co-located rather than scattered
- Easier to find duplicate code

---

### Long Parameter List

**Signs and Symptoms**
More than three or four parameters for a method.

**Reasons**
- Multiple algorithms merged into one method, controlled by flags
- By-product of making classes independent: the code that creates an object was moved to the caller, so the created object is passed as a parameter

**Treatment**
- If a parameter is a result of calling another object's method → **Replace Parameter with Method Call**
- If parameters come from a single object → **Preserve Whole Object**
- If parameters come from different sources → **Introduce Parameter Object**

**Payoff**
- More readable, shorter code
- May reveal previously hidden duplicate code

**When to Ignore**
Do not remove parameters if doing so would introduce an unwanted dependency between classes.

---

### Data Clumps

**Signs and Symptoms**
Different parts of the code contain identical groups of variables (e.g., three fields that always appear together: `host`, `port`, `password` for a database connection). These clumps should become their own classes.

**Reasons**
Poor program structure or copy-paste programming. To test whether a clump is real: delete one value and see if the others still make sense. If not, it belongs in an object.

**Treatment**
- Fields that repeat as a group → **Extract Class**
- Same clump appears in method parameters → **Introduce Parameter Object**
- Some data passed to other methods → **Preserve Whole Object**

**Payoff**
- Operations on the data are now in a single place
- Reduces code size

**When to Ignore**
Passing an entire object (rather than its values) introduces a dependency between classes; sometimes primitive parameters are preferable.

---

## Part 2: Object-Orientation Abusers

These smells occur when code uses OO features incompletely or incorrectly. The structure is in place but the code inside refuses to think in objects.

---

### Switch Statements

**Signs and Symptoms**
Complex `switch` (or equivalent `if`/`else if`) statements, especially when the same condition appears in multiple places across the codebase.

**Reasons**
When object-oriented code is needed, polymorphism handles the branching automatically. Switch statements that check a type code to dispatch behavior are a sign that polymorphism is being missed.

**Treatment**
- Isolate the switch into a single method first with **Extract Method**, then move it with **Move Method**
- If a type code controls which class behavior to invoke → **Replace Type Code with Subclasses** or **Replace Type Code with State/Strategy**, then **Replace Conditional with Polymorphism**
- If only a few cases exist and the switch selects between different methods → **Replace Parameter with Explicit Methods**
- When one option is `null` → **Introduce Null Object**

**Payoff**
- Improved code organization; behavior moves to where the data lives
- Eliminates duplication when the same condition appeared in many places

**When to Ignore**
When a switch performs simple actions, there is no need to use polymorphism. Use polymorphism only when the same type-checking conditions appear in multiple places.

---

### Temporary Field

**Signs and Symptoms**
A class field that is only set and used in certain circumstances and is empty or `null` the rest of the time.

**Reasons**
Temporary fields are often created to avoid long parameter lists: rather than pass many values to a method, they were stuffed into fields. But now those fields only make sense in one context.

**Treatment**
- Move the temporary fields and the code that operates on them → **Extract Class**
- Eliminate the conditional code around these fields → **Introduce Null Object**

**Payoff**
- Better code clarity and organization

---

### Refused Bequest

**Signs and Symptoms**
A subclass inherits methods and data from a parent class but refuses to use them, or actively overrides them to do nothing.

**Reasons**
Someone used inheritance purely for code reuse but the new class has a fundamentally different interface.

**Treatment**
- If the subclass has nothing in common with the superclass → **Replace Inheritance with Delegation**
- If the inheritance hierarchy is appropriate but the subclass simply doesn't need all behavior → **Push Down Method** and **Push Down Field** to push the unwanted code into a sibling subclass

**Payoff**
- Cleaner class hierarchy; the inheritance relationship actually means something

---

### Alternative Classes with Different Interfaces

**Signs and Symptoms**
Two classes perform identical or very similar functions but their methods have different names or signatures.

**Reasons**
The programmer who created one class did not know the other existed.

**Treatment**
- **Rename Method** to make methods identical
- **Move Method**, **Add Parameter**, **Parameterize Method** to make protocols identical
- If only part of each class is duplicated → **Extract Superclass**

**Payoff**
- Eliminates unnecessary duplicate code
- Can ultimately reduce code size after merging the two classes

---

## Part 3: Change Preventers

These smells mean that when you need to change something in one place, you have to make many changes in other places too — making change expensive and risky.

---

### Divergent Change

**Signs and Symptoms**
When you make any change to a class you find yourself changing many unrelated methods in the same class (e.g., adding a new product type requires changing methods for finding, displaying, ordering, and invoicing that product all in the same class).

**Reasons**
Poor program structure or copy-paste programming. The Single Responsibility Principle is violated: the class is doing too many things.

**Treatment**
- Split up the behavior of the class → **Extract Class**
- If different classes have the same behavior → **Extract Superclass** or **Replace Type Code with Subclasses**

**Payoff**
- Better code organization
- Reduced code duplication
- Simpler support

---

### Shotgun Surgery

**Signs and Symptoms**
Making any modification requires many small changes to many different classes. The opposite of Divergent Change: one trigger → many classes.

**Reasons**
A single responsibility was scattered across multiple classes (often by someone trying to avoid Divergent Change and over-compensating).

**Treatment**
- Move existing class behaviors into a single class → **Move Method** and **Move Field**
- If no class is an appropriate home → **Extract Class**
- Bring all the pieces together: methods that call each other frequently → **Inline Class**

**Payoff**
- Better organization
- Less code duplication
- Easier maintenance

---

### Parallel Inheritance Hierarchies

**Signs and Symptoms**
Whenever you create a subclass for one class, you find yourself creating a subclass for another class too.

**Reasons**
A special case of Shotgun Surgery. The hierarchies grew in tandem without either being made the canonical home for the behavior.

**Treatment**
- Make instances of one hierarchy refer to instances of the other
- Use **Move Method** and **Move Field** to eliminate the hierarchy in the referring class

**Payoff**
- Reduces code duplication
- May improve code organization

---

## Part 4: Dispensables

Dispensable code is something pointless and unneeded whose absence would make the code cleaner, more efficient, and easier to understand.

---

### Comments

**Signs and Symptoms**
A method is filled with explanatory comments. Good comments explain *why*, not *what*. If a comment exists to explain *what* the code does, the code should be rewritten to be self-explanatory.

**Treatment**
- If a comment explains a complex expression → **Extract Variable**
- If a comment describes a block of code → **Extract Method** and name the method after the comment
- If a comment still feels necessary after extracting → use **Introduce Assertion** to make the assumption explicit

**When to Keep**
A comment explaining *why* something was done a non-obvious way is valuable and should stay.

---

### Duplicate Code

**Signs and Symptoms**
Two or more code fragments look almost identical.

**Reasons**
"Copy-paste programming." Multiple developers working on the same area simultaneously. Quick hacks under deadline pressure.

**Treatment**
- Same code in two methods of the same class → **Extract Method** + call it from both places
- Same code in two subclasses of the same level → **Extract Method** for both + **Pull Up Field** → **Pull Up Method** → **Pull Up Constructor Body** → **Form Template Method**
- Same code in two completely different classes → **Extract Superclass** (if the classes can share a parent) or **Extract Class** (if they cannot)

**Payoff**
- Any change only needs to be made in one place
- Code becomes shorter and simpler

---

### Lazy Class

**Signs and Symptoms**
A class that does very little — it is nearly empty, barely justifies its own existence, or was once useful but has been slimmed down over time.

**Treatment**
- Nearly useless subclasses → **Collapse Hierarchy**
- Other lazy classes → **Inline Class**

**When to Ignore**
Sometimes a Lazy Class is intentional — a skeleton kept for future extension or to express intent. Use judgement.

---

### Data Class

**Signs and Symptoms**
A class that contains only fields, getters, and setters. It is purely a data holder and has no real behavior.

**Reasons**
New classes typically start this way. The problem is when nothing more gets added — behavior that belongs with the data ends up scattered elsewhere.

**Treatment**
- Public fields → **Encapsulate Field**
- Collection fields → **Encapsulate Collection**
- Find which methods use the data and see if behavior can be moved here → **Move Method**
- After moving, the class likely has enough behavior to no longer be "just a data class"

**Payoff**
- Improved understanding
- Gives you a natural place for behavior that currently lives elsewhere

---

### Dead Code

**Signs and Symptoms**
A variable, parameter, field, method, or class that is no longer used anywhere.

**Reasons**
Requirements changed; the code was left behind. IDEs and compilers cannot always detect this automatically.

**Treatment**
- Unused parameter → **Remove Parameter**
- Unused method or class → delete it
- Unnecessary code in a method → **Inline Class** or **Collapse Hierarchy**

**Payoff**
- Smaller codebase
- Less confusion

---

### Speculative Generality

**Signs and Symptoms**
There is an unused class, method, field, or parameter that was added "just in case we need it someday." The code exists for hypothetical future use only.

**Treatment**
- Abstract classes doing very little → **Collapse Hierarchy**
- Delegation to another class that does almost nothing → **Inline Class**
- Unused method parameters → **Remove Parameter**
- Unused methods → **Inline Method**
- Methods with odd names invented for hypothetical callers → **Rename Method**

**When to Ignore**
Frameworks and libraries should retain their extensibility points even if not currently used.

---

## Part 5: Couplers

These smells involve excessive coupling between classes or problems that arise when coupling is replaced by excessive delegation.

---

### Feature Envy

**Signs and Symptoms**
A method accesses the data of another object more than it accesses its own data.

**Reasons**
The method belongs to the wrong class. It was placed in one class but uses the fields of another.

**Treatment**
- Move the method → **Move Method**
- If only part of the method suffers from envy → **Extract Method** the envious part, then **Move Method**

**Payoff**
- Reduces code duplication
- Better code organization

**When to Ignore**
Sometimes a method is intentionally placed in one class to allow changing the algorithm in a single place (e.g., Strategy, Visitor patterns). In these cases, keep the method where it is.

---

### Inappropriate Intimacy

**Signs and Symptoms**
One class uses the internal fields and methods of another class.

**Reasons**
Classes that are too close together have strong bidirectional dependencies.

**Treatment**
- If two classes are too intimate → **Move Method** and **Move Field** to redistribute their parts
- If they need to share data → **Extract Class** for the shared data
- Replace bidirectional association → **Change Bidirectional Association to Unidirectional**
- If a subclass is overly attached to its superclass → **Replace Delegation with Inheritance** (or vice versa)

---

### Message Chains

**Signs and Symptoms**
`a.getB().getC().getD().doSomething()` — a series of calls where the client navigates through intermediaries to get to the object it actually wants.

**Reasons**
Violates the Law of Demeter: only talk to your immediate neighbors.

**Treatment**
- **Hide Delegate** — add a method to the intermediate class that delegates directly
- Sometimes better to use **Extract Method** to extract the chain and **Move Method** to put it closer to where it is needed

**When to Ignore**
Aggressive hiding can produce many small "manager" classes. Use judgement about how much hiding adds value.

---

### Middle Man

**Signs and Symptoms**
A class exists that does nothing but delegate all its work to another class.

**Reasons**
Over-application of Hide Delegate, or a class that used to do real work but has been gradually emptied out by refactoring.

**Treatment**
- **Remove Middle Man** — talk directly to the object it delegates to
- If only a few methods delegate → **Inline Method** the delegation methods
- If there is still some behavior worth keeping → **Replace Delegation with Inheritance**

---

## Part 6: Other Smells

### Incomplete Library Class

**Signs and Symptoms**
A library class does not have all the methods you need, and you cannot or should not modify the library.

**Treatment**
- Adding a few methods to a library class → **Introduce Foreign Method** (add the method to the client class and call it from there)
- Adding many methods → **Introduce Local Extension** (create a subclass or wrapper that adds the missing methods)
