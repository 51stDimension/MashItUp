from selenium import webdriver
import requests
import getpass
from selenium.webdriver.common.by import By
import time

id_name = input("Enter your Codeforces ID:")
password = getpass.getpass("Enter your Password:")
mashup_code = input("Enter your Gym Unique Code:")

dont_add = set()
add_these = set()

class Codeforces():

    def __init__(self):

        self.driver = webdriver.Chrome()

    def login(self):

        print('Opening Codeforces')

        self.driver.get("https://codeforces.com/")

        time.sleep(2)

        search = self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div[2]/div[2]/a[1]')
        search.click()

        time.sleep(2)

        print('Logging In')

        handle = self.driver.find_element_by_xpath("/html/body/div[6]/div[4]/div/div/div/form/table/tbody/tr[1]/td[2]/input")
        pwd = self.driver.find_element_by_xpath("/html/body/div[6]/div[4]/div/div/div/form/table/tbody/tr[2]/td[2]/input")

        handle.send_keys(id_name)
        pwd.send_keys(password)

        enter = self.driver.find_element_by_xpath("/html/body/div[6]/div[4]/div/div/div/form/table/tbody/tr[4]/td/div[1]/input")
        enter.click()

    def mashup(self):

        def UpdateSet(name):
            url = "https://codeforces.com/api/user.status?handle="+name
            data = requests.get(url).json()
            dat = data['result']
            # print('Problems not to be added:')
            for p in dat:
                # print(str(p['problem']['contestId']) + str(p['problem']['index']))
                dont_add.add(str(p['problem']['contestId']) + str(p['problem']['index']))

        self.driver.get("https://codeforces.com/gymRegistrants/{}".format(mashup_code))
        time.sleep(2)
        reg = self.driver.find_elements_by_class_name("registrants")
        body = reg[0].find_elements(By.TAG_NAME,"tbody")
        trs = body[0].find_elements(By.TAG_NAME ,"tr")
        print('Fetching Problems not to add!')

        for tr in trs[1:]:

            td = tr.find_elements(By.TAG_NAME,"td")[1]
            a_tag = td.find_elements(By.TAG_NAME,"a")[0]
            name = a_tag.get_attribute('title').split()
            UpdateSet(name[1])

        UpdateSet(id_name)

        print('Fetched Problems not to be added! :)')
        print('Total problem fetched:{}'.format(len(dont_add)))

    def prepare_problems(self):

        def add_problems(rating,num):

            url = "https://codeforces.com/api/problemset.problems"
            data = requests.get(url).json()
            dat = data['result']['problems']

            cnt = 0
            req = int(num)

            for prob in dat:
                if 'rating' in prob:

                    pr_str = str(prob['contestId']) + str(prob['index'])

                    if str(prob['rating']) == str(rating) and (pr_str not in dont_add):
                        cnt = cnt+1
                        add_these.add(str(prob['contestId']) + str(prob['index']))

                        if cnt==req:
                            break

        while(True):

            want = input('Do you want to add more problems?')
            if want=="NO":
                break
            rating = input('Type preferred Rating ')
            num = input('Type Number Of Problems ')

            print('Wait while we add {} problem/s rated {}'.format(num,rating))

            add_problems(rating,num)

        print('Problems to be added: {}'.format(len(add_these)))

    def add_problems(self):

        self.driver.get("https://codeforces.com/gym/{}/problems/new".format(mashup_code))

        a = self.driver.find_elements_by_class_name("ac_input")

        for st in add_these:
            a[1].send_keys(st)
            time.sleep(2)
            add = self.driver.find_element_by_xpath("/html/body/div[6]/div[4]/div[2]/div[2]/div[2]/div[6]/table/tbody/tr/td[1]/a/img")
            add.click()
            time.sleep(2)

        time.sleep(2)
        final = self.driver.find_element_by_xpath("/html/body/div[6]/div[4]/div[2]/div[2]/form[2]/input[2]")
        final.click()


bot = Codeforces()
bot.login()
time.sleep(3)
print('Getting the list of participants')
bot.mashup()
print('Gearing up to take problem rating input from you!:)')
time.sleep(3)
bot.prepare_problems()
time.sleep(3)
bot.add_problems()
print('Your problems have been added! All the best!')
