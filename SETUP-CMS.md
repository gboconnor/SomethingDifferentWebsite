# Setting up the browser editor (one-time)

Follow these in order. Take your time — each step is just clicks, and nothing
affects your current live site (which stays on Strive's setup until the very end).

Your GitHub username: **gboconnor**

---

## Step 1 — Create the repository (the home for your site's files)

1. Go to https://github.com/new
2. **Repository name:** `something-different-site`
3. Leave it **Public** (fine) or choose **Private** — either works.
4. Do NOT tick "Add a README" (your files already include one).
5. Click **Create repository**.

You'll land on a mostly empty repo page with an "uploading an existing file" link.

## Step 2 — Upload the site files

1. On that page, click **uploading an existing file** (or **Add file → Upload files**).
2. Unzip the `something-different-site` package I gave you so you have the *folder*.
3. Drag the **whole folder** onto the upload area (drag the folder itself, don't
   open it and select the files — that way hidden config files come along too).
4. Wait for all files to list (there are ~90, including the 77 musings).
5. At the bottom, click **Commit changes**.

> If the editor later says it can't find its config, it means the hidden
> `.pages.yml` file didn't upload. Fix: on the repo, click **Add file → Create new
> file**, name it exactly `.pages.yml`, paste the contents of the `.pages.yml` file
> from your folder, and commit. (I can also paste those contents to you.)

## Step 3 — Connect the repo to Netlify (auto-publishing)

1. In Netlify, click **Add new site → Import an existing project**.
2. Choose **GitHub**, authorise if asked, and pick `something-different-site`.
3. Netlify reads the build settings automatically (from `netlify.toml`) — you
   should see build command `pip install ... && python3 build_site.py` and publish
   directory `.`. Leave them as shown.
4. Click **Deploy**. First build takes a minute or two.
5. When it finishes you'll get a new `something-name.netlify.app` address — open it
   and check the site looks right, musings and all.

This new site is separate from your old one, so nothing clashes. From now on, any
change committed to the repo rebuilds this site automatically.

## Step 4 — Turn on the editor (Pages CMS)

1. Go to https://app.pagescms.org
2. Click **Sign in with GitHub** and authorise it for your `something-different-site` repo.
3. Pick the repo. You'll see a **Musings** collection with all 77 posts.
4. Click **+ Add** to write a new one: Title, Category, Date, an optional header
   image, and the Article body in a rich editor. Save.
5. Saving commits to GitHub → Netlify rebuilds → it's live in a minute. That's it.

## Step 5 — Go live (later, with Strive)

When you're happy, we point `somethingdifferent.co.nz` at this new Netlify site.
Because Strive currently hosts the live site and manages the domain, that's a
coordinated hand-off — I'll give you the exact records/instructions to send them.

---

## Adding the contact-form email + Folk

Same as before: on the **new** Netlify site, set **Forms → notifications** to email
gareth@somethingdifferent.co.nz, and (optionally) connect Netlify Forms → Folk via
Zapier. See README.md for detail.
