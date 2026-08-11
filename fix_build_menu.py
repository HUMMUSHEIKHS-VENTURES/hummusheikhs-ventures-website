import re
with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

# Make sure "Web Design" is in the menu
if 'li("onboarding.html", "Web Design", "webdesign")' not in content:
    content = content.replace(
        "''' + li(\"ventures.html\", \"Our Ventures\", \"ventures\") + '''",
        "''' + li(\"ventures.html\", \"Our Ventures\", \"ventures\") + '''\n      ''' + li(\"onboarding.html\", \"Web Design\", \"webdesign\") + '''"
    )

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)
