import time
import random
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

num_iters = 1
itercount = 1
for i in range(num_iters):
	browser = webdriver.Chrome()

	browser.get("https://www.buzzfeed.com")
	time.sleep(2*random.random())

	elem = browser.find_element_by_tag_name("body")
	no_of_pagedowns = 60

	while no_of_pagedowns:
	    elem.send_keys(Keys.PAGE_DOWN)
	    time.sleep(random.random())
	    no_of_pagedowns-=1
	try:
		with open('text_dict.csv', 'rb') as r: 
			reader = csv.reader(r)
			text_dict = dict(x for x in reader)
	except:
		text_dict = {}

	number_list = []
	for key, value in text_dict.items():
		val_str = ''.join(value[1:len(value)-1])
		number = ((val_str.split(',')))
		for i in range(len(number)):
			num = number[i]
			if num.strip():
				number_list.append(''.join((num.strip())))

	print number_list
	post_elems = browser.find_elements_by_tag_name('h2')

	for post in post_elems:
		if post.text:
			cur_str = post.text.encode('utf8')
			if cur_str not in text_dict.keys():
				print cur_str
				cur_numbers = [int(s) for s in cur_str.split() if s.isdigit()]
				text_dict[cur_str] = cur_numbers
				number_list.extend(cur_numbers)

	post_elems = browser.find_elements_by_tag_name('h3')

	for post in post_elems:
		if post.text:
			cur_str = post.text.encode('utf8')
			if cur_str not in text_dict.keys():
				print cur_str
				cur_numbers = [int(s) for s in cur_str.split() if s.isdigit()]
				text_dict[cur_str] = cur_numbers
				number_list.extend(cur_numbers)

	browser.quit()
	with open('text_dict.csv', 'wb') as w: 
		writer = csv.writer(w)
		for key, value in text_dict.items():
	  		writer.writerow([key, value])

	with open('number_list.csv', 'wb') as w:
		writer = csv.writer(w)
		writer.writerow(number_list)
	print 'Iteration number ', itercount
	itercount +=1
	print len(text_dict)

	time.sleep(random.random())