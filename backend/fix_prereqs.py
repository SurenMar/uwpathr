import json

def foo():
  prereqs = dict()
  # Override prerequisites with curated mapping
  with open('only_prereqs.json', 'r') as f:
    prereqs = json.load(f)

  for course, prereq in list(prereqs.items()):
    code = ''
    if prereq is None:
      continue
    for c in prereq:
      if c.isalpha() or (c.isnumeric() and code):
        code += c
      elif code:
        if code not in prereqs:
          prereqs[course] = None
          print('error')
          break
        code = ''

  with open('only_prereqs.json', 'w') as f:
    json.dump(prereqs, f, indent=2)

foo()
      
