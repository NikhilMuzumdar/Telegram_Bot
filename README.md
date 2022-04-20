# Telegram_Bot
A program that scrapes websites using selenium webdriver and provides updates on telegram using PyTelegramBotAPI.
# Program
This program initiates two while loops in threading:
1) To listen for message commands and update the info when requested 
2) To send messages at specified time 
# Files 
1) main_r4.py
2) scrapper_r4.py
3) sample txt files - logs and sample saves generated as the program runs. 
# Python Libraries used:
1) selenium
2) PyTelegramBotApi
3) pyshortners
4) pytz
5) datetime
6) threading
# Implementation notes
For a working program, you will first need to create a bot using Botfather https://core.telegram.org/bots
Update the generated bot token in main_r4.py either as a string (unsecure) or as a environment variable. 
