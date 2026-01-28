### This is the algorithm for the orderbook.py

in the **match_limit_buy**() function the orders will be stored in buysell
When an order came

### Algorithm:

#### Match an incoming BUY order against the existing sell orders in the order book, following price-time priority.

Steps:

- Initialize Trades List

- Create an empty list to store executed trades for this order.

- Check Sell Book

- If there are no sell orders, return an empty list.

- Otherwise, proceed to match.

- Loop Until Order is Fully Filled or No Matches Exist

- While the incoming BUY order still has remaining quantity and the sell book is not empty:
  - Select the best SELL order (lowest price, earliest timestamp).

  - If the sell price is greater than the buy price, stop matching.

  - Execute a trade for the minimum available quantity.

  - Update remaining quantities for both orders.

  - Remove the SELL order from the book if fully filled.

  - Record the trade.

In the **match_limit_sell**() function

### Algorithm:

#### Match the incoming sell orders against the existing buy orders in the orderbook, following price-time priority

Steps:

- Initialize Trades List

- Create an empty list to store executed trades for this order.

- Check Buy Book

- If there are no Buy orders, return an empty list.

- Otherwise, proceed to match.

- Loop Until Order is Fully Filled or No Matches Exist

- While the incoming BUY order still has remaining quantity and the sell book is not empty:
  - Select the best BUY order (highest price, earliest timestamp)
  - If the buy price is lower than the sell price, stop matching.
  - Execute a trade for the minimum available quantity.
  - Update remaining quantities for both orders.
  - Remove the BUY order from the book if fully filled.
  - Record the trade.
