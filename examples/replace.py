import re
org_string = "This is a sample string"
print("original string = " + org_string)

pattern = r's'
# Replace all occurrences of character s with an empty string
mod_string = re.sub(pattern, '', org_string )
print(mod_string)
