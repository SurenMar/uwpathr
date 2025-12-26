import requests
import json

from courses.utils.course_utils import split_full_code

class UWFlowClient:
  url = 'https://uwflow.com/graphql'

  def fetch_all_courses_data(self):
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
      self.url, 
      json={'query': courses_query},
      timeout=15
    )
    response.raise_for_status()

    data = response.json()
    # TODO SPLIT DATA BEFORE RETURNING DATA
    return data

    # For testing
    # with open('uwflow_courses.json', 'w') as f:
    #   json.dump(data, f, indent=2)

  def fetch_all_program_codes(self):
    courses_query = """
      query {
        course {
          code
        }
      }
    """

    response = requests.post(
      self.url, 
      json={'query': courses_query},
      timeout=15
    )
    response.raise_for_status()

    data = response.json()
    program_codes = list()
    for course in data['data']['course']:
      code, _ = split_full_code(course['code'])
      program_codes.append(code)

    return program_codes
  
    # For testing
    # with open('uwflow_courses_fields.json', 'w') as f:
    #   json.dump(data, f, indent=2)


# For testing
client = UWFlowClient()
client.fetch_all_program_codes()