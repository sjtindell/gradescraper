import urllib2
from bs4 import BeautifulSoup

html = '''
<html>
<head>
</head>
<body>
<div id="1">numberone</div>
<div id="2">numbertwo</div>
</body>
</html>
'''
print BeautifulSoup(html, 'html.parser').find('div', {"id":"1"})


response = urllib2.urlopen('http://simms-teach.com/cis90calendar.php')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
print soup.prettify()
