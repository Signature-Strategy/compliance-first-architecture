# Changelog — Compliance-First Data Processing Architecture

All notable changes to the published paper are documented here.
Versions use Git commit short hashes; the internal version history
(Section 15, Revision History) tracks the paper's editorial evolution
from v0.1 through v0.5.

---

## [v1.1] — 2026-04-03

### Terminology
- Replaced "universal" with "convergent" throughout (~19 instances across
  full papers). The convergence thesis identifies patterns that independent
  traditions arrive at; "convergent" is more accurate and more defensible
  than "universal," which implies exhaustive coverage.

### New content
- **Glossary**: Added "Item" definition (atomic unit of processing output),
  "CMMC" (Cybersecurity Maturity Model Certification), and "DORA" (Digital
  Operational Resilience Act)
- **Section 1**: Author's note restructured as clearly demarcated authorship
  statement (blockquote with heading) per reviewer feedback
- **Section 5**: Added quick-reference card table mapping all nine patterns
  to groups and key invariants
- **Section 7.6**: New subsection on third-party extraction library
  challenges, elevated from Appendix D.8; includes containerized deployment
  considerations
- **Section 10.2**: Acknowledged CFTT test corpus construction as a research
  program; acknowledged fidelity rate ground truth cost
- **Section 10.6**: New subsection on processing SLAs and incremental
  processing
- **Section 12**: Strengthened DoD/IC positioning: CMMC Level 2 mention,
  air-gapped environments, supply-chain attacks reframed as graduated
  architectural concern
- **Section 14**: Strengthened jurisdictional scope note (US perspective,
  internationally adaptable); added cost implications acknowledgment;
  noted recurring panel concerns as out-of-scope future work; reinforced
  independent positioning
- **Appendix A.2**: Added anti-forensics detection as evidence paragraph;
  added mobile device data paragraph; strengthened FSR statutory enforcement
- **Appendix A.4**: Added continuous/streaming processing note, voice
  recording (MiFID II), WORM regulatory uncertainty, DORA/EMIR
- **Appendix A.5**: Added legitimate interest balancing test mapping,
  Art. 20 data portability, chilling effect acknowledgment; strengthened
  erasure tension with EDPB guidance
- **Appendix A.6.1**: Added inference precision (FP32/FP16/INT8) to model
  provenance fields
- **Appendix E**: Added air-gapped and cross-domain deployment paragraph

### Attribution
- Added Bjornar Sigurdsson to Acknowledgments for Hypothesis annotations

### Panel review integration
- 20-persona simulated panel review conducted; findings incorporated
  throughout. Panel endorsed convergence thesis and architectural patterns;
  criticisms were editorial and structural, not foundational. Recurring
  concerns noted as out-of-scope future work in Section 14.

---

## [v1.0] — 2026-03-27

### Version 1.0 Release

Eight deferred panel findings applied:
- **Section 10.2**: Fixed comma splice in validation protocol item 1 (semicolon)
- **Section 6 mode table**: Removed "(always)" qualifier asymmetry from
  non-forensic column — the paragraph below already states seven features
  cannot be toggled off
- **Section 1**: Added bridge sentence connecting Victor Stanley search
  methodology analogy to processing self-verification conclusion
- **Exec Brief traditions table**: Added "(applied by analogy)" qualifier on
  ISO 27037 for digital forensics row
- **Section 9/A.6.3**: SCHUFA ruling date corrected to "December 7, 2023"
- **Section 13**: Added distinguishing sentence — Da Silva Moore and Rio Tinto
  addressed review methodology, not processing architecture; the analogy is
  that Daubert evaluates reliability of the method presented
- **Exec Summary reader guide**: AI-augmented pipelines entry separated from
  five-tradition bulleted list to preserve visual hierarchy
- **Section 5.3**: Added forward-reference to Section 9 and Appendix A.6.1
  for machine-assisted actions audit requirements

### Exec summary voice normalization
- Removed inline citations from Principle #1 Why It Matters column
- Rewrote #5–#9 for consistent active-verb, consequence-focused voice
- Brief Principle #9 rewritten from citation-led to consequence-focused

### Version bump
- Version 1.0 across all files (cover pages, index, README)
- Removed DRAFT label
- Added PDF for GitHub release and SSRN submission

---

## [`bc497d0`] — 2026-03-27

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
