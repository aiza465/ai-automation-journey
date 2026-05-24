from pathlib import Path
import os
print(Path('spam', 'bacon', 'eggs'))
print(str(Path('spam', 'bacon', 'eggs')))
my_files = ['accounts.txt', 'details.csv', 'invite.docx']
for filename in my_files:
   print(Path(r'C:\Users\Al', filename))

Path.cwd()
Path.home()
os.chdir('C:\\Windows\\System32')
Path.cwd()