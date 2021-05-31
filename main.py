import mechanize
from bs4 import BeautifulSoup
import http.cookiejar
import re

# Website Config
# username = input("Username/Email: ")
# password = input("Password: ")
# username = 'pbechard@koreamail.com'
# password = '-642Un769'
# username = 'vicky5'
# password = 'AMY20050916'
username = 'abrahammiha@gmail.com'
password = 'Batdaddy1'
url = 'https://ghs.rosedaleedu.com/login/index.php'

# Authorization Config
cj = http.cookiejar.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open(url)

br.select_form(nr=0)
br.form['username'] = username
br.form['password'] = password
br.submit()

# Scraping for course list
soup = BeautifulSoup(br.response().read(), 'lxml')
courses = soup.find_all('h3', class_='coursename')

# Iteration of courses into dictionary
counter = 1
courses_dict = {}
print("\n====================COURSE LIST====================")
for course in courses:
    print(f'{counter}. {course.text.strip()}')
    courses_dict[counter] = course.text.strip()
    counter += 1

# User input for course of choice
course_choice = input("\nPlease enter the number of the course you need to access: ")
course_choice = courses_dict[int(course_choice)]
print(f"\tYou've chosen {course_choice}")
print(f"\tEntering course page for {course_choice}...")

# Searching dictionary for course
for course in courses:
    if course_choice in course.text:
        # Find link for course page
        course_link = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(course))
        course_link = course_link[0]

        # Opening course page
        br.open(course_link)
        soup = BeautifulSoup(br.response().read(), 'lxml')
        side_menu = soup.find_all('div', class_='column c1')

        # Find link for active students page
        class_list_link = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(side_menu))
        class_list_link = class_list_link[0]

        # Opening active students page
        br.open(class_list_link)
        soup = BeautifulSoup(br.response().read(), 'lxml')
        class_list = soup.find_all('a', class_='aabtn')

        # Iterating list of students
        students = []
        print("\nClass list:")
        for student in class_list:
            print(f'\t>{student.text}')
            students.append(student.text)



