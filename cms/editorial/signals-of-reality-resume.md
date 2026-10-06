# Continuing Signals of Reality

The canonical source is reazromen/website, branch main. This is the 200-article Signals of Reality project; it is distinct from the 300-article Signals Around Us project.

Read cms/signals-of-reality-plan.md for the exact 10-series, 200-title plan. cms/signals-of-reality-progress.json distinguishes published source, existing drafts needing review, and missing articles. Never count a title, outline, short draft, source commit, or successful build as a verified live article.

The previous hserver corpus is /home/romen/work/reazromen-signals. The October 7 release checkout is /home/romen/work/reazromen-signals-batch2-20261007. Always fetch current main before continuing; the old corpus has stale publication flags and malformed metadata. Resume from the corrected committed sources rather than copying those files over current main.

After the October 7 release, IDs 001–010 are in published source, 011–160 are drafts, and 161–200 still need writing. Start publication review at 011. Many later drafts have only about 500–800 words and require substantive expansion to the planned 900–1600-word range. Preserve distinct forms, flowing paragraphs, evidence, primary sources, and explicit limits on analogies. Short files are unfinished work, not completed articles.

For each release, verify its date in Asia/Dhaka, inspect the publication_batches ledger and current main, and count articles already released that real day. The October 7 batch contains 006–010 and exhausts that day's five-article cap. A second October 7 run may research, write, and improve drafts, but must not publish more project articles. Do not evade the cap with backdated metadata. Also enforce the site-wide limit of five published records per date.

Preserve prior public URLs, latest menus, CMS route, topics, and navigation. Use an isolated branch from current main; retain future files as draft: true. Validate all front matter and taxonomy, run cms/build_content.py and cms/package_public.py, inspect the public artifact to confirm that only intended articles become public and drafts are absent, then use a controlled PR/merge workflow. Wait for both GitHub checks and the main Build and publish website workflow. Verify each intended route at the GitHub Pages origin and reazromen.com, including title, English body, publication date, and X-Reaz-Delivery: github-pages-via-cloudflare-pages. Update the progress record after each batch.

Continue authoring and improving missing or unfinished articles toward all 200 even when a day's publication allowance is exhausted. Keep unpublished work private in the Git content sources. Finish the project only after all 200 complete reviewed essays are verified live; article 200 is Reality Arrives as Signals.
