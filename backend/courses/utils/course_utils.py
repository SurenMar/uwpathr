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