import pdfplumber
import re
from pathlib import Path
import time
from bs4 import BeautifulSoup
import requests
from courses.services.uw_web_scraper.courses_data import scrape_courses
from courses.services.uwflow_client.program_data import fetch_all_program_codes


def _find_math_courses():
  programs = ['ACTSC', 'AMATH', 'CO', 'CS', 'MATBUS', 'MATH', 'PMATH', 'STAT']
  courses = [course for program in programs for course in scrape_courses(program)]

  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses

def _find_non_math_courses():
  math_programs = ['ACTSC', 'AMATH', 'CO', 'CS', 'MATBUS', 'MATH', 'PMATH', 'STAT']
  programs = list(set(fetch_all_program_codes()) - set(math_programs))
  courses = [course for program in programs for course in scrape_courses(program)]

  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses

def _find_cs_courses():
  courses = scrape_courses('CS')

  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses

def _find_hum_courses():
  """Scrape humanities subject codes from UW CS breadth requirements page"""
  time.sleep(1)
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url, timeout=15)
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

  courses = [course for program in programs for course in scrape_courses(program)]
  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses


def _find_ss_courses():
  """Scrape social sciences subject codes from UW CS breadth requirements page"""
  time.sleep(1)  # Rate limiting
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url, timeout=15)
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

  courses = [course for program in programs for course in scrape_courses(program)]
  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses

def _find_ps_courses():
  """Scrape pure sciences subject codes from UW CS breadth requirements page"""
  time.sleep(1)  # Rate limiting
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url, timeout=15)
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

  courses = [course for program in programs for course in scrape_courses(program)]
  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses

def _find_as_courses():
  """Scrape applied sciences subject codes from UW CS breadth requirements page"""
  time.sleep(1)  # Rate limiting
  url = 'https://uwaterloo.ca/computer-science/current-undergraduate-students/majors/breadth-and-depth-requirements'
  page = requests.get(url, timeout=15)
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

  courses = [course for program in programs for course in scrape_courses(program)]
  filtered_courses = list()
  for course in courses:
    filtered_courses.append(course['code'] + course['number'])
  return filtered_courses

def _find_comm1_courses():
  """Extract Communication List 1 courses from cs_checklist.pdf"""
  pdf_path = Path(__file__).resolve().parent / 'cs_checklist.pdf'
  courses = list()

  def token_to_courses(token: str):
    token = token.strip().rstrip('.')
    m = re.search(r'(\d{3}[A-Z]?)', token)
    if not m:
      return []
    number = m.group(1)
    prefix = token[:m.start(1)].strip()
    codes_part = prefix.replace(' ', '')
    codes = [c for c in codes_part.split('/') if c]
    return [f"{c}{number}" for c in codes]

  with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
      text = page.extract_text() or ''
      lines = text.split('\n')
      collecting = False
      for line in lines:
        s = line.strip()
        if not collecting:
          if s.startswith('1Communication List') or 'Communication List I:' in s:
            collecting = True
            # Start collecting after the phrase " of " to skip the leading requirement text
            tail = s.split(':', 1)[1] if ':' in s else s
            segment = tail.split(' of ', 1)[1] if ' of ' in tail else tail
            tokens = [t.strip() for t in segment.split(',') if t.strip()]
            for t in tokens:
              courses.extend(token_to_courses(t))
            continue
        else:
          if s.startswith('2Communication List') or 'Communication List II:' in s:
            break
          tokens = [t.strip() for t in s.split(',') if t.strip()]
          for t in tokens:
            courses.extend(token_to_courses(t))
      if courses:
        break

  return courses

def _find_comm2_courses():
  """Extract Communication List 2 courses from cs_checklist.pdf"""
  pdf_path = Path(__file__).resolve().parent / 'cs_checklist.pdf'
  courses = list()
  
  with pdfplumber.open(pdf_path) as pdf:
    # Read all pages to find the communications lists section
    for page in pdf.pages:
      text = page.extract_text() or ''
      lines = text.split('\n')
      collecting = False

      def token_to_courses(token: str):
        token = token.strip().rstrip('.')
        m = re.search(r'(\d{3}[A-Z]?)', token)
        if not m:
          return []
        number = m.group(1)
        prefix = token[:m.start(1)].strip()
        codes_part = prefix.replace(' ', '')
        codes = [c for c in codes_part.split('/') if c]
        return [f"{c}{number}" for c in codes]

      for line in lines:
        s = line.strip()
        if not collecting:
          if s.startswith('2Communication List') or 'Communication List II:' in s:
            collecting = True
            tail = s.split(':', 1)[1] if ':' in s else s
            segment = tail.split(' of ', 1)[1] if ' of ' in tail else tail
            tokens = [t.strip() for t in segment.split(',') if t.strip()]
            for t in tokens:
              courses.extend(token_to_courses(t))
            continue
        else:
          # Continue collecting tokens from subsequent lines (handle continuation)
          tokens = [t.strip() for t in s.split(',') if t.strip()]
          for t in tokens:
            courses.extend(token_to_courses(t))
      if courses:
        break
  
  courses.append('ENGL101B')
  courses.append('MTHEL300')
  return courses
  
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
