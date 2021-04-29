
import re

with open("example_output.txt") as fr:

    out_text = fr.read()

result = []
res = re.findall(r'LibraryIdentifier\s+:\s+Package name:\s+(\S+)\s+', out_text)
if res:
    a = res[0]
    print("/".join(a.split(".")))
res = re.findall(r'LibraryIdentifier\s+:\s+minSdkVersion:\s+(\S+)\s+', out_text)
if res:
    print(res[0])
res = re.findall(r'LibraryIdentifier\s+:\s+targetSdkVersion:\s+(\S+)\s+', out_text)
if res:
    print(res[0])