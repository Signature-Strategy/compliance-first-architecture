"""
Add hyperlinks to internal cross-references and external legal/regulatory
citations in the Compliance-First Data Processing Architecture paper.
"""

import re
import sys

# ── Internal cross-reference ID mapping ──────────────────────────────────
# Maps display text patterns to HTML anchor IDs
SECTION_IDS = {
    "1": "the-problem-processing-as-a-black-box",
    "2": "architectural-foundation",
    "3": "the-five-traditions",
    "4": "convergence-methodology",
    "5": "convergent-architectural-patterns",
    "5.1": "reprocessing-determinism",
    "5.2": "cryptographic-hashing",
    "5.3": "encounter-sequence-numbers",
    "5.3.1": "encounter-sequence-properties",
    "5.4": "chain-of-custody-and-audit-trail",
    "5.5": "content-addressed-binary-storage",
    "5.6": "no-silent-drops",
    "5.7": "source-integrity-verification",
    "5.8": "encrypted-and-password-protected-content",
    "6": "the-processing-mode-question",
    "7": "operational-compliance-constraints",
    "7.1": "throughput-at-scale",
    "7.2": "crash-recovery-and-partial-run-defensibility",
    "7.3": "adversarial-input-resilience",
    "7.4": "checkpoint-overhead",
    "7.5": "distributed-and-cloud-deployment",
    "7.6": "third-party-extraction-libraries",
    "8": "deduplication-as-a-cross-cutting-concern",
    "9": "ai-augmented-processing-algorithmic-decision-transparency",
    "10": "validation-protocol",
    "10.1": "automated-compliance-verification",
    "10.2": "error-rate-framework",
    "10.3": "extraction-fidelity-taxonomy",
    "10.5": "the-three-rate-framework-in-practice",
    "10.6": "processing-slas-and-incremental-processing",
    "11": "security-architecture",
    "12": "security-architecture",
    "13": "case-law",
    "14": "limitations",
}

APPENDIX_IDS = {
    "A": "appendix-a-sector-specific-regulatory-detail",
    "A.1": "a.1-civil-litigation",
    "A.2": "a.2-digital-forensics",
    "A.3": "a.3-federal-records-management",
    "A.4": "a.4-financial-services",
    "A.5": "a.5-privacy-and-cross-border",
    "A.6": "a.6-ai-augmented-processing-pipelines",
    "A.6.1": "a.6.1-audit-trail-for-ai-classification-decisions",
    "A.6.3": "a.6.3-gdpr-article-22-automated-decision-making",
    "B": "appendix-b-extraction-fidelity-taxonomy",
    "C": "appendix-c-hash-algorithm-selection-architecture-and-rationale",
    "C.1": "c.1-single-pass-multi-digest-architecture",
    "C.3": "c.3-the-sha-3-question",
    "C.4": "c.4-per-algorithm-toggleability",
    "C.5": "c.5-implications-for-engine-design",
    "D": "appendix-d-architectural-detail",
    "D.7": "d.7-crash-recovery-mechanics-7.2",
    "D.8": "d.8-adversarial-input-defensive-mechanisms-7.3",
    "E": "appendix-e-distributed-and-cloud-deployment-architecture",
    "E.3": "e.3-air-gapped-and-cross-domain-deployment",
    "F": "appendix-f-empirical-multi-digest-hashing-cost",
    "F.4": "f.4-pipeline-context",
}

# ── External reference URL mapping ───────────────────────────────────────
# Cornell LII for US rules and statutes
EXTERNAL_URLS = {
    # Federal Rules of Evidence
    "FRE 702": "https://www.law.cornell.edu/rules/fre/rule_702",
    "FRE 901": "https://www.law.cornell.edu/rules/fre/rule_901",
    "FRE 901(a)": "https://www.law.cornell.edu/rules/fre/rule_901",
    "FRE 901(b)(9)": "https://www.law.cornell.edu/rules/fre/rule_901",
    "FRE 902": "https://www.law.cornell.edu/rules/fre/rule_902",
    "FRE 902(13)": "https://www.law.cornell.edu/rules/fre/rule_902",
    "FRE 902(14)": "https://www.law.cornell.edu/rules/fre/rule_902",
    "FRE 803(6)": "https://www.law.cornell.edu/rules/fre/rule_803",
    "FRE 502(d)": "https://www.law.cornell.edu/rules/fre/rule_502",
    "FRE 801(a)": "https://www.law.cornell.edu/rules/fre/rule_801",

    # Federal Rules of Civil Procedure
    "FRCP 26(b)(1)": "https://www.law.cornell.edu/rules/frcp/rule_26",
    "FRCP 26(b)(5)(B)": "https://www.law.cornell.edu/rules/frcp/rule_26",
    "FRCP 26(f)": "https://www.law.cornell.edu/rules/frcp/rule_26",
    "FRCP 26(g)": "https://www.law.cornell.edu/rules/frcp/rule_26",
    "FRCP 34(b)": "https://www.law.cornell.edu/rules/frcp/rule_34",
    "FRCP 37(e)": "https://www.law.cornell.edu/rules/frcp/rule_37",
    "FRCP 16(b)": "https://www.law.cornell.edu/rules/frcp/rule_16",

    # USC
    "44 USC": "https://www.law.cornell.edu/uscode/text/44",
    "44 U.S.C.": "https://www.law.cornell.edu/uscode/text/44",
    "18 U.S.C. \u00a7 2071": "https://www.law.cornell.edu/uscode/text/18/2071",
    "5 U.S.C. \u00a7 552a": "https://www.law.cornell.edu/uscode/text/5/552a",
    "5 U.S.C. \u00a7 552": "https://www.law.cornell.edu/uscode/text/5/552",

    # NIST publications
    "NIST SP 800-131A": "https://csrc.nist.gov/pubs/sp/800/131/a/r2/final",
    "NIST SP 800-171": "https://csrc.nist.gov/pubs/sp/800/171/r3/final",
    "NIST SP 800-53": "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final",
    "NIST SP 800-86": "https://csrc.nist.gov/pubs/sp/800/86/final",
    "NIST SP 800-101": "https://csrc.nist.gov/pubs/sp/800/101/r1/final",
    "NIST SP 800-208": "https://csrc.nist.gov/pubs/sp/800/208/final",
    "FIPS 202": "https://csrc.nist.gov/pubs/fips/202/final",
    "FIPS 140": "https://csrc.nist.gov/pubs/fips/140-3/final",
    "NIST AI RMF": "https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence",

    # GDPR - link to EUR-Lex consolidated text
    "GDPR Art.": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",

    # ISO standards
    "ISO 27037": "https://www.iso.org/standard/44381.html",
    "ISO 27042": "https://www.iso.org/standard/44406.html",
    "ISO 27043": "https://www.iso.org/standard/44407.html",
    "ISO 27050": "https://www.iso.org/standard/78647.html",
    "ISO 17025": "https://www.iso.org/standard/66912.html",
    "ISO 27001": "https://www.iso.org/standard/27001",

    # FINRA rules
    "FINRA 3110": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110",
    "FINRA 4511": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/4511",
    "FINRA 8210": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/8210",
    "FINRA Rule 3110": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110",

    # SEC rules - eCFR
    "SEC 17a-4": "https://www.ecfr.gov/current/title-17/section-240.17a-4",
    "SEC 17a-3": "https://www.ecfr.gov/current/title-17/section-240.17a-3",
    "SEC Rule 17a-4": "https://www.ecfr.gov/current/title-17/section-240.17a-4",
    "SEC Rule 17a-3": "https://www.ecfr.gov/current/title-17/section-240.17a-3",
    "SEC Rule 18a-6": "https://www.ecfr.gov/current/title-17/section-240.18a-6",

    # CFR
    "36 CFR 1236": "https://www.ecfr.gov/current/title-36/chapter-XII/subchapter-B/part-1236",
    "36 CFR 1222": "https://www.ecfr.gov/current/title-36/chapter-XII/subchapter-B/part-1222",
    "32 CFR Part 2002": "https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002",
    "31 CFR Part 1010": "https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010",

    # EU AI Act
    "EU AI Act": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",

    # DORA
    "DORA": "https://eur-lex.europa.eu/eli/reg/2022/2554/oj",

    # EMIR
    "EMIR": "https://eur-lex.europa.eu/eli/reg/2012/648/oj",

    # MiFID II
    "MiFID II": "https://eur-lex.europa.eu/eli/dir/2014/65/oj",

    # CFTC
    "CFTC Rule 1.31": "https://www.ecfr.gov/current/title-17/chapter-I/part-1/section-1.31",

    # RFCs
    "RFC 6962": "https://datatracker.ietf.org/doc/html/rfc6962",
    "RFC 8493": "https://datatracker.ietf.org/doc/html/rfc8493",
}

# GDPR article-specific URLs (GDPR-info.eu has per-article pages)
GDPR_ARTICLES = {}
for art_num in range(1, 100):
    GDPR_ARTICLES[str(art_num)] = f"https://gdpr-info.eu/art-{art_num}-gdpr/"


def link_internal_refs(html):
    """Add anchor links to internal Section X and Appendix X references."""
    int_links = []

    def protect_int(link_html):
        int_links.append(link_html)
        return f'__INTLINK_{len(int_links) - 1}__'

    def replace_section(m):
        full = m.group(0)
        num = m.group(1)
        # Try most specific match first (e.g., "5.3.1" before "5.3" before "5")
        anchor = SECTION_IDS.get(num)
        if anchor:
            return protect_int(f'<a href="#{anchor}">{full}</a>')
        return full

    def replace_appendix(m):
        full = m.group(0)
        letter = m.group(1)
        anchor = APPENDIX_IDS.get(letter)
        if anchor:
            return protect_int(f'<a href="#{anchor}">{full}</a>')
        return full

    # Existing links, headings, and id attrs are already replaced with placeholders

    # Section references: "Section 5.3.1", "Section 6"
    html = re.sub(
        r'Section (\d+(?:\.\d+)*)',
        replace_section,
        html
    )

    # Appendix references: "Appendix C.1", "Appendix F"
    html = re.sub(
        r'Appendix ([A-F](?:\.\d+)*)',
        replace_appendix,
        html
    )

    # Restore internal link placeholders
    for i, link in enumerate(int_links):
        html = html.replace(f'__INTLINK_{i}__', link)

    return html


def link_external_refs(html):
    """Add hyperlinks to external legal/regulatory citations."""

    # We protect each newly-created link with a placeholder so subsequent
    # iterations don't match inside anchor text (e.g. "FRE 902" inside
    # an already-linked "FRE 902(14)").
    new_links = []

    def protect(link_html):
        """Replace a newly-created <a> tag with a placeholder."""
        new_links.append(link_html)
        return f'__NEWLINK_{len(new_links) - 1}__'

    # GDPR articles: "GDPR Art. 22(1)", "Art. 5(1)(a)", etc.
    def replace_gdpr(m):
        full = m.group(0)
        art_num = m.group(1)
        url = GDPR_ARTICLES.get(art_num)
        if url:
            return protect(f'<a href="{url}">{full}</a>')
        return full

    html = re.sub(
        r'(?:GDPR )?Art\. (\d+)(?:\([^)]*\))*',
        replace_gdpr,
        html
    )

    # Sort external URLs by key length (longest first) to avoid partial matches
    sorted_refs = sorted(EXTERNAL_URLS.items(), key=lambda x: -len(x[0]))

    for ref_text, url in sorted_refs:
        # Skip GDPR Art. (handled above) and very short keys
        if ref_text == "GDPR Art." or len(ref_text) < 4:
            continue

        escaped = re.escape(ref_text)
        pattern = f'({escaped})'

        def make_replacer(u):
            def replacer(m):
                return protect(f'<a href="{u}">{m.group(1)}</a>')
            return replacer

        html = re.sub(pattern, make_replacer(url), html)

    # Restore all new-link placeholders
    for i, link in enumerate(new_links):
        html = html.replace(f'__NEWLINK_{i}__', link)

    return html


def remove_double_links(html):
    """Clean up any accidentally nested <a> tags."""
    # Find <a href="..."><a href="...">text</a></a> and flatten
    html = re.sub(
        r'<a href="[^"]*">(<a href="[^"]*">[^<]*</a>)</a>',
        r'\1',
        html
    )
    return html


def skip_headings_and_ids(html):
    """Ensure we haven't linked text inside id attributes or heading tags."""
    # Remove any links that got inserted into id="..." attributes
    html = re.sub(r'id="[^"]*<a[^>]*>[^<]*</a>[^"]*"', lambda m: re.sub(r'</?a[^>]*>', '', m.group(0)), html)
    return html


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Split into head and body to only process body
    head_end = html.find('</head>')
    head = html[:head_end + 7]
    body = html[head_end + 7:]

    # Don't link inside <h2>, <h3>, <h4> tags (they contain the targets)
    # Strategy: temporarily replace heading content with placeholders
    headings = []
    def save_heading(m):
        headings.append(m.group(0))
        return f'__HEADING_{len(headings) - 1}__'

    body = re.sub(r'<h[234][^>]*>.*?</h[234]>', save_heading, body, flags=re.DOTALL)

    # Also protect existing <a> tags
    links = []
    def save_link(m):
        links.append(m.group(0))
        return f'__LINK_{len(links) - 1}__'

    body = re.sub(r'<a [^>]*>.*?</a>', save_link, body, flags=re.DOTALL)

    # Also protect id="..." attributes
    ids = []
    def save_id(m):
        ids.append(m.group(0))
        return f'__ID_{len(ids) - 1}__'

    body = re.sub(r'id="[^"]*"', save_id, body)

    # Now apply linking
    body = link_internal_refs(body)
    body = link_external_refs(body)

    # Restore protected content
    for i, id_val in enumerate(ids):
        body = body.replace(f'__ID_{i}__', id_val)

    for i, link in enumerate(links):
        body = body.replace(f'__LINK_{i}__', link)

    for i, heading in enumerate(headings):
        body = body.replace(f'__HEADING_{i}__', heading)

    # Clean up any double-linking
    body = remove_double_links(body)

    result = head + body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

    # Count links added
    original_links = len(re.findall(r'<a ', html))
    new_links = len(re.findall(r'<a ', result))
    print(f"{filepath}: {new_links - original_links} links added ({original_links} -> {new_links})")


if __name__ == '__main__':
    for f in sys.argv[1:]:
        process_file(f)
