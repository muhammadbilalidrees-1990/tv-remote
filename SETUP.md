# Setup — one time, about 20 minutes

You don't need Flutter, Android Studio, or a working dev machine. GitHub builds
the APK, Cloudflare hosts it, your phone downloads it.

Everything below is done in a browser.

---

## Step 1 — Put the code on GitHub

1. Sign in at **github.com** (create an account if you don't have one).
2. Click **+** at the top right, then **New repository**.
3. Name it `tv-remote`. Set it to **Private**. Do **not** tick "Add a README".
   Click **Create repository**.
4. On the next page, click **uploading an existing file**.
5. Unzip `tv-remote-repo.zip` on your PC and drag **everything inside it** onto
   that page — the `lib` folder, `site`, `tool`, `.github`, `pubspec.yaml`,
   the lot.
6. Click **Commit changes**.

The build starts on its own. Click the **Actions** tab to watch it. First run
takes about 6–8 minutes because it downloads Flutter; later runs take 2–3.

> **If the `.github` folder doesn't upload:** Windows hides folders starting
> with a dot in some unzip tools, and the browser drag-and-drop skips them.
> If the Actions tab stays empty, that's what happened — tell me and I'll give
> you the file to paste in manually.

---

## Step 2 — Get the APK (works already, no Cloudflare needed)

When the build finishes:

1. **Actions** tab → click the run at the top.
2. Scroll to **Artifacts** at the bottom → download `tv-remote-apk`.
3. That's a zip with the APKs inside. Move `app-arm64-v8a-release.apk` to your
   phone and install it.

If that works, the app is real and the rest is just convenience.

---

## Step 3 — Cloudflare Pages (gives you a permanent link)

### 3a. Create the Pages project

1. Sign in at **dash.cloudflare.com**.
2. Left sidebar → **Workers & Pages** → **Create** → **Pages** tab →
   **Upload assets**.
3. Project name: **`tv-remote`** — this must match exactly, the workflow
   looks for that name.
4. It asks for files. Upload any small file just to create the project; the
   build overwrites it on the next push.

### 3b. Get your Account ID

On the **Workers & Pages** overview page, the **Account ID** is in the right
sidebar. Copy it.

### 3c. Create an API token

1. Top right profile icon → **Profile** → **API Tokens** → **Create Token**.
2. Find **Edit Cloudflare Workers** in the template list → **Use template**.
3. Leave the defaults. Click through to **Create Token**.
4. **Copy the token now.** Cloudflare shows it once and never again.

### 3d. Put both into GitHub

In your repo: **Settings** → **Secrets and variables** → **Actions** →
**New repository secret**. Add these two, names spelled exactly:

| Name | Value |
|---|---|
| `CLOUDFLARE_API_TOKEN` | the token from 3c |
| `CLOUDFLARE_ACCOUNT_ID` | the ID from 3b |

### 3e. Trigger a build

**Actions** tab → **Build APK and publish to Cloudflare Pages** on the left →
**Run workflow** button → **Run workflow**.

When it's green, your install page is live at:

```
https://tv-remote.pages.dev
```

Open that on your phone and tap Download.

---

## Making changes later

Edit any file on GitHub (or upload a new one) and commit. The build runs
automatically and the page updates itself. No PC setup, ever.

---

## What to send me when something breaks

From the **Actions** tab, open the failed run, click the red step, and copy the
error text. The useful part is usually the last 20 lines.

---

## Things worth knowing

- **The app is signed with a debug key.** Fine for your own phone. It means
  you can't publish it to the Play Store as-is, and if you ever rebuild with a
  real key you'll have to uninstall before reinstalling.
- **The package name is `pk.bilal.tv_remote`.** Change the `--org` flag in
  `.github/workflows/build.yml` if you want something else — but do it before
  you install, or you'll end up with two copies on the phone.
- **The `android/` folder is not in the repo.** The build generates it fresh
  every time and `tool/patch_android.py` adds the permissions. If you ever
  want a custom app icon, that changes — tell me and I'll restructure it.
- **Cloudflare Pages caps files at 25 MB.** The build fails on purpose if the
  APK crosses that, rather than deploying something broken.
