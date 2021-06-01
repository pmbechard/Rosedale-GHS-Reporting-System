import mechanize
from bs4 import BeautifulSoup
import http.cookiejar
import re
from docx import Document
from datetime import date

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
name = soup.find('div', class_='myprofileitem fullname').text
name = name.strip().split(' ')
name = ' '.join(name[1:])
print(f'\nWelcome, {name}!')

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
        side_menu = soup.find_all('li', class_='r0')

        # Find link for active students page
        class_list_link = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(side_menu[3]))
        class_list_link = class_list_link[0]

        # Opening active students page
        br.open(class_list_link)
        soup = BeautifulSoup(br.response().read(), 'lxml')
        class_list = soup.find_all('a', class_='', target='_blank')

        # Iterating list of students
        students = []
        print("\nClass list:")
        for student in class_list:
            if not student.text.isdigit():
                print(f'\t>{student.text.strip()}')
                students.append(student.text.strip())


# Initializing the CT Comments docx, making a copy for new input
print("\n\nInitializing .docx file...")

document = Document('CT Comments and Learning Skills.docx')

course_choice = course_choice.split(' ')
if course_choice[0][0] == '*':
    document.save(f'{course_choice[0][1:]} - CT Comments and Learning Skills - {date.today()}.docx')
else:
    document.save(f'{course_choice[0]} - CT Comments and Learning Skills - {date.today()}.docx')

document.tables[0].cell(0, 1).text = 'Northeastern University branch - Shenyang'
document.tables[0].cell(1, 1).text = course_choice[0][1:]
mid_or_fin = input(f'\t{document.tables[0].cell(2, 0).text} ')
document.tables[0].cell(2, 1).text = mid_or_fin
document.tables[0].cell(3, 1).text = name
document.tables[0].cell(4, 1).text = str(len(students))

if course_choice[0][0] == '*':
    document.save(f'{course_choice[0][1:]} - CT Comments and Learning Skills - {date.today()}.docx')
else:
    document.save(f'{course_choice[0]} - CT Comments and Learning Skills - {date.today()}.docx')

if len(document.tables[1].rows) < len(students):
    for i in range(len(students) - len(document.tables[1].rows) + 1):
        document.tables[1].add_row()

count = 1
for student in students:
    document.tables[1].cell(count, 0).text = student
    count += 1

if course_choice[0][0] == '*':
    document.save(f'{course_choice[0][1:]} - CT Comments and Learning Skills - {date.today()}.docx')
else:
    document.save(f'{course_choice[0]} - CT Comments and Learning Skills - {date.today()}.docx')

