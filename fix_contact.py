import re
with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the "Note on this form" block
pattern = r'<div class="card mt-40">\s*<h3>Note on this form</h3>.*?</div>'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)
