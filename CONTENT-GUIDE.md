# Editing Your Site Without Code

Your site now has a real visual editor built in, similar in spirit to
WordPress: you log in, fill in form fields, upload images by dragging them
in, and click Save. No HTML, no code, ever.

Getting this fully working takes one round of setup, done once. After that,
every future edit is just logging in and clicking around. This guide walks
through the one-time setup, then how to use it day to day.

---

## Part 1: One-time setup

Right now your site is likely deployed by dragging a folder onto Netlify.
That method can't support the visual editor, because the editor needs to
save your changes somewhere permanent, and it does that by saving to a
GitHub repository, which then tells Netlify to rebuild your site
automatically. So the setup below moves you from "drag and drop" to
"connected to GitHub." This sounds technical but each step is just
clicking buttons on websites, no code involved.

### Step 1: Create a GitHub account and repository

1. Go to github.com and sign up if you don't already have an account (free).
2. Click the "+" in the top right, then "New repository."
3. Name it something like `hummusheikhs-ventures-website`. Keep it Private
   or Public, your choice, either works fine here.
4. Click "Create repository."
5. On the next page, click "uploading an existing file."
6. Drag every file and folder from this package into that upload box
   (yes, all of it: the HTML files, `assets`, `content`, `admin`,
   `netlify.toml`, everything), then click "Commit changes."

### Step 2: Connect that repository to Netlify

1. Go to your Netlify dashboard.
2. Click "Add new site," then "Import an existing project."
3. Choose GitHub, and authorize Netlify to access your account if asked.
4. Select the repository you just created.
5. Netlify should automatically detect the build command
   (`python3 build.py`) and publish folder (`.`) from the `netlify.toml`
   file included in this package. If it asks you to confirm them, that's
   what they should say.
6. Click "Deploy." Your site will build and go live on a Netlify address.
7. If you want to keep using `hummusheikhsventures.netlify.app`, go to
   Site settings, then Domain management, and set that as this new site's
   subdomain (you may need to first rename or remove it from the old
   drag-and-drop site if that name is still attached there).

### Step 3: Set up login access for the editor (DecapBridge)

The editor needs a way to know who's allowed to log in and save changes.
We're using a free service built exactly for this, called DecapBridge.

1. Go to decapbridge.com and sign up for a free account.
2. Click "Add your Decap CMS site."
3. Link it to the GitHub repository you created in Step 1.
4. DecapBridge will generate a `backend:` configuration block for you,
   a short piece of text.
5. Go back to your GitHub repository in your browser, open
   `admin/config.yml`, click the pencil/edit icon.
6. Replace the placeholder `backend:` block at the top of that file (the
   first few lines) with the one DecapBridge gave you. Leave everything
   else in the file exactly as it is.
7. Click "Commit changes." Netlify will automatically rebuild your site
   with this update within a minute or two.
8. Back in DecapBridge, invite yourself as a user for this site (you'll
   get an email to confirm). If you later want a client to be able to
   edit their own site, this is also where you'd invite them, using the
   same free plan, up to 10 collaborators per site.

### You're done with setup

From now on, go to `yoursite.netlify.app/admin`, log in with the account
you set up in DecapBridge, and you'll see the visual editor.

---

## Part 2: Using the editor day to day

Once logged in at `/admin`, you'll see a menu on the left with sections
matching what you can edit:

- **Business Info**: your business name, slogan, author name, email,
  WhatsApp number, logo, and author photo. Change any of these and every
  page that uses them updates automatically.
- **Books**: click a book to edit its title, description, features,
  cover image, and buy link, or click "New Books" to add a brand new one.
  Removing a book is done from this same list.
- **FAQ**: add, edit, or remove questions and answers.
- **Our Ventures**: update the status and description of each business
  venture (Books & Publishing, Digital Services, etc.), or mark a new one
  as active once it launches.

Every field here is a plain text box, image upload button, or toggle
switch, never raw code. When you click Save/Publish, the editor commits
your change to GitHub, which triggers Netlify to rebuild your site
automatically, usually live again within about a minute.

### Uploading images

Anywhere you see an image field (book covers, logo, author photo), click
it and either drag your new image in or choose it from your files. The
editor handles placing it correctly, no file naming or folder knowledge
needed.

### One thing to leave alone

Each book has a field called "Internal ID," pre-filled and hidden away
near the top of the book's edit form. This is what determines the book's
web address. It's fine to leave it as-is; there's no need to touch it
unless you're renaming a book's URL on purpose.

---

## Part 3: If you ever need code-level help

You (or any future developer) can still open `content.py` and `build.py`
if a bigger structural change is ever needed, like adding a whole new
type of page beyond books, FAQs, and ventures. That's genuinely
code-level work, not a content edit, so it's the one case where coming
back to Claude, or hiring a developer, still makes sense. Day-to-day
content, this guide covers it all.
