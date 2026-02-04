# Exchange Simulator – Pending Tasks

This document tracks **pending, in-progress, and planned work** for the Exchange Simulator.
Tasks are grouped by subsystem to make ownership and priorities clear.

---

## Engine Core

- [ ] Implement `ExchangeEngine` order intake flow
- [ ] Assign `order_id` and timestamps inside engine
- [ ] Integrate `OrderBook` with engine
- [ ] Handle partial fills and multi-match scenarios
- [ ] Build structured engine -> client response format
- [ ] Notify affected users when trades execute
- [ ] Graceful engine shutdown handling

---
## Order Model (`engine/order.py`)

- [x] Finalize `Order` data model fields
- [x] Implement order state transitions (`NEW → PARTIALLY_FILLED → FILLED`)
- [x] Track `remaining_quantity` correctly
- [x] Validate order attributes on creation
- [x] Implement helper methods:
  - [x] `apply_fill`
  - [x] `is_filled`
  - [x] `is_active`
- [x] Ensure order immutability for side and price
- [x] Add developer-friendly `__repr__`
- [ ] Write unit tests for order state transitions
--- 
## Order Book

- [x] Implement BUY max-heap with price–time priority
- [x] Implement SELL min-heap with price–time priority
- [x] Match LIMIT vs LIMIT orders
- [x] Match MARKET orders
- [x] Handle edge cases (empty book, partial fills)
- [x] Return executed trades in deterministic order

---

## Order Persistence

- [ ] Implement `OrderStore`
- [ ] Serialize active orders (`NEW`, `PARTIALLY_FILLED`)
- [ ] Persist orders to `orders.json` on shutdown
- [ ] Load persisted orders on startup
- [ ] Restore order book state correctly
- [ ] Handle missing or corrupt persistence files

---

## Trade Persistence

- [ ] Implement `TradeWriter`
- [ ] Append executed trades asynchronously
- [ ] Ensure non-blocking trade writes
- [ ] Guarantee append-only iibehavior
- [ ] Flush pending writes on shutdown

---

## Client Notifications

- [ ] Send trade execution messages to affected users
- [ ] Display execution price and quantity in client terminal
- [ ] Handle multiple fills for a single order
- [ ] Support asynchronous updates from engine

---

## Networking Layer

- [ ] Implement `tcp_server.py`
- [ ] Handle multiple client connections
- [ ] Validate incoming JSON payloads
- [ ] Forward orders to engine safely
- [ ] Return engine responses to correct client
- [ ] Handle client disconnects gracefully

- [ ] Implement `tcp_client.py`
- [ ] Serialize order requests
- [ ] Deserialize engine responses
- [ ] Support listening for async updates

---

## Client Layer

- [ ] Implement CLI input flow
- [ ] Validate user input (side, price, quantity)
- [ ] Display order confirmation messages
- [ ] Display trade execution notifications
- [ ] Integrate `session_manager.py`

---

## Session Management

- [ ] Implement `session_manager.py`
- [ ] Create per-user session files
- [ ] Store submitted orders
- [ ] Update order status on engine response
- [ ] Load previous session data on startup

---

## Logging & Utilities

- [ ] Implement `logger.py`
- [ ] Create user-specific audit logs
- [ ] Log order placements
- [ ] Log trade executions

- [ ] Implement `helpers.py`
- [ ] Safe JSON read/write helpers
- [ ] Append-to-file utilities
- [ ] Timestamp generation
- [ ] Directory creation utilities

---

## Simulation

- [ ] Implement `simulator.py`
- [ ] Generate random BUY/SELL orders
- [ ] Control order frequency
- [ ] Simulate multiple users

---

## Testing

- [ ] Write unit tests for `Order`
- [ ] Write unit tests for `OrderBook`
- [ ] Write engine integration tests
- [ ] Write networking tests
- [ ] Test persistence & recovery flow

---

## Documentation

- [ ] Finalize `README.md`
- [ ] Add inline docstrings
- [ ] Document shutdown & recovery behavior
- [ ] Add architecture diagrams

---

## Future Enhancements

- [ ] Cancel order support
- [ ] Modify order support
- [ ] Multiple instruments
- [ ] Order book snapshots
- [ ] Performance benchmarking
- [ ] Web-based UI

---
