import json
import urllib.request
import time
from datetime import datetime
import numpy as np

# create lists to record trade and price data
prices = []  # create empty lists to store the prices and moving averages
moving_avgs = []  # create an empty list to store the trade history
trade_history = []  # create a list of RSI values
rsi_values = []
# initialize the trading strategy parameters
is_trading = True
buy_price_threshold = 17560  # buy when the price falls below this threshold
sell_price_threshold = 17890  # sell when the price rises above this threshold
stop_loss = 0.99  # sell when the falls into a loss
take_profit_percent = 1.01  # sell when the price rises in profit
interval = 5  # time in seconds between each loop
max_trade_size = 100
# initialize the balances
initial_btc_balance = 0
initial_usd_balance = 1000


# show the welcome message
def show_welcome_message():
    print("-------------------------------------")
    print("| Welcome to the Bitcoin Trader Bot |")
    print("-------------------------------------")


# show the current balances
def show_current_balances(btc_balance, usd_balance):
    print("Current balances:")
    print("BTC: ", initial_btc_balance)
    print("USD: ", initial_usd_balance)


# show the main menu
def show_main_menu():
    print("Please select an option:")
    print("1. Set trading strategy parameters")
    print("2. View current strategy parameters")
    print("3. Toggle live trading")
    print("4. View current balances")
    print("5. View trading history")
    print("6. Exit")


# show the trading history
def show_trading_history(history):
    print("-------------------------------------")
    print("| Trading History                   |")
    print("-------------------------------------")
    print("Timestamp | Action | Quantity | Price")
    for trade in history:
        timestamp = trade["timestamp"]
        action = trade["action"]
        quantity = trade["quantity"]
        price = trade["price"]
        print("{} | {} | {} | {}".format(timestamp, action, quantity, price))


# show the current trading parameters
def show_trading_parameters(buy_price_threshold, sell_price_threshold, stop_loss, take_profit_percent, interval, max_trade_size):
    print("-------------------------------------")
    print("| Current Strategy Parameters       |")
    print("-------------------------------------")
    print("buy_price_threshold: ", buy_price_threshold)
    print("sell_price_threshold: ", sell_price_threshold)
    print("stop_loss: ", stop_loss)
    print("take_profit_percent: ", take_profit_percent)
    print("interval: ", interval)
    print("trade_size:", max_trade_size)


# show the trading in progress
def show_trading_in_progress(current_price, btc_balance, usd_balance):
    print("-------------------------------------")
    print("| Trading in progress...            |")
    print("-------------------------------------")
    print("Current price: ", current_price)
    print("Balances:")
    print("BTC: ", btc_balance)
    print("USD: ", usd_balance)


# show the welcome message
show_welcome_message()
# show the current balances
show_current_balances(initial_btc_balance, initial_usd_balance)
# show the main menu
show_main_menu()
# read the user's input
option = input()
# handle the user's input
if option == "1":
    # Set the trading strategy parameters
    buy_price_threshold = input("buy_price_threshold: ")
    sell_price_threshold = input("sell_price_threshold: ")
    stop_loss = input("stop_loss: ")
    take_profit_percent = input("take_profit_percent: ")
    interval = input("interval: ")
    max_trade_size = input("trade_size:")

    # Check if the interval is not an empty string
    if interval:
        # Convert interval to an integer
        interval = int(interval)

    # Check if the buy price is not an empty string
    if buy_price_threshold:
        # Convert buy price to a float
        buy_price_threshold = float(buy_price_threshold)

    # Check if the sell price is not an empty string
    if sell_price_threshold:
        # Convert sell price to a float
        sell_price_threshold = float(sell_price_threshold)

    # Check if the stop loss is not an empty string
    if stop_loss:
        # Convert stop loss to a float
        stop_loss = float(stop_loss)

    # Check if the take profit is not an empty string
    if take_profit_percent:
        # Convert stop loss to a float
        take_profit_percent = float(take_profit_percent)

    show_trading_parameters(buy_price_threshold, sell_price_threshold,
                            stop_loss, take_profit_percent, interval, max_trade_size)
elif option == "2":
    # Show the current strategy parameters
    show_trading_parameters(buy_price_threshold, sell_price_threshold,
                            stop_loss, take_profit_percent, interval, max_trade_size)
elif option == "3":
    # start/stop trading
    if is_trading:
        # stop trading
        is_trading = False
        print("Trading stopped.")

    else:
        # start trading
        is_trading = True
        print("Trading started.")
elif option == "4":
    # Show current balances
    show_current_balances(btc_balance, usd_balance)
elif option == "5":

    # Initialize the trading history
    history = []

    show_trading_history(history)
elif option == "6":
    # Exit the program
    print("Exiting program. Goodbye!")
    quit()


# show trade history on the start page
def show_trade_history(trade_history):
    # Print a message indicating that the trade history is being shown
    print("-------------------------------------")
    print("| Showing trade history...          |")
    print("-------------------------------------")

    # Iterate over the trade history and print each trade
    for trade in trade_history:
        print(trade)


# fetch bitcoin prices
def get_price(USD):
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = urllib.request.urlopen(url)
    the_page = response.read()
    data = json.loads(the_page)
    conversion = data['bpi'][USD]['rate_float']
    return conversion


# calculate new buy and sell price thresholds
def calculate_price_thresholds(latest_price):
    global buy_price_threshold
    global sell_price_threshold

    new_buy_price_threshold = latest_price - 1
    buy_price_threshold = new_buy_price_threshold

    new_sell_price_threshold = latest_price + 1
    sell_price_threshold = new_sell_price_threshold


# calculate the moving average
def calculate_moving_average(prices, period):
    # calculate the moving average for a given time period
    # prices is a list of prices for each time interval
    # period is the number of time intervals to include in the moving average

    # initialize the moving average
    moving_avg = 0

    # loop through the prices and calculate the moving average
    for i in range(period):
        moving_avg += prices[i]

    # divide the sum by the number of periods to get the average
    moving_avg /= period

    return moving_avg


# calculate the volatility index
def calculate_volatility_index(prices):
    # calculate the volatility index for a given time period
    # prices is a list of prices for each time interval
    # a higher value indicates higher volatility and a lower value indicates lower volatility.

    # initialize the variables
    sum_of_squared_errors = 0
    mean = sum(prices) / len(prices)

    # loop through the prices and calculate the sum of squared errors
    for price in prices:
        squared_error = (price - mean)**2
        sum_of_squared_errors += squared_error

    # calculate the volatility index
    volatility_index = (sum_of_squared_errors / len(prices))**0.5

    return volatility_index


# calculate the upper and lower price range
def calculate_price_range(prices, range_percent):
    # calculate the upper and lower price range for a given time period
    # prices is a list of prices for each time interval
    # range_percent is the percentage value to add and subtract from the average price to determine the range

    # calculate the average of the prices
    mean = sum(prices) / len(prices)

    # calculate the upper and lower bounds of the range
    upper_bound = mean + (mean * range_percent)
    lower_bound = mean - (mean * range_percent)

    return upper_bound, lower_bound


# record a trade
def record_trade(trade):
    # Get the current time and date
    time = datetime.now()
    # Convert the time to a string in the format "YYYY-MM-DD HH:MM:SS"
    time_string = time.strftime("%Y-%m-%d %H:%M:%S")
    # Add the formatted time string to the trade
    trade['time'] = time_string
    # Add the trade to the trade history list
    trade_history.append(trade)
    with open('C:/Users/USER/Desktop/trade_history.txt', 'a') as f:
        # Write the trade to the file, one trade per line
        f.write(str(trade) + '\n')


# Define a function to calculate the relative strength index
def relative_strength_index(prices):
    # Convert the prices list to a numpy array
    prices = np.array(prices)

    # Calculate the differences between consecutive prices
    diff = prices[1:] - prices[:-1]

    # Calculate the up and down changes
    up_changes = [x if x > 0 else 0 for x in diff]
    down_changes = [x if x < 0 else 0 for x in diff]

    # Calculate the total gain and total loss
    total_gain = sum(up_changes)
    total_loss = sum(down_changes)

    # Calculate the relative strength
    if total_loss == 0:
        relative_strength = 0
    else:
        relative_strength = total_gain / total_loss

    # Calculate the relative strength index
    rsi = 100 - (100 / (1 + relative_strength))

    return rsi


# main loop for the trading bot
def main():

    # set the initial values for the user's accounts
    now = datetime.now()
    starting_price = 0
    trade_count = 0
    call_count = 0
    stop_loss_count = 0
    take_profit_count = 0
    profit = 0
    profit_percentage = 0
    moving_average = 0
    volatility = 0
    upper_bound = 0
    lower_bound = 0
    rsi = 0
    btc_balance = initial_btc_balance
    usd_balance = initial_usd_balance


    # runs loop indefinitely
    while True:

        time.sleep(interval)  # wait before making the next request
        price = get_price("USD")  # get the current price in USD

        # store the current price in the prices list
        prices.append(price)

        # if there are enough prices in the list, calculate the moving average
        if len(prices) >= 20:
            moving_avg = calculate_moving_average(prices, 10)
            moving_avgs.append(moving_avg)
            moving_average = moving_avg

        # if there are enough prices in the list, calculate the volatility index
        if len(prices) >= 20:
            volatility_index = calculate_volatility_index(prices)
            volatility = volatility_index

        # if there are enough prices in the list, calculate the upper & lower bounds of the price range
        if len(prices) >= 20:
            upper_bound, lower_bound = calculate_price_range(prices, 0.01)

        # calculate the RSI for each set of prices
            rsi = []
            for i in range(len(prices)):
                rsi.append(relative_strength_index(prices[i:]))

        # buy bitcoin
        if price < buy_price_threshold and usd_balance != 0 and call_count > 5:
            # Define the arguments to pass to the order_btc function
            side = "buy"
            # Add the amount of BTC to the BTC balance
            trade_count += 1
            call_count += 1
            latest_price = price
            btc_balance += usd_balance / price
            usd_balance = 0

            # record the trade in the trade history
            record_trade(
                {'type': side, 'amount': btc_balance, 'price': price})

            # Calculate new buy and sell price thresholds after trade
            calculate_price_thresholds(
                latest_price)

            # calculate the profit/loss for the trade
            print("")
            print("--------------------------------------------------")
            print("")
            print("POSITION OPENED")
            print("")
            print("--------------------------------------------------")
            print("")
            print("Trade count:", trade_count)
            print("Call count:", call_count)
            print("")
            print("Today's time:", now)
            print("Bought bitcoin at price: ${:,.2f}".format(price))
            print("BTC balance: {:,.8f}".format(btc_balance))
            print("USD balance: ${:,.2f}".format(usd_balance))
            print("")
            print("")

        # sell bitcoin at desired target price
        if price > sell_price_threshold and btc_balance != 0:
            # sell all of the bitcoin for USD
            side = "sell"
            trade_count += 1
            call_count += 1
            latest_price = price
            usd_balance += btc_balance * price
            btc_balance = 0
            # record the trade in the trade history
            record_trade(
                {'type': 'sell', 'amount': btc_balance, 'price': price})

            # Calculate new buy and sell price thresholds after trade
            calculate_price_thresholds(
                latest_price)

            print("")
            print("--------------------------------------------------")
            print("")
            print("POSITION CLOSED")
            print("")
            print("--------------------------------------------------")
            print("")
            print("Trade count:", trade_count)
            print("Call count:", call_count)
            print("")
            print("Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
            print("Sold bitcoin at price: ${:,.2f}".format(price))
            print("BTC balance: {:,.8f}".format(btc_balance))
            print("USD balance: ${:,.2f}".format(usd_balance))
            print("")
            print("")

        # stop loss
        if price < starting_price * (1 - stop_loss):
            # sell all of the bitcoin for USD
            side = "sell"
            trade_count += 1
            call_count += 1
            stop_loss_count += 1
            latest_price = price
            usd_balance += btc_balance * price
            btc_balance = 0
            # record the trade in the trade history
            record_trade(
                {'type': 'sell', 'amount': btc_balance, 'price': price})
            # Calculate new buy and sell price thresholds after trade
            calculate_price_thresholds(
                latest_price)
            print("")
            print("--------------------------------------------------")
            print("")
            print("STOP LOSS")
            print("")
            print("--------------------------------------------------")
            print("")
            print("Trade count:", trade_count)
            print("Call count:", call_count)
            print("")
            print("Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
            print("Sold bitcoin at price: ${:,.2f}".format(price))
            print("BTC balance: {:,.8f}".format(btc_balance))
            print("USD balance: ${:,.2f}".format(usd_balance))
            print("")

    
        # analyse the market and await making a trade decision (the bot will spend most time doing this)
        else:
            # hold the current position
            profit = usd_balance-initial_usd_balance + (btc_balance * price)
            if initial_usd_balance != 0:
                profit_percentage = ((profit / initial_usd_balance)) * 100
            else: profit_percentage =  (btc_balance * price) / (initial_btc_balance * price)
            call_count += 1
            print("")
            print("----------------------------------------------------------")
            print("Loop #", call_count)
            print("----------------------------------------------------------")
            print("")
            print("/// PRICE STATS ///")
            print("")
            print("--- BTC price: ${:,.2f}".format(price))
            print("--- Target buy price: ${:,.2f}".format(buy_price_threshold))
            print("--- Target sell price: ${:,.2f}".format(sell_price_threshold))
            print("")
            print("/// TRADE STATS ///")
            print("")            
            print("--- BTC balance: {:,.8f}".format(btc_balance))
            print("--- USD balance: ${:,.2f}".format(usd_balance))
            print("--- Profit: ${:,.2f}".format(profit))
            print("--- Account growth: %{:,.2f}".format(profit_percentage))
            print("--- Trade count: ", trade_count)
            print("--- Stop loss count: ", stop_loss_count)
            print("--- Take profit count: ", take_profit_count)
            print("")
            print("/// INDICATORS ///")
            print("")
            print("--- Moving average: ${:,.2f}".format(moving_average))
            print("--- Volatility: ", volatility)
            print("--- Trading range: ${:,.2f} - ${:,.2f}".format(lower_bound, upper_bound))
            print("")
          # print("--- Trade history: ", trade_history)
          # print("Time log:", now.strftime("%Y-%m-%d %H:%M:%S")) (recording the star of the program, not the record instances)
            print("")


# run the main loop
if __name__ == "__main__":
    main()
