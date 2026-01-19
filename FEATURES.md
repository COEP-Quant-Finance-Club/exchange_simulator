# Exchange Simulator – Feature Specification

This document defines the complete feature set of the **Exchange Simulator** project. The system is intentionally designed to model the *core internals* of a real financial exchange in a simplified, deterministic, and testable manner.

---

## A. Order Types & Trading Rules

### A1. Limit Orders Only

* Supports **BUY limit orders**
* Supports **SELL limit orders**
* Every order must include:

  * Price
  * Quantity
* No support for:

  * Market orders
  * Stop orders
  * Conditional orders

---

### A2. Price–Time Priority Matching

Orders are matched based on:

1. **Best price first**
2. **Earlier timestamp first**

This rule is applied independently for:

* Buy order book
* Sell order book

---

### A3. Match Condition

A trade occurs when:

```
BUY.price >= SELL.price
```

---

### A4. Execution Price Rule

* Trades execute at the **resting order price**
* Ensures:

  * Deterministic execution
  * Fair and predictable outcomes

---

## B. Order Lifecycle Management

### B1. Order States

Each order transitions through the following states only:

* `NEW`
* `PARTIALLY_FILLED`
* `FILLED`

No other order states exist.

---

### B2. Partial Fills

* Orders may be partially matched
* Remaining quantity stays active in the order book

---

### B3. Full Fills

* Fully filled orders are removed from the order book

---

### B4. FIFO Processing

* Orders are processed in strict arrival order
* Orders at the same price level respect **FIFO (time priority)**

---

## C. Order Book Features

### C1. Separate Buy & Sell Books

* Buy order book
* Sell order book
* Maintained independently

---

### C2. Heap-Based Priority Queues

* Buy orders stored as a **max-heap**
* Sell orders stored as a **min-heap**
* Enables efficient best-price retrieval

---

### C3. Best Order Retrieval

* `get_best_buy()`
* `get_best_sell()`

Always returns the highest-priority order based on price–time rules.

---

### C4. Order Book Integrity

The system guarantees:

* No duplicate orders
* No negative quantities
* No stale or already-filled orders

---

## D. Matching Engine Capabilities

### D1. Continuous Matching

* Matching is triggered on every new order
* Continues until no valid matches exist

---

### D2. Multiple Trade Generation

* A single incoming order may generate multiple trades

---

### D3. Deterministic Behavior

* Same input order sequence → same trades every time

---

### D4. Stateless Matching Logic

* Matching engine logic does not persist state
* All state is maintained in the order book(Local JSON File)

---

## E. Trade Management

### E1. Trade Object Creation

Each trade includes:

* Trade ID
* Buy Order ID
* Sell Order ID
* Execution Price
* Quantity
* Timestamp

---

### E2. Append-Only Trade Ledger

* Trades are only appended
* No updates or deletions allowed
* Full audit trail preserved

---

### E3. Trade History Access

* Read-only access to executed trades

---

## F. Order Flow & Intake

### F1. Order Validation

Each order is validated for:

* Valid side (`BUY` / `SELL`)
* Price > 0
* Quantity > 0

---

### F2. Order ID Generation

* Unique order ID assigned at intake

---

### F3. Timestamp Assignment

* Timestamp assigned at intake
* Used for FIFO ordering

---

### F4. FIFO Order Queue

* Orders stored in arrival order
* Released to the matching engine sequentially

---

## G. Simulation Features

### G1. Market Simulation

* Randomized buy & sell order generation
* Configurable:

  * Price ranges
  * Quantity ranges

---

### G2. End-to-End Flow Testing

* Simulates real order flow
* Feeds orders through the entire system

---

## H. Testing & Verification

### H1. Pytest Unit Tests

* Order book tests
* Matching engine tests
* Trade creation tests

---

### H2. Edge Case Coverage

* Empty order book
* No-match scenarios
* Partial matches
* Multiple matches
* Same-price FIFO behavior

---

### H3. Deterministic Tests

* No randomness in test cases
* Fully reproducible results

---

## I. Logging & Observability

### I1. Order Events Logging

* Order accepted
* Order matched
* Order filled

---

### I2. Trade Logging

* Trade execution logs
* Useful for debugging and analysis

---

## J. System Constraints (Intentional Design Choices)

### J1. Single Instrument

* Only one tradable symbol supported

---

### J2. Single-Threaded Execution

* No concurrency
* No race conditions

---

### J3. Storage Model

* Core exchange logic runs fully in-memory
* Optional JSON-based persistence for trade history
* Orders and order book remain in-memory only

