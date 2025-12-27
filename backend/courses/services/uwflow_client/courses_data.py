import requests
import time

from courses.utils.course_utils import (
  split_full_code, 
  process_subject_code, 
  strip_number,
)
from courses.services.uw_web_scraper.category_data import scrape_categories


_URL = 'https://uwflow.com/graphql'
#_CATEGORIES = scrape_categories()


def _find_categories(code: str, number: str):
  full_code = code + number
  found_categories = list()
  
  for category, category_list in _CATEGORIES:
    if full_code in category_list:
      found_categories.append(category)
  return found_categories

def fetch_all_courses_data():
  time.sleep(1)

  def percent_or_none(val):
    return None if val is None else round(val * 100, 2)

  courses_query = """
    query {
      course {
        code
        name
        description
        rating {
          filled_count
          liked
          useful
          easy
        }
      }
    }
  """

  response = requests.post(
    _URL, 
    json={'query': courses_query},
    timeout=15
  )
  response.raise_for_status()
  data = response.json()

  # Clean up data and split course names
  courses = list()
  for course in data['data']['course']:
    code, number = split_full_code(course['code'])
    # Filter course
    over_500 = [
      'CIVE', 'GENE', 'SYDE', 'CHE', 'ARCH', 'GEO', 'GEOE', 'BME', 'ME', 
      'MSCI', 'MTE', 'BET', 'ENVE', 'AE'
    ]
    if code.upper().endswith('XXX') or process_subject_code(code) == '' or \
       (number and strip_number(number) >= 500  and code.upper() not in over_500) or \
       (number and strip_number(number) >= 600):
      continue
    courses.append({
      'code': code.upper(),
      'number': number.upper(),
      #'category': _find_categories(code.upper(), number.upper()),
      'title': course['name'],
      'description': course['description'],
      'num_uwflow_ratings': course['rating']['filled_count'] if course['rating']['filled_count'] is not None else None,
      'uwflow_liked_rating': percent_or_none(course['rating']['liked']),
      'uwflow_easy_ratings': percent_or_none(course['rating']['easy']),
      'uwflow_useful_ratings': percent_or_none(course['rating']['useful']),
    })

    # Manually add any missing courses
    

  return courses