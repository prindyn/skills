# Code Smell Checklist

Walk through each category systematically when reviewing code. Check off smells that are present and note their location.

---

## Category 1: Bloaters

Bloaters are things that have grown too large. They accumulate over time.

### Long Method
- [ ] Does any method exceed ~10 lines of non-trivial code?
- [ ] Are there comments inside a method that could be replaced by extracting a named method?
- [ ] Does any method contain both a loop and substantial logic outside the loop?
- [ ] Is there a conditional block long enough to warrant its own method?

**Location(s) found:** _______________

---

### Large Class
- [ ] Does any class have more than ~20 methods?
- [ ] Does any class exceed ~200 lines?
- [ ] Does any class seem to have two or more unrelated sets of responsibilities?
- [ ] Do some fields only matter for a subset of instances?

**Location(s) found:** _______________

---

### Primitive Obsession
- [ ] Are currency amounts, dates, ranges, or phone numbers stored as plain primitives?
- [ ] Are type codes stored as integers or strings instead of an enum or class?
- [ ] Are there string constants used as dictionary/array keys?
- [ ] Are there groups of primitives that always travel together?

**Location(s) found:** _______________

---

### Long Parameter List
- [ ] Does any method have more than 3–4 parameters (excluding `self`/`cls`)?
- [ ] Are there groups of parameters that are always passed together?
- [ ] Could some parameters be obtained by the method itself through a query?

**Location(s) found:** _______________

---

### Data Clumps
- [ ] Do the same 3+ fields appear together in multiple classes?
- [ ] Do the same 3+ parameters appear together in multiple method signatures?
- [ ] Would any one of those fields/parameters lose its meaning if the others were removed?

**Location(s) found:** _______________

---

## Category 2: Object-Orientation Abusers

OO is in place but the code is not thinking in objects.

### Switch Statements
- [ ] Are there `switch` / `if-elif-else` chains that check a type code or kind?
- [ ] Does the same type-checking condition appear in multiple places?
- [ ] Could behavior be dispatched by polymorphism instead?

**Location(s) found:** _______________

---

### Temporary Field
- [ ] Are there instance variables that are `None` / empty most of the time?
- [ ] Are there instance variables set only inside certain methods and not in `__init__`?
- [ ] Do certain methods only make sense when those fields are set?

**Location(s) found:** _______________

---

### Refused Bequest
- [ ] Does a subclass override parent methods to raise `NotImplementedError` or do nothing?
- [ ] Does a subclass use fewer than half of the inherited methods?
- [ ] Would the relationship be better expressed as composition?

**Location(s) found:** _______________

---

### Alternative Classes with Different Interfaces
- [ ] Are there two classes that do the same thing but with different method names?
- [ ] Could they share a common interface or superclass?

**Location(s) found:** _______________

---

## Category 3: Change Preventers

These make change expensive.

### Divergent Change
- [ ] When adding a new type/product/use-case, do you need to change many unrelated methods in the same class?
- [ ] Does the class have multiple reasons to change?

**Location(s) found:** _______________

---

### Shotgun Surgery
- [ ] When making one logical change, do you have to touch many different classes?
- [ ] Is related behavior scattered across multiple files?

**Location(s) found:** _______________

---

### Parallel Inheritance Hierarchies
- [ ] When you add a subclass in one hierarchy, do you have to add a corresponding subclass in another?
- [ ] Do two class hierarchies use the same naming prefix?

**Location(s) found:** _______________

---

## Category 4: Dispensables

These add no value and should be removed.

### Comments
- [ ] Are there comments that explain *what* the code does (rather than *why*)?
- [ ] Would the comment be unnecessary if the code were better named?
- [ ] Could the commented explanation become a method name instead?

**Location(s) found:** _______________

---

### Duplicate Code
- [ ] Are there two or more code fragments that look almost identical?
- [ ] Are there methods in sibling subclasses that do essentially the same thing?
- [ ] Is copy-paste visible in the git history?

**Location(s) found:** _______________

---

### Lazy Class
- [ ] Are there classes that do almost nothing?
- [ ] Have any classes been made very thin by prior refactoring?
- [ ] Are there subclasses that differ only in a constant value?

**Location(s) found:** _______________

---

### Data Class
- [ ] Does any class contain only fields plus getters and setters?
- [ ] Is there behavior elsewhere in the codebase that manipulates this class's data?

**Location(s) found:** _______________

---

### Dead Code
- [ ] Are there methods, classes, or parameters that are never called?
- [ ] Are there blocks guarded by a condition that can never be true?
- [ ] Are there commented-out blocks of code?

**Location(s) found:** _______________

---

### Speculative Generality
- [ ] Are there abstract classes or methods that have only one concrete implementation?
- [ ] Are there parameters that are never passed different values?
- [ ] Is there extension infrastructure that no current code exercises?

**Location(s) found:** _______________

---

## Category 5: Couplers

Excessive coupling between classes.

### Feature Envy
- [ ] Does any method access the data of another object far more than its own?
- [ ] Does a method use many getter calls on a foreign object in sequence?

**Location(s) found:** _______________

---

### Inappropriate Intimacy
- [ ] Does one class reach into the private fields of another?
- [ ] Do two classes call each other's private methods?
- [ ] Is there a bidirectional dependency where one direction is not needed?

**Location(s) found:** _______________

---

### Message Chains
- [ ] Are there chains like `a.getB().getC().doD()`?
- [ ] Does client code have to know the internal structure of an object graph?

**Location(s) found:** _______________

---

### Middle Man
- [ ] Does a class delegate more than half its methods to another class?
- [ ] Has aggressive use of Hide Delegate produced a class that does nothing itself?

**Location(s) found:** _______________

---

## Category 6: Other

### Incomplete Library Class
- [ ] Are there helper methods that exist because a library class is missing a feature?
- [ ] Are there wrapper/utility functions that work around a library's limitations?

**Location(s) found:** _______________

---

## Summary

| Category | # Smells Found | Severity |
|----------|----------------|----------|
| Bloaters | | |
| OO Abusers | | |
| Change Preventers | | |
| Dispensables | | |
| Couplers | | |
| Other | | |
| **Total** | | |
