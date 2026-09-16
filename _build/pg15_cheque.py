#!/usr/bin/env python3
# Session 107 — PRODUCT GUIDE 15: Cheque reading and CTS.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one thing: turning a paper cheque into structured data a
banking system can act on, inside the rules of India's <strong>Cheque Truncation System</strong>.</p>
<p>Cheques are widely assumed to be dying. RBI still classifies paper clearing as a
<strong>System-Wide Important Payment System</strong>, which is the same category as the rails you
would never call obsolete. The volumes are falling and the values are not.</p>
''' + warn("<strong>The clock changed eleven months ago and most published guidance predates it.</strong> RBI circular <strong>RBI/2025-26/73 of 13 August 2025</strong> introduced <strong>Continuous Clearing and Settlement on Realisation</strong> in CTS with effect from <strong>4 October 2025</strong>. Cheques presented during the day now settle in hourly cycles with realisation by the evening of the same working day, replacing the two batch sessions that had governed cheque clearing for decades. <strong>Anything you read that describes a next-working-day cycle is describing the old system.</strong>")

g_what = '''
<p>The first thing to be precise about: <strong>you are not reading a photograph of a cheque.</strong>
CTS defines exactly what a cheque image is, and a pipeline built for arbitrary document photos is
solving a different problem.</p>
<table>
<tr><th>Image view</th><th>Specification</th><th>What it is for</th></tr>
<tr><td><strong>Front, greyscale</strong></td><td>Minimum <strong>100 DPI</strong>, JFIF/JPEG, <strong>8 bits per pixel</strong> (256 levels)</td><td>Handwriting &mdash; the amount, the payee, the signature</td></tr>
<tr><td><strong>Front, black and white</strong></td><td>Minimum <strong>200 DPI</strong>, TIFF, CCITT G4</td><td>Contrast, archival, machine reading</td></tr>
<tr><td><strong>Rear, black and white</strong></td><td>Minimum <strong>200 DPI</strong>, TIFF, CCITT G4</td><td>Endorsements and stamps</td></tr>
</table>
''' + note("<strong>The image is signed, and it is signed at the point of capture.</strong> It is mandatory for the presenting bank to digitally sign the image and data <strong>from the point of origin</strong>, and image and data remain secured by PKI through the whole cycle &mdash; capture system, presenting bank, clearing house, drawee bank. The system is built to be compliant with the <strong>IT Act, 2000</strong>. <strong>A pipeline that re-encodes, crops or enhances an image after capture breaks the signature</strong>, and therefore breaks the instrument. Any enhancement you do for your own reading happens on a copy.") + '''
<p><strong>Who you are changes the whole build:</strong></p>
<table>
<tr><th>You are</th><th>Your problem</th></tr>
<tr><td><strong>The presenting bank</strong></td><td>Capture, sign, extract, present into clearing. The full build.</td></tr>
<tr><td><strong>The drawee bank</strong></td><td>Verify against the account, match Positive Pay, pay or return &mdash; <strong>within the hour</strong>.</td></tr>
<tr><td><strong>A corporate depositor</strong></td><td>Reconciling what you banked against what cleared. No CTS integration at all.</td></tr>
<tr><td><strong>A vendor</strong></td><td>You sell into one of the first two. Their constraints are your specification.</td></tr>
</table>
<p><strong>What this is not:</strong></p>
<ul>
<li><strong>Not an OCR benchmark.</strong> Accuracy on a public handwriting dataset predicts very
little here. Step 5.</li>
<li><strong>Not a legacy project.</strong> The clearing cycle was rebuilt in 2025.</li>
<li><strong>Not finished at extraction.</strong> The extraction has to agree with something the drawer
already declared. Step 6.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Establish which side you are on</strong></td><td>Presenting, drawee, depositor or vendor.</td></tr>
<tr><td>2</td><td><strong>Capture the image triple</strong></td><td>To specification, signed at origin.</td></tr>
<tr><td>3</td><td><strong>Read the MICR band</strong></td><td>The easy, reliable, machine-printed part.</td></tr>
<tr><td>4</td><td><strong>Read CAR and LAR</strong></td><td>Amount in figures, amount in words. Handwritten.</td></tr>
<tr><td>5</td><td><strong>Reconcile the two</strong></td><td><strong>The law already decided which one wins.</strong></td></tr>
<tr><td>6</td><td><strong>Match Positive Pay</strong></td><td>Against what the drawer declared in advance.</td></tr>
<tr><td>7</td><td><strong>Present, and watch the clock</strong></td><td>Hourly cycles, same-day realisation.</td></tr>
<tr><td>8</td><td><strong>Handle returns</strong></td><td>Reasons, timelines, and the customer.</td></tr>
</table>
''' + note("<strong>Steps 5, 6 and 7 are where this differs from every other document-AI build</strong>, and they are the three that a vendor demonstration skips. Steps 2 to 4 are the part that looks like the product. <strong>An extraction engine that is excellent at 4 and silent on 5 and 6 has automated the easy half.</strong>")

i_step123 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Which side are you on?</h3>
<p>Answer this before anything else, because the three builds share almost no code.</p>
<p>The <strong>presenting bank</strong> captures, signs and presents; its risk is a bad capture
entering clearing. The <strong>drawee bank</strong> receives an image and must decide to pay or
return; its risk is paying something it should have stopped, and its constraint is now time. A
<strong>corporate depositor</strong> has no CTS integration at all and a genuine reconciliation
problem: what was banked, what cleared, what bounced, and which invoice each one settles.</p>
<p><strong>The corporate case is the largest addressable one and the least discussed</strong>, because
it needs no bank integration and no clearing membership &mdash; it is an internal reconciliation
product that happens to start with a cheque image.</p>

<h3 id="s-indigo-s2">Step 2 &mdash; Capture</h3>
<p>Two rules that override anything a scanner vendor tells you. <strong>Capture to the CTS
specification, not to what your model prefers.</strong> And <strong>sign at origin, then never touch
the original again</strong> &mdash; every enhancement, deskew, crop or contrast adjustment happens on
a working copy.</p>
<p>What ruins a capture, in order of frequency: a rubber stamp overlapping the date, payee, amount or
signature; light-coloured ink; alterations, which CTS does not accept at all except for date
validation; and a cheque that is not CTS-2010 compliant, which has been out of clearing since
<strong>31 December 2018</strong>.</p>

<h3 id="s-indigo-s3">Step 3 &mdash; The MICR band</h3>
<p>The MICR line is machine-printed in magnetic ink to a fixed specification, and it is the only field
on the cheque you should expect near-perfect accuracy on. It carries the cheque number, the MICR code
identifying the branch, the account number and the transaction code.</p>
''' + note("<strong>Read the MICR band magnetically where you can, optically only as a fallback, and reconcile the two.</strong> Magnetic reading is immune to the things that defeat vision &mdash; a stamp across the band, a fold, a photocopy &mdash; and a disagreement between the magnetic and optical reads is one of the cheapest fraud signals available. <strong>It is also the only field where a mismatch means something unambiguous</strong>, which is why it is worth the extra hardware.")

code_read = code('Python — steps 4 to 6, read the amounts, reconcile them, match Positive Pay', r'''from decimal import Decimal

# STEP 4. TWO AMOUNTS, BOTH HANDWRITTEN, ON THE SAME CHEQUE.
#   CAR — Courtesy Amount Recognition — the amount in FIGURES
#   LAR — Legal Amount Recognition   — the amount in WORDS
# Read them independently. Never derive one from the other: an engine that
# parses the figures and "confirms" the words has one reading and a
# rationalisation, which is exactly the check you needed.

def read_amounts(grey_image):
    car = read_car(grey_image)      # {"value": Decimal, "confidence": float}
    lar = read_lar(grey_image)      # {"value": Decimal, "confidence": float}
    assert car["source_region"] != lar["source_region"], "same region read twice"
    return car, lar

# STEP 5. WHEN THEY DISAGREE. THE LAW ALREADY DECIDED THIS.
# Negotiable Instruments Act, 1881, section 18: where the amount is stated
# differently in figures and in words, THE AMOUNT IN WORDS is the amount
# ordered to be paid.
#
# So the words are not a check on the figures. The words ARE the amount, and
# the figures are the check. Most pipelines are built the other way round
# because figures are easier to read.

def resolve_amount(car, lar, policy):
    if car["value"] == lar["value"]:
        return {"amount": car["value"], "route": "auto", "agreed": True}
    # A disagreement is not an error to resolve with a confidence score.
    # It is a legal question with an answer, and a human should see it.
    return {
        "amount": lar["value"],          # section 18: words govern
        "route": "manual_review",        # do not auto-pay a disagreement
        "agreed": False,
        "car": car["value"], "lar": lar["value"],
        "why": "figures and words differ; words govern, review before paying",
    }

# Confidence thresholds are a business decision, not a model setting.
def route(car, lar, policy):
    if min(car["confidence"], lar["confidence"]) < policy["min_confidence"]:
        return "manual_review"
    if car["value"] >= policy["always_review_above"]:
        return "manual_review"           # value, not confidence
    return "auto"

# STEP 6. POSITIVE PAY. THE DRAWER ALREADY TOLD THE BANK WHAT THIS SAYS.
# For cheques of Rs 50,000 and above the issuer submits the date, the payee
# and the amount to their bank in advance. CTS cross-checks the presented
# cheque against that declaration and flags any discrepancy to both banks.

def positive_pay_check(extracted, declared):
    if declared is None:
        return {"status": "no_declaration", "action": "follow_bank_policy"}
    mismatches = [f for f in ("date", "payee", "amount")
                  if normalise(extracted[f]) != normalise(declared[f])]
    return {"status": "match" if not mismatches else "mismatch",
            "fields": mismatches,
            # A payee mismatch is the alteration case Positive Pay exists for.
            "action": "pay" if not mismatches else "flag_to_both_banks"}

# WHAT TO CHECK
# [ ] CAR and LAR read INDEPENDENTLY, from different regions, by paths that
#     cannot see each other's output
# [ ] a disagreement routes to a human. Never auto-resolve by confidence
# [ ] where you must act on one, act on the WORDS. Section 18 is not a
#     preference
# [ ] normalise before comparing payee names, or Positive Pay flags every
#     cheque over a full stop
# [ ] a value threshold for manual review, independent of confidence. A
#     confident wrong reading on a large cheque is the expensive failure
# [ ] reconcile magnetic and optical MICR reads and treat disagreement as a
#     fraud signal, not a retry
''')

i_step456 = '''
<h3 id="s-indigo-s4">Steps 4 to 6 &mdash; Read, reconcile, match</h3>
''' + code_read + '''
<p><strong>THE finding:</strong> <strong>the extraction is the easy half. The hard half is that your
reading has to agree with something the drawer already declared &mdash; and now inside an
hour.</strong></p>
<p>Under the <strong>Positive Pay System</strong>, the issuer of a cheque submits the date, the payee
name and the amount to their own bank in advance, through SMS, the mobile app, internet banking or an
ATM. CTS cross-checks the presented instrument against that declaration and flags any discrepancy to
both the drawee and the presenting bank. Banks enable it for cheques of <strong>&#8377;50,000 and
above</strong>, and may make it mandatory above <strong>&#8377;5 lakh</strong>.</p>
<p>That changes what accuracy means. <strong>Your engine is not trying to be right in the abstract; it
is trying to agree with a specific prior statement.</strong> A reading that is objectively correct and
disagrees with the declaration still stops the cheque &mdash; and it should.</p>
''' + warn("<strong>The comparison is where this goes wrong, not the reading.</strong> <em>M/s Sharma Traders</em> against <em>Sharma Traders Pvt Ltd</em>. A trailing full stop. An initial with and without a space. <strong>Normalise aggressively before comparing, or Positive Pay will flag a large share of perfectly good cheques</strong> &mdash; and a system that flags everything is a system a bank switches off. The payee field is where the value is, because payee alteration is precisely the fraud Positive Pay was introduced to catch.")

code_clock = code('Python — steps 7 and 8, the hourly cycle and the return path', r'''from datetime import datetime, timedelta

# STEP 7. CONTINUOUS CLEARING. THE DEADLINE IS NOW PER ITEM, NOT PER DAY.
# Before 4 October 2025 an item joined a batch and the batch had a deadline.
# Now each item has its own confirmation window, bounded by the Item Expiry
# Time. A review that used to "make today's cut-off" now has to make an hour.

def review_deadline(presented_at, cutoffs):
    """When this specific item stops being yours to decide."""
    return min(presented_at + cutoffs["confirmation_window"],
               cutoffs["item_expiry_time_for"](presented_at))

def route_with_clock(item, policy, staffing):
    decision = route(item["car"], item["lar"], policy)   # auto | manual_review
    if decision == "auto":
        return {"action": "auto", "by": None}
    due = review_deadline(item["presented_at"], policy["cutoffs"])
    # The question is not "is a human available" but "is one available BEFORE
    # this item expires". A queue drained at day end answers the first.
    if not staffing.reviewer_available_before(due):
        # Do not let it expire silently. An expiry is a return the customer
        # did not earn and nobody decided.
        return {"action": "escalate_now", "due_ist": due, "why": "no reviewer in window"}
    return {"action": "manual_review", "due_ist": due}

# STEP 8. RETURNS.
def handle_return(item, reason_code, store):
    # Keep the evidence WITH the return. The dispute arrives later and the
    # question is always what the instrument actually said.
    store.attach(item["id"], images=item["image_triple"],
                 extraction=item["extraction"], positive_pay=item["pp_result"])
    return {
        "reason_code": reason_code,
        # Plain language reaches the customer; the code reaches the system.
        "customer_message": PLAIN[reason_code],
        "at_ist": now_ist(),
    }

def return_rate_by_reason(window, baseline):
    """A rising 'signature differs' rate is a capture or model problem wearing
    a customer-behaviour costume. Nothing else in the reporting shows it."""
    rates = group(window, "reason_code")
    return {r: {"rate": v, "drifted": v > baseline[r] * 1.5} for r, v in rates.items()}

# WHAT TO CHECK
# [ ] compute the deadline PER ITEM, not per session. The batch mental model
#     is the single biggest carry-over risk from the old cycle
# [ ] alert when no reviewer is available before an item expires, rather
#     than discovering it in the return file
# [ ] never let an item expire silently into a return. That is a decision
#     nobody made, reaching a customer who did not earn it
# [ ] attach the images and the extraction to every return. The dispute is
#     later and the evidence is not reconstructable
# [ ] track return rate BY REASON against a baseline, and treat a jump in a
#     capture-sensitive reason as a pipeline alert
# [ ] every timestamp in IST against the clearing calendar, never a UTC day
''')

i_step78 = '''
<h3 id="s-indigo-s7">Step 7 &mdash; Present, and the clock that changed</h3>
<p>Until October 2025, cheque clearing ran in two batch sessions and the beneficiary typically waited
until the next working day. <strong>RBI circular RBI/2025-26/73 of 13 August 2025</strong> replaced
that with <strong>continuous clearing and settlement on realisation</strong>, effective
<strong>4 October 2025</strong>.</p>
<table>
<tr><th>Then</th><th>Now</th></tr>
<tr><td>Two fixed batch sessions</td><td><strong>Continuous presentation through the working day</strong></td></tr>
<tr><td>Settlement at session close</td><td><strong>Hourly settlement on realisation</strong></td></tr>
<tr><td>Credit typically next working day</td><td><strong>Credit the same working day</strong> once the paying bank confirms</td></tr>
<tr><td>A confirmation window measured in hours</td><td>A confirmation window measured in <strong>the hour</strong>, bounded by the <strong>Item Expiry Time</strong></td></tr>
</table>
''' + code_clock + warn("<strong>For a drawee bank this is the change that matters and it is an operations change, not a technology one.</strong> The decision to pay or return used to have most of a day behind it, with a queue of exceptions worked through by people. It now has to be made inside an hourly cycle. <strong>Anything that routes to manual review needs a reviewer available during clearing hours, not a queue drained at four o'clock.</strong> A pipeline that auto-approves 95% and leaves 5% for a team that works batch-style will miss the window on the 5% that mattered enough to flag.") + '''

<h3 id="s-indigo-s8">Step 8 &mdash; Returns</h3>
<p>A returned cheque is not an error state in your pipeline &mdash; it is a normal outcome with a
reason code, a customer on the other end, and in some cases legal consequences under the Negotiable
Instruments Act.</p>
<p>Three things to build properly. <strong>Carry the reason through to the customer in plain
language</strong>: <em>insufficient funds</em>, <em>signature differs</em>, <em>alteration requires
drawer confirmation</em>, <em>Positive Pay mismatch</em>. Second, <strong>keep the image and the
extraction against the return</strong>, because the dispute arrives later and the question is always
what the instrument actually said. Third, <strong>track your return rate by reason</strong> &mdash; a
rising <em>signature differs</em> rate is a model or capture problem wearing a customer-behaviour
costume, and nothing else in your reporting will tell you that.</p>
'''

i_cost = registry("Cheque reading &mdash; what it costs", [
 ("Capture hardware", "direct",
  "Scanners meeting the CTS image specification, with <strong>magnetic MICR reading</strong> rather "
  "than optical alone. The magnetic read is worth the hardware: it is immune to stamps, folds and "
  "photocopies, and disagreement with the optical read is a free fraud signal."),
 ("Extraction", "direct",
  "Per document or a licence. <strong>Cheaper than it looks and less decisive than it is sold as</strong> "
  "&mdash; the MICR band is reliable, and CAR and LAR are the only genuinely hard fields."),
 ("Manual review capacity", "direct",
  "<strong>The line that decides whether the system works.</strong> Since continuous clearing, reviewers "
  "must be available <em>during</em> clearing hours rather than draining a queue at day end. This is a "
  "staffing model, not a headcount."),
 ("Positive Pay integration", "direct",
  "Matching against the drawer's declaration, with the normalisation work that stops it flagging good "
  "cheques. <strong>Budget the normalisation, not the match</strong> &mdash; the match is trivial and "
  "the normalisation is the product."),
 ("Archival", "direct",
  "Signed images retained to specification, retrievable years later when a dispute arrives. Storage is "
  "cheap; <strong>retrievability under a legal request is the requirement</strong>."),
 ("Getting it wrong", "indirect",
  "Paying an altered cheque is a loss the bank absorbs and a customer relationship it does not. On the "
  "other side, <strong>a false-positive rate high enough to be annoying gets the system switched "
  "off</strong>, which is the more common failure and the harder one to recover from."),
], "September 2026") + note("<strong>The number to compute first: what share of cheques by VALUE currently needs a human, and could a human reach them inside an hour?</strong> Not the volume share &mdash; the value share. That single figure tells you whether continuous clearing is a timing problem you can staff or an architecture problem you cannot, and it is answerable from last quarter's data in an afternoon.")

a_builds = '''
<h3 id="s-amber-week">Reconcile what you banked</h3>
<p><strong>Build:</strong> photograph or scan on deposit &rarr; read MICR and CAR &rarr; match against
your receivables ledger &rarr; reconcile against the bank statement when it clears.</p>
<p><strong>You get:</strong> the corporate depositor product. <strong>No CTS integration, no clearing
membership, no regulator</strong> &mdash; and it solves a real reconciliation problem that most
finance teams still do by hand.</p>

<h3 id="s-amber-proper">Presenting-bank capture</h3>
<p><strong>Build:</strong> capture to the CTS image specification &rarr; sign at origin &rarr;
magnetic MICR with optical reconciliation &rarr; independent CAR and LAR &rarr; disagreement routes to
a human &rarr; present into the continuous cycle.</p>
<p><strong>Trade:</strong> real hardware and real clearing-house integration. <strong>The enhancement
rule bites here</strong> &mdash; the signed original is the instrument, and everything you do to read
it happens on a copy.</p>

<h3 id="s-amber-big">Drawee-bank decisioning</h3>
<p><strong>Build:</strong> the above, plus Positive Pay matching with proper normalisation, signature
verification against specimens, account-level checks, a review queue staffed <em>during</em> clearing
hours, and return handling with reasons carried through to the customer.</p>
<p><strong>It breaks when:</strong> the review queue is designed for the old batch rhythm. <strong>The
technology was never the constraint; the hour is.</strong></p>
''' + note("If you take one thing from this page: <strong>read the amount in words independently, and when it disagrees with the figures, the words govern.</strong> Section 18 of the Negotiable Instruments Act settled that in 1881. Most pipelines treat the figures as the answer and the words as a check, because figures are easier to read &mdash; which is exactly backwards.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Signature broken by enhancement</strong></td><td>Deskew or contrast applied to the original.</td><td>Sign at origin. Enhance a copy.</td></tr>
<tr><td><strong>LAR derived from CAR</strong></td><td>The words are hard; the figures are easy.</td><td>Independent reads, or you have one reading and a rationalisation.</td></tr>
<tr><td><strong>Disagreement auto-resolved by confidence</strong></td><td>Treated as a model problem.</td><td>It is a legal question. Words govern; a human sees it.</td></tr>
<tr><td><strong>Positive Pay flags good cheques</strong></td><td>Payee compared without normalisation.</td><td>Normalise aggressively. A system that flags everything gets switched off.</td></tr>
<tr><td><strong>Confident wrong reading on a large cheque</strong></td><td>Routing by confidence only.</td><td>A value threshold as well, independent of confidence.</td></tr>
<tr><td><strong>MICR misread on a stamped band</strong></td><td>Optical reading only.</td><td>Magnetic read; treat disagreement as a fraud signal.</td></tr>
<tr><td><strong>Review queue misses the cycle</strong></td><td>Designed for two batch sessions.</td><td>Reviewers available during clearing hours.</td></tr>
<tr><td><strong>Non-CTS-2010 cheque in the pipeline</strong></td><td>Still valid as an instrument, not in clearing.</td><td>Detect and route to another collection mode.</td></tr>
<tr><td><strong>Alteration accepted</strong></td><td>Treated as a low-confidence read.</td><td>CTS does not accept alterations except date validation. Return it.</td></tr>
<tr><td><strong>Return reason not carried to the customer</strong></td><td>Reason code stays in the system.</td><td>Plain language, and keep the image against the return.</td></tr>
<tr><td><strong>Rising "signature differs" rate unexplained</strong></td><td>Read as customer behaviour.</td><td>It is usually capture or model drift. Track returns by reason.</td></tr>
</table>
'''

SRC=[('official','RBI circular RBI/2025-26/73 dated 13 August 2025 — Continuous Clearing and Settlement on Realisation in CTS','the replacement of two batch clearing sessions with continuous presentation and hourly settlement from 4 October 2025, same-working-day realisation once the paying bank confirms, and the Item Expiry Time that bounds the confirmation window.','https://www.rbi.org.in'),
 ('official','NPCI — Cheque Truncation System documentation and FAQs','CTS as an image-based clearing system operated by NPCI under the amended Negotiable Instruments Act 1881, RBI&rsquo;s classification of paper clearing as a System-Wide Important Payment System, retention of the physical instrument at the presenting bank, and the clearing-house interface behaviour including duplicate detection.','https://www.npci.org.in'),
 ('official','RBI / NPCI CTS image and interface specification','the three image views per instrument — front greyscale at a minimum of 100 DPI in JFIF/JPEG at 8 bits per pixel, and front and rear black and white at a minimum of 200 DPI in TIFF with CCITT G4 compression — the mandatory digital signature applied by the presenting bank from the point of origin, PKI protection across the whole cycle, and compliance with the IT Act, 2000.','https://www.npci.org.in'),
 ('official','RBI — CTS-2010 Standard for cheque forms','the security features required of a compliant instrument, including micro-lettering, bleeding ink, security thread and the UV band over the legal amount, courtesy amount, signature and beneficiary fields; and the discontinuation of separate clearing for non-CTS-2010 instruments from 31 December 2018.','https://www.rbi.org.in'),
 ('official','RBI — Positive Pay System for CTS','the requirement that banks enable Positive Pay for cheques of ₹50,000 and above, with discretion to mandate it above ₹5 lakh; the drawer&rsquo;s advance submission of date, payee and amount through SMS, mobile app, internet banking or ATM; and the cross-check by CTS with discrepancies flagged to both the drawee and presenting banks.','https://www.rbi.org.in'),
 ('official','Negotiable Instruments Act, 1881 — section 18','that where the amount is stated differently in figures and in words, the amount stated in words is the amount ordered to be paid. Also the basis, as amended, for truncation replacing the physical instrument with its image and MICR data.','https://www.indiacode.nic.in'),
 ('official','RBI guidance to customers on cheque preparation','the use of image-friendly dark ink, care with rubber stamps so they do not overshadow the date, payee, amount or signature, and that cheques carrying alterations other than date validation are not accepted under CTS.','https://www.rbi.org.in'),
 ('industry','Implementation commentary on CTS capture and clearing','the practitioner read on capture-system architecture, magnetic versus optical MICR reading, and operational staffing under the continuous cycle. Directional; confirm every specification against the notified NPCI document before building to it.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. The clearing cycle changed on 4 October 2025 &mdash; treat any guidance '
 'describing next-working-day clearing as out of date, including anything published before then.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/products/document-ai/" class="mod-card"><div class="mod-num">GUIDE 01</div><h3>Document AI</h3><p>Extraction, classification and confidence routing, in general.</p></a>
<a href="/fintech-ai/products/sme-treasury/" class="mod-card"><div class="mod-num">GUIDE 13</div><h3>SME Treasury</h3><p>The corporate side — reconciling what you banked against what cleared.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Control totals, full outer joins, and settlement you do not control.</p></a>
<a href="/fintech-ai/fraud-risk/" class="mod-card"><div class="mod-num">MODULE 04</div><h3>Fraud and Risk</h3><p>Where alteration detection and signature verification belong.</p></a>
</div>
''' + warn("This page is a guide, not a specification. CTS participation is governed by RBI circulars and NPCI procedural documents that are revised regularly, and the clearing cycle itself changed in October 2025. Nothing here is legal advice. Build from the current NPCI specification your clearing membership gives you, and confirm every image and timing parameter against it.")

lanes={'green':[("How to use this page",g_read),("What a cheque image actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 to 3 — side, capture, MICR",i_step123),
           ("Steps 4 to 6 — read, reconcile, match",i_step456),
           ("Steps 7 and 8 — present, and returns",i_step78),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Cheque Reading: How to Build It"
META=("Build cheque data extraction step by step: the CTS image specification, why the words govern "
      "the figures, Positive Pay, and the clock that changed in 2025.")
LEAD=("A step-by-step guide to reading cheques inside India's Cheque Truncation System. Eight stages, "
      "the options at each one, exactly how each step connects to the next, real costs, and what "
      "breaks. Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
MD=_re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')
for nm,lane in lanes.items():
    for t,c in lane:
        s=MD.findall(_re.sub(r'<[^>]+>',' ',c)); assert not s, 'markdown in %s: %s'%(t,s[:3])
page(path="fintech-ai/products/cheque-reading",title=TITLE,meta=META,lead=LEAD,label="Product Guide 15",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/cheque-reading/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Turning paper cheques into '
  'data? The eight steps, the CTS image specification, and what the October 2025 clearing change means: '
  '<a href="/fintech-ai/products/cheque-reading/"><strong>Cheque Reading: How to Build It &rarr;</strong>'
  '</a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('payments-reconciliation', 'fraud-risk'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/cheque-reading' in src:
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
