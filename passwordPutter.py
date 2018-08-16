import importlib
from splinter import Browser
password2 = 'fakepassword'
browser2 = Browser()
browser2.visit('fakesite')
browser2.find_by_name('Pass1').first.fill(password2)
browser2.find_by_name('Submit0').first.click()
print (browser2.html)
browser2.quit()