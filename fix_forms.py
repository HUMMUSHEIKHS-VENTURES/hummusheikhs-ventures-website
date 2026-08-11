import os

files = [
    "onboarding-form.html",
    "onboarding-design-agreement.html",
    "onboarding-handover-checklist.html",
    "onboarding-maintenance-agreement.html"
]

for file in files:
    if not os.path.exists(file): continue
    
    with open(file, "r") as f:
        content = f.read()
        
    # Make input text larger and use brand gold for focus
    content = content.replace("font-size: 0.875rem;", "font-size: 1.05rem;")
    content = content.replace("border-bottom-color: #3b82f6;", "border-bottom-color: #d4af37;")
    content = content.replace("accent-color: #0f172a;", "accent-color: #d4af37;")
    
    # Make the container responsive
    content = content.replace(
        "width: 210mm; min-height: 297mm; margin: 40px auto;", 
        "max-width: 900px; width: 100%;  margin: 80px auto;"
    )
    content = content.replace("padding: 20mm;", "padding: 40px 24px;")
    
    with open(file, "w") as f:
        f.write(content)
