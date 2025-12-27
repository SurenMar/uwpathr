import requests
import time
from courses.utils.course_utils import split_full_code, process_subject_code


_URL = 'https://uwflow.com/graphql'


def fetch_all_program_codes():
  time.sleep(1)

  courses_query = """
    query {
      course {
        code
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

  program_codes = list()
  for course in data['data']['course']:
    code, _ = split_full_code(course['code'])
    code = process_subject_code(code)
    if code == '':
      continue
    program_codes.append(code.upper())

  # Remove duplicates and return
  return list(set(program_codes))

import json
data = fetch_all_program_codes()
with open('subject_codes.json', 'w') as f:
  json.dump(data, f, indent=2)