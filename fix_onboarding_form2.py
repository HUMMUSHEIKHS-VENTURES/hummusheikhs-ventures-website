import re
with open("onboarding-form.html", "r", encoding="utf-8") as f:
    content = f.read()

# Wrap in form
content = content.replace(
    '<h2 class="text-xl font-bold text-brand-900 mb-6 uppercase tracking-wider">Client Project Information</h2>',
    '<h2 class="text-xl font-bold text-brand-900 mb-6 uppercase tracking-wider">Client Project Information</h2>\n    <form name="onboarding" method="POST" data-netlify="true" action="onboarding.html">'
)

content = content.replace(
    '  </div>\n</body>',
    '    </form>\n  </div>\n</body>'
)

# Add submit button at the end of the form, just before </form>
content = content.replace(
    '    </form>',
    '      <div class="mt-8 pt-8 border-t border-slate-200 no-print flex justify-end">\n        <button type="submit" class="bg-brand-900 text-white px-6 py-3 rounded shadow hover:bg-slate-800 transition font-medium">Submit Project Form</button>\n      </div>\n    </form>'
)

with open("onboarding-form.html", "w", encoding="utf-8") as f:
    f.write(content)
