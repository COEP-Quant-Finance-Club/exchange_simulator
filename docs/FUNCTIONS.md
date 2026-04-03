# Exchange Simulator

A **simplified electronic exchange simulator** that models how real-world trading engines work.
The system supports limit and market orders, price–time priority matching, partial fills,
persistent order recovery across restarts, and real-time client notifications for executed trades.

The primary goal of this project is **clean architecture and separation of responsibilities**,
so that any developer can understand *what goes where* immediately.

---

## High-Level Architecture
```
Client (CLI)
↓
TCP Client
↓
TCP Server
↓
Exchange Engine
├── OrderBook (matching logic)
├── TradeWriter (async trade persistence)
├── OrderStore (order recovery)
└── Logger (audit logs)
```
---

## Core Concepts

- Orders are matched using **price–time priority**
- Orders can be **partially filled**
- Trades are **immutable and append-only**
- Active orders are **persisted on shutdown**
- Order book is **restored on startup**
- Clients are **notified when their orders are executed**

---

## Supported Features

- BUY / SELL orders
- LIMIT orders
- MARKET orders
- Partial fills
- Multiple matches per order
- Persistent order book
- Asynchronous trade logging
- Per-user audit logs
- Terminal-based client UI

---

## Project Structure & Responsibilities

This section defines **exactly what belongs where**.

---

## 1. Root Level

### `README.md`

**Purpose**
- Public-facing documentation

**Responsibilities**
- Describe the exchange simulator
- Explain high-level architecture
- How to run the engine, client, and simulator
- Explain persistence & recovery behavior

**Must NOT**
- Contain business logic
- Contain implementation details

---

### `tasks.md`

**Purpose**
- Internal development roadmap

**Responsibilities**
- Pending features
- Refactor notes
- Future enhancements

---

## 2. Client Layer (`client/`)

### `client/client.py`

**Purpose**
- Terminal-based user interface

**Responsibilities**
- Parse CLI arguments (`--user Alice`)
- Prompt user for:
  - BUY / SELL
  - Price
  - Quantity
- Display:
  - Order accepted / rejected messages
  - Trade execution notifications
  - Execution price and quantity

**Must NOT**
- Match orders
- Generate order IDs
- Modify order book
- Persist data

> This file is a **dumb UI**, not a decision-maker.

---

### `client/session_manager.py`

**Purpose**
- Maintain **per-user session order history**

**Responsibilities**
- Create `orders_userX.json` if missing
- Store new orders with status `NEW`
- Update order status (`PARTIALLY_FILLED`, `FILLED`)
- Load existing session orders on startup

**Must NOT**
- Match orders
- Calculate prices
- Handle sockets

---

## 3. Networking Layer (`networking/`)

### `networking/tcp_client.py`

**Purpose**
- Client-side TCP communication

**Responsibilities**
- Open TCP connection to engine
- Serialize orders to JSON
- Send orders to engine
- Receive responses
- Deserialize responses for client UI

**Must NOT**
- Prompt user
- Persist data
- Implement matching logic

---

### `networking/tcp_server.py`

**Purpose**
- Engine-side TCP gateway

**Responsibilities**
- Start TCP server
- Accept multiple clients
- Receive order JSON
- Forward orders to engine
- Send engine responses back to clients

**Must NOT**
- Match orders
- Modify order book
- Persist trades

> This file is a **bridge**, not the brain.

---

## 4. Engine Core (`engine/`)

### `engine/engine.py`

**Purpose**
- Core matching engine (the brain)

**Responsibilities**
- Receive validated orders
- Assign:
  - `order_id`
  - timestamp
- Route orders to the order book
- Coordinate matching
- Update order status
- Generate trade objects
- Build structured responses for clients
- Notify affected users when trades occur

**Must NOT**
- Perform file I/O directly
- Manage sockets
- Print terminal output

---

### `engine/order.py`

**Purpose**
- Define the **Order** data model

**Responsibilities**
- Store order attributes:
  - order_id
  - user
  - side
  - price
  - quantity
  - remaining_quantity
  - status
  - timestamp
- Handle order state transitions

**Must NOT**
- Match orders
- Access order book
- Read/write files

---

### `engine/orderbook.py`

**Purpose**
- Maintain unmatched orders and execute matching

**Responsibilities**
- Maintain:
  - BUY max-heap
  - SELL min-heap
- Enforce price–time priority
- Execute matches
- Update remaining quantities
- Return executed trades

**Must NOT**
- Generate order IDs
- Persist trades
- Communicate with clients

---

### `engine/trade.py`

**Purpose**
- Define executed trade structure

**Responsibilities**
- Trade attributes:
  - trade_id
  - buy_order_id
  - sell_order_id
  - price
  - quantity
  - timestamp

**Must NOT**
- Persist trades
- Decide matching logic

---

## 5. Persistence & Storage (`storage/`)

### `storage/order_store.py`

**Purpose**
- Persist active orders and restore order book state

**Responsibilities**
- Save `NEW` and `PARTIALLY_FILLED` orders on shutdown
- Load persisted orders on startup
- Reconstruct Order objects
- Provide snapshot-based recovery

**Must NOT**
- Match orders
- Modify order state
- Handle sockets

---

### `storage/trade_writer.py`

**Purpose**
- Asynchronous trade persistence

**Responsibilities**
- Append executed trades to `trades.json`
- Run in background (non-blocking)
- Ensure append-only guarantees

**Must NOT**
- Match orders
- Block engine execution

---

### `storage/trades/trades.json`

**Purpose**
- Global immutable trade ledger

**Rules**
- Append-only
- Never edited or deleted

---

### `storage/session_orders/orders_userX.json`

**Purpose**
- Per-user session order history

**Written by**
- `session_manager.py`

**Rules**
- Engine must not modify directly

---

### `storage/logs/logs_userX.txt`

**Purpose**
- Human-readable audit logs

**Written by**
- Logger utility

---

## 6. Utilities (`utils/`)

### `utils/helpers.py`

**Purpose**
- Shared utility functions

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
- Centralized logging

**Responsibilities**
- Write timestamped log messages
- User-specific logs
- Record order placement and trade execution events

---

## 7. Simulation (`simulation/`)

### `simulation/simulator.py`

**Purpose**
- Automated order generation

**Responsibilities**
- Generate random BUY/SELL orders
- Randomize price and quantity
- Send orders via TCP client
- Simulate real users

**Must NOT**
- Modify engine internals
- Match orders

---

## 8. Tests (`tests/`)

### `test_engine.py`
- Matching correctness
- Partial fills
- Multi-order matching

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
- Restore order book from disk
- Start TCP server

### `start_client.py`
- Launch client with CLI args

### `start_simulation.py`
- Run simulator mode

---

## Shutdown & Recovery Behavior

- On graceful shutdown:
  - Active orders are saved to disk
  - Trades are flushed
- On startup:
  - Orders are restored
  - Order book is rebuilt
  - Matching resumes seamlessly

---

## Design Philosophy

- Clear separation of concerns
- Deterministic matching
- Crash-safe persistence
- No hidden side effects

This project favors **clarity over cleverness**.
