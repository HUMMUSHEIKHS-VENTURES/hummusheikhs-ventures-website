with open("onboarding-form.html", "r") as f:
    content = f.read()

import re
# Remove all submit blocks
content = re.sub(r'<div class="mt-8 pt-8 border-t border-slate-200 no-print flex justify-end">.*?</div>', '', content, flags=re.DOTALL)
# Remove rogue </form>
content = content.replace("</form>", "")

# Add one submit block before footer, and one </form>
footer_idx = content.rfind("<footer")
submit_block = '''      <div class="mt-8 pt-8 border-t border-slate-200 no-print flex justify-end">
        <button type="submit" class="bg-[#d4af37] text-white px-6 py-3 rounded shadow hover:bg-[#c9a24b] transition font-medium">Submit Project Form</button>
      </div>
    </form>
'''
content = content[:footer_idx] + submit_block + content[footer_idx:]

with open("onboarding-form.html", "w") as f:
    f.write(content)
