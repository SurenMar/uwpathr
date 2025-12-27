import requests
import time

from courses.utils.course_utils import split_full_code
from courses.services.uw_web_scraper.category_data import scrape_categories


_URL = 'https://uwflow.com/graphql'
_CATEGORIES = scrape_categories()


def _find_categories(code: str, number: str):
  full_code = code + number
  found_categories = list()
  
  for category, category_list in _CATEGORIES:
    if full_code in category_list:
      found_categories.append(category)
  return found_categories

def fetch_all_courses_data(self):
  time.sleep(1)

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
    courses.append({
      'code': code.upper(),
      'number': number.upper(),
      'category': _find_categories(code.upper(), number.upper()),
      'title': course['name'],
      'description': course['description'],
      'num_uwflow_ratings': course['rating']['filled_count'],
      'uwflow_liked_rating': round(course['rating']['liked'] * 100, 2),
      'uwflow_easy_ratings': round(course['rating']['easy'] * 100, 2),
      'uwflow_useful_ratings': round(course['rating']['useful'] * 100, 2),
    })

  return courses