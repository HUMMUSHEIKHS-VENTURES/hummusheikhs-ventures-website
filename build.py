#!/usr/bin/env python3
"""Static site generator for HUMMUSHEIKHS VENTURES.

Edit content.py for text/data changes, then run this file to rebuild the
HTML pages. This file only contains layout/template logic.
"""
import os, re
from content import *

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- HELPERS

def img_path(name):
    """Normalise a CMS-supplied image value (bare filename or /assets/img/...) 
    into the relative path our templates expect."""
    n = (name or "").lstrip("/")
    if not n.startswith("assets/"):
        n = "assets/img/" + n
    return n

def book_by_slug(slug):
    for b in BOOKS:
        if b["slug"] == slug:
            return b
    return None


def nav_html(active=""):
    def li(href, label, key):
        cls = ' class="is-active"' if key == active else ""
        return '<li><a href="{href}"{cls}>{label}</a></li>'.format(href=href, cls=cls, label=label)

    books_dropdown = "".join(
        '<li><a href="book-{slug}.html">{title}</a></li>'.format(slug=b["slug"], title=b["short"] if len(b["short"]) < 46 else b["title"])
        for b in BOOKS
    )

    return '''
<header class="site-header">
  <nav class="nav" aria-label="Primary">
    <a href="index.html" class="brand">
      <img src="''' + img_path(LOGO) + '''" alt="HUMMUSHEIKHS VENTURES logo">
      <span class="brand-text">
        <span class="brand-name">HUMMUSHEIKHS VENTURES</span>
        <span class="brand-tag">Building Ideas &middot; Creating Value</span>
      </span>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="primary-menu" aria-label="Toggle menu">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      <span class="menu-text" style="font-size:0.85rem; font-weight:600; margin-left:6px; padding-right:2px;">Menu</span>
    </button>
    <ul class="nav-links" id="primary-menu">
      ''' + li("index.html", "Home (Main Menu)", "home") + '''
      ''' + li("about.html", "About", "about") + '''
      ''' + li("ventures.html", "Our Ventures", "ventures") + '''
      ''' + li("onboarding.html", "Web Design", "webdesign") + '''
      ''' + li("trueprofit.html", "TRUEPROFIT™", "trueprofit") + '''
      <li class="has-dropdown''' + (' is-open' if active == 'books' else '') + '''">
        <a href="books.html"''' + (' class="is-active"' if active == 'books' else '') + '''>Books &amp; Publishing</a>
        <ul class="dropdown">
          <li><a href="bookshelf.html">Full Bookshelf</a></li>
          ''' + books_dropdown + '''
        </ul>
      </li>
      ''' + li("author.html", "Author", "author") + '''
      ''' + li("blog.html", "Blog", "blog") + '''
      ''' + li("faq.html", "FAQ", "faq") + '''
      ''' + li("contact.html", "Contact", "contact") + '''
    </ul>
    <div class="nav-actions">
      <button class="search-toggle" aria-expanded="false" aria-label="Open search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </button>
      <a href="bookshelf.html" class="btn btn--outline btn--sm">Bookshelf</a>
      <a href="contact.html" class="btn btn--gold btn--sm">Get in Touch</a>
    </div>
  </nav>
  <div class="search-panel">
    <form data-site-search data-target="bookshelf.html" role="search">
      <label for="site-search-input" class="visually-hidden">Search books</label>
      <input id="site-search-input" type="search" name="q" placeholder="Search books, e.g. AI, side hustle, romance&hellip;">
      <button type="submit" class="btn btn--gold btn--sm">Search</button>
    </form>
  </div>
</header>
'''


def footer_html():
    book_links = "".join(
        '<li><a href="book-{slug}.html">{title}</a></li>'.format(slug=b["slug"], title=b["title"] if len(b["title"]) < 42 else b["short"])
        for b in BOOKS[:5]
    )
    return '''
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="brand">
          <img src="''' + img_path(LOGO) + '''" alt="HUMMUSHEIKHS VENTURES logo">
          <span class="brand-name">HUMMUSHEIKHS VENTURES</span>
        </a>
        <p>''' + TAGLINE + '''</p>
        <div class="social-row">
          <a href="''' + WHATSAPP_URL + '''" aria-label="WhatsApp" target="_blank" rel="noopener">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.39 1.26 4.81L2 22l5.42-1.35c1.36.72 2.9 1.13 4.62 1.13 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Z"/></svg>
          </a>
          <a href="mailto:''' + EMAIL + '''" aria-label="Email">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>
          </a>
        </div>
      </div>
      <div class="footer">
        <h4>Quick Links</h4>
        <ul class="footer-links">
          <li><a href="index.html">Home (Main Menu)</a></li>
          <li><a href="about.html">About Us</a></li>
          <li><a href="ventures.html">Our Ventures</a></li>
          <li><a href="onboarding.html">Premium Web Design</a></li>
          <li><a href="trueprofit.html">TRUEPROFIT™</a></li>
          <li><a href="author.html">Meet the Author</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="faq.html">FAQ</a></li>
        </ul>
      </div>
      <div class="footer">
        <h4>Books</h4>
        <ul class="footer-links">
          ''' + book_links + '''
          <li><a href="bookshelf.html">View all books &rarr;</a></li>
        </ul>
      </div>
      <div class="footer">
        <h4>Contact</h4>
        <ul class="footer-links">
          <li><a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></li>
          <li><a href="''' + WHATSAPP_URL + '''" target="_blank" rel="noopener">WhatsApp: ''' + WHATSAPP_DISPLAY + '''</a></li>
          <li><a href="contact.html">Contact page &rarr;</a></li>
        </ul>
        <h4 style="margin-top:22px;">Newsletter</h4>
        <form name="newsletter" method="POST" data-netlify="true">
          <div style="display:flex;gap:8px;">
            <label for="footer-newsletter" class="visually-hidden">Email address</label>
            <input id="footer-newsletter" type="email" required placeholder="Your email" style="min-width:0;">
            <button type="submit" class="btn btn--gold btn--sm">Join</button>
          </div>
          
        </form>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year></span> HUMMUSHEIKHS VENTURES. All rights reserved.</span>
      <span><a href="privacy.html">Privacy Policy</a> &middot; <a href="terms.html">Terms of Use</a></span>
    </div>
  </div>
</footer>
'''


FLOURISH = '<svg class="flourish" viewBox="0 0 120 14" aria-hidden="true"><path d="M2 8c14-10 22 6 36-2s22 6 36-2 22 6 36-2"/></svg>'


def page(title, description, active, body, extra_head="", canonical=None, og_image=None, full_title=None):
    canonical = canonical or (SITE_URL + "/")
    og_image = og_image or (SITE_URL + "/" + img_path(LOGO))
    display_title = full_title or (title + " | " + BIZ)
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + display_title + '''</title>
<meta name="description" content="''' + description + '''">
<link rel="canonical" href="''' + canonical + '''">
<meta name="robots" content="index, follow">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="''' + BIZ + '''">
<meta property="og:title" content="''' + display_title + '''">
<meta property="og:description" content="''' + description + '''">
<meta property="og:url" content="''' + canonical + '''">
<meta property="og:image" content="''' + og_image + '''">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="''' + display_title + '''">
<meta name="twitter:description" content="''' + description + '''">
<meta name="twitter:image" content="''' + og_image + '''">

<link rel="icon" href="assets/img/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
''' + extra_head + '''
<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
''' + nav_html(active) + '''
<main id="main">
''' + body + '''
</main>
''' + footer_html() + '''
<script src="assets/js/main.js" defer></script>
<script>
  if (window.netlifyIdentity) {
    window.netlifyIdentity.on("init", user => {
      if (!user) {
        window.netlifyIdentity.on("login", () => {
          document.location.href = "/admin/";
        });
      }
    });
  }
</script>
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

</html>
'''


def book_card(b, eager=False):
    loading = "eager" if eager else "lazy"
    return '''
    <article class="book-card reveal" data-categories="''' + b["cats"] + '''" data-search="''' + b["title"].lower() + " " + b["short"].lower() + '''">
      <a href="book-''' + b["slug"] + '''.html" class="book-cover">
        <img src="''' + img_path(b["cover"]) + '''" alt="''' + b["title"] + ''' book cover" loading="''' + loading + '''" width="600" height="900">
      </a>
      <div class="book-body">
        <span class="tag tag--muted">''' + b["category"] + '''</span>
        <h3><a href="book-''' + b["slug"] + '''.html">''' + b["title"] + '''</a></h3>
        <p class="book-excerpt">''' + b["excerpt"] + '''</p>
        <div class="book-actions">
          <a href="book-''' + b["slug"] + '''.html" class="btn btn--outline btn--sm">Details</a>
          <a href="''' + b["selar"] + '''" class="btn btn--gold btn--sm" target="_blank" rel="noopener">Buy Now</a>
        </div>
      </div>
    </article>'''


def schema_book(b):
    return '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "''' + b["title"].replace('"', '\\"') + '''",
  "author": {"@type": "Person", "name": "''' + AUTHOR + '''"},
  "publisher": {"@type": "Organization", "name": "''' + BIZ + '''"},
  "image": "''' + SITE_URL + "/" + img_path(b["cover"]) + '''",
  "offers": {"@type": "Offer", "url": "''' + b["selar"] + '''", "availability": "https://schema.org/InStock"}
}
</script>'''


os.makedirs(os.path.join(ROOT), exist_ok=True)


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ================================================================ HOME
def build_home():
    fan = "".join(
        '<img src="{cover}" alt="{title} cover">'.format(cover=img_path(b["cover"]), title=b["title"])
        for b in [BOOKS[6], BOOKS[3], BOOKS[2]]
    )
    featured = "".join(book_card(b, eager=(i == 0)) for i, b in enumerate(BOOKS[:4]))
    venture_cards = "".join(
        '''
        <div class="card venture-card reveal {cls}">
          <span class="venture-status">{status}</span>
          <div class="icon">{icon}</div>
          <h3>{name}</h3>
          <p>{desc}</p>
          {link}
        </div>'''.format(
            cls="is-active" if v["active"] else "is-future",
            status=v["status"], icon=v["icon"], name=v["name"], desc=v["desc"],
            link='<a href="{}" class="btn btn--outline btn--sm">Explore</a>'.format(v["link"]) if v["link"] else ""
        ) for v in VENTURES[:3]
    )
    body = '''
<section class="hero">
  <div class="container hero-grid">
    <div>
      <p class="eyebrow" style="color:var(--gold-300)">HUMMUSHEIKHS VENTURES</p>
      <h1>''' + TAGLINE + '''</h1>
      <p class="lede">A multi-purpose company built by ''' + AUTHOR + ''', starting with Books &amp; Publishing, expanding into Premium Web Design, and introducing TRUEPROFIT™.</p>
      <div class="hero-cta">
        <a href="bookshelf.html" class="btn btn--gold">Explore the Bookshelf</a>
        <a href="about.html" class="btn btn--ghost-light">About the Company</a>
      </div>
      <div class="hero-stats">
        <div class="hero-stat"><b>''' + str(len(BOOKS)) + '''</b><span>Published Books</span></div>
        <div class="hero-stat"><b>3</b><span>Active Ventures</span></div>
        <div class="hero-stat"><b>1</b><span>Mission</span></div>
      </div>
    </div>
    <div class="hero-art">
      <div class="hero-fan">''' + fan + '''</div>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <p class="eyebrow">Our Ventures</p>
    <h2>One company. Several ways we create impact.</h2>
    <svg class="flourish" viewBox="0 0 120 14" aria-hidden="true"><path d="M2 8c14-10 22 6 36-2s22 6 36-2 22 6 36-2"/></svg>
    <p class="max-60">Books &amp; Publishing is where HUMMUSHEIKHS VENTURES started. Today, we offer premium web design services, the TRUEPROFIT™ business tool, and are continuously expanding into new, lawful ventures to create even more value.</p>
<div class="grid grid--3 mt-40">
        <div class="card venture-card reveal is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128214;</div>
          <h3>Books & Publishing</h3>
          <p>Practical, well-researched ebooks across wealth, health, lifestyle, and entertainment.</p>
          <a href="books.html" class="btn btn--outline btn--sm">Explore Books</a>
        </div>
        <div class="card venture-card reveal is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128187;</div>
          <h3>Premium Web Design</h3>
          <p>Professional, mobile-friendly websites designed to grow your brand and business.</p>
          <a href="onboarding.html" class="btn btn--outline btn--sm">Explore Design</a>
        </div>
        <div class="card venture-card reveal is-active">
          <span class="venture-status">Active</span>
          <div class="icon">&#128176;</div>
          <h3>TRUEPROFIT™</h3>
          <p>The Real Price Calculator. Understand your real costs, selling prices, and actual profits.</p>
          <a href="trueprofit.html" class="btn btn--outline btn--sm">Explore TRUEPROFIT</a>
        </div>
      </div>
    <p class="mt-40"><a href="ventures.html" class="btn btn--outline">See all ventures &rarr;</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow">Books &amp; Publishing</p>
    <h2>Featured books</h2>
    ''' + FLOURISH + '''
    <div class="grid grid--4 mt-40">''' + featured + '''</div>
    <p class="mt-40"><a href="bookshelf.html" class="btn btn--gold">Browse the full bookshelf</a></p>
  </div>
</section>

<section class="section section--dark">
  <div class="container two-col">
    <div>
      <img src="''' + img_path(AUTHOR_PHOTO) + '''" alt="''' + AUTHOR + ''', author and digital creator" style="border-radius:var(--radius-lg);box-shadow:var(--shadow-deep);">
    </div>
    <div>
      <p class="eyebrow">The Author</p>
      <h2>Meet ''' + AUTHOR + '''</h2>
      ''' + FLOURISH + '''
      <p>Author and digital creator, passionate about collecting useful information, organizing knowledge, and turning valuable ideas into practical learning books that make a difference in people's lives.</p>
      <a href="author.html" class="btn btn--ghost-light">Read the full story</a>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="newsletter">
      <div>
        <h3 style="color:var(--ivory);margin-bottom:6px;">Stay in the loop</h3>
        <p style="color:#d9c9ec;margin:0;">New books and new ventures, straight to your inbox.</p>
      </div>
      <form name="newsletter" method="POST" data-netlify="true">
        <label for="home-newsletter" class="visually-hidden">Email address</label>
        <input id="home-newsletter" type="email" required placeholder="Your email address">
        <button type="submit" class="btn btn--gold">Subscribe</button>
      </form>
    </div>
  </div>
</section>
'''
    write("index.html", page(
        "Home",
        "HUMMUSHEIKHS VENTURES is a growing business brand dedicated to empowering ideas, building solutions, and creating lasting impact through digital services, publishing, business ventures, and other lawful opportunities that create value for individuals, businesses, and communities.",
        "home", body, canonical=SITE_URL + "/",
        full_title="HUMMUSHEIKHS VENTURES | Building Ideas. Creating Value. Inspiring Business Growth.",
        extra_head='<meta name="google-site-verification" content="XVS0Ej8FNVgTMG9AmKf7lrZQzb6-g0oSOaJVUGHsUko" />'
    ))


# ================================================================ ABOUT
def build_about():
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">About Us</p>
    <h1>About HUMMUSHEIKHS VENTURES</h1>
    ''' + FLOURISH + '''
    <p class="max-60">A multi-purpose company empowering ideas, building solutions, and creating impact, one venture at a time.</p>
  </div>
</section>

<section class="section">
  <div class="container two-col">
    <div>
      <p class="eyebrow">Who We Are</p>
      <h2>Built to grow beyond books</h2>
      ''' + FLOURISH + '''
      <p>HUMMUSHEIKHS VENTURES is a digital publishing and solutions brand founded by ''' + AUTHOR + '''. We are dedicated to creating valuable resources that educate, inspire, entertain, and provide useful knowledge for everyday life.</p>
      <p>Through carefully created books, and the ventures we are building alongside them, we aim to share information, tools, and practical resources that help people learn, grow, and discover new ideas. Our current collection covers health, wealth, lifestyle, and personal development. Every book is made with the goal of keeping learning simple, accessible, and meaningful.</p>
      <p>As we continue to grow, HUMMUSHEIKHS VENTURES is structured to expand into various other lawful business ventures, ensuring we consistently deliver practical tools and resources to our community.</p>
    </div>
    <div>
      <img src="''' + img_path(LOGO) + '''" alt="HUMMUSHEIKHS VENTURES logo" style="border-radius:var(--radius-lg);box-shadow:var(--shadow-soft);">
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="grid grid--3">
      <div class="card reveal">
        <div class="icon">&#127919;</div>
        <h3>Our Mission</h3>
        <p>To educate, inspire, and empower people through well-researched, well-organized, and effective resources that bring real value.</p>
      </div>
      <div class="card reveal">
        <div class="icon">&#128161;</div>
        <h3>Our Approach</h3>
        <p>We research deeply, organize everything, simplify for easy learning, and create books and solutions that solve real problems.</p>
      </div>
      <div class="card reveal">
        <div class="icon">&#127793;</div>
        <h3>Our Direction</h3>
        <p>We currently operate Books & Publishing, Premium Web Design, and TRUEPROFIT™, while remaining open to exploring and launching other lawful businesses in the future.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container center">
    <p class="eyebrow center">Get Involved</p>
    <h2>Explore what we've built so far</h2>
    ''' + FLOURISH.replace('margin:6px 0 22px;', 'margin:6px auto 22px;') + '''
    <div class="hero-cta" style="justify-content:center;">
      <a href="bookshelf.html" class="btn btn--gold">Browse Our Books</a>
      <a href="ventures.html" class="btn btn--outline">See Our Ventures</a>
    </div>
  </div>
</section>
'''
    write("about.html", page(
        "About Us", "Learn about HUMMUSHEIKHS VENTURES, a multi-purpose company founded by " + AUTHOR + ".",
        "about", body, canonical=SITE_URL + "/about.html"
    ))


# ================================================================ VENTURES
def build_ventures():
    cards = "".join(
        '''
    <div class="card venture-card reveal {cls}">
      <span class="venture-status">{status}</span>
      <div class="icon">{icon}</div>
      <h3>{name}</h3>
      <p>{desc}</p>
      {link}
    </div>'''.format(
            cls="is-active" if v["active"] else "is-future",
            status=v["status"], icon=v["icon"], name=v["name"], desc=v["desc"],
            link='<a href="{}" class="btn btn--outline btn--sm">Explore {}</a>'.format(v["link"], v["name"]) if v["link"] else '<span class="tag tag--muted">Reserved for future growth</span>'
        ) for v in VENTURES
    )
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Our Ventures</p>
    <h1>One company, several ways we create impact</h1>
    ''' + FLOURISH + '''
    <p class="max-60">HUMMUSHEIKHS VENTURES is structured as a portfolio of ventures, including Books &amp; Publishing and Premium Web Design.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--3">''' + cards + '''</div>
  </div>
</section>

<section class="section section--dark">
  <div class="container center">
    <p class="eyebrow center">Currently Active</p>
    <h2>Books &amp; Publishing</h2>
    ''' + FLOURISH.replace('margin:6px 0 22px;', 'margin:6px auto 22px;') + '''
    <p class="max-60 mx-auto">Practical, well-researched ebooks across wealth, health, lifestyle, and entertainment. This is the foundation venture of HUMMUSHEIKHS VENTURES.</p>
    <a href="books.html" class="btn btn--gold">Visit Books &amp; Publishing</a>
  </div>
</section>
'''
    write("ventures.html", page(
        "Our Ventures", "The ventures of HUMMUSHEIKHS VENTURES: Books & Publishing and Premium Web Design.",
        "ventures", body, canonical=SITE_URL + "/ventures.html"
    ))


# ================================================================ BOOKS LANDING
def build_books_landing():
    cards = "".join(book_card(b, eager=(i < 2)) for i, b in enumerate(BOOKS))
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">A HUMMUSHEIKHS VENTURES Company</p>
    <h1>Books &amp; Publishing</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Ebooks created to educate, inspire, and entertain across wealth, health, lifestyle, and personal development, written by ''' + AUTHOR + '''.</p>
    <a href="bookshelf.html" class="btn btn--gold">Open the Full Bookshelf</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow">The Collection</p>
    <h2>All ''' + str(len(BOOKS)) + ''' titles</h2>
    ''' + FLOURISH + '''
    <div class="grid grid--4 mt-40">''' + cards + '''</div>
  </div>
</section>
'''
    write("books.html", page(
        "Books & Publishing", "Explore the full HUMMUSHEIKHS VENTURES book collection by " + AUTHOR + " " + "across wealth, health, lifestyle, and entertainment.",
        "books", body, canonical=SITE_URL + "/books.html"
    ))


# ================================================================ BOOKSHELF
def build_bookshelf():
    chips = "".join(
        '<button type="button" class="chip{active}" data-shelf-chip="{key}">{label}</button>'.format(
            active=" is-active" if key == "all" else "", key=key, label=label
        ) for key, label in CATEGORIES
    )
    cards = "".join(book_card(b, eager=(i < 4)) for i, b in enumerate(BOOKS))
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Books &amp; Publishing</p>
    <h1>The Bookshelf</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Search or filter by category to find your next read.</p>
  </div>
</section>

<section class="section">
  <div class="container" data-bookshelf>
    <div class="shelf-toolbar">
      <div class="shelf-search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <label for="shelf-search-input" class="visually-hidden">Search books</label>
        <input id="shelf-search-input" type="search" data-shelf-search placeholder="Search by title or topic&hellip;">
      </div>
      <div class="filter-row">''' + chips + '''</div>
    </div>
    <div class="grid grid--4">''' + cards + '''</div>
    <p data-shelf-empty style="display:none;text-align:center;padding:40px 0;color:var(--text-soft);">No books match your search. Try another keyword or category.</p>
  </div>
</section>
'''
    write("bookshelf.html", page(
        "Bookshelf", "Search and filter the full HUMMUSHEIKHS VENTURES bookshelf by category or keyword.",
        "books", body, canonical=SITE_URL + "/bookshelf.html"
    ))


# ================================================================ BOOK DETAIL PAGES
def build_book_pages():
    for b in BOOKS:
        others = [x for x in BOOKS if x["slug"] != b["slug"]][:4]
        related = "".join(book_card(x) for x in others)
        desc_html = "".join('<p>{}</p>'.format(p) for p in b["description"])
        features_html = "".join('<li>{}</li>'.format(f) for f in b["features"])
        benefits_html = "".join('<li>{}</li>'.format(x) for x in b["benefits"])
        body = '''
<section class="section--tight">
  <div class="container">
    <p class="breadcrumb"><a href="books.html">Books &amp; Publishing</a> / <a href="bookshelf.html">Bookshelf</a> / ''' + b["title"] + '''</p>
    <div class="book-hero">
      <div class="book-hero-cover">
        <img src="''' + img_path(b["cover"]) + '''" alt="''' + b["title"] + ''' book cover" width="700" height="1050">
        <a href="''' + b["selar"] + '''" class="btn btn--gold btn--block mt-40" target="_blank" rel="noopener">Buy Now on Selar</a>
      </div>
      <div>
        <span class="tag">''' + b["category"] + '''</span>
        <h1>''' + b["title"] + '''</h1>
        <p class="lede" style="color:var(--text-soft);font-size:1.08rem;">''' + b["short"] + '''</p>
        ''' + desc_html + '''
        <h3 class="mt-40">What's inside</h3>
        <ul class="feature-list">''' + features_html + '''</ul>
        <h3 class="mt-40">Why readers choose this book</h3>
        <ul class="benefit-list">''' + benefits_html + '''</ul>
        <a href="''' + b["selar"] + '''" class="btn btn--gold mt-40" target="_blank" rel="noopener">Get Your Copy Now</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <p class="eyebrow">You may also like</p>
    <h2>Related books</h2>
    ''' + FLOURISH + '''
    <div class="related-strip mt-40">''' + related + '''</div>
  </div>
</section>
''' + schema_book(b)
        write("book-" + b["slug"] + ".html", page(
            b["title"], b["excerpt"], "books", body,
            canonical=SITE_URL + "/book-" + b["slug"] + ".html",
            og_image=SITE_URL + "/" + img_path(b["cover"])
        ))


# ================================================================ AUTHOR
def build_author():
    written = "".join(
        '<li><a href="book-{slug}.html">{title}</a></li>'.format(slug=b["slug"], title=b["title"])
        for b in BOOKS
    )
    body = '''
<section class="section section--dark">
  <div class="container author-hero">
    <div>
      <img class="author-portrait" src="''' + img_path(AUTHOR_PHOTO) + '''" alt="''' + AUTHOR + ''', author and digital creator">
    </div>
    <div>
      <p class="eyebrow">Author &amp; Digital Creator</p>
      <h1 style="color:var(--ivory);">''' + AUTHOR + '''</h1>
      ''' + FLOURISH + '''
      <p class="author-quote">&ldquo;I love collecting useful information and gathering everything to build useful, effective, and practical learning books that make a difference in people's lives.&rdquo;</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container two-col">
    <div>
      <p class="eyebrow">About the Author</p>
      <h2>In her own words</h2>
      ''' + FLOURISH + '''
      <p>In the name of Allah, the Most Gracious, the Most Merciful.</p>
      <p>I am ''' + AUTHOR + ''', an author and digital creator passionate about collecting useful information, organizing knowledge, and turning valuable ideas into practical learning books.</p>
      <p>I have always believed that knowledge is a powerful tool when it is shared in a simple, clear, and meaningful way. My aim is to make useful information easier to understand and apply in everyday life, helping readers learn, grow, and discover new possibilities.</p>
      <p>My creative journey is inspired by curiosity, learning, and the desire to transform ideas into something valuable. I enjoy researching, gathering helpful information, and presenting it in a way that feels simple and accessible.</p>
      <p>I am a Muslim woman who strives to live according to the guidance of the Qur'an and the authentic Sunnah. My faith in Allah is the foundation of my life, and it shapes my values, my purpose, and the way I approach my work.</p>
      <p>I am a wife, a mother, a sister, and a friend. These roles have taught me patience, responsibility, compassion, and a deeper understanding of people and their different experiences.</p>
      <p>Through my writing and digital creations, I hope to share knowledge that benefits others and leaves a positive impact. I believe every useful piece of knowledge has the potential to make a difference.</p>
      <p>All success comes from Allah alone, and I ask Him to place goodness and benefit in everything I create.</p>
    </div>
    <div>
      <div class="card reveal">
        <h3>What I write about</h3>
        <ul class="feature-list mt-40">
          <li><strong>Health:</strong> practical guides for better health and long-term wellness</li>
          <li><strong>Wealth:</strong> smart money habits, income ideas, and financial freedom</li>
          <li><strong>Lifestyle:</strong> productivity, personal growth, and purposeful living</li>
          <li><strong>Entertainment:</strong> fun, inspiring, positive stories that refresh the mind</li>
        </ul>
      </div>
      <div class="card mt-40">
        <h3>Books written</h3>
        <ul class="footer-links" style="margin-top:14px;">''' + written + '''</ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream center">
  <div class="container">
    <p class="eyebrow center">My Mission</p>
    <h2 class="max-60 mx-auto">To educate, inspire, and empower readers through well-researched, well-organized, and effective books that bring real value.</h2>
    ''' + FLOURISH.replace('margin:6px 0 22px;', 'margin:24px auto 22px;') + '''
    <a href="bookshelf.html" class="btn btn--gold">Read My Books</a>
  </div>
</section>
'''
    write("author.html", page(
        "Meet the Author", "Meet " + AUTHOR + ", author and digital creator behind HUMMUSHEIKHS VENTURES.",
        "author", body, canonical=SITE_URL + "/author.html",
        og_image=SITE_URL + "/" + img_path(AUTHOR_PHOTO)
    ))


# ================================================================ BLOG
def build_blog():
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Blog</p>
    <h1>Notes from HUMMUSHEIKHS VENTURES</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Updates on new books, new ventures, and ideas worth sharing. New posts will appear here as they're published.</p>
  </div>
</section>

<section class="section center">
  <div class="container">
    <div class="card reveal" style="max-width:560px;margin:0 auto;padding:50px 30px;">
      <div class="icon" style="margin:0 auto 18px;">&#9998;</div>
      <h3>The first post is coming soon</h3>
      <p>The first article will appear here as soon as it is available, and in the meantime, explore the bookshelf or get in touch.</p>
      <div class="hero-cta" style="justify-content:center;">
        <a href="bookshelf.html" class="btn btn--gold btn--sm">Browse Books</a>
        <a href="contact.html" class="btn btn--outline btn--sm">Contact Us</a>
      </div>
    </div>
  </div>
</section>
'''
    write("blog.html", page(
        "Blog", "Updates, ideas, and news from HUMMUSHEIKHS VENTURES.",
        "blog", body, canonical=SITE_URL + "/blog.html"
    ))


# ================================================================ FAQ
def build_faq():
    items = "".join(
        '''
    <div class="faq-item">
      <button class="faq-q" aria-expanded="false">{q}<span class="plus">+</span></button>
      <div class="faq-a"><p>{a}</p></div>
    </div>'''.format(q=q, a=a) for q, a in FAQS
    )
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">FAQ</p>
    <h1>Frequently asked questions</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Everything you need to know about HUMMUSHEIKHS VENTURES, our books, and how to get in touch.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:800px;">''' + items + '''</div>
</section>
'''
    schema = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [''' + ",".join(
        '{"@type":"Question","name":"' + q.replace('"', '\\"') + '","acceptedAnswer":{"@type":"Answer","text":"' + a.replace('"', '\\"') + '"}}'
        for q, a in FAQS
    ) + ''']
}
</script>'''
    write("faq.html", page(
        "FAQ", "Frequently asked questions about HUMMUSHEIKHS VENTURES and our books.",
        "faq", body + schema, canonical=SITE_URL + "/faq.html"
    ))


# ================================================================ CONTACT
def build_contact():
    body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Contact</p>
    <h1>Let's talk</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Have questions, feedback, or need support? We would love to hear from you.</p>
  </div>
</section>

<section class="section">
  <div class="container two-col">
    <div>
      <h2>Send a message</h2>
      <form name="contact" method="POST" data-netlify="true">
        <div class="form-grid">
          <div>
            <label for="c-name">Full name</label>
            <input id="c-name" name="name" type="text" required>
          </div>
          <div>
            <label for="c-email">Email address</label>
            <input id="c-email" name="email" type="email" required>
          </div>
          <div class="full">
            <label for="c-subject">Subject</label>
            <input id="c-subject" name="subject" type="text">
          </div>
          <div class="full">
            <label for="c-message">Message</label>
            <textarea id="c-message" name="message" required></textarea>
          </div>
          <div class="full">
            <button type="submit" class="btn btn--gold btn--block">Send Message</button>
            
          </div>
        </div>
      </form>
    </div>
    <div>
      <h2>Direct contact</h2>
      <div class="contact-info-item">
        <div class="icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg></div>
        <div><h3 style="margin-bottom:2px;font-size:1rem;">Email</h3><p><a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></p></div>
      </div>
      <div class="contact-info-item">
        <div class="icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.39 1.26 4.81L2 22l5.42-1.35c1.36.72 2.9 1.13 4.62 1.13 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Z"/></svg></div>
        <div><h3 style="margin-bottom:2px;font-size:1rem;">WhatsApp</h3><p><a href="''' + WHATSAPP_URL + '''" target="_blank" rel="noopener">''' + WHATSAPP_DISPLAY + '''</a></p></div>
      </div>
      
    </div>
  </div>
</section>
'''
    write("contact.html", page(
        "Contact", "Get in touch with HUMMUSHEIKHS VENTURES by email or WhatsApp.",
        "contact", body, canonical=SITE_URL + "/contact.html"
    ))


# ================================================================ PRIVACY / TERMS
def build_legal():
    privacy_body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1>Privacy Policy</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Last updated: to be confirmed by ''' + BIZ + ''' before publishing.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:760px;">
    <p>This Privacy Policy explains how HUMMUSHEIKHS VENTURES (&ldquo;we&rdquo;, &ldquo;us&rdquo;) handles information when you visit this website or purchase a book.</p>
    <h3>Information we collect</h3>
    <p>If you contact us by email, WhatsApp, or the contact form, we receive whatever information you choose to share (such as your name, email address, and message). If you purchase a book, your payment and delivery details are handled directly by our payment partner, Selar, under its own privacy policy.</p>
    <h3>How we use information</h3>
    <p>We use the information you share with us to respond to your questions, provide support, and, if you opt in, send updates about new books and ventures. We do not sell your information to third parties.</p>
    <h3>Cookies</h3>
    <p>This site does not currently set marketing or tracking cookies. If analytics or advertising tools are added later, this policy will be updated to reflect that.</p>
    <h3>Third-party services</h3>
    <p>Book purchases are processed by Selar. Please review Selar's own privacy policy for details on how it handles payment and order information.</p>
    <h3>Contact</h3>
    <p>Questions about this policy can be sent to <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a>.</p>
    <p class="form-note" style="margin-top:30px;"><em>Placeholder note: replace this draft with a policy reviewed against your local data protection requirements before going live.</em></p>
  </div>
</section>
'''
    write("privacy.html", page(
        "Privacy Policy", "Privacy Policy for HUMMUSHEIKHS VENTURES.",
        "", privacy_body, canonical=SITE_URL + "/privacy.html"
    ))

    terms_body = '''
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Legal</p>
    <h1>Terms of Use</h1>
    ''' + FLOURISH + '''
    <p class="max-60">Last updated: to be confirmed by ''' + BIZ + ''' before publishing.</p>
  </div>
</section>
<section class="section">
  <div class="container" style="max-width:760px;">
    <p>By using this website, you agree to the following terms. Please read them carefully.</p>
    <h3>Use of content</h3>
    <p>All text, book covers, logos, and other content on this site belong to HUMMUSHEIKHS VENTURES and ''' + AUTHOR + ''' unless otherwise stated, and may not be copied or redistributed without permission.</p>
    <h3>Purchases</h3>
    <p>Books listed on this site are sold through our payment partner, Selar. Purchases are subject to Selar's own terms and checkout process. Digital products are delivered instantly on successful payment.</p>
    <h3>No professional advice</h3>
    <p>Our books share practical guidance and personal experience. They are not a substitute for professional legal, medical, financial, or religious advice specific to your situation.</p>
    <h3>Limitation of liability</h3>
    <p>HUMMUSHEIKHS VENTURES provides this website and its content &ldquo;as is&rdquo; and is not liable for losses arising from its use, to the fullest extent permitted by law.</p>
    <h3>Contact</h3>
    <p>Questions about these terms can be sent to <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a>.</p>
    <p class="form-note" style="margin-top:30px;"><em>Placeholder note: replace this draft with terms reviewed by a legal professional before going live.</em></p>
  </div>
</section>
'''
    write("terms.html", page(
        "Terms of Use", "Terms of Use for HUMMUSHEIKHS VENTURES.",
        "", terms_body, canonical=SITE_URL + "/terms.html"
    ))


# ================================================================ 404
def build_404():
    body = '''
<section class="error-hero">
  <div class="container">
    <div class="error-code">404</div>
    <h1>This page has wandered off</h1>
    <p class="max-60 mx-auto">The page you're looking for doesn't exist or may have moved. Let's get you back on track.</p>
    <div class="hero-cta" style="justify-content:center;">
      <a href="index.html" class="btn btn--gold">Back to Home</a>
      <a href="bookshelf.html" class="btn btn--outline">Browse Books</a>
    </div>
  </div>
</section>
'''
    write("404.html", page(
        "Page Not Found", "The page you're looking for doesn't exist.",
        "", body, canonical=SITE_URL + "/404.html"
    ))


# ================================================================ ROBOTS / SITEMAP / README
def build_robots_sitemap():
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "/sitemap.xml\n")

    pages = ["index.html", "about.html", "ventures.html", "books.html", "bookshelf.html",
             "author.html", "blog.html", "faq.html", "contact.html", "privacy.html", "terms.html"]
    pages += ["book-" + b["slug"] + ".html" for b in BOOKS]
    urls = "".join(
        "  <url><loc>" + SITE_URL + "/" + p + "</loc></url>\n" for p in pages
    )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"
    write("sitemap.xml", sitemap)


README = '''# HUMMUSHEIKHS VENTURES Website

This is a complete static website: plain HTML, CSS, and JavaScript. There is
no build step, server, or database required to run it; it works anywhere
that can serve static files.

See `CONTENT-GUIDE.md` in this same folder for exactly where to go when you
need to update a book, an image, or a contact detail.

## What's inside

- `index.html`, `about.html`, `ventures.html`, `books.html`, `bookshelf.html`,
  `author.html`, `blog.html`, `faq.html`, `contact.html`, `privacy.html`,
  `terms.html`, `404.html`: every page of the site
- `book-*.html`: one page per book (7 total)
- `assets/css/styles.css`: all styling
- `assets/js/main.js`: navigation, search, filters, and FAQ behaviour
- `assets/img/`: logo, favicon, and all book covers, already compressed for web
- `robots.txt`, `sitemap.xml`: for search engines
- `content.py` and `build.py`: the source files used to generate this site
  (only needed if you want to regenerate pages from updated content; see
  `CONTENT-GUIDE.md`)

## Before you go live: three things to update

1. **Domain.** Every page currently points to a placeholder address
   (`https://www.hummusheikhsventures.com`) in its SEO tags and in
   `sitemap.xml`. Once you have a real domain, do a find-and-replace for
   that placeholder across all files and swap in your actual domain.
2. **Contact form.** The contact form and newsletter box currently just show
   a message on submit; they are not yet connected to your inbox. The
   fastest fix if you host on Netlify is to add `data-netlify="true"` and a
   hidden `form-name` input to the `<form name="newsletter" method="POST" data-netlify="true">` elements, and
   Netlify will email you every submission automatically for free. Full
   steps are below.
3. **Legal pages.** `privacy.html` and `terms.html` are solid drafts built
   from your business details, but they are marked as drafts on purpose:
   have them checked against your local rules before publishing.

## How to put this online (free options)

### Option A: Netlify (easiest)
1. Go to app.netlify.com and sign up (free).
2. On your dashboard, drag the whole website folder onto the page where it
   says "Drag and drop your site folder here."
3. Netlify uploads everything and gives you a live link in under a minute,
   e.g. `random-name-123.netlify.app`.
4. To use your own domain: Site settings, then Domain management, then Add a
   custom domain, then follow Netlify's DNS instructions.
5. To make the contact form actually deliver to your email: open
   `contact.html`, find `<form name="newsletter" method="POST" data-netlify="true">`, add
   `data-netlify="true" name="contact"` to that tag, and add this line
   right after the opening `<form>` tag:
   `<input type="hidden" name="form-name" value="contact">`
   Re-upload the folder, and Netlify will show submissions under
   Site, then Forms, and can email them to you.

### Option B: Cloudflare Pages
1. Go to the Cloudflare dashboard, then Workers & Pages, then Create, then
   Pages, then Upload assets.
2. Upload this folder (or connect a GitHub repo containing it).
3. Cloudflare gives you a live `*.pages.dev` link immediately.
4. Add your own domain under Custom domains once you have one.

### Option C: GitHub Pages
1. Create a new GitHub repository and upload all files in this folder to it.
2. Go to Settings, then Pages, then Source, then select the `main` branch
   and `/root`.
3. GitHub gives you a live link at `yourusername.github.io/repo-name`.
4. Add a custom domain under the same Pages settings once you have one.

## Notes

- All book "Buy Now" buttons link directly to your existing Selar checkout
  pages, so purchases work immediately with no extra setup.
- Images have been resized and compressed for fast loading, and pages below
  the fold use lazy loading.
- The site is built mobile-first and keyboard-accessible (visible focus
  states, alt text on every image, ARIA labels on the menu and search
  controls).
'''



# ================================================================ TRUEPROFIT

def build_trueprofit():
    body = '''
<style>
.tp-hero { background: var(--plum-900); color: var(--ivory); padding: 80px 20px; text-align: center; }
.tp-hero h1 { font-size: 3rem; color: var(--gold-300); font-family: "Playfair Display", serif; margin-bottom: 10px; }
.tp-hero p { font-size: 1.2rem; color: var(--ivory); max-width: 600px; margin: 0 auto 30px; opacity: 0.9; }
.tp-hero .problem-statement { font-style: italic; font-size: 1.3rem; color: #a996c0; margin-bottom: 40px; font-weight: 500; }
.tp-features { background: var(--cream); padding: 60px 20px; }
.tp-features .container { max-width: 1000px; }
.tp-features h2 { text-align: center; color: var(--plum-900); font-family: "Playfair Display", serif; font-size: 2.2rem; margin-bottom: 40px; }
.tp-grid-3 { display: grid; grid-template-columns: 1fr; gap: 30px; }
@media (min-width: 768px) { .tp-grid-3 { grid-template-columns: repeat(3, 1fr); } }
.tp-feature-card { background: var(--white); border-radius: 12px; padding: 30px; border: 1px solid var(--line); box-shadow: var(--shadow-sm); transition: transform 0.3s, box-shadow 0.3s; }
.tp-feature-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-deep); }
.tp-feature-card .icon { font-size: 2rem; color: var(--gold-500); margin-bottom: 15px; }
.tp-feature-card h3 { color: var(--plum-900); margin-bottom: 10px; font-size: 1.2rem; }
.tp-audience { padding: 60px 20px; background: var(--white); }
.tp-audience h2 { text-align: center; color: var(--plum-900); font-family: "Playfair Display", serif; font-size: 2.2rem; margin-bottom: 20px; }
.tp-audience p { text-align: center; max-width: 700px; margin: 0 auto 40px; color: var(--text-soft); }
.tp-pill-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; max-width: 800px; margin: 0 auto; }
.tp-pill { background: var(--cream); color: var(--plum-900); padding: 8px 16px; border-radius: 20px; font-weight: 500; border: 1px solid var(--line-dark); }
.tp-cta-section { text-align: center; padding: 80px 20px; background: var(--plum-900); color: var(--ivory); }
.tp-cta-section h2 { font-size: 2.2rem; color: var(--gold-300); font-family: "Playfair Display", serif; margin-bottom: 20px; }
.tp-cta-section p { font-size: 1.1rem; max-width: 600px; margin: 0 auto 30px; }
.tp-price { font-size: 3rem; font-family: "Playfair Display", serif; color: var(--white); margin-bottom: 30px; font-weight: bold; }
.tp-price span { font-size: 1.2rem; color: #a996c0; font-family: "Inter", sans-serif; font-weight: normal; }
</style>

<section class="tp-hero">
  <div class="container">
    <h1>TRUEPROFIT&trade;</h1>
    <p>The Real Price Calculator</p>
    <div class="problem-statement">
      &ldquo;I am selling things, but do I actually know how much I am making?&rdquo;
    </div>
    <div style="max-width: 600px; margin: 0 auto; text-align: left; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
      <h3 style="color: var(--gold-300); margin-bottom: 15px; font-family: 'Inter', sans-serif; font-size: 1.2rem;">Core Promise:</h3>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 10px; display: flex; gap: 10px;"><span style="color: var(--gold-500);">&#10003;</span> Know your real cost.</li>
        <li style="margin-bottom: 10px; display: flex; gap: 10px;"><span style="color: var(--gold-500);">&#10003;</span> Know your real profit.</li>
        <li style="display: flex; gap: 10px;"><span style="color: var(--gold-500);">&#10003;</span> Price your business with confidence.</li>
      </ul>
      <p style="margin-top: 20px; font-size: 0.9rem; color: #a996c0; line-height: 1.5;">TRUEPROFIT&trade; helps you calculate relevant costs and understand your actual profit. Note: Market pricing also depends on competition, demand, location, and your strategy. We provide the cost-informed foundation.</p>
    </div>
    <div style="margin-top: 40px;">
      <a href="#get-access" class="btn btn--gold">GET TRUEPROFIT&trade; ACCESS</a>
    </div>
  </div>
</section>

<section class="tp-features">
  <div class="container">
    <h2>Why TRUEPROFIT&trade;?</h2>
    <div class="tp-grid-3">
      <div class="tp-feature-card">
        <div class="icon">&#128181;</div>
        <h3>Hidden Costs Included</h3>
        <p>Don't just calculate buying price. Account for transport, packaging, labour, electricity, and wastage so nothing eats your profit.</p>
      </div>
      <div class="tp-feature-card">
        <div class="icon">&#128200;</div>
        <h3>Target Margins</h3>
        <p>Set a desired profit margin and let the engine instantly calculate the recommended selling price for you.</p>
      </div>
      <div class="tp-feature-card">
        <div class="icon">&#128722;</div>
        <h3>Per Unit Breakdown</h3>
        <p>Calculate bulk costs and instantly see your exact cost, selling price, and profit per individual unit.</p>
      </div>
      <div class="tp-feature-card">
        <div class="icon">&#128178;</div>
        <h3>Break-Even &amp; Safe Minimums</h3>
        <p>Know exactly what your absolute minimum price must be to avoid taking a loss on your products.</p>
      </div>
      <div class="tp-feature-card">
        <div class="icon">&#127991;</div>
        <h3>Discount Calculator</h3>
        <p>Want to offer a sale? Safely calculate discounts and see exactly how much profit remains.</p>
      </div>
      <div class="tp-feature-card">
        <div class="icon">&#128274;</div>
        <h3>Business Privacy</h3>
        <p>Your numbers remain your own. An intuitive, account-based tool that grows with your business needs.</p>
      </div>
    </div>
  </div>
</section>

<section class="tp-audience">
  <div class="container">
    <h2>Built For Every Business Model</h2>
    <p>TRUEPROFIT&trade; is intentionally universal. You aren't forced to use every field. Enter only what applies to your business&mdash;whether you are a small start-up or an established enterprise.</p>
    <div class="tp-pill-grid">
      <span class="tp-pill">Producers</span>
      <span class="tp-pill">Manufacturers</span>
      <span class="tp-pill">Retailers</span>
      <span class="tp-pill">Wholesalers</span>
      <span class="tp-pill">Service Providers</span>
      <span class="tp-pill">Provision Sellers</span>
      <span class="tp-pill">Fashion Businesses</span>
      <span class="tp-pill">Food Businesses</span>
      <span class="tp-pill">Spare-Parts Sellers</span>
      <span class="tp-pill">Beauty Businesses</span>
    </div>
  </div>
</section>

<section class="tp-cta-section" id="get-access">
  <div class="container">
    <h2>Start Pricing With Confidence</h2>
    <p>Get legitimate commercial access to the TRUEPROFIT&trade; calculator. Stop guessing your profit and take control of your business pricing.</p>
    
    <a href="https://selar.com/28o4b14m9g" target="_blank" class="btn btn--gold" style="font-size: 1.1rem; padding: 16px 32px; display: inline-block; margin-bottom: 15px;">GET TRUEPROFIT&trade; ACCESS</a><br><a href="trueprofit-app.html" class="btn btn--outline" style="font-size: 0.95rem; padding: 10px 20px; color: #ffffff; border: 2px solid rgba(255, 255, 255, 0.6); border-radius: 30px;">Already purchased? Log in to App</a>
    <p style="margin-top: 30px; font-size: 0.85rem; color: #a996c0; max-width: 500px; margin-left: auto; margin-right: auto;">
      After payment verification on Selar, you will gain access to the secure TRUEPROFIT&trade; application.
    </p>
  </div>
</section>
'''
    return write("trueprofit.html", page(
        "TRUEPROFIT™ | The Real Price Calculator", "The Real Price Calculator for business owners. Know your real cost and actual profit.",
        "trueprofit", body, canonical=SITE_URL + "/trueprofit.html"
    ))

def build_trueprofit_app():
    pass
def build_all():
    build_home()
    build_about()
    build_ventures()
    build_books_landing()
    build_bookshelf()
    build_book_pages()
    build_author()
    build_blog()
    build_faq()
    build_contact()
    build_legal()
    build_404()
    build_trueprofit()
    build_trueprofit_app()
    build_robots_sitemap()
    write("README.md", README)
    print("Site built:", len(BOOKS) + 12, "HTML pages")


if __name__ == "__main__":
    build_all()
