# Design Pattern Decision Tree

Use this guide when you have a refactoring need and want to find the right pattern to refactor toward. Start at the top and follow the questions.

---

## Step 1: What problem are you solving?

```
Are you solving a CREATION problem?
(how objects are made, what type is instantiated, how complex objects are built)
  → Go to Section A: Creational Patterns

Are you solving a STRUCTURE problem?
(how classes and objects are composed, connected, or wrapped)
  → Go to Section B: Structural Patterns

Are you solving a BEHAVIOR problem?
(how responsibilities are distributed, how objects communicate, how algorithms vary)
  → Go to Section C: Behavioral Patterns
```

---

## Section A: Creational Patterns

**Q: Do you need to create objects without specifying their exact class?**

```
Do subclasses decide which class to instantiate?
  → Factory Method

Do you need to create families of related objects?
  → Abstract Factory

Do you need to construct a complex object step by step?
  → Builder

Do you need to copy an existing object rather than create from scratch?
  → Prototype

Do you need exactly one instance of a class?
  → Singleton (use carefully — see trade-offs)
```

**Choosing between Factory Method and Abstract Factory:**
- Factory Method: one product type, one dimension of variation (the creator subclass)
- Abstract Factory: multiple product types that must be consistent with each other (a family)

**Choosing between Builder and Factory:**
- Use Builder when the construction process is complex, multi-step, or produces different representations
- Use Factory when you just need to decouple the caller from the concrete class

---

## Section B: Structural Patterns

**Q: What relationship are you trying to manage?**

```
Incompatible interface between two existing classes?
  → Adapter

Abstraction and implementation that should vary independently?
  → Bridge

Tree of objects that should be treated uniformly?
  → Composite

Adding behavior to an object without subclassing?
(especially when you need to combine behaviors at runtime)
  → Decorator

Simplifying access to a complex subsystem?
  → Facade

Many similar small objects consuming too much memory?
  → Flyweight

Controlling or intercepting access to an object?
(lazy init, access control, caching, remote access)
  → Proxy
```

**Adapter vs. Facade:**
- Adapter: makes one incompatible interface match an expected one (1:1 object wrapping)
- Facade: provides a simplified view of a complex subsystem (1:many)

**Decorator vs. Inheritance:**
- Use Decorator when you need to add behavior at runtime, or when the number of combinations would make subclassing impractical
- Use Inheritance when the behavior is invariant and known at compile time

**Proxy vs. Decorator:**
- Proxy: controls access, lifecycle, or location of the real subject
- Decorator: adds or overrides behavior transparently

---

## Section C: Behavioral Patterns

**Q: How should responsibilities be distributed?**

```
An object's behavior should change when its state changes?
  → State

You want to select an algorithm at runtime?
  → Strategy

You want to define a skeleton algorithm in a base class
and let subclasses fill in the steps?
  → Template Method

You need to traverse a collection without knowing its structure?
  → Iterator

You need to perform many different operations on an object structure
without modifying those objects?
  → Visitor
```

**Q: How should objects communicate?**

```
One object changes and many others need to know?
  → Observer

Many objects interact in complex ways and you want to centralize
the coordination?
  → Mediator

Objects in a chain should each get a chance to handle a request?
  → Chain of Responsibility

You want to encapsulate a request as an object
(for undo, logging, queuing, or parameterization)?
  → Command

You need to save and restore an object's state
(undo/redo, snapshots)?
  → Memento
```

---

## Pattern vs. Smell Alignment

| If you see this smell… | Consider this pattern |
|------------------------|-----------------------|
| Switch statements checking type code | **Strategy** or **State** |
| Long method with multiple algorithm variants | **Strategy** |
| Parallel inheritance hierarchies | **Bridge** |
| Feature envy toward a family of related classes | **Visitor** |
| Many small objects with shared representation | **Flyweight** |
| Repeated null checks | **Null Object** (not a GoF pattern, but a common idiom) |
| Many places creating objects of varying types | **Factory Method** |
| Inconsistent object families being constructed | **Abstract Factory** |
| Complex multi-step object construction | **Builder** |
| One-to-many notification dependency | **Observer** |
| Object needs to be undoable | **Command** + **Memento** |
| Subsystem too hard to use directly | **Facade** |
| Behavior needs to be added/removed at runtime | **Decorator** |
| Access to object needs to be controlled | **Proxy** |
| Tree structures of uniform-interface objects | **Composite** |

---

## Anti-Patterns: When NOT to Use a Pattern

| Pattern | Skip it when… |
|---------|---------------|
| Singleton | You are using it to avoid passing dependencies — use dependency injection instead |
| Observer | The update chain is complex and hard to debug — consider event buses or explicit calls |
| Abstract Factory | You have only one product family today — defer until the second family appears |
| Visitor | You frequently add new element types — the interface change cost is too high |
| Strategy | There are only 2–3 algorithms and they never change — a simple if/else is clearer |
| Decorator | Decoration depth is always 1 — just subclass or extend directly |
| Mediator | It becomes a "god object" — split into smaller, more focused coordinators |
| Factory Method | Every class has its own factory and they all just call `new` — pure boilerplate |
