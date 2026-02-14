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

### Install that using requirements.txt

``` bash
pip3 install -r requirements.txt
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
cd exchange-simulator
```

### Windows

``` powershell
git clone https://github.com/COEP-Quant-Finance-Club/exchange_simulator.git
cd exchange-simulator
```

------------------------------------------------------------------------

## 2. Start the Matching Engine (Start FIRST)

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

``` bash
python3 start_client.py --user Alice
```

Example:

``` bash
python3 start_client.py --user Bob
```

### Windows

``` powershell
python start_client.py --user Alice
```

Example:

``` powershell
python start_client.py --user Bob
```
## Data Storage

-   Session orders → storage/session_orders/
-   Trades ledger → storage/trades/trades.json
-   Logs → storage/logs/system.log
-   order snapshot → orders_snapshot.json

## Matching Rules

-   BUY priority → Higher price first
-   SELL priority → Lower price first
-   Tie → Earlier timestamp wins

Match condition:

BUY.price >= SELL.price
for market and limit orders.

## Author

Exchange Simulator Project --- built for learning matching engine
internals and system design.
