# Exchange Simulator

A terminal-based stock exchange simulator demonstrating how a real
matching engine works --- including order submission, price-time
priority matching, order book management, trade logging, and
session-level history.

## Features

-   Limit BUY and SELL orders
-   Price-Time Priority matching
-   Partial and full order execution
-   Persistent order book (pending orders)
-   Immutable trade ledger
-   Session-level order history per user
-   Interactive terminal messages
-   Multi-client TCP architecture

## Requirements

Install dependencies using requirements.txt:

### Linux / macOS

```bash
pip3 install -r requirements.txt
```
### Windows

```bash
pip install -r requirements.txt
```
# Run Instructions (Windows & Linux)

## Prerequisites

-   Python 3.8 or higher
-   Git (optional, for cloning)

Check Python:

### Linux / macOS

``` bash
python3 --version
```

### Windows (PowerShell / CMD)

``` powershell
python --version
```

------------------------------------------------------------------------

## 1. Clone the Repository

### Linux / macOS

``` bash
git clone https://github.com/COEP-Quant-Finance-Club/exchange_simulator.git
cd exchange_simulator
```

### Windows

``` powershell
git clone https://github.com/COEP-Quant-Finance-Club/exchange_simulator.git
cd exchange_simulator
```



## 2. Start the Matching Engine (Start FIRST)

#### Note: 

- *Start the matching engine BEFORE starting any client sessions.*

- *Otherwise clients will fail to connect.*

### Linux / macOS

``` bash
python3 start_engine.py
```

### Windows

``` powershell
python start_engine.py
```

Expected output:

    Matching Engine started...
    Listening for client connections...

------------------------------------------------------------------------

## 3. Start Client Sessions

Open a new terminal for each user.

### Linux / macOS

Start client for Alice:
``` bash
python3 start_client.py --user Alice
```
Start another client for Bob:

``` bash
python3 start_client.py --user Bob
```

### Windows

Start client for Alice:
``` powershell
python start_client.py --user Alice
```

Start another client for Bob:
``` powershell
python start_client.py --user Bob
```
## Data Storage

-   Session orders : storage/session_orders/
-   Trades ledger : storage/trades/trades.json
-   Logs : storage/logs/system.log
-   order snapshot : orders_snapshot.json

## Matching Rules

-   BUY priority : Higher price first
-   SELL priority : Lower price first
-   Tie : Earlier timestamp wins

### Match condition:

Limit orders match when:

BUY.price >= SELL.price

Market orders match immediately against best available opposite orders.

## Author

Developed as a learning project to simulate exchange matching engine behavior, order processing, and trade execution.
