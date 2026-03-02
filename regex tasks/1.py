import re

pattern = r"^ab*$"

test_strings = ["a", "ab", "abb", "abbb", "b", "aa", "ac"]

for s in test_strings:
    if re.match(pattern, s):
        print(f"{s} -> Match")
    else:
        print(f"{s} -> No match")