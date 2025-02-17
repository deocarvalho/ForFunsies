
def longest_substrand(str1, str2):
  smallest = str1 if len(str1) <= len(str2) else str2
  smallest_original = smallest
  biggest = str1 if smallest == str2 else str2
  smallest_length = len(smallest)
  biggest_length = len(biggest)

  while len(smallest) > 0:
    n = biggest_length // len(smallest)
    m = smallest_length // len(smallest)
    if smallest * n == biggest and smallest * m == smallest_original:
      return smallest
    smallest = smallest[:-1]
   
  return ''

str1 = "ATCATCATCATCATC"
str2 = "ATCATC"
print(f"Input: str1 = '{str1}' and str2 = '{str2}'")
print(f"Output: '{longest_substrand(str1, str2)}'")

str1 = "CCCCCCCCC"
str2 = "CC"
print(f"Input: str1 = '{str1}' and str2 = '{str2}'")
print(f"Output: '{longest_substrand(str1, str2)}'")

str1 = "ATAG"
str2 = "ATAGATAGATAGATAG"
print(f"Input: str1 = '{str1}' and str2 = '{str2}'")
print(f"Output: '{longest_substrand(str1, str2)}'")
