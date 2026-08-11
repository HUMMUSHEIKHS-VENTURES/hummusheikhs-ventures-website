with open("onboarding-form.html", "r") as f:
    content = f.read()

content = content.replace(
    '<textarea rows="2" placeholder="e.g. Home, About Us, Services, Contact..." name="notes"></textarea>',
    '<textarea rows="2" placeholder="e.g. Home, About Us, Services, Contact..." name="pages_required"></textarea>'
)

with open("onboarding-form.html", "w") as f:
    f.write(content)
