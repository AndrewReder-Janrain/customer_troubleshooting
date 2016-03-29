#!/usr/bin/env
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class SiteLoginPage:
	login_url = ""
	username = ""
	password = ""
	username_field_id = ""
	password_field_id = ""
	login_submit_id = ""
	logout_id = ""

	def __init__(self,login_url,username,password,username_field_id,password_field_id,login_submit_id,logout_url,logout_id):
		self.login_url = login_url
		self.username = username
		self.password = password
		self.username_field_id = username_field_id
		self.password_field_id = password_field_id
		self.login_submit_id = login_submit_id
		self.logout_url = logout_url
		self.logout_id = logout_id

# def make_site_login_page(login_url,username,password,username_field_id,password_field_id,login_submit_id,logout_url,logout_id):
# 	site_login_page = SiteLoginPage(login_url,username,password,username_field_id,password_field_id,login_submit_id,logout_url,logout_id)
# 	return site_login_page

def main ():
	site_1 = SiteLoginPage(
			"https://www.pfizerforprofessional.com/login",
			"ericjsilva+cn2@gmail.com",
			"Pass@word1",
			"edit-username",
			"edit-password",
			"edit-submit--2",
			"https://www.pfizermedicalinformation.cn/UserProfile.aspx?update=1",
			"ctl00_loginViewAnonymous_Status")
	driver = webdriver.Chrome()
	
	navigate_and_log_in(driver,site_1)
	driver.close()
	
	# assert "Silva Eric" in driver.page_source
def bypass_verification(driver,verify_class):
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, verify_class)))
	sleep(1)
	elem.click()
	
def navigate_and_log_in (driver,site):
	driver.get(site.login_url)
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/pfizer-grv/user/login/nojs"]')))
	sleep(1)
	elem.click()
	elem = wait.until(EC.element_to_be_clickable((By.ID, site.login_submit_id)))
	elem = driver.find_element_by_id(site.username_field_id)
	elem.send_keys(site.username)
	elem = driver.find_element_by_id(site.password_field_id)
	elem.send_keys(site.password)
	elem = driver.find_element_by_id(site.login_submit_id)
	elem.click()
	elem = driver.find_element_by_id(site.login_submit_id)
	elem = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "usr")))
	# assert site.username in driver.page_source
	print elem.text
	
if __name__ == "__main__":
    main()
