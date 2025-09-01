# Importing the BeautifulSoup library
from bs4 import BeautifulSoup

with open('html_file.html', 'r') as html_file:
    content= html_file.read()
# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(content, 'html.parser')

tags= soup.find_all('p')
print('All paragraph tags:')
for tag in tags:
    print(tag)

courses= soup.find_all('div', class_='course')
for course in courses:  
    course_name = course.h2.text
    course_price = course.find('span', class_='price').text.split()[-1]
    print(f' \n{course_name} course costs {course_price}')