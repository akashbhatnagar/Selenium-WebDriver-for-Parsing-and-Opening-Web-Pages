from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

path_to_cd = '/Users/akash/Downloads/chromedriver'
driver = webdriver.Chrome(executable_path = path_to_cd)
url = 'https://isgweb.nmhc.org/isgweb/Membership/MemberDirectorySearch.aspx'
driver.get(url)
driver.find_element_by_xpath('//*[@id="Name-ISGweb_CompanyDirectory5"]/option[15]').click()
driver.find_element_by_name('btnSearch').click()
#page will take some time load
driver.implicitly_wait(10)

# open all the windows first
def open_company_windows(page):
	print("page: " + str(page))
	companies = driver.find_elements_by_class_name('isg_formData')
	companies_odd = driver.find_elements_by_class_name('isg_formDataWhite')
	#actionChains = ActionChains(driver)

	print(len(companies))
	for company in companies:
		cell = company.find_elements_by_tag_name("td")[0]
		link = cell.find_element_by_tag_name("a")
		print(link.text)
		link.click()
		time.sleep(5)


	#last element will give the pagination links
	# first two do not contain the element a

	i = 2
	last_index = len(companies_odd) - 1
	print(len(companies_odd))

	while i < last_index:
		cell = companies_odd[i].find_elements_by_tag_name("td")[0]
		link = cell.find_element_by_tag_name("a")
		print(link.text)
		i = i + 1
		link.click()
		time.sleep(5)

	page_links = companies_odd[last_index].find_element_by_tag_name("td")
	atags = page_links.find_elements_by_tag_name("a")
	if page == 2: # want to stop early
		return

	if page > 20:
		j = page - 20 + 8
	elif page > 10:
	    j = page - 9
	else:
	    j = page - 1

	atag  = atags[j]
	print("clicking link " + atag.text)
	atag.click()
	time.sleep(10)
	open_company_windows(page + 1) # recursive    

	"""
	while j < len(atags) - 1:
		atag = atags[j]
		print(atag.text)
		atag.click()
		time.sleep(10)
		open_company_windows(page + 1)
		
	"""

# call the function starting with page 1
open_company_windows(1)

print(len(driver.window_handles))

k = 1
handles = driver.window_handles
while k < len(handles):
	driver.switch_to_window(handles[k])
	time.sleep(5)
	company_web_link = driver.find_element_by_xpath('//*[@id="frmPage"]/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/a[1]')
	print(company_web_link.text)
	if company_web_link.is_displayed():
		ActionChains(driver).key_down(Keys.SHIFT).click(company_web_link).key_up(Keys.SHIFT).perform()
	else:
		print('link not active')
	#company_web_link.click()
	driver.find_element_by_xpath('//*[@id="btnCancel"]').click()
	k = k + 1

"""
page_links = companies_odd[last_index].find_element_by_tag_name("td")
atags = page_links.find_elements_by_tag_name("a")
j = 1
while j < len(atags) - 1:
	atag = atags[j]
	print(atag.text)
	atag.click()
	time.sleep(10)
"""
