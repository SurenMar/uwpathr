from bs4 import BeautifulSoup
import requests
import time
from courses.utils.course_utils import split_full_code


def scrape_courses(program: str):
  """
  Scrapes course reqs and units for all courses in a program.
  Client must process the prerequisite list themeselves.
  """
  time.sleep(3)
  print(program)
  url = f'https://ucalendar.uwaterloo.ca/2324/COURSE/course-{program.upper()}.html'
  page = requests.get(url, timeout=120)
  if page.status_code == 404:
    return []
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
# - Have courses ordered in an order that they can be added to the list. Sort by each 
#   program name and add them one at a time, from lowest to highest level.
# - THE PREREQS HAVE TO FIRST BE SENT TO GPT THEN TO FILL_COURSES!!!!!!!!!!!!!!!!!
# - Fill checklists from up to 4 years back
# - Add scripts that copy appropriate checklist whenever user account is made



  