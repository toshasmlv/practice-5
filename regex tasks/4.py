import re

pattern = r"\b[A-Z][a-z]+\b"

text = "Hello world, This is a Test String with Some Words"

matches = re.findall(pattern, text)

print(matches)