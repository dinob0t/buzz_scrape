import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome()

browser.get("https://www.buzzfeed.com")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")
print elem
no_of_pagedowns = 2

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.random())
    no_of_pagedowns-=1

post_elems = browser.find_elements_by_tag_name('h2')

text_list = []
number_list = []
for post in post_elems:
	if post.text:
		cur_str = post.text.encode('utf8')
		text_list.append(cur_str)
		number_list.extend([int(s) for s in cur_str.split() if s.isdigit()])
post_elems = browser.find_elements_by_tag_name('h3')

text_list = []
for post in post_elems:
	if post.text:
		cur_str = post.text.encode('utf8')
		text_list.append(cur_str)
		number_list.extend([int(s) for s in cur_str.split() if s.isdigit()])

#print text_list
print number_list
browser.quit()
print random.random()
print random.random()