import re

pattern = r"\b[a-z]+_[a-z]+\b"

text = "this_is a test_string with some_examples and Invalid_Example"

matches = re.findall(pattern, text)

print(matches)