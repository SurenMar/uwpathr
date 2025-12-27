from django.core.management.base import BaseCommand
import json
from courses.services.uwflow_client.program_data import fetch_all_program_codes
from courses.services.uw_web_scraper.courses_data import scrape_courses

class Command(BaseCommand):
  help = "Scrape courses prerequisites and store them in uw_course_reqs.py"

  def handle(self, *args, **options):
    data = [
      course
      for code in fetch_all_program_codes()
      for course in scrape_courses(code)
    ]
    with open('uw_course_reqs.json', 'w') as f:
      json.dump(data, f, indent=2)