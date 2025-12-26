from bs4 import BeautifulSoup
import requests
import time
import pdfplumber
import re
from pathlib import Path

from courses.utils.course_utils import split_full_code
from courses.services.uwflow_client import fetch_all_program_codes


def scrape_courses(program: str):
  """
  Scrapes course reqs and units for all courses in a program.
  Client must process the prerequisite list themeselves.
  """
  time.sleep(1)
  url = f'https://ucalendar.uwaterloo.ca/2324/COURSE/course-{program.upper()}.html'
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  courses_html = soup.find_all('center')
  requisites = list()
  
  for course_html in courses_html:
    # Find course name
    a_tag = course_html.find('a')
    if not a_tag or 'name' not in a_tag.attrs:
      continue
    course_name = a_tag['name']
    code, number = split_full_code(course_name)

    # Find units
    units = None
    strong_tag = course_html.find('strong')
    if strong_tag:
      strong_text = strong_tag.get_text(' ', strip=True)
      for part in reversed(strong_text.split()):
        try:
          units = float(part)
          break
        except ValueError:
          continue
    
    requisites.append({
      'code': code,
      'number': number,
      'units': int(units * 100),
    })

    # Find course prereqs
    prereq_tag = course_html.find('em', string=lambda text: 
      text and text.strip().lower().startswith('prereq:'))
    course_prereqs = prereq_tag.text if prereq_tag else None
    requisites[-1]['prereqs'] = course_prereqs

    # Find course antireqs
    antireq_tag = course_html.find('em', string=lambda text: 
      text and text.strip().lower().startswith('antireq:'))
    course_antireqs = antireq_tag.text if antireq_tag else None

    # Process antirequisites
    requisites[-1]['antireqs'] = course_antireqs

    # Find course coreqs
    coreq_tag = course_html.find('em', string=lambda text: 
      text and text.strip().lower().startswith('coreq:'))
    course_coreqs = coreq_tag.text if coreq_tag else None

    # Process corequisites
    requisites[-1]['coreqs'] = course_coreqs

  return requisites


def _find_math_courses():
  programs = ['ACTSC', 'AMATH', 'CO', 'CS', 'MATBUS', 'MATH', 'PMATH', 'STAT']
  courses = [scrape_courses(program) for program in programs]

  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_non_math_courses():
  math_programs = ['ACTSC', 'AMATH', 'CO', 'CS', 'MATBUS', 'MATH', 'PMATH', 'STAT']
  programs = list(set(fetch_all_program_codes()) - set(math_programs))
  courses = [scrape_courses(program) for program in programs]

  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_cs_courses():
  courses = scrape_courses('CS')

  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_hum_courses():
  """Scrape humanities subject codes from UW CS breadth requirements page"""
  time.sleep(1)
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  
  # Find the breadth requirements table and extract humanities row
  tables = soup.find_all('table')
  programs = list()
  for table in tables:
    rows = table.find_all('tr')
    for row in rows:
      cells = row.find_all('td')
      if cells and 'Humanities' in cells[0].get_text():
        # Extract subject codes from the third column
        codes_text = cells[2].get_text(strip=True)
        programs = [code.strip().upper() for code in codes_text.split(',')]
        break

  courses = [scrape_courses(program) for program in programs]
  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses


def _find_ss_courses():
  """Scrape social sciences subject codes from UW CS breadth requirements page"""
  time.sleep(1)  # Rate limiting
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  
  # Find the breadth requirements table and extract social sciences row
  tables = soup.find_all('table')
  programs = list()
  for table in tables:
    rows = table.find_all('tr')
    for row in rows:
      cells = row.find_all('td')
      if cells and 'Social Sciences' in cells[0].get_text():
        # Extract subject codes from the third column
        codes_text = cells[2].get_text(strip=True)
        programs = [code.strip().upper() for code in codes_text.split(',')]
        break

  courses = [scrape_courses(program) for program in programs]
  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_ps_courses():
  """Scrape pure sciences subject codes from UW CS breadth requirements page"""
  time.sleep(1)  # Rate limiting
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  
  # Find the breadth requirements table and extract pure sciences row
  tables = soup.find_all('table')
  programs = list()
  for table in tables:
    rows = table.find_all('tr')
    for row in rows:
      cells = row.find_all('td')
      if cells and 'Pure Sciences' in cells[0].get_text() and 'Applied' not in cells[0].get_text():
        # Extract subject codes from the third column
        codes_text = cells[2].get_text(strip=True)
        programs = [code.strip().upper() for code in codes_text.split(',')]
        break

  courses = [scrape_courses(program) for program in programs]
  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_as_courses():
  """Scrape applied sciences subject codes from UW CS breadth requirements page"""
  time.sleep(1)  # Rate limiting
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  
  # Find the breadth requirements table and extract pure and applied sciences row
  tables = soup.find_all('table')
  programs = list()
  for table in tables:
    rows = table.find_all('tr')
    for row in rows:
      cells = row.find_all('td')
      if cells and 'Pure and Applied Sciences' in cells[0].get_text():
        # Extract subject codes from the third column
        codes_text = cells[2].get_text(strip=True)
        programs = [code.strip().upper() for code in codes_text.split(',')]
        break

  courses = [scrape_courses(program) for program in programs]
  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_comm1_courses():
  """Extract Communication List 1 courses from cs_checklist.pdf"""
  pdf_path = Path(__file__).resolve().parents[2] / 'cs_checklist.pdf'
  courses = set()
  
  with pdfplumber.open(pdf_path) as pdf:
    # Read all pages to find the communications lists section
    for page in pdf.pages:
      text = page.extract_text()
      if 'Communication (List 1)' in text or 'Communications (List 1)' in text:
        # Extract course codes after the List 1 heading
        lines = text.split('\n')
        in_list1 = False
        for line in lines:
          if 'Communication' in line and 'List 1' in line:
            in_list1 = True
            continue
          if in_list1:
            # Stop when we hit List 2 or another section
            if 'List 2' in line or 'Breadth' in line or 'Depth' in line:
              break
            # Extract course codes (e.g., ENGL119, CS100)
            matches = re.findall(r'\b([A-Z]{2,10}\s?\d{3}[A-Z]?)\b', line)
            for match in matches:
              # Remove any spaces
              course = match.replace(' ', '')
              courses.add(course)
  
  return list(courses)

def _find_comm2_courses():
  """Extract Communication List 2 courses from cs_checklist.pdf"""
  pdf_path = Path(__file__).resolve().parents[2] / 'cs_checklist.pdf'
  courses = set()
  
  with pdfplumber.open(pdf_path) as pdf:
    # Read all pages to find the communications lists section
    for page in pdf.pages:
      text = page.extract_text()
      if 'Communication (List 2)' in text or 'Communications (List 2)' in text:
        # Extract course codes after the List 2 heading
        lines = text.split('\n')
        in_list2 = False
        for line in lines:
          if 'Communication' in line and 'List 2' in line:
            in_list2 = True
            continue
          if in_list2:
            # Stop when we hit another major section
            if 'Breadth' in line or 'Depth' in line or 'Notes:' in line:
              break
            # Extract course codes (e.g., ENGL119, CS100)
            matches = re.findall(r'\b([A-Z]{2,10}\s?\d{3}[A-Z]?)\b', line)
            for match in matches:
              # Remove any spaces
              course = match.replace(' ', '')
              courses.add(course)
  
  return list(courses)
  
def scrape_categories():
  return {
    'math': _find_math_courses(),           # Math
    'non_math': _find_non_math_courses(),   # Non-Math
    'cs': _find_cs_courses(),               # Computer Science
    'hum': _find_hum_courses(),             # Humanities
    'ss': _find_ss_courses(),               # Social Science
    'ps': _find_ps_courses(),               # Pure Science
    'as': _find_as_courses(),               # Applied Science
    'comm1': _find_comm1_courses(),         # Communications List 1
    'com,2': _find_comm2_courses(),         # Communications List 2
  }

# TODO moce to fill_courses.py
def scrape_all_programs_reqs():
  client = UWFlowClient()
  program_codes = client.fetch_all_program_codes()
  data = dict()

  for code in program_codes:
    data[code.upper()] = UWWebScraper.scrape_program_reqs(code.upper())

  return data


# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------
# TO DO LIST -----------------------------------------------------------------------------

# - Have fill_courses orchestrate everything, meaning it should be the one to call
#   fetch_all_program_codes from UWFlowClient. fill_course should have a main() 
#   function to do this, along with calling the other services/ methods.
# - Find correct course categories
# - THE PREREQS HAVE TO FIRST BE SENT TO GPT THEN TO FILL_COURSES!!!!!!!!!!!!!!!!!
# - Fill checklists from up to 4 years back
# - Add scripts that copy appropriate checklist whenever user account is made