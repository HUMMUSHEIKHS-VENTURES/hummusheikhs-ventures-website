import re
with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

# Update link in index.html grid to onboarding.html
content = content.replace(
    '<a href="web-design.html" class="btn btn--outline btn--sm">Explore Design</a>',
    '<a href="onboarding.html" class="btn btn--outline btn--sm">Explore Design</a>'
)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)

with open("content/ventures.json", "r", encoding="utf-8") as f:
    json_content = f.read()

json_content = json_content.replace('"link": "web-design.html"', '"link": "onboarding.html"')

with open("content/ventures.json", "w", encoding="utf-8") as f:
    f.write(json_content)

