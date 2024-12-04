import re
import sys

memory = sys.stdin.read()
findings = re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory)
print(sum(list(int.__mul__(*map(int, finding.groups())) for finding in findings)))
