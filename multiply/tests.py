from ast import keyword
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class PlayerFormTest(LiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome()
    #Choose your url to visit
    selenium.get('http://127.0.0.1:8000/')
    #find the elements you need to submit form

    keyword = selenium.find_element_by_id('item')

    submit = selenium.find_element_by_id('submit_button')

    #populate the form with data
    keyword.send_keys('Dell Latitude')
    

    #submit form
    submit.send_keys(Keys.RETURN)

    #check result; page source looks at entire html document
    assert 'Dell Latitude' in selenium.page_source