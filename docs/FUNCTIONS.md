# Exchange Simulator – File-Level Responsibilities (Developer Guide)

This document explains **what each file is responsible for**, what logic **must be implemented there**, and what **must not be implemented there**.  
The goal is that **any developer can open a file and immediately know what to build**.

---

## 1. Root Level

### `README.md`

**Purpose**
- Public-facing entry point for the project.

**Responsibilities**
- Describe what the Exchange Simulator is
- High-level architecture overview
- How to run:
  - Start engine
  - Start client
  - Start simulation mode
- Supported order types
- Key assumptions & limitations

**Must NOT contain**
- Deep implementation details
- Business logic

---

### `tasks.md`

**Purpose**
- Internal development roadmap.

**Responsibilities**
- Pending features
- Known limitations
- Refactor notes
- Future enhancements (market orders, persistence, multi-instrument, etc.)

**Audience**
- Developers only

---

## 2. Client Layer (`client/`)

### `client/client.py`

**Purpose**
- Terminal-based user interaction (UI layer).

**Responsibilities**
- Parse CLI arguments (`--user Alice`)
- Prompt user for:
  - BUY / SELL
  - Price
  - Quantity
- Display responses from engine
- Show order confirmation and trade execution messages

**Owns**
- User input handling
- Input validation (basic)
- Display formatting

**Must NOT**
- Match orders
- Generate order IDs
- Modify order book
- Decide order status

> This file is a **dumb UI**, not a decision-maker.

---

### `client/session_manager.py`

**Purpose**
- Manage **session-level order history** for a single user.

**Responsibilities**
- Create `orders_userX.json` if missing
- Store new orders with status `NEW`
- Update order status (`PARTIALLY_FILLED`, `FILLED`)
- Load existing session orders on startup

**Owns**
- Session JSON file I/O
- Mapping order_id → order status

**Must NOT**
- Match orders
- Calculate trade prices
- Handle socket communication

---

## 3. Networking Layer (`networking/`)

### `networking/tcp_client.py`

**Purpose**
- Client-side TCP communication abstraction.

**Responsibilities**
- Open TCP connection to engine
- Serialize order to JSON
- Send order to engine
- Receive engine response
- Deserialize response for `client.py`

**Owns**
- Client-side sockets
- JSON serialization/deserialization

**Must NOT**
- Prompt user
- Store session data
- Implement matching logic

---

### `networking/tcp_server.py`

**Purpose**
- Engine-side TCP server gateway.

**Responsibilities**
- Start TCP server
- Accept multiple client connections
- Receive order JSON
- Forward order to `engine.py`
- Send engine response back to client

**Owns**
- Socket lifecycle
- Client connection handling

**Must NOT**
- Match orders
- Modify order book
- Persist trades

> This file is a **bridge**, not the brain.

---

## 4. Engine Core (`engine/`)

### `engine/engine.py`

**Purpose**
- Core matching engine (the brain of the exchange).

**Responsibilities**
- Receive validated orders
- Assign:
  - `order_id`
  - timestamp
- Decide if order matches immediately
- Call `orderbook` for matching
- Generate trades
- Update order status
- Build response messages for client

**Owns**
- Order lifecycle
- Matching workflow
- Trade coordination

**Must NOT**
- Perform file I/O directly
- Manage sockets
- Print terminal output

---

### `engine/order.py`

**Purpose**
- Define the **Order** data model.

**Responsibilities**
- Order attributes:
  - order_id
  - user
  - side
  - price
  - quantity
  - remaining_quantity
  - status
  - timestamp
- Order state transitions

**Owns**
- Order behavior and state

**Must NOT**
- Match orders
- Access order book
- Read/write files

> Pure **data + behavior**.

---

### `engine/orderbook.py`

**Purpose**
- Maintain unmatched orders and execute matching.

**Responsibilities**
- Maintain:
  - BUY max-heap
  - SELL min-heap
- Enforce price-time priority
- Match incoming orders
- Update remaining quantities
- Return executed trades

**Owns**
- Matching mechanics
- Heap operations
- FIFO ordering at same price

**Must NOT**
- Generate order IDs
- Persist trades
- Communicate with clients

> This is **pure market logic**.

---

### `engine/trade.py`

**Purpose**
- Define executed trade structure.

**Responsibilities**
- Trade attributes:
  - trade_id
  - buy_order_id
  - sell_order_id
  - price
  - quantity
  - timestamp

**Owns**
- Trade object creation

**Must NOT**
- Persist trades
- Decide matching logic

---

## 5. Simulation (`simulation/`)

### `simulation/simulator.py`

**Purpose**
- Automated order generation for testing and demos.

**Responsibilities**
- Generate random BUY/SELL orders
- Randomize price and quantity
- Send orders via TCP client
- Simulate real clients

**Owns**
- Random order generation
- Timing control

**Must NOT**
- Modify engine internals
- Match orders

---

## 6. Storage (`storage/`)

### `storage/session_orders/orders_userX.json`

**Purpose**
- Per-user session order history.

**Written by**
- `session_manager.py`

**Contains**
- Orders submitted by that user
- Current order status

**Rules**
- Engine must not modify directly

---

### `storage/trades/trades.json`

**Purpose**
- Global immutable trade ledger.

**Written by**
- Engine (via helpers)

**Rules**
- Append-only
- Never edited or deleted

---

### `storage/logs/logs_userX.txt`

**Purpose**
- Human-readable audit log.

**Written by**
- Logger utility

**Contains**
- Order placements
- Trade executions
- Timestamps

---

## 7. Utilities (`utils/`)

### `utils/helpers.py`

**Purpose**
- Shared utility functions.

**Responsibilities**
- Safe JSON read/write
- Append-to-file helpers
- Timestamp generation
- Directory/file creation

**Must NOT**
- Contain business logic
- Know trading rules

---

### `utils/logger.py`

**Purpose**
- Centralized logging.

**Responsibilities**
- Write formatted log messages
- Timestamped entries
- User-specific logs

**Used by**
- Engine
- Client
- Session manager

---

## 8. Tests (`tests/`)

### `test_engine.py`
- Matching correctness
- Partial fills
- Multiple matches

### `test_orderbook.py`
- Heap behavior
- FIFO correctness
- Edge cases

### `test_networking.py`
- TCP connectivity
- JSON integrity

---

## 9. Run Scripts (`run/`)

### `start_engine.py`
- Initialize engine
- Start TCP server
- Keep process alive

### `start_client.py`
- Launch client with arguments

### `start_simulation.py`
- Run simulator mode

---
