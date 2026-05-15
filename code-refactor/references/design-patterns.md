# Design Patterns Catalog

The 22 classic GoF design patterns organized into three groups. Each entry covers: Intent, Problem it solves, Structure summary, Real-world analogy, and Trade-offs.

Design patterns are the catalog of shapes worth refactoring *toward*. They are proven solutions to commonly recurring design problems. Study them so you can recognize the situations where they apply — and also when they would be over-engineering.

## Table of Contents
- [Creational Patterns](#creational-patterns) — Factory Method, Abstract Factory, Builder, Prototype, Singleton
- [Structural Patterns](#structural-patterns) — Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- [Behavioral Patterns](#behavioral-patterns) — Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

---

## Creational Patterns

Creational patterns abstract the instantiation process. They help make systems independent of how their objects are created, composed, and represented.

---

### Factory Method

**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate. Defers instantiation to subclasses.

**Problem it solves:** A class cannot anticipate the class of objects it must create. You want subclasses to specify the objects they create.

**Structure:**
- `Creator` declares the factory method that returns a `Product`
- `ConcreteCreator` overrides the factory method to return a `ConcreteProduct`
- Client code calls the factory method on a Creator reference; it never calls `new` directly

**Real-world analogy:** A logistics company (Creator) has a `createTransport()` factory method. Road logistics returns `Truck`; sea logistics returns `Ship`. Client code works with the `Transport` interface without knowing which concrete class is used.

**Trade-offs:**
- Pro: Eliminates tight coupling between creator and concrete products; easy to add new products without changing existing code (Open/Closed Principle)
- Con: Requires a whole new subclass hierarchy; can become overly complex when all you need is a simple object

---

### Abstract Factory

**Intent:** Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**Problem it solves:** A system must be independent of how its products are created; you need to enforce a consistency constraint across a family of objects.

**Structure:**
- `AbstractFactory` declares creation methods for each product type in the family
- `ConcreteFactory` implements those methods for a specific product family
- Products within a family are designed to work together

**Real-world analogy:** A furniture factory interface declares `createChair()`, `createSofa()`, `createTable()`. `VictorianFactory` and `ModernFactory` implement it; all products from one factory share a consistent style.

**Trade-offs:**
- Pro: Guarantees compatibility between products; easy to swap product families
- Con: Hard to add new kinds of products (all factories must be updated); increases the number of classes

**vs. Factory Method:** Factory Method uses inheritance and relies on a subclass to supply the object. Abstract Factory uses composition and explicitly delegates object creation to a factory object.

---

### Builder

**Intent:** Separate the construction of a complex object from its representation so the same construction process can create different representations.

**Problem it solves:** Creating complex objects step by step; the same construction steps should produce different types/representations of an object.

**Structure:**
- `Builder` interface declares steps for building the product
- `ConcreteBuilder` implements the steps and tracks the state of the product being built
- `Director` defines the order of building steps (optional; client can drive directly)
- `Product` is the resulting object

**Real-world analogy:** Constructing a house: you can instruct a builder to build walls, install a roof, or add plumbing. Different builders (WoodenHouseBuilder, StoneHouseBuilder) follow the same steps but produce different results.

**Trade-offs:**
- Pro: Finer control over construction; step-by-step construction; same process → different products
- Con: Increases code complexity; overkill for simple object creation

---

### Prototype

**Intent:** Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

**Problem it solves:** Creating an object is expensive (deep copying of complex state) or the class is not known at runtime.

**Structure:**
- `Prototype` interface declares a `clone()` method
- `ConcretePrototype` implements `clone()` to copy itself

**Real-world analogy:** Cell division: a cell clones itself to produce another cell with the same DNA, rather than building a new cell from scratch.

**Trade-offs:**
- Pro: Clone complex objects without coupling to their concrete classes; alternative to subclassing for creating object variants
- Con: Cloning complex objects with circular references can be tricky (need to decide between shallow and deep copy)

---

### Singleton

**Intent:** Ensure a class has only one instance and provide a global access point to it.

**Problem it solves:** Some classes should have exactly one instance (a configuration object, a thread pool, a logger). Global variables let you access the object anywhere, but do not protect against multiple instances.

**Structure:**
- Static field holds the single instance
- Constructor is private
- Static `getInstance()` method returns the instance (creating it on first call)

**Trade-offs:**
- Pro: Controlled access to the sole instance; reduced namespace pollution compared to globals
- Con: Violates Single Responsibility Principle; makes unit testing difficult (hard to mock); can hide dependencies; tricky with multithreading (need double-checked locking or eager initialization)

---

## Structural Patterns

Structural patterns concern class and object composition — how to assemble objects and classes into larger structures while keeping those structures flexible and efficient.

---

### Adapter

**Intent:** Convert the interface of a class into another interface clients expect. Adapter lets classes work together that otherwise could not because of incompatible interfaces.

**Problem it solves:** You want to use an existing class but its interface does not match what you need.

**Structure (Object Adapter):**
- `Client` works with `Target` interface
- `Adapter` implements `Target`, holds a reference to an `Adaptee`
- `Adapter` translates calls from `Target` into calls on `Adaptee`

**Real-world analogy:** A travel adapter converts a US plug to a European socket. The laptop (client) knows only the US plug interface; the socket (adaptee) knows only the European interface.

**Trade-offs:**
- Pro: Allows reuse of existing classes without modifying them; separates interface conversion from business logic
- Con: Extra layer of indirection; class adapter (via multiple inheritance) is harder to set up

---

### Bridge

**Intent:** Decouple an abstraction from its implementation so that the two can vary independently.

**Problem it solves:** You want to avoid a permanent binding between an abstraction and its implementation; both should be independently extensible.

**Structure:**
- `Abstraction` holds a reference to an `Implementor`
- `RefinedAbstraction` extends the interface of the Abstraction
- `ConcreteImplementor` provides the actual implementation

**Real-world analogy:** A remote control (Abstraction) works with any TV (Implementor). You can add new remote types without changing TV classes, and new TV models without changing remotes.

**Trade-offs:**
- Pro: Decouples interface and implementation; both can grow independently; hides implementation details from clients
- Con: More complex design; the indirection can be confusing in simple cases

---

### Composite

**Intent:** Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

**Problem it solves:** You need to represent hierarchical structures (trees); clients should be able to ignore the difference between individual and composite objects.

**Structure:**
- `Component` interface for both leaf and composite objects
- `Leaf` implements `Component`; has no children
- `Composite` implements `Component`; stores child components and implements operations by delegating to children

**Real-world analogy:** A file system: files and directories both implement a `FileSystemItem` interface. A directory holds a list of items, each of which can be a file or another directory.

**Trade-offs:**
- Pro: Simplifies client code (treats leaves and composites the same); easy to add new component types
- Con: Can make the design overly general; hard to restrict what can be added to a composite

---

### Decorator

**Intent:** Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

**Problem it solves:** You want to add behavior to individual objects, not to an entire class; and you want to compose behaviors flexibly.

**Structure:**
- `Component` interface defines the basic operations
- `ConcreteComponent` is the base object
- `Decorator` wraps a Component and delegates to it
- `ConcreteDecorator` adds behavior before/after the delegation

**Real-world analogy:** A coffee shop: plain coffee is the base component. Add milk → `MilkDecorator`. Add sugar → `SugarDecorator`. Each wrapper adds its behavior while delegating to the wrapped object.

**Trade-offs:**
- Pro: More flexible than static inheritance; can compose behaviors at runtime; Single Responsibility: divide a feature-heavy class into smaller classes
- Con: Many small objects; decorators are hard to debug because calls wind through multiple layers

---

### Facade

**Intent:** Provide a simplified interface to a complex subsystem.

**Problem it solves:** A complex subsystem is hard for clients to use directly; you want to expose a high-level interface that covers the common use cases.

**Structure:**
- `Facade` class knows which subsystem classes are responsible for each request and delegates to them
- Subsystem classes are still accessible directly for advanced use

**Real-world analogy:** Calling customer support: the single phone number (facade) routes your call to the right department. You do not need to know the company's internal structure.

**Trade-offs:**
- Pro: Isolates clients from subsystem components; promotes weak coupling; simplifies the common case
- Con: Can become a "god object" that is coupled to everything; does not prevent direct access to subsystem

---

### Flyweight

**Intent:** Use sharing to support large numbers of fine-grained objects efficiently.

**Problem it solves:** A large number of similar objects is consuming too much memory. The objects' state can be split into intrinsic (shared) and extrinsic (context-dependent) parts.

**Structure:**
- `Flyweight` stores intrinsic state; accepts extrinsic state in method parameters
- `FlyweightFactory` creates and manages flyweight objects; returns existing instances instead of creating duplicates
- `Client` stores extrinsic state and passes it when calling flyweight methods

**Real-world analogy:** A text editor stores one `CharacterGlyph` object per distinct character (intrinsic: font, shape) rather than per character instance on the page. Position and color (extrinsic) are passed in at render time.

**Trade-offs:**
- Pro: Significant RAM savings when many similar objects are needed
- Con: Trades RAM for CPU (extrinsic state must be computed or passed every time); adds complexity; only worthwhile when the memory saving is significant

---

### Proxy

**Intent:** Provide a surrogate or placeholder for another object to control access to it.

**Problem it solves:** You need additional behavior when accessing an object (lazy initialization, access control, logging, caching) without changing the object's interface.

**Types of Proxy:**
- **Virtual Proxy:** Lazy initialization — creates the real object only when first needed
- **Protection Proxy:** Access control — checks permissions before forwarding requests
- **Remote Proxy:** Represents an object in a different address space
- **Caching Proxy:** Caches results of expensive operations

**Trade-offs:**
- Pro: Control access to the original object; lifecycle management; transparent to clients
- Con: Extra layer of indirection; can introduce latency; response from service may get delayed

---

## Behavioral Patterns

Behavioral patterns are concerned with algorithms and the assignment of responsibilities between objects.

---

### Chain of Responsibility

**Intent:** Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain.

**Problem it solves:** More than one object may handle a request; which object is not known at the time the request is made.

**Structure:**
- `Handler` interface declares a method to handle requests and an optional reference to the next handler
- Each `ConcreteHandler` either handles the request or passes it to the next handler

**Real-world analogy:** Technical support escalation: level-1 support handles simple issues; escalates to level-2 if needed; escalates further to specialists.

**Trade-offs:**
- Pro: Reduced coupling; flexible assignment of responsibilities at runtime
- Con: No guarantee that a request is handled; debugging can be difficult

---

### Command

**Intent:** Encapsulate a request as an object, allowing parameterization of clients with different requests, queuing, logging, and undoable operations.

**Problem it solves:** You need to parameterize objects by an action; support undo; support logging; support transaction-like behavior.

**Structure:**
- `Command` interface declares `execute()` (and optionally `undo()`)
- `ConcreteCommand` stores the receiver reference and calls receiver operations in `execute()`
- `Invoker` asks the command to execute the request
- `Receiver` knows how to perform the actual operations

**Real-world analogy:** A restaurant order: the waiter writes down your order (command) and takes it to the kitchen (invoker passes to receiver). The order can be queued, modified, or cancelled.

**Trade-offs:**
- Pro: Decouples invoker from receiver; easy undo/redo; easy to compose commands; supports logging
- Con: Extra class per command; can be over-engineering for simple cases

---

### Iterator

**Intent:** Provide a way to access elements of a collection sequentially without exposing its underlying representation.

**Problem it solves:** You want to traverse a collection without knowing its internal structure; you want multiple simultaneous traversals.

**Structure:**
- `Iterator` interface declares `hasNext()` and `next()`
- `ConcreteIterator` implements traversal for a specific collection
- `Aggregate` (Collection) creates an iterator

**Trade-offs:**
- Pro: Single Responsibility; clean traversal without exposing internal structure; supports multiple simultaneous traversals
- Con: May be overkill for simple collections; less efficient than direct index access for arrays

---

### Mediator

**Intent:** Define an object that encapsulates how a set of objects interact. Promotes loose coupling by keeping objects from referring to each other explicitly.

**Problem it solves:** Many objects communicate in complex, hard-to-change ways. The coupling makes reuse difficult.

**Structure:**
- `Mediator` interface declares communication methods
- `ConcreteMediator` coordinates interaction between `Colleague` objects
- Each `Colleague` only knows about the mediator, not about other colleagues

**Real-world analogy:** An air traffic controller (mediator) manages communication between aircraft (colleagues). Planes do not communicate directly with each other.

**Trade-offs:**
- Pro: Reduces coupling; centralizes control; simplifies object interactions
- Con: Mediator can become a "god object" that knows too much; single point of failure

---

### Memento

**Intent:** Without violating encapsulation, capture and externalize an object's internal state so the object can be restored to this state later.

**Problem it solves:** You need undo/redo or snapshot functionality but do not want to expose internal state.

**Structure:**
- `Originator` creates a memento containing a snapshot of its current state; can restore from a memento
- `Memento` stores the internal state of the Originator (opaque to everyone except the Originator)
- `Caretaker` holds the memento but never examines its contents

**Trade-offs:**
- Pro: Preserves encapsulation; easy undo implementation
- Con: Frequent mementos can be expensive in RAM; caretaker must know the originator's lifecycle

---

### Observer

**Intent:** Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**Problem it solves:** One object changes and others need to be informed, but you do not want tight coupling between them.

**Structure:**
- `Subject` (Observable) maintains a list of observers; notifies them on state change
- `Observer` interface declares the `update()` method
- `ConcreteObserver` implements `update()` to react to subject changes

**Real-world analogy:** A newspaper subscription: you subscribe (observe) and receive new issues (notifications) when they publish; you can unsubscribe at any time.

**Trade-offs:**
- Pro: Loose coupling; dynamic subscription; broadcast communication
- Con: Observers are notified in undefined order; can cause cascading updates; memory leaks if observers are not unregistered

---

### State

**Intent:** Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

**Problem it solves:** An object's behavior depends on its state, and it must change behavior at runtime depending on that state.

**Structure:**
- `Context` holds a reference to a `State` object representing the current state
- `State` interface declares methods for each behavior that varies with state
- `ConcreteState` classes implement state-specific behavior and manage transitions

**Real-world analogy:** A traffic light: same interface (`signal()`), but behavior changes depending on current state (Red, Yellow, Green).

**Trade-offs:**
- Pro: Eliminates large state-based conditionals; state transitions are explicit
- Con: If there are only a few states, the pattern is over-engineering; transition logic can be scattered across states

---

### Strategy

**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable. Lets the algorithm vary independently from clients that use it.

**Problem it solves:** Multiple variants of an algorithm exist; you want to select the algorithm at runtime or make it easily replaceable.

**Structure:**
- `Context` holds a reference to a `Strategy`
- `Strategy` interface declares the algorithm method
- `ConcreteStrategy` classes implement the algorithm

**Real-world analogy:** Navigation apps: a `Router` context selects a `RouteStrategy` (fastest route, shortest route, cycling route) at runtime based on user preference.

**Trade-offs:**
- Pro: Algorithm families can be defined and switched independently; eliminates conditionals; easy to add new strategies
- Con: Clients must be aware of different strategies and choose the right one; extra classes; overkill if there are only two or three variations

**Strategy vs. State:** Both use composition to delegate behavior. Strategy is about choosing an algorithm; the strategy object does not know about the context. State is about object lifecycle; state objects often hold a reference back to the context to trigger transitions.

---

### Template Method

**Intent:** Define the skeleton of an algorithm in a base class, deferring some steps to subclasses. Lets subclasses redefine certain steps without changing the algorithm's structure.

**Problem it solves:** Several classes implement the same algorithm but with varying steps. You want to avoid code duplication while keeping the invariant parts in one place.

**Structure:**
- Abstract base class defines the `templateMethod()` which calls abstract (or hook) methods in the right order
- Subclasses override the abstract steps

**Real-world analogy:** A housing construction template: the skeleton (pour foundation, build walls, add roof) is fixed; the specific house type (wooden, brick) varies the implementation of each step.

**Trade-offs:**
- Pro: Code reuse; the invariant part of the algorithm lives in one place (Open/Closed Principle for variations)
- Con: Template methods can be hard to maintain as they grow; Liskov Substitution Principle can be violated if subclasses change the algorithm's intent

**Template Method vs. Strategy:** Template Method uses inheritance; the variation happens at compile time. Strategy uses composition; the variation happens at runtime.

---

### Visitor

**Intent:** Represent an operation to be performed on elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

**Problem it solves:** You need to perform many distinct and unrelated operations on an object structure without polluting the classes of those objects.

**Structure:**
- `Visitor` interface declares a `visit()` method for each `ConcreteElement` type
- `ConcreteVisitor` implements each visit method with the specific operation
- `Element` interface declares an `accept(visitor)` method
- `ConcreteElement` implements `accept()` by calling `visitor.visit(this)`

**Real-world analogy:** A tax inspector visits different types of buildings and calculates taxes differently for residential vs. commercial properties — without changing the building classes.

**Trade-offs:**
- Pro: Open/Closed for new operations (add a new visitor without changing elements); consolidates related operations in one place
- Con: Open/Closed violated for new element types (must add a new `visit()` method to every visitor); Visitor requires access to private state, which may break encapsulation

### Visitor and Double Dispatch

Visitor relies on double dispatch: the operation executed depends on the type of *both* the visitor and the element. When `element.accept(visitor)` is called, the element's `accept()` calls back `visitor.visit(this)` — and at that point both the concrete visitor type and the concrete element type are known to the runtime. Languages without multimethods (Java, C#, Python) require this two-call pattern to achieve the same effect.
