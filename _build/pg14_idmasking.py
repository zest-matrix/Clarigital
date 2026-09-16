#!/usr/bin/env python3
# Session 106 — PRODUCT GUIDE 14: Government ID masking and the Aadhaar Data Vault.
# First guide about DESTROYING data rather than collecting it.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one thing: making sure a government identity number stops
existing in your systems once you no longer need it, while the document it came from remains usable.</p>
<p><strong>Every other product guide on this site is about collecting something. This one is about
getting rid of it.</strong> That inversion changes the whole shape of the work &mdash; there is no
conversion funnel to optimise and no revenue attached, and the failure is invisible until somebody
looks.</p>
''' + warn("<strong>The product almost everyone builds is the visible 10% of the obligation.</strong> Teams hear &ldquo;Aadhaar masking&rdquo; and build image redaction: detect the number on a scan, black out the first eight digits, store the masked copy. That part is real and required. It is also the easy part. <strong>The harder requirement is that the Aadhaar number must not sit in your business databases at all</strong> &mdash; it belongs in a separate encrypted vault, referenced everywhere else by a token. A team that ships beautiful redaction and keeps the number in a customer table has done the visible part and missed the obligation.")

g_what = '''
<p>Two separate duties, frequently confused, with different sources and different failure modes:</p>
<table>
<tr><th></th><th>Masking</th><th>Vaulting</th></tr>
<tr><td><strong>What it is</strong></td><td>Obscuring the number on the <em>document image</em></td><td>Keeping the number out of your <em>databases</em></td></tr>
<tr><td><strong>Who requires it</strong></td><td><strong>RBI, IRDAI, SEBI</strong> for their regulated entities</td><td><strong>UIDAI</strong>, for anyone storing Aadhaar numbers</td></tr>
<tr><td><strong>What good looks like</strong></td><td>First eight digits <strong>and the QR code</strong> obscured</td><td>Number only in the vault; a <strong>Reference Key</strong> everywhere else</td></tr>
<tr><td><strong>How it fails</strong></td><td>Visibly &mdash; a reviewer sees the number</td><td><strong>Invisibly</strong> &mdash; until an audit or a breach</td></tr>
</table>
''' + note("<strong>The regulatory spine, and it is four bodies rather than one.</strong> <strong>UIDAI</strong>'s 2018 circular established that a masked Aadhaar is valid proof of identity. <strong>RBI</strong>'s amendment of <strong>29 May 2019</strong> to the KYC Master Direction requires regulated entities to redact the number where authentication is not required. <strong>IRDAI</strong> followed on <strong>29 January 2019</strong> and <strong>SEBI</strong> on <strong>24 April 2020</strong>. Underneath all of them sits the <strong>Aadhaar Act, 2016</strong> and the Supreme Court's 2018 judgment, which upheld the scheme subject to conditions on how the number may be held and used.") + '''
<p><strong>What this is not:</strong></p>
<ul>
<li><strong>Not an OCR project.</strong> Detection is a solved problem and the least of your
difficulties. Steps 4 to 8 are the work.</li>
<li><strong>Not only about Aadhaar.</strong> PAN, passport, voter ID and driving licence numbers are
personal data under the DPDP framework even without a dedicated vault rule.</li>
<li><strong>Not finished when the pipeline ships.</strong> The number is already in places nobody
listed. Step 6.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Find out what you hold</strong></td><td>Before designing anything. It is more places than the list says.</td></tr>
<tr><td>2</td><td><strong>Decide what you may keep</strong></td><td>The cheapest number to protect is one you never stored.</td></tr>
<tr><td>3</td><td><strong>Mask at capture</strong></td><td>First eight digits <strong>and the QR</strong>. The visible layer.</td></tr>
<tr><td>4</td><td><strong>Tokenise</strong></td><td><strong>The Reference Key. The step that is actually the product.</strong></td></tr>
<tr><td>5</td><td><strong>Build the vault</strong></td><td>Separate, encrypted, isolated, keys in an HSM.</td></tr>
<tr><td>6</td><td><strong>Purge where it leaked</strong></td><td>Logs, tickets, backups, video frames. The hard one.</td></tr>
<tr><td>7</td><td><strong>Serve it back</strong></td><td>For the few cases that genuinely need the real number.</td></tr>
<tr><td>8</td><td><strong>Prove it</strong></td><td>Access logs, retention, and evidence that survives a question.</td></tr>
</table>
''' + note("<strong>Steps 1, 6 and 8 are the ones that get skipped, and they are the ones that decide whether any of this worked.</strong> Steps 3 to 5 are the part that looks like a project and a vendor will sell you all three. <strong>Nobody sells you the discovery or the purge</strong>, because both are unglamorous and specific to your estate.")

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Find out where the number already is</h3>
<p>Start with an inventory, not an architecture. In every organisation that has been operating for
more than a year, the answer is longer than the application diagram suggests.</p>
<p>The places to look, in roughly the order teams are surprised by them:</p>
<ul>
<li><strong>The obvious ones:</strong> the customer table, the KYC document store, the onboarding
database.</li>
<li><strong>Application logs.</strong> A request body logged at debug level, an error trace with the
payload attached, a third-party logging service that has been retaining it for two years.</li>
<li><strong>The support system.</strong> Customers send their Aadhaar as an attachment; agents paste
numbers into ticket notes. This is almost always the largest uncontrolled store.</li>
<li><strong>Email.</strong> Documents sent to an operations mailbox, sitting in an archive.</li>
<li><strong>Analytics and monitoring</strong>, where a form field was captured as an event property.</li>
<li><strong>Backups and data warehouses</strong>, which hold every version of the table you are about
to clean.</li>
<li><strong>Video KYC recordings</strong>, where the customer held the card up to the camera.</li>
</ul>
''' + warn("<strong>The video case is the one that is most often missed and hardest to fix.</strong> A V-CIP session where the customer displays their Aadhaar produces a stored recording with the number legible in individual frames. <strong>Redaction obligations follow the number, not the file format</strong> &mdash; a number visible in a stored frame is a stored Aadhaar number. Frame-level detection and redaction on video is materially harder than on a scan, and the recordings usually have a long mandated retention. If you run Video KYC, put this on the plan at the start rather than discovering it in an audit.") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; Decide what you are entitled to keep</h3>
<p>The cheapest number to protect is the one you never stored. Before building a vault, work through
what you actually need.</p>
<p><strong>Do you need the number, or do you need the verification?</strong> For most onboarding
journeys the answer is the second: you need to know the identity was verified, not to retain the
identifier afterwards. Where that is true, <strong>store the verification result and the reference,
and discard the number entirely.</strong></p>
<p><strong>Do you need the document image, or the extracted fields?</strong> Name, date of birth and
address often suffice, in which case the image can go.</p>
<p><strong>What is your retention period, and who set it?</strong> &ldquo;Indefinite&rdquo; is a
decision, usually one nobody made. Under the DPDP framework personal data is not to be kept beyond
the purpose it was collected for, and <strong>there is no legitimate-interest basis in India</strong>
to fall back on.</p>
'''

code_mask = code('Python — steps 3 to 5, mask, tokenise, vault', r'''from dataclasses import dataclass

# STEP 3. MASK AT CAPTURE. THE VISIBLE LAYER.
# The requirement is specific: the first EIGHT digits, and the QR code, which
# encodes the full number and is the part teams forget. Last four stay
# visible; name, date of birth, gender and address stay visible.

def mask_document(image):
    regions = detect(image)                    # number, QR, and any repeats
    assert regions["qr"], "QR not located — do not store this image"
    out = image
    for r in regions["number"]:                # a card may show it twice
        out = redact(out, r, keep_last=4)
    out = redact(out, regions["qr"], keep_last=0)
    verify = extract_digits(out)               # read your own output back
    assert not verify["full_number_visible"], "masking did not take"
    return out

# STEP 4. TOKENISE. THIS IS THE ACTUAL PRODUCT.
# UIDAI Circular No. 14 of 2025: every business system stores a REFERENCE KEY
# instead of the number. The actual number must not be stored in any business
# database other than the Aadhaar Data Vault.
#
# The reference key must not computationally permit working back to the
# number. So: a random token, not a hash of the number, and not a derivation
# from it -- a hash is guessable across a 12-digit space.

@dataclass
class Reference:
    key: str            # random, opaque, stored everywhere
    created_at: str

def tokenise(aadhaar, vault):
    assert len(aadhaar) == 12 and aadhaar.isdigit()
    existing = vault.lookup_by_number(aadhaar)     # inside the vault only
    if existing:
        return existing
    ref = Reference(key=random_token(32), created_at=now_ist())
    vault.store(aadhaar=aadhaar, reference=ref)    # the ONLY place both meet
    return ref

# Everything downstream stores ref.key. Nothing downstream stores aadhaar.
def create_customer(db, profile, ref):
    assert "aadhaar" not in profile, "number reached the business layer"
    return db.insert({**profile, "id_reference": ref.key})

# STEP 5. THE VAULT.
VAULT_REQUIREMENTS = {
    "separate_store": True,        # not a column on an existing table
    "single_logical_instance": True,
    "encryption": "AES-256_or_higher",
    "keys_in_hsm": True,           # and the HSM is not shared with anyone else
    "network": "restricted_zone_isolated_from_other_internal_zones",
    "access": "internal_systems_only",
    "ha_dr": True,
    "access_logged": True,
}

# WHAT TO CHECK
# [ ] the QR is masked, not just the digits. It encodes the whole number
# [ ] read your own masked output back and assert the number is gone. A
#     redaction that draws a box without removing the underlying pixels is
#     not a redaction, and some libraries do exactly that
# [ ] the reference key is RANDOM. A hash of a 12-digit number is brute
#     forceable in seconds
# [ ] assert at the boundary that no business write contains the number.
#     Make it fail the request, not log a warning
# [ ] the HSM is not shared with another legal entity. Where a group shares
#     one, each entity needs logical isolation and its own crypto keys
# [ ] the vault is one logical instance, not one per service
''')

i_step345 = '''
<h3 id="s-indigo-s3">Steps 3 to 5 &mdash; Mask, tokenise, vault</h3>
''' + code_mask + '''
<p><strong>THE finding, and it is the reason this page exists:</strong> <strong>masking the image is
the visible tenth of the obligation. The requirement is that the number stops existing in your
business systems.</strong></p>
<p>UIDAI's framework has been in place since a first circular in <strong>July 2017</strong> and was
substantially revised by <strong>Circular No. 14 of 2025, dated 18 July 2025</strong>, with updated
FAQs on <strong>3 November 2025</strong>. Its central instruction is unambiguous: <strong>all systems
requiring storage of Aadhaar numbers should maintain only the reference key, and the actual number
should not be stored in any business database other than the Aadhaar Data Vault.</strong></p>
<p>Alongside it: the vault as a <strong>single logical instance</strong> per entity, encryption at
<strong>AES-256 or higher</strong>, encryption keys held in an <strong>HSM that is not shared with
any other legal entity</strong>, the whole thing in a <strong>restricted network zone isolated from
other internal zones</strong>, accessible through internal systems only, with high availability and
disaster recovery.</p>
''' + note("<strong>A group structure does not let you share the HSM freely.</strong> Where a sub-entity uses its parent's HSM, the configuration must provide <strong>logical isolation and dedicated crypto keys for each regulated entity</strong>, and the parent must not be able to read the sub-entity's vault. This is the detail most often got wrong in a shared-services model, because sharing infrastructure is exactly what a shared-services model is for.") + '''
<p>Note also what belongs <em>in</em> the vault: not only the number, but the <strong>e-KYC XML, the
Aadhaar PDF returned in an e-KYC response, and the related demographic data</strong>. A team that
vaults the number and leaves the e-KYC response in object storage has moved the problem rather than
solved it.</p>
'''

code_purge = code('Python — steps 6 to 8, purge, serve back, prove', r'''# STEP 6. PURGE WHERE IT ALREADY LEAKED. THE UNGLAMOROUS ONE.
# A clean pipeline from today does nothing about the last three years.

PURGE_TARGETS = [
    "application_logs", "error_traces", "third_party_log_retention",
    "support_tickets", "ticket_attachments", "operations_mailbox",
    "analytics_event_properties", "data_warehouse", "backups",
    "vcip_recordings", "developer_laptops_and_exports",
]

def purge_plan(target, scanner):
    hits = scanner.find_id_numbers(target)      # pattern + checksum, not regex alone
    return {
        "target": target,
        "found": len(hits),
        # Deleting a support ticket may break an audit trail you are separately
        # required to keep. Redact IN PLACE where the record must survive.
        "action": "redact_in_place" if target in ("support_tickets", "vcip_recordings")
                  else "delete",
        "backups_note": "a purge that skips backups restores the problem on the "
                        "next restore -- schedule it against the retention cycle",
    }

# STEP 7. SERVE IT BACK, FOR THE FEW CASES THAT NEED IT.
def resolve(reference_key, purpose, actor, vault):
    # Every de-tokenisation is an event with a reason and a name attached.
    assert purpose in ("regulatory_filing", "authentication", "lawful_request")
    entry = vault.read(reference_key, actor=actor, purpose=purpose)
    vault.log_access(reference_key, actor, purpose, at=now_ist())
    return entry            # held in memory, never written downstream

# STEP 8. PROVE IT.
def evidence(period, vault, scanner):
    return {
        "access_log": vault.accesses(period),        # who, what, why, when
        "unresolved_scan_hits": scanner.sweep(PURGE_TARGETS),
        "retention_expiries_actioned": vault.expired_and_deleted(period),
        "hsm_key_rotation": vault.key_events(period),
        "masking_sample_reverified": sample_and_recheck(period, n=50),
    }

# WHAT TO CHECK
# [ ] run the scanner against your OWN systems on a schedule, not once. New
#     leaks appear with every feature that logs a request body
# [ ] validate with the checksum, not the pattern. Any 12 digits matches a
#     naive regex, and a phone number plus two digits is not an Aadhaar
# [ ] purge backups against the retention cycle, or the next restore undoes
#     the work
# [ ] every de-tokenisation is logged with an actor and a purpose. An access
#     log with no purpose column cannot answer the question that gets asked
# [ ] re-verify a sample of masked documents periodically. Pipelines drift,
#     and a model update can change what gets detected
# [ ] timestamp everything in IST. An access log in UTC is read by a
#     regulator in IST, and a five-and-a-half hour offset on an access
#     timestamp is exactly the detail that turns a routine question awkward
''')

i_step678 = '''
<h3 id="s-indigo-s6">Steps 6 to 8 &mdash; Purge, serve back, prove</h3>
''' + code_purge + '''
<p><strong>The second finding, and the one that costs the most:</strong> <strong>a clean pipeline
from today does nothing about the last three years.</strong> The number is already in your logs, your
support tickets, your operations mailbox, your warehouse and your backups, and it got there through
ordinary engineering decisions that nobody would call a mistake at the time.</p>
<p>Two details that decide whether the purge works. <strong>Validate with the checksum rather than
the pattern</strong> &mdash; a naive twelve-digit regex matches phone numbers, order ids and
timestamps, and a scan that returns thousands of false positives is a scan nobody finishes. And
<strong>schedule the backup purge against the retention cycle</strong>, because a restore from an
unpurged backup puts everything back.</p>
''' + warn("<strong>Redact in place where the record has to survive.</strong> Deleting a support ticket to remove an Aadhaar number can breach a separate obligation to retain the interaction. The same applies to V-CIP recordings, which carry their own mandated retention. <strong>These two duties &mdash; keep the record, remove the number &mdash; are simultaneous rather than alternative</strong>, and a purge designed as deletion will be stopped by compliance halfway through.")

i_cost = registry("Government ID masking &mdash; what it costs", [
 ("Discovery", "direct",
  "The step nobody sells and nobody budgets. Scanning logs, tickets, mailboxes, warehouses and "
  "backups across your estate. <strong>Expect it to find more than the architecture diagram "
  "suggests</strong>, and expect the support system to be the largest store."),
 ("Masking", "direct",
  "Per document, or a licence. <strong>The cheapest line on this list and the one that gets the "
  "attention</strong>, because it is the part that demonstrates well."),
 ("The vault and the HSM", "direct",
  "A separate encrypted store, keys in a hardware security module <strong>not shared with any other "
  "legal entity</strong>, in an isolated network zone, with high availability and disaster recovery. "
  "This is real infrastructure with real running cost."),
 ("Retrofitting the application", "indirect",
  "<strong>Usually the largest line and never in the estimate.</strong> Every query, report, export "
  "and integration that currently reads the number has to be changed to read a reference key. On a "
  "system of any age this is months, not weeks."),
 ("The purge", "direct",
  "One-off across the historical estate, then a standing scheduled scan. Budget both; the second is "
  "the one that keeps it clean."),
 ("Video redaction", "direct",
  "<strong>If you run Video KYC, price this separately and early.</strong> Frame-level detection on "
  "recordings with long mandated retention is materially harder and more expensive than redacting a "
  "scan."),
 ("Getting it wrong", "indirect",
  "A KYC violation can attract penalties that accrue <strong>per day for as long as it continues</strong>, "
  "and Indian regulators have imposed penalties in the <strong>crores</strong> on banks and NBFCs for "
  "systematic KYC failures. Alongside that sits DPDP exposure reaching <strong>&#8377;250 crore</strong>."),
], "September 2026") + note("<strong>The number worth computing before anything else: how many systems currently read the identity number?</strong> That count is your retrofit cost, it is knowable in an afternoon, and it is almost always the figure that turns a three-month plan into a nine-month one. Everything else on this list is smaller and better understood.")

a_builds = '''
<h3 id="s-amber-week">Do not store it at all</h3>
<p><strong>Build:</strong> verify identity &rarr; keep the verification result and a reference &rarr;
discard the number and, where you can, the image.</p>
<p><strong>You get:</strong> the obligation reduced to almost nothing. <strong>This is the correct
answer far more often than it is chosen</strong>, and the reason it is not chosen is usually that
nobody asked whether the number was needed after onboarding.</p>

<h3 id="s-amber-proper">Mask and tokenise</h3>
<p><strong>Build:</strong> masking at capture including the QR &rarr; random reference key &rarr;
encrypted vault with HSM-held keys in an isolated zone &rarr; a boundary assertion that fails any
business write containing the number &rarr; a scheduled scan across logs, tickets and warehouse.</p>
<p><strong>Trade:</strong> real infrastructure and a real retrofit, against an obligation that is not
optional if you are regulated.</p>

<h3 id="s-amber-big">The full estate</h3>
<p><strong>Build:</strong> the above, plus the historical purge including backups, frame-level
redaction on V-CIP recordings, de-tokenisation logged with actor and purpose, retention expiry
actioned automatically, and periodic re-verification of masked output.</p>
<p><strong>It breaks when:</strong> the project is scoped as the pipeline and the estate is treated as
a later phase. <strong>The estate is the project</strong>; the pipeline is the part that stops it
getting worse.</p>
''' + note("If you take one thing from this page: <strong>assert at the boundary that no business write contains an identity number, and make it fail the request rather than log a warning.</strong> It is a few lines, it is the only control that holds as the system grows, and it turns an invisible failure into a visible one.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Digits masked, QR left intact</strong></td><td>The QR is not read as part of the number.</td><td>It encodes the whole number. Mask it.</td></tr>
<tr><td><strong>Redaction draws a box over the pixels</strong></td><td>Some libraries overlay rather than remove.</td><td>Read your own output back and assert.</td></tr>
<tr><td><strong>Reference key is a hash of the number</strong></td><td>It looks opaque.</td><td>A 12-digit space is brute forceable. Use a random token.</td></tr>
<tr><td><strong>Number still in the customer table</strong></td><td>Masking shipped; vaulting did not.</td><td>Reference key everywhere; number only in the vault.</td></tr>
<tr><td><strong>e-KYC XML left in object storage</strong></td><td>Only the number was treated as in scope.</td><td>XML, PDF and demographic data belong in the vault too.</td></tr>
<tr><td><strong>Number in application logs</strong></td><td>A request body logged at debug level.</td><td>Boundary assertion, plus a scheduled log scan.</td></tr>
<tr><td><strong>Support tickets full of numbers</strong></td><td>Customers attach documents; agents paste.</td><td>Redact in place. The record may have to survive.</td></tr>
<tr><td><strong>Purge undone by a restore</strong></td><td>Backups were out of scope.</td><td>Schedule against the retention cycle.</td></tr>
<tr><td><strong>V-CIP recordings show the card</strong></td><td>Redaction scoped to scans.</td><td>The obligation follows the number, not the format.</td></tr>
<tr><td><strong>Shared HSM across group entities</strong></td><td>Shared services is the point of shared services.</td><td>Logical isolation and dedicated keys per entity.</td></tr>
<tr><td><strong>Scanner returns thousands of false hits</strong></td><td>Twelve-digit regex with no checksum.</td><td>Validate with the checksum. Otherwise nobody finishes the scan.</td></tr>
<tr><td><strong>Access log with no purpose column</strong></td><td>Logged the read, not the reason.</td><td>Actor and purpose on every de-tokenisation.</td></tr>
</table>
'''

SRC=[('official','UIDAI Circular No. 14 of 2025 on the Aadhaar Data Vault, dated 18 July 2025','the requirement that all business systems store a Reference Key rather than the Aadhaar number, that the actual number not be stored in any business database other than the vault, the single logical instance per entity, AES-256 or higher encryption, keys held in an HSM, the restricted and isolated network zone, internal-systems-only access, and high availability and disaster recovery. Updated FAQs were published on 3 November 2025. This revises the original circular of 25 July 2017.','https://uidai.gov.in'),
 ('official','UIDAI guidance on masked Aadhaar','the 2018 position that a masked Aadhaar showing only the last four digits is valid proof of identity for KYC, and the requirement that the first eight digits and the QR code be obscured.','https://uidai.gov.in'),
 ('official','RBI Master Direction — Know Your Customer, as amended 29 May 2019','the requirement that regulated entities redact or black out the Aadhaar number where authentication of the number is not required, before the document is filed or stored.','https://www.rbi.org.in'),
 ('official','IRDAI circular of 29 January 2019 and SEBI circular of 24 April 2020','the parallel obligations extending masked-Aadhaar acceptance and redaction duties to insurers and their intermediaries, and to securities-market intermediaries.','https://irdai.gov.in'),
 ('official','Aadhaar (Targeted Delivery of Financial and other Subsidies, Benefits and Services) Act, 2016','the statutory basis for the scheme and the restrictions on holding, using and disclosing the Aadhaar number, as upheld with conditions by the Supreme Court in 2018.','https://www.indiacode.nic.in'),
 ('official','Digital Personal Data Protection Act, 2023 and the DPDP Rules, 2025','purpose limitation and storage limitation for identity numbers generally, the absence of a legitimate-interest basis, and penalties reaching ₹250 crore. Identity numbers other than Aadhaar — PAN, passport, voter ID, driving licence — are personal data under this framework even without a dedicated vault rule.','https://www.meity.gov.in'),
 ('industry','Legal commentary on the 2025 ADV circular','the practitioner reading of scope, of sub-entity use of a parent HSM with logical isolation and dedicated crypto keys, and of what must be held in the vault beyond the number itself — e-KYC XML, the Aadhaar PDF from an e-KYC response, and related demographic data. Interpretation, not the notified text.',''),
 ('industry','Reporting on KYC enforcement','penalties accruing per day for a continuing KYC violation, and enforcement actions in the crores against banks and NBFCs for systematic KYC failures. Directional; confirm any figure against the order before relying on it.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. The Aadhaar Data Vault circular was revised in July 2025 and its FAQs in '
 'November 2025 &mdash; verify the current text before designing to any provision here.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/products/video-kyc/" class="mod-card"><div class="mod-num">GUIDE 02</div><h3>Video KYC</h3><p>Where the recordings come from, and why the frames are in scope.</p></a>
<a href="/fintech-ai/products/document-ai/" class="mod-card"><div class="mod-num">GUIDE 01</div><h3>Document AI</h3><p>Extraction and classification — the pipeline this sits inside.</p></a>
<a href="/fintech-ai/identity-onboarding/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 01</div><h3>Identity &amp; Onboarding</h3><p>Every tool for identity work, what each costs, and three recommended builds.</p></a>
<a href="/fintech-ai/infrastructure/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 08</div><h3>Infrastructure</h3><p>Data residency, the three planes, and designing for reversibility.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Handling Aadhaar data is governed by the Aadhaar Act and by UIDAI circulars that have been revised repeatedly, most recently in 2025. Nothing here is legal advice. Have your vault design, your retention periods and your purge plan reviewed by qualified counsel, and work from the current circular text rather than from this page.")

lanes={'green':[("How to use this page",g_read),("Masking and vaulting are two different duties",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — what you hold, and what you may keep",i_step12),
           ("Steps 3 to 5 — mask, tokenise, vault",i_step345),
           ("Steps 6 to 8 — purge, serve back, prove",i_step678),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Government ID Masking: How to Build It"
META=("Build identity-number masking step by step: what the Aadhaar Data Vault actually requires, "
      "where the number has already leaked, and what breaks.")
LEAD=("A step-by-step guide to masking and vaulting government identity numbers in India. Eight "
      "stages, the options at each one, exactly how each step connects to the next, real costs, and "
      "what breaks. Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
MD=_re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')
for nm,lane in lanes.items():
    for t,c in lane:
        s=MD.findall(_re.sub(r'<[^>]+>',' ',c))
        assert not s, 'markdown in %s: %s'%(t,s[:3])
page(path="fintech-ai/products/id-masking",title=TITLE,meta=META,lead=LEAD,label="Product Guide 14",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/id-masking/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Need the number to stop '
  'existing in your systems? The eight steps, what the Aadhaar Data Vault actually requires, and where '
  'it has already leaked: <a href="/fintech-ai/products/id-masking/"><strong>Government ID Masking: How '
  'to Build It &rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('identity-onboarding', 'infrastructure'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/id-masking' in src:
        print('  = already linked from /' + mod + '/'); continue
    n = src.count(ANCHOR)
    assert n == 1, 'anchor appears ' + str(n) + ' times in ' + p
    i = src.find(ANCHOR); assert i != -1
    out = src[:i] + NOTE_BLOCK + src[i:]
    assert out.count('<div') == src.count('<div') + 1
    assert out.count('</div>') == src.count('</div>') + 1
    assert len(out) == len(src) + len(NOTE_BLOCK)
    _io.open(p, 'w', encoding='utf-8').write(out)
    print('  + linked from /' + mod + '/')
