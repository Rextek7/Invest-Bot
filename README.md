# Invest-Bot
Bot for learning trading based on tinkoff sandbox

# Library stack
### telebot - for writing commands for the tg bot itself
### tinkoff - directly allowed to get data from the exchange and interact with the sandbox
### shelve - for storing user ids
### requests - for receiving gifs

# Structure:
## main - file that starts the bot, importing the remaining files
## Bot_base - this file is a handler of the bot tag itself, i.e. it is in this file that the bot is configured to interact with the user. 
## invest_bot - This file represents the interaction of the Telegram bot with the stock exchange

# Goal
### This bot is an assistant for beginner traders on tinkoff stock exchange, as well as for those who want to get up-to-date summaries on securities by simply pressing 2 buttons.
### Thanks to the presence of a sandbox, a tool for trading virtual shares, the bot allows you to try out your schemes on the exchange without costs, study data from it and buy and sell shares. However, since the sandbox receives data from the real stock exchange, all the information that is visible to the user is up-to-date 

### It should be noted that buying and selling of shares is possible only during the operation of Мосбиржи

# Functionality
## Using the /info button the user can get a detailed description of the functions presented in the bot. This list consists of 12 items. Let's proceed in order. 
## 1) Create a new account:  
### The command creates a new account in the sandbox and returns the id of this account to the user. This is necessary for further buying of shares, selling and receiving information on the account. The number of accounts for 1 user account is not limited 

## 2) Get list of accounts:  
### The command displays all accounts available on the account 

## 3) Send currency data: 
### The command outputs the current information about Dollars, Yuan and Gold. This limitation on currencies exists due to the limitations of sandbox functions. Also in this command is implemented mailing for all users who use the bot. This is realised through the shelve library, which is roughly speaking a mini database. The bot receives the id of the user when he just starts the bot. 

## 4) Delete account: 
### The command deletes the account whose id the user enters. Starting with this command, the data that the user sends to the bot is processed. This handler will be discussed later. 

## 5) Refill account:  
### The command replenishes the account with n rubles and k kopecks. It requires the id of the account to be replenished 

## 6) Get account information:  
### The command displays all available account information. The id of the account is required 

## 7) Get information about available shares:  
### The command outputs the names of the stocks you can trade. Since the number of stocks is quite large, the command only outputs the exact names of the stocks so that the user can copy the names and in the next function already see the information about the specific stock 

## 8) Get information about the stock:  
### The command outputs information about a stock. The exact name of the stock is required 

## 9) Buy stock:  
### The command allows you to buy a virtual share. The account id and figi of the share are required 

## 10) Sell shares:  
### The command allows you to sell a virtual share. Requires account id and figi of the stock 

## 11) Stonks:  
### This command outputs a gif image using the giphy api 

## 12) No stonks:  
### Similar to the previous one. 

# Possibilities of extending
## Since the bot uses sandbox - its functionality is limited, but there is a possibility to use this bot for a real stock exchange with real shares in which the number of functions is many times more, as well as possible to add more informative mailings, processing of documents with schemes from the user and mailings of information from tinkoff pulse. Therefore, in short, this bot within the framework of even one tinkoff library can be expanded almost infinitely. 
