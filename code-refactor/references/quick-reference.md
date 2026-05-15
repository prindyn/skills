# Quick Reference: Smell → Technique → Pattern

Use this table as a fast lookup. Start from the smell you detected, find the recommended techniques, then check whether the result maps to a known design pattern.

## Smell → Technique Mapping

| Smell | Primary Technique(s) | Also Consider |
|-------|---------------------|---------------|
| Long Method | Extract Method | Replace Temp with Query, Decompose Conditional, Replace Method with Method Object |
| Large Class | Extract Class, Extract Subclass | Extract Interface, Duplicate Observed Data |
| Primitive Obsession | Replace Data Value with Object | Introduce Parameter Object, Replace Type Code with Class/Subclasses/State-Strategy |
| Long Parameter List | Introduce Parameter Object | Preserve Whole Object, Replace Parameter with Method Call |
| Data Clumps | Extract Class | Introduce Parameter Object, Preserve Whole Object |
| Switch Statements | Replace Conditional with Polymorphism | Replace Type Code with Subclasses, Introduce Null Object |
| Temporary Field | Extract Class | Introduce Null Object |
| Refused Bequest | Replace Inheritance with Delegation | Push Down Method, Push Down Field |
| Alternative Classes with Different Interfaces | Rename Method | Extract Superclass, Move Method |
| Divergent Change | Extract Class | Extract Superclass |
| Shotgun Surgery | Move Method, Move Field | Inline Class |
| Parallel Inheritance Hierarchies | Move Method, Move Field | — |
| Comments | Extract Method | Extract Variable, Introduce Assertion |
| Duplicate Code | Extract Method | Pull Up Method, Extract Superclass, Form Template Method |
| Lazy Class | Inline Class | Collapse Hierarchy |
| Data Class | Move Method | Encapsulate Field, Encapsulate Collection |
| Dead Code | Remove Parameter | Inline Method, Inline Class |
| Speculative Generality | Inline Class | Remove Parameter, Rename Method |
| Feature Envy | Move Method | Extract Method |
| Inappropriate Intimacy | Move Method, Move Field | Extract Class, Change Bidirectional Association to Unidirectional |
| Message Chains | Hide Delegate | Extract Method, Move Method |
| Middle Man | Remove Middle Man | Inline Method, Replace Delegation with Inheritance |
| Incomplete Library Class | Introduce Foreign Method | Introduce Local Extension |

---

## Technique → Pattern Pathway

After applying refactoring techniques, the result often naturally matches a design pattern. Use this as a hint.

| Technique Applied | Likely Target Pattern |
|-------------------|-----------------------|
| Replace Constructor with Factory Method | Factory Method |
| Multiple factory methods on an abstract class | Abstract Factory |
| Builder methods that return `this` for chaining | Builder |
| `clone()` on complex objects | Prototype |
| Static `getInstance()`, private constructor | Singleton |
| Wrapper implementing the same interface | Adapter / Decorator |
| Wrapper simplifying a complex subsystem | Facade |
| Replace Inheritance with Delegation (behavior choice) | Strategy |
| Replace Type Code with State/Strategy | State / Strategy |
| Replace Conditional with Polymorphism | Strategy / State / Command |
| Form Template Method | Template Method |
| Observer/notify pattern for field changes | Observer |
| Encapsulate a request as an object | Command |
| Wrap object access with permission/lazy logic | Proxy |
| Traverse children uniformly | Composite / Iterator |
| Mediate between many communicating objects | Mediator |
| Save/restore object state for undo | Memento |
| Double dispatch on element types | Visitor |
| Decouple abstraction from implementation | Bridge |
| Share immutable intrinsic state | Flyweight |
| Handle request in a chain of handlers | Chain of Responsibility |

---

## When to Apply a Pattern vs. When Not To

| Situation | Do | Don't |
|-----------|-----|-------|
| Same switch statement in multiple places | Replace with polymorphism (Strategy, State) | Add another case to the existing switch |
| Need multiple product families that must be consistent | Abstract Factory | Instantiate products directly |
| Constructing complex objects step-by-step | Builder | Overloaded constructors |
| Need to add behavior at runtime | Decorator | Create a subclass for every combination |
| Complex subsystem with many entry points | Facade | Expose every class to client |
| Many small objects with shared state | Flyweight | One object per representation |
| Only 1-2 algorithm variants, never changes | Simple if/else or subclass | Strategy (overkill) |
| Only one instance needed | Singleton | Global variable |

---

## Refactoring Technique Quick Index

### By Category

**Composing Methods**
Extract Method · Inline Method · Extract Variable · Inline Temp · Replace Temp with Query · Split Temporary Variable · Remove Assignments to Parameters · Replace Method with Method Object · Substitute Algorithm

**Moving Features between Objects**
Move Method · Move Field · Extract Class · Inline Class · Hide Delegate · Remove Middle Man · Introduce Foreign Method · Introduce Local Extension

**Organizing Data**
Self Encapsulate Field · Replace Data Value with Object · Change Value to Reference · Change Reference to Value · Replace Array with Object · Duplicate Observed Data · Change Unidirectional Association to Bidirectional · Change Bidirectional Association to Unidirectional · Replace Magic Number with Symbolic Constant · Encapsulate Field · Encapsulate Collection · Replace Type Code with Class · Replace Type Code with Subclasses · Replace Type Code with State/Strategy · Replace Subclass with Fields

**Simplifying Conditional Expressions**
Decompose Conditional · Consolidate Conditional Expression · Consolidate Duplicate Conditional Fragments · Remove Control Flag · Replace Nested Conditional with Guard Clauses · Replace Conditional with Polymorphism · Introduce Null Object · Introduce Assertion

**Simplifying Method Calls**
Rename Method · Add Parameter · Remove Parameter · Separate Query from Modifier · Parameterize Method · Replace Parameter with Explicit Methods · Preserve Whole Object · Replace Parameter with Method Call · Introduce Parameter Object · Remove Setting Method · Hide Method · Replace Constructor with Factory Method · Replace Error Code with Exception · Replace Exception with Test

**Dealing with Generalization**
Pull Up Field · Pull Up Method · Pull Up Constructor Body · Push Down Method · Push Down Field · Extract Subclass · Extract Superclass · Extract Interface · Collapse Hierarchy · Form Template Method · Replace Inheritance with Delegation · Replace Delegation with Inheritance
