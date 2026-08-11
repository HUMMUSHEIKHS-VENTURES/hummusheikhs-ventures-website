import re
with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

# Update lede text
content = content.replace(
    'A multi-purpose company built by \'\'\' + AUTHOR + \'\'\', starting with Books &amp; Publishing, and structured to grow into digital services, training, and products.',
    'A multi-purpose company built by \'\'\' + AUTHOR + \'\'\', starting with Books &amp; Publishing, and expanding into Premium Web Design.'
)

# Update about text 1
content = content.replace(
    '<p>The name has changed as the company has grown. What began as a books-only project is now structured as HUMMUSHEIKHS VENTURES: a company built so that new, lawful ventures, including digital services, training, and products, can be added over time without starting over.</p>',
    '<p>The name has changed as the company has grown. What began as a books-only project is now structured as HUMMUSHEIKHS VENTURES: a company built so that new, lawful ventures, including Premium Web Design, can be added over time without starting over.</p>'
)

# Update about text 2
content = content.replace(
    '<p>Books &amp; Publishing today; digital services, training, and products next, each new venture building on the last.</p>',
    '<p>Books &amp; Publishing today, expanding into Premium Web Design, each new venture building on the last.</p>'
)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)
