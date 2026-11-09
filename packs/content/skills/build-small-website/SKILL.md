---
name: build-small-website
description: Plans and builds a small public website with several pages, shared navigation and checked visitor journeys. Use for a club, charity or service site. Use campaign-website for a single campaign action.
---

# Build a small website

**Stage:** Operate. **Rules:** 1 Stop at the boundaries, 2 Agree acceptance first, 3 Read back the real result, 4 Claim only what you can show.

## Context and handoff

Start with the owner, audience, existing site, approved source material and a destination you can verify. Keep design, hosting and publishing decisions with the same site brief. Give a campaign with one conversion action to `campaign-website`. Use `verify-live-release` after an authorised publication.

Record the approved source brief (file, revision and owner) at the top of the working record or handover, never in the public or buyer-facing copy. If there is no brief yet, the brief step creates it. Every claim traces to the brief or to this skill's own source list; anything else is a question for the owner. If `.work/capabilities.md` exists, read the section for this runtime. If a browser or local server is missing, say so first, build static pages and a manual journey script and mark the check pending.

## When not to use this

Use a smaller task for an existing site's isolated fix. For a site requiring new accounts, payments or sensitive forms, agree the relevant permissions and delivery route before building the integration. A local demonstration can still show the journey.

## Steps

1. **Agree the journeys.** Choose up to three tasks visitors need to complete. Record the entry page, exact expected outcome, content and approved action for each. Identify owner, required host or stack, approved claims, asset rights and any unresolved dependencies. Keep claims with missing evidence out of the public copy.
2. **Build to the map.** Reuse the existing design and navigation where appropriate. Use semantic headings and links, labelled controls, visible keyboard focus and layouts that work on narrow and wide screens. Label fictional content. A demonstration action stays local and its page explains what it does.
3. **Exercise the paths.** Open direct URLs as well as navigating from Home. Test the actual destination or visible result for each agreed journey, including keyboard and narrow layouts. If a form is in scope, check the relevant empty, error and success states with authorised test data. Record the environment and any external delivery that needs separate proof.
4. **Hand over.** Save the source revision, preview, page map, verified journeys and content owner. Keep public release pending until the owner authorises the exact destination and revision.

## Output and checks

Use the [site brief](template.md). Record what the visitor can do, where each check ran and what is still open. A preview can pass its own checks while publication and public read-back remain pending.

**Reviewer check:** open the page map, pick one agreed journey and follow it from a direct URL to its stated outcome. Confirm each page claim appears in the cited brief.
