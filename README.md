# HUMMUSHEIKHS VENTURES Website

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
