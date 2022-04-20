# random.choice is used in one of the functions to fetch a random quote
import random
# Web scrapping is implemented using selenium webdriver
from selenium import webdriver
from datetime import datetime
# pytz is used to localize the timezone for some of the functions
import pytz
# pyshorteners is used to compress the long urls so that it is shorter in the telegram messages
import pyshorteners

# below webdriver initiations and configs for implementation on linux (In this case GCP virtual machine)
# for windows, use driver = webdriver.Chrome(executable_path=<your chrome driver path>)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Define the Scraper class
# A class is used for the ease of calling functions as a method later in the main file.
class Scraper:

    def __init__(self):
        # We need only time with the initiation of class as it is used in various methods and for logging
        self.ist_time()

    # below are 2 sets of functions, first one looks for data and saves into a text file
    # second one is a method that reads the text file and returns the info as a string
    # All the processes (functions) when executed are logged using a logger function defined at the end
    # All urls are shortened using a small function based on pyshortners library
    def inshorts_write(self):
        """ Returns all articles from the inshorts website, also creates a text file"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/inshorts.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t In-shorts\n\n")
        url = 'https://www.inshorts.com/en/read'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url=url)

        sr_no = 1
        headlines = [element.text for element in driver.find_elements_by_tag_name("a span") if len(element.text) >30]
        contents = [element.text for element in driver.find_elements_by_class_name('news-card-content')]

        for _ in range(len(headlines)):
            with open('/home/nikhil_neon_codetest/current_version/fetched-data/inshorts.txt', mode="a",
                      encoding="utf-8") as file:
                file.write(f'{sr_no}\t{headlines[_]}\n----------------------------------\n\t{contents[_]}\n\n')
                sr_no += 1
        self.logger('inshorts_write')
        driver.quit()

    def inshorts_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/inshorts.txt', mode="r") as file:
            for line in file.readlines():
                if line[:1] == "7":
                    break
                else:
                    output += line
        self.logger('inshorts_read')
        return output

    def techcrunch_write(self):
        """ Returns all articles from the tech-crunch website, also creates a text file"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/techcrunch.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t Tech-Crunch\n\n")
        url = 'https://techcrunch.com/'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        sr_no = 1
        headlines = [element.text for element in driver.find_elements_by_class_name("post-block__header h2 a")]
        links = [self.url_compress(element.get_attribute('href')) for element in driver.find_elements_by_tag_name(".post-block__header h2 a")]
        # contents = [element.text for element in driver.find_elements_by_class_name("post-block__content")]
        for element in range(len(headlines)):
            with open('/home/nikhil_neon_codetest/current_version/fetched-data/techcrunch.txt', mode="a", encoding="utf-8") as file:
                file.write(f'{sr_no}\t{headlines[element]}\n\t{links[element]}\n\n')
                sr_no += 1

        self.logger('techcrunch_write')
        driver.quit()

    def techcrunch_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/techcrunch.txt', mode="r") as file:
            for line in file.readlines():
                if line[:2] == "11":
                    break
                else:
                    output += line
        self.logger('techcrunch_read')
        return output

    def filmfare_write(self):
        """ Returns all articles from the film-fare website, also creates a text file"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/filmfare.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t Bollywood Masala\n\n")
        url = 'https://www.filmfare.com/news'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url=url)

        sr_no = 1
        headlines = [element.text for element in driver.find_elements_by_class_name('news-section-content')]
        links = [self.url_compress(element.get_attribute('href')) for element in
                 driver.find_elements_by_css_selector('.news-section figure a')]

        for _ in range(len(headlines)):
            with open('/home/nikhil_neon_codetest/current_version/fetched-data/filmfare.txt', mode="a",
                      encoding="utf-8") as file:
                file.write(f'{sr_no}\t{headlines[_]}\n\t{links[_]}\n\n')
                sr_no += 1
        self.logger('filmfare_write')
        driver.quit()

    def filmfare_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/filmfare.txt', mode="r") as file:
            for line in file.readlines():
                if line[:2] == "21":
                    break
                else:
                    output += line
        self.logger('filmfare_read')
        return output

    def wion_write(self):
        """ Returns all articles from the wion website, also creates a text file"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/wion.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t Wion News\n\n")
        url = 'https://www.wionews.com/'
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Chrome(executable_path='C://Users/20002128/PycharmProjects/chromedriver.exe')
        driver.get(url)

        sr_no = 1
        headlines = [element.get_attribute("text").strip() for element in
                     driver.find_elements_by_css_selector('.content-holder a')]
        links = [self.url_compress(element.get_attribute("href")) for element in driver.find_elements_by_css_selector('.content-holder a')]

        for element in range(len(headlines)):
            # To eleminate junk values like "Read More" #Facebook etc
            if len(headlines[element]) < 20:
                pass
            else:
                with open('/home/nikhil_neon_codetest/current_version/fetched-data/wion.txt', mode="a", encoding="utf-8") as file:
                    file.write(f'{sr_no}\t{headlines[element]}\n\t{links[element]}\n\n')
                    sr_no += 1
        self.logger('wion_write')
        driver.quit()

    def wion_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/wion.txt', mode="r") as file:
            for line in file.readlines():
                if line[:2] == "11":
                    break
                else:
                    output += line
        self.logger('wion_read')
        return output

    def finshots_write(self, no_pages=1):
        """ Returns all articles from finshots website, also creates a text file.
        If pages are specified, will fetch accordingly, else all pages"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/finshots.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t Finshots\n\n")
        url = f'https://finshots.in/archive/page/1/'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        place_holder = 0
        current_page = 1
        max_pages = int(driver.find_element_by_class_name('page-number').text.split()[-1])

        while current_page < min(no_pages + 1, max_pages + 1):
            finshot_url = f'https://finshots.in/archive/page/{current_page}/'
            driver.get(finshot_url)
            titles = [element.text for element in driver.find_elements_by_class_name('post-card-title')]
            briefs = [element.text for element in driver.find_elements_by_class_name('post-card-excerpt')]
            links = [self.url_compress(element.get_attribute("href")) for element in
                     driver.find_elements_by_class_name('post-card-content-link')]

            for i in range(len(titles)):
                sr_no = place_holder + 1
                place_holder = sr_no
                with open('/home/nikhil_neon_codetest/current_version/fetched-data/finshots.txt', mode="a", encoding='utf-8') as file:
                    file.write(f'{sr_no}\t{titles[i]}\n{briefs[i]}\n{links[i]}\n\n')

            current_page += 1
        self.logger('finshots_write')
        driver.quit()

    def finshots_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/finshots.txt', mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                if line[0] == "4":
                    break
                else:
                    output += line
        self.logger('finshots_read')
        return output

    def this_day_in_past_write(self):
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/tdip.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t This Day in Past\n\n")

        self.ist_time()
        day = self.day
        month = self.month
        url = f'https://www.onthisday.com/day/{month}/{day}'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        sr_no = 1
        events = [element.text.split("\n")[0] for element in driver.find_elements_by_css_selector('.event-list')]
        date = driver.find_element_by_class_name("date-large").text.split()

        with open('/home/nikhil_neon_codetest/current_version/fetched-data/tdip.txt', mode="a", encoding="utf-8") as file:
            file.write("--"+date[1]+"th "+date[0]+"--"+"\n\n")

        for element in range(len(events)):
            if len(events[element]) < 20:
                pass
            else:
                with open('/home/nikhil_neon_codetest/current_version/fetched-data/tdip.txt', mode="a", encoding="utf-8") as file:
                    file.write(f'{sr_no}\n{events[element]}\n\n')
                    sr_no += 1
        self.logger("this_day_in_the_past_write")
        driver.quit()

    def this_day_in_the_past_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/tdip.txt', mode="r") as file:
            for line in file.readlines():
                if line[:2] == "11":
                    break
                else:
                    output += line
        self.logger('this_day_in_the_past_read')
        return output

    def team_bhp_hot_threads_write(self, no_pages=1):
        """ Returns all articles from teambhp hot threads, also creates a text file.
                If pages are specified, will fetch accordingly, else all pages"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/team_bhp_hot_threads.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t T-BHP Threads\n\n")
        counter = 1
        driver = webdriver.Chrome(options=chrome_options)

        for page in range(1, no_pages + 1):
            url = f'https://www.team-bhp.com/hot-threads?page={page}'
            driver.get(url)
            titles = [element.text for element in driver.find_elements_by_tag_name("h2")]
            brief = [element.text for element in driver.find_elements_by_class_name('past_shornote')]
            links = [self.url_compress(element.get_attribute('href')) for element in driver.find_elements_by_class_name("holderImg")]

            for i in range(len(titles)):
                serial = counter
                with open('/home/nikhil_neon_codetest/current_version/fetched-data/team_bhp_hot_threads.txt', mode="a", encoding='utf-8') as file:
                    file.write(f'{serial} {titles[i]}\n{links[i]}\n{brief[i]}\n\n')
                    counter = counter + 1
        self.logger("team_bhp_hot_threads_write")
        driver.close()

    def team_bhp_hot_threads_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/team_bhp_hot_threads.txt', mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                if line[0] == "11":
                    break
                else:
                    output += line
        self.logger('team_bhp_hot_threads_read')
        return output

    def team_bhp_news_write(self, no_pages=1):
        """ Returns all articles from teambhp news threads, also creates a text file.
                If pages are specified, will fetch accordingly, else all pages"""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/team_bhp_news.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t T-BHP News\n\n")
        counter = 1
        driver = webdriver.Chrome(options=chrome_options)

        for page in range(1, no_pages + 1):
            url = f'https://www.team-bhp.com/news?page={page}'
            driver.get(url)
            titles = [element.text for element in driver.find_elements_by_tag_name("h2")]
            brief = [element.text for element in driver.find_elements_by_class_name('past_shornote')]
            links = [self.url_compress(element.get_attribute('href')) for element in driver.find_elements_by_class_name("holderImg")]

            for i in range(len(titles)):
                serial = counter
                with open('/home/nikhil_neon_codetest/current_version/fetched-data/team_bhp_news.txt', mode="a", encoding='utf-8') as file:
                    file.write(f'{serial} {titles[i]}\n{links[i]}\n{brief[i]}\n\n')
                    counter = counter + 1
        driver.close()
        self.logger('team_bhp_news_write')

    def team_bhp_news_read(self):
        output = ""
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/team_bhp_news.txt', mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                if line[0] == "11":
                    break
                else:
                    output += line
        self.logger('team_bhp_news_read')
        return output

    def culture_quotes(self):
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/culture.txt', mode="w") as file:
            file.write(f"Updated: {self.date}-{self.ist_time()}\t Culture Quotes\n\n")

        url = 'https://www.brainyquote.com/search_results?q=culture'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        quotes = [element.text for element in driver.find_elements_by_class_name("grid-item") if len(element.text) > 10]
        driver.quit()

        for quote in quotes:
            with open('/home/nikhil_neon_codetest/current_version/fetched-data/culture.txt', mode="a") as file:
                file.write(f'{quote}\n\n')
        self.logger('culture quotes')
        return f"{self.date}-{self.ist_time()}\n\n{random.choice(quotes)}"

    def logger(self, func_name):
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        time = datetime_ist.strftime("%m/%d/%Y %H:%M:%S")
        string = f'\t{time} - executed {func_name}'
        print(string)
        with open('/home/nikhil_neon_codetest/current_version/fetched-data/logger.txt', mode="a") as file:
            file.write(f'{string}\n')

    def ist_time(self):
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        # time = datetime_ist.strftime("%m/%d/%Y %H:%M:%S")
        time = datetime_ist.strftime("%H:%M:%S")
        self.day = int(datetime_ist.day)
        self.month = datetime_ist.strftime("%B").lower()
        self.date = datetime_ist.strftime('%d-%b-%y')
        self.minute = datetime_ist.strftime('%M')
        self.time = time
        return time

    def url_compress(self, link):
        short = pyshorteners.Shortener()
        return short.tinyurl.short(link)

    def separator(self, func):
        return f'------------------------\n\n{func}\n\n------------------------'


