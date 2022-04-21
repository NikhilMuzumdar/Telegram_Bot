# Imports
# Scrapper class uses selenium to fetch and write data into txt files and read when required
from scrapper_r4 import Scraper
# Install PyTelegramBotAPI and telebot and import telebot to create a bot instance
import telebot
# time module is required to send scheduled updates
import time
# Threading is used to implement 2 while loops in parallel, one to update information and
# another to check if the bot has received command
import threading

# Bot Token, In telegram ping BotFather to create a bot and generate a token
TOKEN = 'YOUR TOKEN HERE'
# initiate the bot instance. Not that this will be the same bot used in both while loops
bot = telebot.TeleBot(token=TOKEN)
# A print statement to indicate the start of program
print("Bot is listening")
# Initiate Scrapper Object
data = Scraper()

# Initialize write functions
# Each of these write programs generate txt files with data from various websites
# It only fetches the headlines, subtitles and the relevant links
def initialize():
    data.wion_write()
    time.sleep(10)
    data.team_bhp_news_write()
    time.sleep(10)
    data.finshots_write()
    time.sleep(10)
    data.this_day_in_past_write()
    time.sleep(10)
    data.team_bhp_hot_threads_write()
    time.sleep(10)
    data.inshorts_write()
    time.sleep(10)
    data.filmfare_write()
    data.techcrunch_write()

# Infinite polling constantly listens for commands made to the bot via telegram
# A command is to be preceded by "/" in telegram and must be defined for the bot to act
# Message handler is an inbuilt PyTelegramBotAPI function
def infinite_polling():
    print("Infinite polling is running")
    # This indicates that initialize was successful and the while loop is now running

    @bot.message_handler(commands=['help'])
    def send_welcome(message):
    # Various commands are defined for the bot to act.
    # In telegram, the bot replies with this below text if /help is sent
        bot.reply_to(message, "I provide following information"
                              ": \n\n/team_bhp_news\n\n/team_bhp_hot_threads"
                              "\n\n/wion_news\n\n/finshots_updates\n\n/"
                              "culture_updates\n\n/this_day_in_the_past"
                              "\n\n/inshorts\n\n/bollywood_masala\n\n/techcrunch_updates",
                     disable_web_page_preview=True,
                     )

    # defined below are the commands and the relevant functions (in this case methods since we have a class)
    @bot.message_handler(commands=['wion_news'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.wion_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['techcrunch_updates'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.techcrunch_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['bollywood_masala'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.filmfare_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['inshorts'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.inshorts_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['this_day_in_the_past'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.this_day_in_the_past_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['team_bhp_news'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.team_bhp_news_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['team_bhp_hot_threads'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.team_bhp_hot_threads_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['finshots_updates'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.finshots_read()), disable_web_page_preview=True)

    @bot.message_handler(commands=['culture_updates'])
    def send_welcome(message):
        bot.reply_to(message, data.separator(data.culture_quotes()), disable_web_page_preview=True)

    # this is to let the bot always listen for commands / messages
    bot.infinity_polling()


# To send updates at scheduled time
def scheduled_messaging():
    print("Scheduled messaging is running") # To indicate that the second while loop is running
    # Define the desired hrs at which the update is to be sent by the bot
    wion_hrs = [7, 10, 14, 16, 18, 20, 23]
    tbhp_ht_hrs = [9, 13]
    tbhp_news_hrs = [12, 19]
    finshots_hrs = [8]
    this_day_in_past_hrs = [5]
    culture_quotes_hrs = [7]
    filmfare_hrs = [8, 18]
    inshorts_hrs = list(range(6, 24))
    tech_chrunch_hrs = [8, 20]

    # This function checks if the hour matches and the minute is within 0-5 min of the said hr
    # if true, it returns True
    def check_if_to_execute(hours=[0]):
        """Enter the Hr at which a function is to be executed
        it will return True till that Hr + 5 minutes"""
        output = False
        if int(data.ist_time()[:2]) in hours:
            if int(data.ist_time()[3:5]) in list(range(0, 6)):
                output = True
        return output

    # To keep a count of no of while loops executed, use a counter.
    # This data is saved as a log file named status_log.txt
    counter = 1
    while True:
        # Loging & Printing While loop status
        status = f"{data.date} {data.ist_time()}: While loop run count\t{counter}"
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/'
                  'status_log.txt', mode="a") as file:
            file.write(status+"\n")
        print(status)
        counter += 1

        # Below set of functions check the time and execute the mapped functions
        # Note that in most cases here, the web scrapping doesn't take place.
        # This only reads from the saved txt files thus improving response speed.
        # To send messages, you will have to update the chat id to which the bot should reply.
        # How to get chat id: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
        # Faster way is to open a conversation with the bot on telegram web and get the 9-digit number from the url
        if check_if_to_execute(hours=wion_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.wion_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=tech_chrunch_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.techcrunch_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=tbhp_ht_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.team_bhp_hot_threads_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=tbhp_news_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.team_bhp_news_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=finshots_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.finshots_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=this_day_in_past_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.this_day_in_the_past_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=culture_quotes_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.culture_quotes()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=filmfare_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.filmfare_read()), disable_web_page_preview=True)
            except:
                pass

        if check_if_to_execute(hours=inshorts_hrs):
            try:
                bot.send_message(chat_id='<Your Chat id>', text=data.separator(data.inshorts_read()), disable_web_page_preview=True)
            except:
                pass
        # If the minute is between 45 to 46 (2 min window to allow for execution time), web scraping is executed to update the files.
        if int(data.minute) in [45, 46]:
            try:
                initialize()
                # in order to not run twice in the 2 minutes window, the program waits here for 2 minutes
                time.sleep(120)
            except:
                pass
        # We do not want the func to execute twice if hr = whole no and min between 0 & 5, hence it waits for 5 min
        if int(data.ist_time()[3:5]) in list(range(0, 6)):
            time.sleep(300)

        # Slowing down the while loop to one cycle per min
        time.sleep(60)


# This is where the main program runs
# Run initialize to update all txt files so that all read functions work
initialize()
# initiate two threads, one for listening to command and another to send scheduled messages
t1 = threading.Thread(target=infinite_polling)
t2 = threading.Thread(target=scheduled_messaging)

# start and join the threads
t1.start()
t2.start()

t1.join()
t2.join()

print("Bot is Sleeping!")
