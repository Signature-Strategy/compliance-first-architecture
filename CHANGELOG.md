# Changelog — Compliance-First Data Processing Architecture

All notable changes to the published paper are documented here.
Versions use Git commit short hashes; the internal version history
(Section 15, Revision History) tracks the paper's editorial evolution
from v0.1 through v0.5.

---

## [`c21d60c`] — 2026-03-27

### Author's Note & AI Disclosure
- **Expanded author's note** (Section 1): Replaced citation-only disclaimer
  with systems integrator perspective framing. The note now states that the
  paper is written from the perspective of a systems integrator working across
  multiple regulated sectors who observed convergence in practice. The
  architectural thesis, nine principles, and conclusions are identified as the
  author's own assertions.
- **Expanded AI disclosure** (Afterword): Now explicitly describes the
  structured multi-persona review process using AI-generated panelists
  representing distinct regulatory and technical perspectives. Adds sentence
  distinguishing AI-assisted review from human peer review.

### Processing Modes
- **Renamed "standard mode" to "non-forensic mode"** throughout all four HTML
  variants (~11 occurrences in each full paper, 1 in each brief). The new
  name makes the implications of mode selection explicit.
- **Reframed Section 6 introduction**: Non-forensic mode is now justified by
  two reasons: (1) data not governed by the regulatory traditions in this
  paper (internal investigations, R&D, data scanning), and (2) proportionality
  analysis within regulated contexts (routine FINRA 3110 supervisory review,
  GRS 6.1 temporary records migration). The proportionality argument under
  FRCP 26(b)(1) and Sedona Commentary is retained.
- **Strengthened transparency requirement**: Every artifact, log, report, and
  reconciliation must indicate that forensic mode was off for that run.

### Ninth Principle Normalization
- **Algorithmic decision transparency is now a full peer** of principles 1–8,
  not a latecomer. Section 5 groups the nine patterns into four categories
  (data integrity, accountability, boundary handling, algorithmic
  transparency) instead of three-plus-one.
- **Section 9 heading** changed from "The Ninth Universal Pattern" to
  "Algorithmic Decision Transparency." Introduction rewritten to lead with
  5/5 regulatory convergence rather than emergence narrative.
- **Honest maturity qualifier**: Section 5 notes that the regulatory sources
  underlying pattern 9 are newer than patterns 1–8, but the directional
  convergence is clear and accelerating.
- **Executive brief Principle #9** now explicitly cites all five traditions
  (FRE 702, ISO 27042/SWGDE, OMB M-24-10, SEC/FINRA, GDPR Art. 22) plus
  EU AI Act and NIST AI RMF.

### Reviewer Attribution
- **De-anonymized peer reviewer**: "A.B." replaced with "Aidan Booth
  (Ashcroft Forensic Advisory)" in Acknowledgments and revision history.
- **Third-round feedback credited**: Acknowledgments now reference Aidan's
  third review round covering non-forensic mode framing, verification
  independence language, and audit trail completeness definitions.

### Substantive Changes (Aidan Booth feedback, third round)
- **Chain of custody** (Section 4 convergence paragraph): Changed "integrity
  is intact" to "chain of custody is intact" — precision matters when the
  sentence is about custody, not data integrity.
- **Verification independence** (Section 2, third pillar): Added "segregated
  verification component, architecturally firewalled from the processing
  pipeline" and "takes precedence where conflicts arise."
- **Audit trail completeness** (Section 5.4): Added "system-generated
  actions, human actions, and machine-assisted actions" to clarify what the
  audit trail must cover.

### Editorial
- **Em dash replacement**: ~199 em dashes replaced with commas or semicolons
  in full papers, ~13 per brief. Context-aware: negation clauses use commas,
  conjunctive clauses use semicolons.
- **Comma splice fixes**: Restored parenthetical structure in "necessary but
  not sufficient" paragraph (all four files) and Principle #7 in briefs.

---

## [`38b8d02`] — 2026-03-26

Replace "processing depth" with "processing rigor" in Two Processing Modes
section heading and body text across all four HTML variants.

## [`a764e78`] — 2026-03-26

Use consistent sun/moon emoji icons for light/dark theme switcher in
executive brief cards.

## [`21159e7`] — 2026-03-26

Add `<link rel="canonical">` tags so that Hypothesis annotations merge
across light/dark theme variants of the same document.

## [`81bffc9`] — 2026-03-26

Add themed executive briefs (`short-light.html`, `short-dark.html`).
Sync light and dark full paper variants to ensure identical content.

## [`4a55e18`] — 2026-03-25

Add executive brief — a condensed single-page overview covering the core
thesis, nine principles table, processing modes summary, and validation
framework. Links to full paper for regulatory citations and appendices.

## [`d3687e6`] — 2026-03-25

Add acknowledgments section for Aidan Booth (peer reviewer) and Adam Blak
(marketing and positioning feedback).

## [`a55d6be`] — 2026-03-25

Revise README with academic framing ("Written from the perspective of a
systems integrator working across multiple regulated sectors") and
CC BY-NC-ND 4.0 license. Add Hypothesis feedback instructions.

## [`2cc6aa2`] — 2026-03-25

Add README with abstract, reading links (light/dark themes), and basic
project description.

## [`7eeb95d`] — 2026-03-24

**Initial publication.** Compliance-First Data Processing Architecture,
v0.5-DRAFT. Four HTML files:
- `light.html` — Full paper, light theme
- `dark.html` — Full paper, dark theme

Core framework: nine universal architectural patterns derived from
convergence analysis of five regulatory traditions (civil litigation,
digital forensics, federal records, financial services, privacy). Includes
processing modes, validation protocol, three-rate error framework,
sector-specific requirements, security architecture, and five appendices.

Internal version history (v0.1–v0.5) documents the editorial evolution
including two rounds of peer review feedback integration.
