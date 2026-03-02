import re

pattern = r"^a.*b$"

test_strings = ["ab", "acb", "a123b", "aXYZb", "a_b", "a", "b", "ba"]

for s in test_strings:
    if re.match(pattern, s):
        print(f"{s} -> Match")
    else:
        print(f"{s} -> No match")