import re
with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove Training & Education from the grid
old_grid = r'''<div class="grid grid--3 mt-40">
        <div class="card venture-card is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128214;</div>
          <h3>Books & Publishing</h3>
          <p>Practical, well-researched ebooks across wealth, health, lifestyle, and entertainment.</p>
          <a href="books.html" class="btn btn--outline btn--sm">Explore Books</a>
        </div>
        <div class="card venture-card is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128187;</div>
          <h3>Premium Web Design</h3>
          <p>Professional, mobile-friendly websites designed to grow your brand and business.</p>
          <a href="web-design.html" class="btn btn--outline btn--sm">Explore Design</a>
        </div>
        <div class="card venture-card is-future">
          <span class="venture-status">Coming Soon</span>
          <div class="icon">&#127891;</div>
          <h3>Training & Education</h3>
          <p>Hands-on courses and workshops turning our books' step-by-step methods into guided learning.</p>
          <span class="tag tag--muted">Reserved</span>
        </div>
      </div>'''

new_grid = r'''<div class="grid grid--2 mt-40">
        <div class="card venture-card is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128214;</div>
          <h3>Books & Publishing</h3>
          <p>Practical, well-researched ebooks across wealth, health, lifestyle, and entertainment.</p>
          <a href="books.html" class="btn btn--outline btn--sm">Explore Books</a>
        </div>
        <div class="card venture-card is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128187;</div>
          <h3>Premium Web Design</h3>
          <p>Professional, mobile-friendly websites designed to grow your brand and business.</p>
          <a href="web-design.html" class="btn btn--outline btn--sm">Explore Design</a>
        </div>
      </div>'''

content = content.replace(old_grid, new_grid)

# Update hero stats from 4 Ventures Planned to 2 Active Ventures
content = content.replace(
    '<div class="hero-stat"><b>4</b><span>Ventures Planned</span></div>',
    '<div class="hero-stat"><b>2</b><span>Active Ventures</span></div>'
)

# Update lede text
content = content.replace(
    'A multi-purpose company built by Adetoro Sururat Olatayo, starting with Books &amp; Publishing, and structured to grow into digital services, training, and products.',
    'A multi-purpose company built by Adetoro Sururat Olatayo, starting with Books &amp; Publishing, and expanding into Premium Web Design.'
)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)
