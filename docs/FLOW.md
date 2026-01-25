# Exchange Simulator – Detailed Project Flow

This document explains **how the Exchange Simulator works step by step**, including user input, engine matching, order book management, trade logging, session-level order history, and interactive user messages.

---

## 1. Start a User Session (Client)

Run the single client script for a new user:

```bash
python3 client.py --user Alice
```

* Each run represents **a new user session**.
* Users interact via **terminal input** (BUY/SELL, price, quantity).

**Inputs from user:**

* Side: BUY or SELL
* Quantity: integer > 0
* Price: integer > 0 (for Limit orders)

**Outputs to user:**

* Confirmation of order submission
* Status updates (`NEW`, `PARTIALLY_FILLED`, `FILLED`)

**Example message:**

```text
Order Placed Successfully!
Order ID: 101
Side: BUY
Quantity: 10
Price: 100
Status: NEW
```

---

## 2. Order Submission

* Client sends the order **over TCP** to the **Matching Engine**.
* Each order is a JSON object:

```json
{
  "user": "Alice",
  "side": "BUY",
  "price": 100,
  "quantity": 10,
  "timestamp": "2026-01-25T15:30:00"
}
```

* Optionally, the client can store the order **locally in session JSON** (`orders_userAlice.json`) immediately as `NEW`.

---

## 3. Matching Engine – Order Intake

When the engine receives an order:

1. **Validation**

   * Side is either BUY or SELL
   * Price > 0
   * Quantity > 0

2. **Assign Metadata**

   * Unique `order_id`
   * Timestamp if not already present

3. **Decision**

   * Check if the order can be **matched immediately** with opposite orders in the order book
   * Else, add to order book as **pending order**

---

## 4. Order Matching Logic

**Core Rules:**

1. **Price-Time Priority**

   * **Buy orders:** Higher price → priority
   * **Sell orders:** Lower price → priority
   * **Tie-breaker:** Earlier timestamp → priority

2. **Match Condition**

```text
If BUY.price >= SELL.price -> trade occurs
```

3. **Execution**

   * Trade quantity = minimum(BUY quantity, SELL quantity)
   * Trade price = resting order price (seller’s price for limit order)
   * Update quantities in the order book

**Interactive Message Example:**

```text
Trade Executed!
Buy Order ID: 101
Sell Order ID: 55
Traded Quantity: 6
Trade Price: 95
Remaining Quantity (if any): 4
```

For **market orders**:

```text
Market Order Completed!
Total Quantity Executed: 10
Average Price: 97.5
Total Cost: 975
```

---

## 5. Order Book Management

* **Separate books** for BUY and SELL:

  * BUY: max-heap (highest price on top)
  * SELL: min-heap (lowest price on top)
* Orders at same price → FIFO order
* Remaining unmatched quantity stays in the book
* Optional snapshot of current order book saved in `orders_userX.json`

---

## 6. Trade Logging

* Each executed trade is recorded as a **Trade Object**:

```json
{
  "trade_id": 101,
  "buy_order_id": 12,
  "sell_order_id": 23,
  "price": 95,
  "quantity": 6,
  "timestamp": "2026-01-25T15:31:00"
}
```

* Stored in **shared `trades.json`**
* **Immutable**: never edited or deleted
* Optional **plain text logs** per user in `logs_userX.txt`:

```
[2026-01-25 15:30:00] Order Placed: BUY 10 @ 100 (Order ID: 101)
[2026-01-25 15:31:00] Trade Executed: 6 units @ 95 (Buy ID:101, Sell ID:55)
```

---

## 7. Updating Order Status

After matching:

* If order fully matched → **status = FILLED**
* If partially matched → **status = PARTIALLY_FILLED**
* If unmatched → **status = NEW**

**Update session-level order history** for the user:

* Write back updated status to `orders_userX.json`

---

## 8. Respond Back to Client

* Engine sends **confirmation** back to user:

```text
Order #12 partially filled (4 units remaining)
Trade executed: 6 units at 95
```

* Client terminal **updates display** for interactive session
* **Market orders**: display total executed quantity, average price, total cost

---

## 9. Repeat Flow

1. User submits next order
2. Engine validates & matches
3. Order book updates
4. Trade ledger updates
5. Session history updates

This repeats until:

* User exits session, or
* Simulation ends

---

## Optional Simulation Mode

* Engine can accept **automatically generated orders**
* Useful for **demo or testing**
* Randomly generate:

  * BUY/SELL side
  * Price ranges
  * Quantity ranges
* Feeds orders to engine like a real client

---

## Key Notes / Assumptions

* **Single instrument** (stock)
* **No real money**
* **Single-threaded engine** (deterministic)
* **Multi-user simulated via multiple client processes**
* **Order book** = unmatched orders
* **Trades ledger** = executed trades
* **Session-level order history** = all orders submitted by that client
* **Interactive logging** shows order placement, trade execution, and market order totals

---

## Summary of Files(temporary)

| Component             | File / Storage              | Purpose                        |
| --------------------- | --------------------------- | ------------------------------ |
| Client                | `client.py`                 | Terminal input for user        |
| IPC         |             `tcp_client.py`, `tcp_server.py` | All networking and message passing 
| Engine                | `engine/engine.py`          | Receives orders, matches them  |
| Order Class           | `engine/order.py`           | Structure of orders            |
| Order Book            | `engine/orderbook.py`       | Maintains pending orders       |
| Trade Class           | `engine/trade.py`           | Structure of trades            |
| Session Order History | `storage/orders_userX.json` | Track user orders              |
| Trade Ledger          | `storage/trades.json`       | Record executed trades         |
| Simulation            | `simulation/simulator.py`   | Generate random orders         |
| Logs (optional)       | `storage/logs_userX.txt`    | Interactive messages / history |
| utils | `helpers.py` | helper funtions for json and file handling

---

## 🔹 Data Flow Overview

```text
client.py (user input)
       |
       v
   Matching Engine
       |
+------+------+
|             |
v             v
Order Book  Trades Ledger
(holds      (records executed trades)
pending orders)
       |
       v
Confirmation & Interactive Messages back to client
```

* Multiple **clients** can run simultaneously
* Single **engine process** handles all order matching
* Each client maintains its **session order history** separately
* **Interactive logging** shows real-time updates for users

## Required Libraries

| Library | Purpose |
|---------|---------|
| `socket` | To create TCP connections for client-engine communication (IPC) |
| `json` | To serialize and deserialize orders and trades to JSON format |
| `datetime` | To assign timestamps for FIFO order matching |
| `heapq` | To maintain buy/sell order books as priority queues (min/max heaps) |
| `threading` | Optional: to run engine and clients concurrently if needed |
| `random` | Optional: for simulation mode to generate random orders |
| `os` | For file operations like saving session JSON/log files |


## Folder structure
```
exchange-simulator/
│
├── README.md
├── tasks.md
│
├── client/
│   ├── client.py
│   ├── session_manager.py
│   └── __init__.py
│
├── networking/
│   ├── tcp_client.py
│   ├── tcp_server.py 
│   └── __init__.py
│
├── engine/
│   ├── engine.py                
│   │
│   ├── order.py                 
│   ├── orderbook.py             
│   ├── trade.py                 
│   │
│   └── __init__.py
│
├── simulation/
│   ├── simulator.py
│   └── __init__.py
│
├── storage/
│   ├── session_orders/
│   │   ├── orders_userAlice.json
│   │   └── orders_userBob.json
│   │
│   ├── trades/
│   │   └── trades.json           # Immutable trade ledger
│   │
│   ├── logs/
│   │   ├── logs_userAlice.txt
│   │   └── logs_userBob.txt
│   │
│   └── .gitkeep
│
├── utils/
│   ├── helpers.py        
│   ├── logger.py                
│   └── __init__.py
│
├── tests/
│   ├── test_engine.py
│   ├── test_orderbook.py
│   ├── test_networking.py
│   └── __init__.py
│
└── run/
    ├── start_engine.py
    ├── start_client.py         
    └── start_simulation.py     
```