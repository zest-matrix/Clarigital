#!/usr/bin/env python3
"""Session 63 — the sources pass, part 1: build sheets + product guides.

Design decisions:
  * A numbered block at the FOOT of the page, not inline footnotes. Inline
    markers wreck the reading flow of a page meant to be worked through.
  * Every entry is TYPED: Official / Vendor / Research / Industry. A reader
    can see at a glance which numbers are primary-sourced and which are
    industry reporting. Pretending everything is primary would be worse than
    citing nothing.
  * Each entry says WHAT IT SUPPORTS, not just what it is. A bare link list is
    decoration; "this is where the ₹1.51 lakh fee cap comes from" is a source.
  * Only sources actually used during the build are listed.
"""
import io, re, glob

CSS = """
.srcs{margin-top:10px;border-top:1px solid var(--border);padding-top:16px}
.srcs ol{list-style:none;counter-reset:s;padding:0;margin:0}
.srcs li{counter-increment:s;position:relative;padding:9px 0 9px 30px;border-bottom:1px solid var(--border);font-size:.82rem;line-height:1.6;color:var(--muted)}
.srcs li:last-child{border-bottom:0}
.srcs li::before{content:counter(s);position:absolute;left:0;top:10px;font-size:.68rem;font-weight:700;color:var(--faint);font-variant-numeric:tabular-nums}
.src-k{display:inline-block;font-size:.6rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;border-radius:100px;margin-right:7px;vertical-align:1px}
.src-official{background:rgba(20,184,166,.12);color:var(--teal);border:1px solid rgba(20,184,166,.3)}
.src-research{background:rgba(99,102,241,.12);color:var(--indigo);border:1px solid rgba(99,102,241,.3)}
.src-vendor{background:rgba(245,158,11,.12);color:var(--amber);border:1px solid rgba(245,158,11,.3)}
.src-industry{background:rgba(148,163,184,.1);color:var(--muted);border:1px solid var(--border2)}
.srcs strong{color:var(--fg);font-weight:600}
.srcs a{word-break:break-word}
"""

INTRO = ('<p>Every figure, rule and date on this page, and where to check it. '
         'Entries are typed so you can see which numbers are primary-sourced and which are '
         'industry reporting &mdash; they are not equivalent, and treating them as if they were '
         'is how a confident wrong number gets repeated.</p>')

def block(rows, verified):
    lis = ''.join(
        f'<li><span class="src-k src-{k}">{k}</span><strong>{name}</strong> &mdash; {what}'
        + (f' <a href="{url}" target="_blank" rel="noopener">{url.split("//")[-1].split("/")[0]}</a>' if url else '')
        + '</li>' for k, name, what, url in rows)
    return (f'<h2 id="sources">Sources</h2>{INTRO}'
            f'<div class="srcs"><ol>{lis}</ol>'
            f'<p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
            f'Checked {verified}. Pricing and draft regulation move; the date is part of the claim.</p></div>')

O, R, V, I = 'official', 'research', 'vendor', 'industry'

PAGES = {
 'fintech-ai/aml-compliance/build-sheet': ('September 2026', [
  (O,'OFSI penalty notice, Bank of Scotland','the &pound;160,000 penalty, the 24 payments totalling &pound;77,383.39, the eight aggravating factors, and the 20&ndash;24 February window in which &pound;75,000 of the &pound;76,000 arrived.','https://www.gov.uk/government/collections/enforcement-of-financial-sanctions'),
  (O,'OFAC Sanctions List Service','the free feeds, the four-file legacy series (SDN, ALT, ADD, SDN_COMMENTS) and OFAC&rsquo;s own warning about downloading only one.','https://ofac.treasury.gov/sanctions-list-service'),
  (O,'RBI Master Direction on KYC','Section 51 (UAPA), Section 52 (WMD Act) and the nodal-officer list in Section 54.','https://www.rbi.org.in'),
  (O,'MHA &mdash; UAPA designations and nodal officers','UAPA Schedules 1 and 4, and the contact list that must be treated as refreshable reference data.','https://www.mha.gov.in'),
  (O,'FIU-IND','FINGate 2.0 filing, the CTR / STR / CBWTR thresholds and deadlines, and the PMLA s.13 penalty range.','https://fiuindia.gov.in'),
  (R,'Allen &amp; Hatfield, FEDS 2025-092','the ~92% false-positive reduction, ~11% detection gain, the four-orders-of-magnitude latency penalty, and the cascade recommendation.','https://www.federalreserve.gov/econres/feds/'),
  (V,'OpenSanctions pricing and licensing','the &euro;0.10 per successful call, the logical-query billing model, and CC BY-NC 4.0 versus the commercial licence tiers.','https://www.opensanctions.org/licensing/'),
  (V,'Elastic License 2.0','the managed-service prohibition that rules Marble out for BaaS and PSP use.','https://www.elastic.co/licensing/elastic-license'),
  (I,'Screening vendor pricing','entry-tier and mid-tier figures, and the per-monitoring-scan unit. Compiled from vendor pages and third-party contract data; confirm the entity allowance in writing.',''),
 ]),
 'fintech-ai/payments-reconciliation/build-sheet': ('September 2026', [
  (O,'RBI (Regulation of Payment Aggregators) Directions, 2025','the PA-O / PA-P / PA-CB categories, net worth, escrow rules, the &#8377;25 lakh PA-CB cap, and the 15 September 2026 legacy-merchant CDD deadline.','https://www.rbi.org.in'),
  (O,'Payment and Settlement Systems Act, 2007','the statute the 2026 amendment Bill modifies to enable charges on digital transactions.','https://www.rbi.org.in'),
  (O,'NPCI','UPI volume and value, the dispute mechanism, and the third-party market-share cap timeline.','https://www.npci.org.in'),
  (O,'RBI Ombudsman Scheme (RB-IOS)','the award limits and the complaint route through the CMS portal.','https://cms.rbi.org.in'),
  (I,'Taxation and Other Laws (Amendment) Bill, 2026 &mdash; reporting','the reported 0.25&ndash;0.4% range, the large-merchant turnover threshold and the &#8377;2,000 ticket floor. <strong>Rates are not notified.</strong> Treat as direction, not figures.',''),
  (V,'Razorpay, Cashfree and PayU published pricing','the ~2% domestic rate, ~3% premium and international, and settlement timing options.','https://razorpay.com/pricing/'),
  (I,'Legacy gateway pricing','the 1.6&ndash;1.8% headline plus setup and annual maintenance. Vendor-published and third-party compiled.',''),
 ]),
 'fintech-ai/customer-operations/build-sheet': ('September 2026', [
  (O,'WhatsApp Business Platform pricing','the India per-message rates effective 1 July 2026 and the 1 October 2026 change to service-message charging.','https://developers.facebook.com/docs/whatsapp/pricing'),
  (O,'RBI directions on recovery agents and responsible conduct','the 08:00&ndash;19:00 contact window covering digital channels, recording and retention, and the prohibition on remote disabling.','https://www.rbi.org.in'),
  (O,'RBI Ombudsman Scheme (RB-IOS) 2026','the escalation path, acknowledgement and resolution timelines, and award limits.','https://cms.rbi.org.in'),
  (V,'Intercom Fin pricing','the $0.99 per-outcome rate, the 50-outcome minimum and the no-seats model.','https://fin.ai/pricing/'),
  (V,'Zendesk AI agent pricing','the $2.00 per automated resolution rate and the January 2026 overage terms.','https://www.zendesk.com/pricing/'),
  (I,'Enterprise agent contract data','Sierra, Decagon and Ada ranges, implementation costs and deployment timelines. Third-party compiled &mdash; none of these vendors publishes a rate card.',''),
  (I,'Indian voice AI pricing','the &#8377;2&ndash;12/min range, the 2&ndash;4&times; effective multiplier, connect rates and the telecaller benchmark. Industry reporting; verify against your own pilot.',''),
 ]),
 'fintech-ai/wealth-advisory/build-sheet': ('September 2026', [
  (O,'SEBI (Investment Advisers) Regulations and amendments','the deposit-based requirement replacing net worth, the 300-client / &#8377;3 crore corporatisation trigger, the any-discipline graduate qualification, and the part-time IA category.','https://www.sebi.gov.in'),
  (O,'SEBI guidelines for investment advisers, January 2025','the &#8377;1.51 lakh annual fee cap, the AUA and fixed-fee modes, and the prohibition on trading calls.','https://www.sebi.gov.in'),
  (O,'SEBI circular on AI/ML use by intermediaries','responsibility resting solely with the IA/RA irrespective of scale of AI usage, and the disclosure obligation.','https://www.sebi.gov.in'),
  (O,'BSE &mdash; Investment Adviser Administration and Supervision Body','the IAASB function, appointed July 2024 for five years.','https://www.bseasl.com'),
  (O,'AMFI','the daily NAV feed for every Indian scheme.','https://www.amfiindia.com'),
  (V,'Kite Connect pricing','the free Personal tier without market data, and the &#8377;500/month paid tier including live and historical data.','https://kite.trade/'),
  (I,'SEBI enforcement reporting','the December 2025 impoundment order cited as the unregistered-advisory example.',''),
 ]),
 'fintech-ai/infrastructure/build-sheet': ('September 2026', [
  (O,'RBI payment data storage direction','the requirement that end-to-end payment data be stored only in India, and the return-and-delete window for offshore processing.','https://www.rbi.org.in'),
  (O,'Digital Personal Data Protection Act, 2023','consent, purpose limitation and breach obligations for personal data generally.','https://www.meity.gov.in'),
  (O,'IndiaAI Mission','the subsidised compute programme and empanelled GPU capacity.','https://indiaai.gov.in'),
  (V,'Model provider pricing pages','the three-tier structure and the specific per-million-token rates. <strong>These move faster than anything else on the site</strong> &mdash; one provider cut a model 80% in a day during 2026.',''),
  (I,'Indian GPU cloud pricing','H100, L40S and L4 hourly rates, reserved and spot, and the hyperscaler comparison. Compiled from provider pages and third-party comparisons.',''),
  (I,'Benchmark and price comparisons','the observation that five models sit within 0.4 points on one coding benchmark while output prices span tenfold.',''),
 ]),
 'fintech-ai/governance/build-sheet': ('September 2026', [
  (O,'RBI draft Guidance on Regulatory Principles for Model Risk Management, 2026','Press Release 2026-2027/528, 24 June 2026. The broadened definition of &ldquo;model&rdquo;, the 11 RE categories, three lines of defence, the inventory prohibition on unlisted models, and the kill-switch requirement. <strong>Draft.</strong>','https://www.rbi.org.in'),
  (O,'RBI FREE-AI committee report, 13 August 2025','the seven sutras, 26 recommendations and six pillars.','https://www.rbi.org.in'),
  (O,'EU AI Act (Regulation 2024/1689)','the risk tiers, Annex III high-risk classification of credit scoring, and the fine bands.','https://eur-lex.europa.eu'),
  (O,'NIST AI Risk Management Framework','the Govern / Map / Measure / Manage structure.','https://www.nist.gov/itl/ai-risk-management-framework'),
  (O,'ISO/IEC 42001','the AI management system standard and its relationship to ISO/IEC 27001.','https://www.iso.org/standard/81230.html'),
  (O,'Federal Reserve SR 11-7','the supervisory articulation of model validation that most global framing descends from.','https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm'),
  (I,'EU Digital Omnibus reporting','the 7 May 2026 provisional agreement deferring Annex III to 2 December 2027. <strong>Pending ratification</strong> &mdash; the original date stands until adoption.',''),
  (I,'ISO 42001 certification cost and timeline','audit fees, all-in year-one ranges and the ISO 27001 leverage. Compiled from certification bodies and consultancies; scope drives the number.',''),
 ]),
 'fintech-ai/products/document-ai': ('September 2026', [
  (V,'AWS Textract pricing','plain OCR, AnalyzeID, tables, forms and queries, and the high-volume tiering.','https://aws.amazon.com/textract/pricing/'),
  (V,'Azure AI Document Intelligence pricing','prebuilt and custom extraction rates, and the volume tiers.','https://azure.microsoft.com/pricing/details/ai-document-intelligence/'),
  (V,'Google Document AI pricing','processor rates, the per-hour deployed custom processor charge, and per-page billing on multi-page files.','https://cloud.google.com/document-ai/pricing'),
  (O,'DigiLocker','the issued-document route that skips most of the pipeline for supported documents.','https://www.digilocker.gov.in'),
  (O,'Income Tax Department &mdash; PAN','the PAN format used in the validation step.','https://www.incometax.gov.in'),
  (I,'Open-source OCR projects','PaddleOCR, docTR and Tesseract, and the licence check required on any model pulled with them.',''),
 ]),
}

# pages whose sources were already established in earlier build sheets
PAGES['fintech-ai/identity-onboarding/build-sheet'] = ('May 2026', [
  (V,'AWS Textract pricing','the ~$1.50 per 1,000 plain OCR rate and the AnalyzeID band.','https://aws.amazon.com/textract/pricing/'),
  (V,'Azure AI Document Intelligence pricing','prebuilt and custom model rates and the volume tiering.','https://azure.microsoft.com/pricing/details/ai-document-intelligence/'),
  (O,'UIDAI','Aadhaar verification routes and the checksum used in validation.','https://uidai.gov.in'),
  (O,'RBI Master Direction on KYC','V-CIP requirements and the record-keeping obligations.','https://www.rbi.org.in'),
  (I,'Open-source OCR licensing','the research-only restrictions that apply to some models distributed with otherwise permissive tooling.',''),
])
PAGES['fintech-ai/credit-underwriting/build-sheet'] = ('May 2026', [
  (O,'RBI Digital Lending Directions','the regulated-entity obligations, disclosure requirements and the LSP relationship.','https://www.rbi.org.in'),
  (O,'Account Aggregator framework','the consent architecture for fetching financial data.','https://sahamati.org.in'),
  (O,'Credit Information Companies (Regulation) Act','the bureau reporting and dispute obligations.','https://www.rbi.org.in'),
  (I,'Bureau and alternative data pricing','per-pull costs and alternative data vendor ranges. Compiled; contracts vary widely by volume.',''),
])
PAGES['fintech-ai/fraud-risk/build-sheet'] = ('May 2026', [
  (O,'RBI directions on digital payment security','the authentication and customer liability framework.','https://www.rbi.org.in'),
  (O,'NPCI','UPI dispute resolution and the chargeback mechanism.','https://www.npci.org.in'),
  (V,'Device intelligence and fraud vendor pricing','per-check and per-session rates.',''),
  (I,'Mule account and fraud typology reporting','the behavioural signals described in the detection section.',''),
])

built = 0
for path, (verified, rows) in PAGES.items():
    f = f'{path}/index.html'
    h = io.open(f, encoding='utf-8').read()
    if 'id="sources"' in h:
        continue
    if '.srcs{' not in h:
        h = h.replace('</style>', CSS + '</style>', 1)
    blk = block(rows, verified)
    # insert at the END of the final amber lane-section, before it closes
    m = list(re.finditer(r'<div class="lane-section" data-lane="amber">', h))
    assert m, f'{f}: no amber lane'
    start = m[-1].start(); d = 0; end = None
    for t in re.finditer(r'<div\b|</div>', h[start:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0:
            end = start + t.start(); break
    assert end, f'{f}: amber lane unbalanced'
    h = h[:end] + blk + h[end:]
    b = re.sub(r'<script.*?</script>', '', h[h.find('<body'):], flags=re.S)
    assert b.count('<div') == b.count('</div>'), f'{f}: div'
    assert b.count('<a ') == b.count('</a>'), f'{f}: a'
    assert h.count('</html>') == 1
    io.open(f, 'w', encoding='utf-8').write(h)
    built += 1
    print(f"  ✅ {path}  ({len(rows)} sources, checked {verified})")

print(f"\nsources block added to {built} pages")
