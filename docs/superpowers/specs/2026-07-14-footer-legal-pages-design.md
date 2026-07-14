# Compact Footer and Kit Legal Pages Design

## Goal

Refine the Phoxia DevKit footer so its links read as compact text, align the mobile layout with phoxia.org, and add product-specific bilingual privacy and terms pages for kit.phoxia.org.

## Footer contract

The existing four-area desktop footer remains. Footer navigation links use normal inline text styling with no button-like padding or oversized hit surface. Each group uses an 8px vertical gap.

The Trust & support group contains, in order:

1. Security
2. Support
3. Privacy
4. Terms
5. Code of Conduct

AGPLv3 is removed from this navigation group and remains only in the bottom legal line. Support links to `mailto:support@phoxia.org`. Privacy and Terms link to `/privacy` and `/terms` on kit.phoxia.org.

On screens up to 600px, the footer brand, description, navigation groups, bottom legal line, Discord, and GitHub align to the center. Navigation remains a two-column grid to avoid an unnecessarily long single-column footer. Group headings and links are centered.

## Legal-page contract

The site gains a local legal-page component and two routes:

- `/privacy`: privacy policy for kit.phoxia.org and the Phoxia DevKit website.
- `/terms`: terms of use for kit.phoxia.org and the Phoxia DevKit website.

Both routes support English and Brazilian Portuguese through the site's existing locale state. They reuse the established phoxia.org information architecture: page title, last-updated metadata, section navigation on wide screens, and readable section content. The implementation remains local to this repository and does not import code from phoxia-org.

Content is adapted to the Kit. It must not copy unverified infrastructure, retention, TLS-version, analytics, account, payment, or data-processing claims from phoxia.org. Product licensing remains AGPLv3, while website and documentation terms are stated only where repository evidence supports them.

## Legal status

The policy and terms are published as effective documents at the user's direction. Each page shows only its last-updated date, without draft, version, or pending-review labels.

## Legal-page alignment and contacts

On wide screens, the legal-page header uses the same two-column grid as the page body. Its first column remains empty so the icon, title, and updated date align exactly with the first content section. On narrow screens, the header and content use the same natural left edge.

Contact details in the final section appear after the explanatory sentence, with one contact per line. Privacy, security, legal, and support addresses are not compressed into a single paragraph line.

## Accessibility and behavior

- Footer links retain visible keyboard focus and sufficient contrast.
- External Discord and GitHub links keep accessible names.
- Legal-page section navigation uses native links where possible and remains usable without JavaScript.
- Page titles follow `Phoxia • Page`.
- Normal product copy avoids em dashes.

## Verification

Automated coverage verifies:

- compact footer link styling and 8px group gaps;
- mobile footer centering without horizontal overflow;
- Support, Privacy, Terms, Security, Code of Conduct, Discord, and GitHub destinations;
- AGPLv3 is absent from Trust & support and present in the bottom legal line;
- both legal routes render effective English and Brazilian Portuguese copy without draft labels;
- legal titles align with the content column and contacts render one per line;
- site type checks, locale validation, public-boundary validation, production build, and responsive Playwright tests pass.
