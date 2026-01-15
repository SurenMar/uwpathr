#!/bin/bash
set -euo pipefail

echo "Applying migrations..."
python manage.py migrate --noinput

# Load fixtures only if tables are empty
COURSE_COUNT=$(python manage.py shell -c \
  "from courses.models import Course; print(Course.objects.count())" \
  2>/dev/null | tail -n 1)
if [ "$COURSE_COUNT" = "0" ]; then
  echo "Loading fixtures..."
  # Courses and prerequisites
  python manage.py loaddata fixtures/courses/courses.json
  python manage.py loaddata fixtures/courses/course_prerequisites.json

  # Checklists and related data
  python manage.py loaddata fixtures/checklists/requirements/specializations.json
  python manage.py loaddata fixtures/checklists/checklist/checklists.json
  python manage.py loaddata fixtures/checklists/checklist/checklist_nodes.json
  python manage.py loaddata fixtures/checklists/checklist/checkbox_allowed_courses.json
  python manage.py loaddata fixtures/checklists/requirements/non_course_requirements.json
fi
