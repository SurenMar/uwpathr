import requests
import json

class UWFlowClient:
  url = 'https://uwflow.com/graphql'

  def fetch_all_courses_data(self):
    courses_query = """
      query {
        course {
          id
          code
          name
          description
          rating 
          course_easy_buckets_aggregate {
            aggregate_course_easy_buckets_aggregate
          }
          course_useful_buckets_aggregate {
            aggregate_course_easy_buckets_aggregate
          }
        }
      }
    """

    fields_query = """
    query {
      __type(name: "aggregate_course_rating") {
        name
        fields {
          name
          type {
            kind
            name
            ofType {
              kind
              name
            }
          }
        }
      }
    }
    """

    response = requests.post(
      self.url, 
      json={'query': fields_query},
      timeout=15
    )
    response.raise_for_status()

    data = response.json()
    with open('uwflow_courses_fields.json', 'w') as f:
      json.dump(data, f, indent=2)


'''
from courses.services.uwflow_client import UWFlowClient
client = UWFlowClient()
data = client.fetch_course("CS246")
print(data)
'''

client = UWFlowClient()
client.fetch_all_courses_data()