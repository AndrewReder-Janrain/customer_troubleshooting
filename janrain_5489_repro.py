#!/usr/bin/env
# -*- coding: utf-8 -*-

import json
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

	def __init__(self,login_url,login_link_url,username,password,username_field_id,password_field_id,login_submit_id,profile_username_id,logout_url,logout_id):
		self.login_url = login_url
		self.login_link_url = login_link_url
		self.username = username
		self.password = password
		self.username_field_id = username_field_id
		self.password_field_id = password_field_id
		self.login_submit_id = login_submit_id
		self.profile_username_id = profile_username_id
		self.logout_url = logout_url
		self.logout_id = logout_id

def main():
	with open('credentials.json') as credentials_file:   
		credentials = json.load(credentials_file)
	# # print credentials
	
	site_1 = SiteLoginPage(
			"https://www.pfizerforprofessional.com/login",
			"/pfizer-grv/user/login/nojs",
			credentials["username"],
			credentials["password"],
			"edit-username",
			"edit-password",
			"edit-submit--2",
			"usr",
			"https://www.pfizermedicalinformation.cn/UserProfile.aspx?update=1",
			"grv_end_session")
	site_2 = SiteLoginPage(
			"https://pfizermedicalinformation.cn",
			"/pfizer-grv/user/login/nojs",
			credentials["username"],
			credentials["password"],
			"ctl00_loginViewAnonymous_HcpLogin_Username",
			"ctl00_loginViewAnonymous_HcpLogin_Password",
			"ctl00_loginViewAnonymous_HcpLogin_btnSignIn",
			"ctl00_BodyContent_txtEmail",
			"https://www.pfizermedicalinformation.cn/UserProfile.aspx?update=1",
			"ctl00_loginViewAnonymous_Status")
	driver = webdriver.Chrome()
	navigate_and_log_in(driver,site_1)
	navigate_and_sso(driver,site_2)
	log_out(driver,site_1)
	navigate_and_confirm_logout(driver,site_2)
	navigate_and_login_simple(driver,site_2)
	modify_local_storage(driver,site_2)
	navigate_and_sso(driver,site_1)
	# driver.close()
	
	# assert "Silva Eric" in driver.page_source
def bypass_verification(driver,verify_class):
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, verify_class)))
	sleep(1)
	elem.click()
	
def navigate_and_log_in(driver,site):
	driver.get(site.login_url)
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="'+site.login_link_url+'"]')))
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
	elem = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, site.profile_username_id)))
	# assert site.username in driver.page_source
	print elem.text

def navigate_and_sso(driver,site):
	driver.get(site.login_url)
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.visibility_of_element_located((By.ID, site.profile_username_id)))
	sleep(1)
	print elem.get_attribute("value")

def navigate_and_confirm_logout(driver,site):
	driver.get(site.login_url)
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.visibility_of_element_located((By.ID, site.username_field_id)))
	sleep(1)
	# print elem.get_attribute("value")

def modify_local_storage(driver,site):
	driver.execute_script('localStorage.setItem("janrainCaptureTokenRefresh","Tue, 29 Mar 2016 00:24:21 GMT")')

def navigate_and_login_simple(driver,site):
	driver.get(site.login_url)
	wait = WebDriverWait(driver,20)

	elem = wait.until(EC.element_to_be_clickable((By.ID, site.login_submit_id)))
	elem = driver.find_element_by_id(site.username_field_id)
	elem.send_keys(site.username)
	elem = driver.find_element_by_id(site.password_field_id)
	elem.send_keys(site.password)
	elem = driver.find_element_by_id(site.login_submit_id)
	sleep(1)
	elem.click()
	elem = driver.find_element_by_id(site.login_submit_id)
	wait.until(EC.alert_is_present())
	alert = driver.switch_to_alert()
	alert.accept()
	elem = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, site.profile_username_id)))
	# assert site.username in driver.page_source
	print elem.text

def log_out(driver,site):
	driver.get(site.login_url)
	wait = WebDriverWait(driver,20)
	elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, site.logout_id)))
	sleep(1)
	elem.click()
	

if __name__ == "__main__":
    main()
