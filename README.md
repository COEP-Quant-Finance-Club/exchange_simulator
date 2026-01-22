# Exchange Simulator

The **Exchange Simulator** is a learning project that shows **how buying and selling happens inside a real stock exchange**, in a very simple and understandable way.

---

## What Is an Exchange?

An exchange is a system where:
- Some people want to **buy**
- Some people want to **sell**
- The system decides:
  - who trades with whom
  - at what price
  - and in what order

In this project:
- We assume there is **only one stock**
- Users are **not concerned about which stock** they are buying or selling

The goal is to understand **how matching works**, not stock names.

--- 

## What Kind of Orders Are Allowed?
This simulator accepts **only one type of order**.

### Limit Orders

A limit order means:
- You choose the **price**
- You choose the **quantity**

Examples:
- “I want to BUY 10 units at price 100”
- “I want to SELL 5 units at price 98”

There are **no other order types**.

This is done intentionally to keep the project simple and easy to understand.

---

## How Does Matching Work?

A trade happens when:
- A buyer is willing to pay **the same or higher price**
- A seller is willing to sell **at that price**

### Simple Rule
```bash
If buyer’s price ≥ seller’s price → trade happens
```
If this condition is not satisfied, the orders simply wait.

---

## Who Gets Priority?

The system follows **two simple priority rules**.

### Rule 1: Price Priority
- Buyers offering **higher price** get matched first
- Sellers asking **lower price** get matched first

### Rule 2: Time Priority
- If prices are the same, the **earlier order goes first**

So:
- Better price always wins
- Same price → first come, first served

This is how fairness is maintained.

---

## How the Engine Works (With Examples)

Think of the engine like a **referee**.  
It checks orders **one by one** and follows the same rules every time.

---

### Example 1: No Trade Happens

1. BUY 10 units at price 100  
2. SELL 5 units at price 110  

Check:
- Buyer price = 100
- Seller price = 110  

Since 100 < 110 → no trade

Both orders wait.

---

### Example 2: Trade Happens

3. SELL 6 units at price 95  

Check:
- Best buyer = 100
- Best seller = 95  

Since 100 ≥ 95 → trade happens

- Traded quantity = 6
- Trade price = 95

Remaining:
- Buyer still wants 4 units
- Seller is fully done

---

### Example 3: Same Price, Earlier Order First

Orders come in this order:
1. BUY 5 units at price 100  
2. BUY 5 units at price 100  

Then:
3. SELL 6 units at price 100  

What happens:
- First buyer gets 5 units
- Second buyer gets remaining 1 unit

Earlier order gets priority.

---

### Example 4: One Order Matches Many Orders

Waiting BUY orders:
- BUY 5 at price 105
- BUY 5 at price 102
- BUY 5 at price 100

New order:
- SELL 12 at price 100  

Matching happens step by step:
- Match with 105 → 5 units
- Match with 102 → 5 units
- Match with 100 → 2 units

One order creates **multiple trades**.

---

## What Happens After Matching?

An order can be:
- **Fully completed** → all quantity traded
- **Partially completed** → some quantity traded

If quantity is left:
- It stays in the system
- It waits for future matching orders

---

## Important Assumptions (Very Important)

- There is **only ONE stock**
- We do **not track different users**
- Orders are processed **one after another**
- Everything happens **step by step**

This is **not a real multi-user trading system**.  
It is a **single-flow simulation** built only for learning.

---

## Order Life (Very Simple)

Every order goes through only these stages:
- **NEW** → order just entered
- **PARTIALLY FILLED** → some quantity matched
- **FILLED** → completely matched

There is:
- No cancelling
- No editing

Simple and clean flow.

---

## Trade Record

Every time a trade happens:
- It is recorded
- The record is **never changed**
- The record is **never deleted**

This keeps a clear and honest history of all trades.

---

## Simulation Mode

The project can:
- Automatically create buy and sell orders
- Send them into the system
- Show how trades happen step by step

This helps visualize how an exchange behaves.

---

## What This Project Is NOT

To keep learning simple, this project does **not** include:
- Real money
- Internet usage
- Multiple stocks
- Multiple users trading together
- Complex order types

All of this is avoided on purpose.

