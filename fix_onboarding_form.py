import re
with open("onboarding-form.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace inputs with named inputs
content = content.replace('<input type="text" placeholder="Enter full name" />', '<input type="text" name="client_name" placeholder="Enter full name" required />')
content = content.replace('<input type="text" placeholder="Enter business name" />', '<input type="text" name="business_name" placeholder="Enter business name" />')
content = content.replace('<input type="text" placeholder="Enter email" />', '<input type="email" name="email" placeholder="Enter email" required />')
content = content.replace('<input type="text" placeholder="Enter phone number" />', '<input type="tel" name="phone" placeholder="Enter phone number" required />')

# Replace checkboxes
content = content.replace('<input type="checkbox"> We have a high-res logo ready', '<input type="checkbox" name="logo_status" value="Ready"> We have a high-res logo ready')
content = content.replace('<input type="checkbox"> We need a new logo designed', '<input type="checkbox" name="logo_status" value="Need Design"> We need a new logo designed')

content = content.replace('<input type="checkbox"> Contact / Booking Form', '<input type="checkbox" name="features[]" value="Contact Form"> Contact / Booking Form')
content = content.replace('<input type="checkbox"> E-Commerce / Store', '<input type="checkbox" name="features[]" value="E-Commerce"> E-Commerce / Store')
content = content.replace('<input type="checkbox"> CMS / Blog', '<input type="checkbox" name="features[]" value="Blog"> CMS / Blog')
content = content.replace('<input type="checkbox"> Gallery / Portfolio', '<input type="checkbox" name="features[]" value="Gallery"> Gallery / Portfolio')
content = content.replace('<input type="checkbox"> Client Portal / Login', '<input type="checkbox" name="features[]" value="Portal"> Client Portal / Login')

content = content.replace('<input type="checkbox"> Domain Name Available', '<input type="checkbox" name="infrastructure[]" value="Domain"> Domain Name Available')
content = content.replace('<input type="checkbox"> Web Hosting Setup Required', '<input type="checkbox" name="infrastructure[]" value="Hosting"> Web Hosting Setup Required')
content = content.replace('<input type="checkbox"> Content (Text/Images) Ready', '<input type="checkbox" name="infrastructure[]" value="Content"> Content (Text/Images) Ready')
content = content.replace('<input type="checkbox"> Advanced SEO Required', '<input type="checkbox" name="infrastructure[]" value="SEO"> Advanced SEO Required')

# Add textareas if they exist, let's just use regex for textareas
content = re.sub(r'<textarea(.*?)></textarea>', r'<textarea\1 name="notes"></textarea>', content)

# Wrap content in a form tag
# The fields start after the header
form_start = '<form name="onboarding" method="POST" data-netlify="true" action="onboarding.html" class="space-y-8">'
content = content.replace('<div class="grid grid-cols-2 gap-8">', form_start + '\n    <div class="grid grid-cols-2 gap-8">')

# Add submit button at the end
# The form probably ends before the closing </div> of the a4-container
form_end = '''      <div class="mt-8 pt-8 border-t border-slate-200 no-print flex justify-end">
        <button type="submit" class="bg-brand-900 text-white px-6 py-3 rounded shadow hover:bg-slate-800 transition font-medium">Submit Project Form</button>
      </div>
    </form>'''
# Let's find a good place to insert it. The last checkbox section.
content = re.sub(r'(<label class="checkbox-label"><input type="checkbox" name="infrastructure\[\]" value="SEO"> Advanced SEO Required</label>\s*</div>\s*</div>\s*</div>)', r'\1\n' + form_end, content)

with open("onboarding-form.html", "w", encoding="utf-8") as f:
    f.write(content)
