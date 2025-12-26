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

  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_non_math_courses():
  math_programs = ['ACTSC', 'AMATH', 'CO', 'CS', 'MATBUS', 'MATH', 'PMATH', 'STAT']
  programs = list(set(fetch_all_program_codes()) - set(math_programs))
  courses = [course for program in programs for course in scrape_courses(program)]

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

  courses = [course for program in programs for course in scrape_courses(program)]
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

  courses = [course for program in programs for course in scrape_courses(program)]
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

  courses = [course for program in programs for course in scrape_courses(program)]
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

  courses = [course for program in programs for course in scrape_courses(program)]
  filtered_courses = set()
  for course in courses:
    filtered_courses.add(course['code'] + course['number'])
  return filtered_courses

def _find_comm1_courses():
  """Extract Communication List 1 courses from cs_checklist.pdf"""
  pdf_path = Path(__file__).resolve().parent / 'cs_checklist.pdf'
  courses = set()
  
  with pdfplumber.open(pdf_path) as pdf:
    # Read all pages to find the communications lists section
    for page in pdf.pages:
      text = page.extract_text()
      # Look for the footnote line starting with "1Communication List I:"
      lines = text.split('\n')
      for line in lines:
        if line.strip().startswith('1Communication List') or 'Communication List I:' in line:
          # Handle slash format first (e.g., "EMLS/ENGL 129R")
          slash_matches = re.findall(r'([A-Z]+)/([A-Z]+)\s+(\d{3}[A-Z]?)', line)
          for code1, code2, number in slash_matches:
            courses.add(f"{code1}{number}")
            courses.add(f"{code2}{number}")
          
          # Remove slash patterns from line to avoid double-matching
          line_cleaned = re.sub(r'([A-Z]+)/([A-Z]+)\s+(\d{3}[A-Z]?)', '', line)
          
          # Extract remaining course codes (format: CODE 123X)
          matches = re.findall(r'([A-Z]+)\s+(\d{3}[A-Z]?)', line_cleaned)
          for code, number in matches:
            courses.add(f"{code}{number}")
          break
  
  return list(courses)

def _find_comm2_courses():
  """Extract Communication List 2 courses from cs_checklist.pdf"""
  pdf_path = Path(__file__).resolve().parent / 'cs_checklist.pdf'
  courses = set()
  
  with pdfplumber.open(pdf_path) as pdf:
    # Read all pages to find the communications lists section
    for page in pdf.pages:
      text = page.extract_text()
      # Look for the footnote line starting with "2Communication List II:"
      lines = text.split('\n')
      for line in lines:
        if line.strip().startswith('2Communication List') or 'Communication List II:' in line:
          # Handle slash format with same number first (e.g., "EMLS/ENGL 129R")
          slash_same = re.findall(r'([A-Z]+)/([A-Z]+)\s+(\d{3}[A-Z]?)', line)
          for code1, code2, number in slash_same:
            courses.add(f"{code1}{number}")
            courses.add(f"{code2}{number}")
          
          # Handle slash format with different numbers (e.g., "ENGL 378/MTHEL 300")
          slash_diff = re.findall(r'([A-Z]+)\s+(\d{3}[A-Z]?)/([A-Z]+)\s+(\d{3}[A-Z]?)', line)
          for code1, number1, code2, number2 in slash_diff:
            courses.add(f"{code1}{number1}")
            courses.add(f"{code2}{number2}")
          
          # Remove slash patterns from line to avoid double-matching
          line_cleaned = re.sub(r'([A-Z]+)/([A-Z]+)\s+(\d{3}[A-Z]?)', '', line)
          line_cleaned = re.sub(r'([A-Z]+)\s+(\d{3}[A-Z]?)/([A-Z]+)\s+(\d{3}[A-Z]?)', '', line_cleaned)
          
          # Extract remaining course codes (format: CODE 123X)
          matches = re.findall(r'([A-Z]+)\s+(\d{3}[A-Z]?)', line_cleaned)
          for code, number in matches:
            courses.add(f"{code}{number}")
          break
  
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

categories = scrape_categories()
for category, codes in categories:
  print(category)
  print(codes)
  print('\n\n')