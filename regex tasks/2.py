import re

pattern = r"^ab{2,3}$"

test_strings = ["abb", "abbb", "abbbb", "ab", "a", "b"]

for s in test_strings:
    if re.match(pattern, s):
        print(f"{s} -> Match")
    else:
        print(f"{s} -> No match")