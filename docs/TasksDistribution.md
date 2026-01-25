# Exchange Simulator – Team Task Division (Adjusted for Skill Levels)

This task division is designed considering:
- Mixed skill levels
- Limited DSA knowledge across the team
- Mandatory inclusion of all members in actual coding
- Low risk of project failure

## Member 1 – Lead Developer (Bhavesh)

**Role**
- Own all *hard logic* so nothing breaks.

### Files Owned
- `engine/engine.py`
- `engine/orderbook.py`
- `engine/order.py`
- `engine/trade.py`
- `run/start_engine.py`

### Responsibilities
- Order matching logic
- Price-time priority
- Partial fills
- Trade generation
- Overall architecture
- Integration of all modules

 **Why**
- Centralizes complexity
- Prevents dependency deadlocks
- You can explain everything in viva/interview

---

##  Member 2 – Networking & Flow Control (Basic DSA)

**Role**
- Make things talk to each other.

### Files Owned
- `networking/tcp_client.py`
- `networking/tcp_server.py`
- `run/start_client.py`

### Responsibilities
- TCP connection setup
- JSON send/receive
- Forward requests to engine
- Return engine responses

**Why**
- Minimal algorithms
- Mostly structured flow
- DSA knowledge not heavily required

---

## Member 3 – Testing & Integration (Basic DSA)

**Role**
- Verify that the system behaves correctly.

### Files Owned
- `tests/test_engine.py`
- `tests/test_orderbook.py`
- `tests/test_networking.py`

### Responsibilities
- Write test cases
- Validate matching outcomes
- Test edge cases
- Ensure no regressions

**Why**
- Uses logic understanding, not creation
- Improves confidence in system
- Good learning role

---

## Member 4 – Client UI & Session Handling (Low DSA)

**Role**
- User-facing interaction and persistence.

### Files Owned
- `client/client.py`
- `client/session_manager.py`

### Responsibilities
- Terminal input handling
- Display responses
- Create/update `orders_userX.json`
- Maintain session order history

**Why**
- Real coding
- No algorithmic complexity
- Clear, visible contribution

---

## Member 5 – Utilities, Logging & Simulation (Low DSA)

**Role**

- Support systems & automation.

### Files Owned
- `utils/helpers.py`
- `utils/logger.py`
- `simulation/simulator.py`
- `storage/` folder setup

### Responsibilities
- JSON helpers
- File/directory creation
- Logging logic
- Random order generation
- Append-only trade logging support

 **Why**
- Backend coding without heavy DSA
- Essential to system
- Not reduced to documentation

---

## Shared Responsibilities

| Task | Members |
|----|-------|
| README.md |  ALL |
| tasks.md | All |
| Debugging | All |
| Final integration | Bhavesh |


---

