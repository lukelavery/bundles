import re


test = "2001.04.11 - Particulars of Claim"
test2 = "A. Court Documents"

pattern = "[0-9]{4}\.[0-9]{2}\.[0-9]{2} - .+"

if re.match(pattern=pattern, string=test):
    print('match')
else:
    print('no match')
