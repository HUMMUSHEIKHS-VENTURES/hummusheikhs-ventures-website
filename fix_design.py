import os

with open("assets/css/styles.css", "r") as f:
    css = f.read()

# Make hero darker
css = css.replace(
    "background:radial-gradient(130% 160% at 20% -10%,var(--plum-600) 0%,var(--plum-900) 45%,var(--ink) 100%);",
    "background:radial-gradient(130% 160% at 20% -10%,var(--plum-900) 0%,var(--ink) 40%,#09060e 100%);"
)

# Add animations
animation_css = """
/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.hero h1 { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.hero .lede { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both; }
.hero-cta { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both; }
.hero-stats { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.45s both; }
.hero-fan { animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both; }

/* Scroll Reveal Animations */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}
"""

if "@keyframes fadeInUp" not in css:
    css += animation_css

with open("assets/css/styles.css", "w") as f:
    f.write(css)

with open("build.py", "r") as f:
    build_code = f.read()

# Add a script for scroll animations to FOOTER in build.py
reveal_script = """
<script>
  document.addEventListener("DOMContentLoaded", function() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  });
</script>
</body>
"""

# Replace closing body tag in build.py template with the script
if "</body>" in build_code and "IntersectionObserver" not in build_code:
    build_code = build_code.replace("</body>", reveal_script)
    
    # Add 'reveal' class to cards in build.py
    build_code = build_code.replace('class="card venture-card', 'class="card venture-card reveal')
    build_code = build_code.replace('class="book-card"', 'class="book-card reveal"')
    build_code = build_code.replace('class="card"', 'class="card reveal"')

    with open("build.py", "w") as f:
        f.write(build_code)
    
print("Fixed design and animations")
