# Exchange Simulator – Feature Specification

This document defines the complete feature set of the **Exchange Simulator*- project.  
The system is intentionally designed to model the **core internals of a real financial exchange*- in a simplified, deterministic, and testable manner.

---

## A. Order Types & Trading Rules

### A1. Supported Order Types

The simulator supports **two order types**.

---

#### A1.1 Limit Orders

- Supports **BUY limit orders**
- Supports **SELL limit orders**
- Every limit order must include:
  - Price
  - Quantity

Limit orders:
- Can stay in the order book
- Are matched using price–time priority
- May be partially filled

---

#### A1.2 Market Orders

- Supports **BUY market orders**
- Supports **SELL market orders**
- Every market order must include:
  - Quantity only

Market orders:
- Execute **immediately**
- Do **not specify a price**
- Match against the **best available opposite orders**
- May generate **multiple trades**
- Do *not rest* - in the order book
- Any unfilled quantity is **discarded**

**Market orders guarantee execution, not price**.

---

### A2. Price–Time Priority Matching

Orders are matched using:

1. **Best price first**
2. **Earlier timestamp first**

This rule is applied independently for:
- Buy order book
- Sell order book

Market orders bypass price comparison and consume the best available prices directly.

---

### A3. Match Condition

For limit orders, a trade occurs when:

```bash
if BUY.price >= SELL.price
```


Market orders automatically satisfy this condition by accepting available prices.

---

### A4. Execution Price Rules

- **Limit orders*- execute at the **resting order price**
- **Market orders*- execute at the **best available resting prices**

This ensures:
- Deterministic execution for limit orders
- Realistic execution behavior for market orders

---

## B. Order Lifecycle Management

### B1. Order States

Each order can exist only in the following states:

- `NEW`
- `PARTIALLY_FILLED`
- `FILLED`

No other order states exist.

---

### B2. Partial Fills

- Limit orders may be partially filled  
  - Remaining quantity stays in the order book
- Market orders may be partially filled  
  - Remaining quantity is **discarded**

---

### B3. Full Fills

- Fully filled orders are removed from the system
- Market orders are removed immediately after execution

---

### B4. FIFO Processing

- Orders are processed strictly in arrival order
- Orders at the same price level follow **FIFO (time priority)**

---

## C. Order Book Features

### C1. Separate Buy & Sell Books

- Buy order book
- Sell order book
- Maintained independently

Only *limit orders*  are stored in the order book.

---

### C2. Heap-Based Priority Queues

- Buy orders stored as a **max-heap**
- Sell orders stored as a **min-heap**

This allows efficient retrieval of best prices.

---

### C3. Best Order Retrieval

- `get_best_buy()`
- `get_best_sell()`

Always returns the highest-priority **limit order**.

---

### C4. Order Book Integrity

The system guarantees:

- No duplicate orders
- No negative quantities
- No already-filled orders in the book
- No market orders stored in the book

---

## D. Matching Engine Capabilities

### D1. Continuous Matching

- Matching is triggered on every incoming order
- Continues until no valid matches exist

---

### D2. Multiple Trade Generation

- A single incoming order (limit or market) may generate multiple trades

---

### D3. Deterministic Behavior

- Same input order sequence → same trade results

---

### D4. Stateless Matching Logic

- Matching engine logic is stateless
- All state is maintained in:
  - Order book (in-memory)
  - Trade ledger (local JSON file)

---

## E. Trade Management

### E1. Trade Object Creation

Each trade includes:

- Trade ID
- Buy Order ID
- Sell Order ID
- Execution Price
- Quantity
- Timestamp

---

### E2. Append-Only Trade Ledger

- Trades are append-only
- No updates allowed
- No deletions allowed
- Full audit trail preserved

---

### E3. Trade History Access

- Trade history is read-only

---

## F. Order Flow & Intake

### F1. Order Validation

Each order is validated for:

- Valid side (`BUY` / `SELL`)
- Quantity > 0
- Price > 0 (**limit orders only**)

---

### F2. Order ID Generation

- Unique order ID assigned at intake

---

### F3. Timestamp Assignment

- Timestamp assigned at intake
- Used for FIFO ordering

---

### F4. Order Processing Flow

- Orders are processed sequentially
- Market orders are executed immediately
- Limit orders may enter the order book

---


## G. Persistence & Recovery Model
### G1. Runtime Storage

- Order book is maintained entirely in memory

- Matching engine performs no disk I/O during execution

- This ensures:

  - High performance

  - Clean and deterministic matching behavior

### G2. Shutdown Snapshot Persistence

On system shutdown:

- Only pending limit orders (NEW, PARTIALLY_FILLED) are serialized

- Orders are written to a local JSON snapshot file

- Fully filled orders are never persisted

### G3. Restart Recovery

On system startup:

- Order book is reconstructed from the JSON snapshot

- Matching resumes from the last known consistent state

This provides basic fault tolerance without affecting runtime performance.


## H. Testing & Verification

### H1. Market Simulation

- Randomized buy and sell order generation

- Configurable:
  - Price ranges
  - Quantity ranges

Supports both limit and market orders

---

## H2. End-to-End Flow Testing

- Simulates realistic order flow

- Feeds orders through the entire system

### H3. Deterministic Tests

- No randomness in test cases
- Fully reproducible results

---


## I. Testing & Verification

### I1. Unit Tests

- Order book behavior

- Matching engine logic

- Trade generation

### I2. Edge Case Coverage

- Empty order book

- No-match scenarios

- Partial fills

- Multiple fills

- Same-price FIFO behavior

- Market order execution

### I3. Deterministic Tests

- No randomness in test cases

- Fully reproducible results

## J. System Constraints (Intentional Design Choices)

### J1. Single Instrument

- Only one tradable symbol exists

---

### J2. Single-Threaded Execution

- No concurrency
- No race conditions

---
## K. System Constraints (Intentional Design Choices)
###  K1. Single Instrument

- Only one tradable symbol exists

### K2. Single-Threaded Execution

- No concurrency

- No race conditions

### K3. Storage Model Summary

- Matching and order book logic run fully in-memory

- Trade history stored in an append-only JSON file

- Pending limit orders persisted only during shutdown

## L. Multi-User Simulation Model (Single Engine + IPC Clients)

The simulator supports **multiple users trading from a single machine** using a **single matching engine process** and **multiple client processes** communicating via **Inter-Process Communication (IPC)**.\

```bash
Terminal 1 ── client.py ─┐
Terminal 2 ── client.py ─┼──► engine.py (ONE process)
Terminal 3 ── client.py ─┘        |
                                  ├─ Order Book (in memory)
                                  ├─ Matching Engine
                                  └─ Trade Ledger
```
This design closely mirrors real exchange architecture while remaining simple, deterministic, and suitable for learning.

---

### L1. Single Matching Engine (Authoritative State)

- The **matching engine runs as one dedicated process**
- The engine exclusively owns:
  - The in-memory order book
  - Matching logic
  - Trade generation
- The order book **never lives inside client processes**

This guarantees:
- One source of truth
- No duplicated state
- No race conditions

---

### L2. Multiple Clients via IPC

- Each user runs a separate **client process** (`client.py`)
- Clients communicate with the engine using **IPC (local sockets)**
- All communication happens on the same machine (`localhost`)

Example:

```bash
python engine.py
python client.py --user User_A
python client.py --user User_B
python client.py --user User_C
```

Each client:
- Acts as an independent trader
- Has its own `user_id`
- Sends orders to the engine
- Never directly accesses the order book

---

### L3. Why IPC (Local Sockets)

IPC using localhost sockets is chosen because it:

- Keeps the order book **fully in memory**
- Allows **multiple processes** to interact safely
- Avoids shared-memory complexity
- Is extremely fast on a single machine
- Matches real exchange client–gateway–engine models

There is **no internet usage** and **no network latency**.

---

### L4. Order Submission Flow

1. Client creates an order:
   - `user_id`
   - Side (BUY / SELL)
   - Type (LIMIT / MARKET)
   - Quantity
   - Price (limit orders only)

2. Client sends the order to the engine via IPC

3. Engine:
   - Validates the order
   - Assigns order ID and timestamp
   - Runs matching logic
   - Updates the in-memory order book
   - Appends trades to the trade ledger

Clients are **stateless** and only submit requests.

---

### L5. Deterministic Multi-User Behavior

Even with multiple users:

- Orders are processed **one at a time**
- No concurrency exists inside the engine
- Execution order is fully deterministic

Same submission sequence → same trades

---

### L6. Intentional Design Choice

This model is intentionally selected because it:

- Reflects real exchange architecture
- Keeps focus on **matching logic**, not infrastructure
- Is easy to test and debug
- Scales conceptually to real systems

This is a **learning-oriented exchange simulator**, not a production trading platform.