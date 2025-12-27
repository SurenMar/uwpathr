def split_full_code(full_code: str):
    """Splits course code: 'CS246' -> ('CS', '246')"""
    code: str = ''
    number: str = ''
    reading_num: bool = False
    for c in full_code:
      if c.isnumeric():
        reading_num = True

      if not reading_num:
        code += c
      else:
        number += c
    return (code, number)

def process_subject_code(code: str):
  """Trims course code: 'CSXXX' -> 'CS'"""
  code = code.upper()
  if code.endswith('XXX'):
    return code.removesuffix('XXX')

  # Return blank if code contains a non letter character (not a valid code)
  for c in code:
    c = c.upper()
    if not c.isalpha():
      return ''
    
  return code
      
