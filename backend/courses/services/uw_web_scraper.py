from bs4 import BeautifulSoup
import requests

from courses.utils.course_utils import split_full_code
from courses.services.uwflow_client import UWFlowClient

class UWWebScraper:
  base_url = 'https://ucalendar.uwaterloo.ca/2324/COURSE/'

  def scrape_program_reqs(self, program: str):
    url = UWWebScraper.base_url + f'course-{program.upper()}.html'
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
      requisites.append({
        'code': code,
        'number': number,
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
      requisites[-1]['antireqs'] = course_antireqs

      # Find course coreqs
      coreq_tag = course_html.find('em', string=lambda text: 
        text and text.strip().lower().startswith('coreq:'))
      course_coreqs = coreq_tag.text if coreq_tag else None
      requisites[-1]['coreqs'] = course_coreqs

    return requisites

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
# - Reorganize the data given from fetch_all_courses_data in UWFlowClient in a
#   predictable format.
# - THE PREREQS HAVE TO FIRST BE SENT TO GPT THEN TO FILL_COURSES!!!!!!!!!!!!!!!!!