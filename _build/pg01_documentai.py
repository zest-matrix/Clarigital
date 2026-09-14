#!/usr/bin/env python3
# Session 52 — PRODUCT GUIDE 01: Document AI  (new page type: product journey)
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

# ---------------------------------------------------------------- GREEN

g_read = '''
<p>This page is different from the rest of this section. The modules explain how things work. The
build sheets list what to buy. This page walks you through <strong>building one product, start to
finish</strong>.</p>
<p>It is written for someone who has not built this before. Every step says what goes in, what comes
out, and how to plug it into the next step.</p>
<table>
<tr><th>If you want...</th><th>Read...</th></tr>
<tr><td>To understand why document reading is hard</td><td><a href="/fintech-ai/identity-onboarding/">the Identity module</a></td></tr>
<tr><td>A full list of every tool, with prices</td><td><a href="/fintech-ai/identity-onboarding/build-sheet/">the Identity Build Sheet</a></td></tr>
<tr><td><strong>To build the thing</strong></td><td><strong>this page</strong></td></tr>
</table>
<p>Nothing here is secret. All of it is doable by two engineers in a few weeks. The hard part is not
any single step. It is knowing which eight steps there are, and what to connect to what.</p>
'''

g_what = '''
<p>Document AI takes a picture of a document and gives you back <strong>fields you can put in a
database</strong>.</p>
<p>Picture of a PAN card goes in. Out comes: name, PAN number, date of birth, father's name. Each
one with a score saying how sure the system is.</p>
<p>People also call it ICR, which stands for Intelligent Character Recognition. Older OCR read
printed text. ICR is meant to also read handwriting and understand layout. In practice the words get
used loosely and nobody minds.</p>
<p><strong>What it is not:</strong></p>
<ul>
<li>It is <strong>not</strong> a decision. It reads a document. It does not tell you whether to open
the account.</li>
<li>It is <strong>not</strong> verification. Reading "Rajesh Kumar" off a card does not prove Rajesh
Kumar exists or that this is his card. That is a different product.</li>
<li>It is <strong>not</strong> one model. It is six or seven things in a row. This is the single
biggest surprise for teams who thought they were buying an API.</li>
</ul>
<p>Who buys it: banks, lenders, insurers, and anyone who currently has people typing things off
scanned paper. The business case is almost always <em>we have forty people doing data entry</em>.</p>
'''

g_map = '''
<p>Here is the whole thing. Eight steps. Read this table once and the rest of the page is just
detail.</p>
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Get the file</strong></td><td>The document arrives from somewhere.</td></tr>
<tr><td>2</td><td><strong>Check it is usable</strong></td><td>Is it too blurry to read? Find out before you pay to read it.</td></tr>
<tr><td>3</td><td><strong>Work out what it is</strong></td><td>PAN card? Bank statement? You cannot extract fields until you know.</td></tr>
<tr><td>4</td><td><strong>Read the text</strong></td><td>Turn pixels into words. This is the bit everyone calls "the OCR".</td></tr>
<tr><td>5</td><td><strong>Turn words into fields</strong></td><td>A pile of words is not data. Which word is the name?</td></tr>
<tr><td>6</td><td><strong>Check the fields are real</strong></td><td>Does the PAN number pass its checksum? Does the date make sense?</td></tr>
<tr><td>7</td><td><strong>Accept, review or reject</strong></td><td>Send the uncertain ones to a human.</td></tr>
<tr><td>8</td><td><strong>Keep the evidence</strong></td><td>What you read, from which image, how sure you were, when.</td></tr>
</table>
''' + note("Steps 2, 6, 7 and 8 are the ones people skip. They are also the ones that decide whether this works in production or only in the demo. A team that builds steps 1, 3, 4 and 5 has built a demo. That is not an insult &mdash; it is just a much smaller thing than it looks.") + '''
<p>Steps 3 and 4 are where the money goes. Steps 2, 6, 7 and 8 are where the product lives.</p>
'''

# ---------------------------------------------------------------- INDIGO

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Get the file</h3>
<p><strong>What it does:</strong> the document gets from the customer to your server.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Effort</th><th>Pick this when</th></tr>
<tr><td><strong>A. Plain upload</strong></td><td>A file input on a web page.</td><td>Hours</td><td>Always start here. It works and it costs nothing.</td></tr>
<tr><td><strong>B. Mobile SDK capture</strong></td><td>A vendor's camera component that guides the user and rejects bad shots on the phone.</td><td>Days, plus a licence</td><td>Consumer app, high volume, and bad photos are killing you.</td></tr>
<tr><td><strong>C. DigiLocker fetch</strong></td><td>The customer consents and you receive the issued document directly.</td><td>Weeks, needs approval</td><td>You want a document that is already verified. Skips steps 2&ndash;6 entirely for supported documents.</td></tr>
</table>
<p><strong>What comes out:</strong> a file on disk or in object storage, plus an id.</p>
<p><strong>Connect it to step 2:</strong> do not pass the file around. Save it once, give it an id, and
pass the id. Every later step reads from storage using that id. If you pass image bytes between
services you will run out of memory on the day someone uploads a 40&nbsp;MB scan.</p>
''' + warn("<strong>Option C deserves more thought than it usually gets.</strong> If DigiLocker can give you the document directly, you are not reading a photograph of a PAN card &mdash; you are receiving the issued record. No blur, no glare, no OCR, no confidence score. Teams build the whole eight-step pipeline and only afterwards discover that a large share of their documents could have come down a route that skips six of the steps. Check what is available before you build.") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; Check it is usable</h3>
<p><strong>What it does:</strong> looks at the image and decides whether it is worth reading. Blurry,
dark, cropped, upside down, or a photo of a screen.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Roughly costs</th><th>Pick this when</th></tr>
<tr><td><strong>A. Simple maths</strong></td><td>OpenCV. Measure blur, brightness and resolution with about thirty lines of code.</td><td>Free</td><td>Start here. It catches most of the bad ones.</td></tr>
<tr><td><strong>B. A small model</strong></td><td>A trained classifier that scores image quality.</td><td>Your own GPU time</td><td>Simple maths is passing things that later fail.</td></tr>
<tr><td><strong>C. Skip it</strong></td><td>Send everything to the OCR and see what happens.</td><td>You pay per page, so this is the expensive option</td><td>Never, once you are past a few hundred documents a day.</td></tr>
</table>
''' + code('Python — step 2, the cheapest useful quality gate', r'''import cv2

# This is the whole thing. It is not clever. It works.
def usable(path):
    img = cv2.imread(path)
    if img is None:
        return {"ok": False, "why": "not_an_image"}

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = grey.shape

    # Blur. Laplacian variance: sharp images have high variance, blurry ones low.
    blur = cv2.Laplacian(grey, cv2.CV_64F).var()

    # Brightness. A photo taken in the dark, or washed out by flash.
    bright = grey.mean()

    checks = {
        "too_small":  w < 800 or h < 500,
        "too_blurry": blur < 100,       # tune this on YOUR documents
        "too_dark":   bright < 50,
        "too_bright": bright > 205,
    }
    failed = [k for k, v in checks.items() if v]
    return {"ok": not failed, "why": failed,
            "blur": round(blur, 1), "brightness": round(bright, 1)}

# WHAT TO CHECK
# [ ] tune the thresholds on 200 of YOUR real documents, not on the numbers
#     above. A PAN card photographed indoors and a scanned bank statement have
#     completely different normal ranges
# [ ] tell the user WHICH check failed. "Please try again" makes people retry
#     the same bad photo. "Too dark - move to a window" gets you a good one
# [ ] let the user override after two failures and send it to human review.
#     A gate with no escape hatch becomes a customer who cannot open an account
# [ ] log the scores even when the image passes. When accuracy drops next month
#     you will want to know whether the images got worse
''') + '''
<p><strong>What comes out:</strong> a yes/no, and if no, <em>which</em> check failed.</p>
<p><strong>Connect it to step 3:</strong> only files that pass go forward. Files that fail go back to
the user with the specific reason. This is the cheapest step on the page and it removes more OCR cost
than anything else you will do.</p>
'''

i_step34 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; Work out what the document is</h3>
<p><strong>What it does:</strong> decides whether this is a PAN card, an Aadhaar, a passport, a
salary slip or a bank statement.</p>
<p>You need this because step 4 and step 5 are different for each type. There is no general "read any
document" that gives you clean fields.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Roughly costs</th><th>Pick this when</th></tr>
<tr><td><strong>A. Ask the user</strong></td><td>A dropdown: "what are you uploading?"</td><td>Free</td><td>Start here. Genuinely. Most products never need more.</td></tr>
<tr><td><strong>B. Keyword rules</strong></td><td>Run cheap OCR, look for giveaway words ("INCOME TAX DEPARTMENT", "Permanent Account Number").</td><td>≈ $1.50 per 1,000 pages</td><td>You have a few document types and they have distinctive text.</td></tr>
<tr><td><strong>C. A classifier model</strong></td><td>Azure or Google classify the document before reading it.</td><td>≈ $3 per 1,000</td><td>Many types, or documents arrive in bulk with no user to ask.</td></tr>
</table>
''' + note("Option A sounds lazy and is usually right. If the user is standing in your app uploading their PAN card, they know it is a PAN card. Asking costs nothing and is more accurate than any classifier. Save the classifier for post boxes and bulk scans, where there is no user to ask.") + '''
<p><strong>What comes out:</strong> a document type, and a confidence score if you used B or C.</p>
<p><strong>Connect it to step 4:</strong> the document type chooses <em>which</em> reader you call. PAN
and Aadhaar go to an identity-document API. A bank statement goes to a table extractor. Sending a
bank statement to an ID reader gets you nothing useful and still bills you.</p>

<h3 id="s-indigo-s4">Step 4 &mdash; Read the text</h3>
<p><strong>What it does:</strong> turns the picture into words, with a position on the page and a
confidence for each one.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Roughly costs per 1,000 pages</th><th>Pick this when</th></tr>
<tr><td><strong>A. Plain OCR</strong></td><td>AWS, Google or Azure. Just gives you words and boxes.</td><td><strong>≈ $1.50</strong>, all three within cents of each other</td><td>You will do the field-finding yourself in step 5.</td></tr>
<tr><td><strong>B. Identity-document API</strong></td><td>AWS Textract AnalyzeID and equivalents. Knows what a passport and a driving licence look like.</td><td><strong>≈ $10&ndash;25</strong></td><td>ID documents specifically. It does steps 4 and 5 together.</td></tr>
<tr><td><strong>C. Prebuilt or custom models</strong></td><td>Azure and Google models for invoices, receipts, and your own trained ones.</td><td>Prebuilt <strong>≈ $10</strong>, custom <strong>≈ $30</strong></td><td>A document type with a stable layout and real volume.</td></tr>
<tr><td><strong>D. Self-hosted</strong></td><td>PaddleOCR, docTR, Tesseract on your own machine.</td><td><strong>No per-page fee.</strong> You pay for CPU, and GPU if you use a vision model</td><td>Data cannot leave your building, or volume is high enough that per-page pricing hurts.</td></tr>
</table>
''' + warn("<strong>Plain OCR is a commodity. Do not spend a week choosing.</strong> AWS, Google and Azure price it at roughly $1.50 per 1,000 pages and match each other to the cent. Pick the one your infrastructure already uses. The interesting choice is <strong>B versus A-plus-your-own-step-5</strong>, and that is a build-versus-buy decision, not a vendor comparison.") + '''
<p><strong>What comes out:</strong> a list of text pieces. Each has the text, a box saying where it sat
on the page, and a confidence between 0 and 1.</p>
<p><strong>Connect it to step 5:</strong> this is the most important handoff on the page, so it has its
own section below.</p>
'''

code_wire = code('The wiring — what step 4 hands to step 5, and what step 5 hands back', r'''# STEP 4 GIVES YOU THIS. Every OCR engine returns roughly this shape, with
# different key names. Normalise to one shape IMMEDIATELY, in one small adapter
# per engine. Then nothing downstream knows or cares which engine you used --
# and swapping engines becomes a one-file change instead of a rewrite.

ocr_output = {
    "doc_id": "doc_8814",
    "engine": "textract-v1",          # keep this. You WILL need to know later.
    "pages": [{
        "page": 1,
        "words": [
            # text,            box (x, y, width, height as 0-1 fractions), score
            {"text": "INCOME",   "box": [0.10, 0.05, 0.08, 0.03], "score": 0.99},
            {"text": "TAX",      "box": [0.19, 0.05, 0.04, 0.03], "score": 0.99},
            {"text": "ABCDE1234F","box": [0.10, 0.44, 0.22, 0.04], "score": 0.97},
            {"text": "RAJESH",   "box": [0.10, 0.52, 0.12, 0.03], "score": 0.94},
            {"text": "KUMAR",    "box": [0.23, 0.52, 0.11, 0.03], "score": 0.95},
        ],
    }],
}

# STEP 5 MUST GIVE YOU THIS. Note what is carried through: the score, and WHERE
# on the page it came from. Without those two, steps 6, 7 and 8 cannot work.

fields_output = {
    "doc_id": "doc_8814",
    "doc_type": "pan_card",
    "fields": {
        "pan":  {"value": "ABCDE1234F", "score": 0.97,
                 "source": {"page": 1, "box": [0.10, 0.44, 0.22, 0.04]}},
        "name": {"value": "RAJESH KUMAR", "score": 0.94,   # LOWEST of its words
                 "source": {"page": 1, "box": [0.10, 0.52, 0.24, 0.03]}},
    },
    "missing": ["father_name", "dob"],      # ALWAYS list what you did not find
}

# WHAT TO CHECK
# [ ] boxes as fractions of the page (0-1), never pixels. Pixels break the
#     moment someone uploads the same document at a different resolution
# [ ] a joined field takes the LOWEST score of its parts, not the average.
#     "RAJESH" at 0.99 and "KUMAR" at 0.60 is a 0.60 name, not a 0.80 one.
#     Averaging confidence is how bad reads get through
# [ ] "missing" is a real list, not an absence of keys. "We could not find the
#     date of birth" and "we never looked for it" are different facts
# [ ] keep the box. When a human reviews this in step 7, you want to highlight
#     the exact spot on the image. Reviewers go three to five times faster when
#     they can see where the value came from
# [ ] keep the engine name and its version. When accuracy shifts next quarter,
#     the first question is whether the vendor changed the model
# [ ] normalise every engine into this ONE shape in an adapter. Do not let
#     Textract's key names leak into your database
''')

i_wiring = '''
<p>Most guides stop after "call the OCR API". That is where the actual work starts, so this is the
part we are going to be precise about.</p>
<p>Step 4 gives you <strong>words</strong>. Step 5 needs to produce <strong>fields</strong>. The
contract between them is where teams lose a fortnight.</p>
''' + code_wire + '''
<p>The rule underneath all of that: <strong>carry the confidence and the position all the way
through.</strong> They feel like debugging information at step 5. By step 7 they are the product, and
by step 8 they are your evidence.</p>
'''

i_step56 = '''
<h3 id="s-indigo-s5">Step 5 &mdash; Turn words into fields</h3>
<p><strong>What it does:</strong> decides which of those words is the name, which is the PAN number,
which is the date of birth.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Roughly costs</th><th>Pick this when</th></tr>
<tr><td><strong>A. Position rules</strong></td><td>On a PAN card the number is always in the same place. Take whatever text sits in that box.</td><td>Free</td><td>Fixed-layout documents. Fast, free, and completely predictable.</td></tr>
<tr><td><strong>B. Label matching</strong></td><td>Find the word "Name", take what is to the right of it.</td><td>Free</td><td>Forms with printed labels. Handles small layout shifts.</td></tr>
<tr><td><strong>C. Pattern matching</strong></td><td>A PAN is five letters, four digits, one letter. Find anything that matches.</td><td>Free</td><td>Fields with a strict format. Combine with A or B.</td></tr>
<tr><td><strong>D. Let the API do it</strong></td><td>You picked option B in step 4, so fields come back already extracted.</td><td>Included in the $10&ndash;25</td><td>ID documents. Least code by a distance.</td></tr>
<tr><td><strong>E. Ask a language model</strong></td><td>Give the model the OCR text and ask for JSON.</td><td>Per token, so it depends</td><td>Messy or varied layouts where A, B and C all fail.</td></tr>
</table>
''' + warn("<strong>Option E has a trap.</strong> A language model will happily invent a plausible date of birth if the OCR did not read one. You asked for JSON with a <code>dob</code> field and it will give you a <code>dob</code> field. Two rules if you use it: pass only the OCR text and <strong>never the image description</strong>, and then check every returned value actually appears in the OCR output. If the model returns something the OCR never read, throw it away and mark the field missing. This is the same rule as the refusal gate in <a href=\"/fintech-ai/customer-operations/build-sheet/\">Build Sheet 06</a> &mdash; the value must be present in the retrieved text, not merely plausible.") + '''
<p><strong>Connect it to step 6:</strong> pass the whole field object, with scores and boxes. Do not
flatten it to plain strings here. Step 6 needs the scores and step 7 needs the boxes.</p>

<h3 id="s-indigo-s6">Step 6 &mdash; Check the fields are real</h3>
<p><strong>What it does:</strong> catches wrong values that the OCR was <em>confident</em> about. This
is the step that separates a demo from a product.</p>
<p>A confidence score tells you how clearly the system saw the characters. It does not tell you
whether the answer is right. An OCR engine can read a smudged 8 as a 3 with 0.98 confidence.</p>
<table>
<tr><th>Check</th><th>What it catches</th><th>Costs</th></tr>
<tr><td><strong>Format</strong></td><td>A PAN that is not five letters, four digits, one letter. An eleven-digit phone number.</td><td>Free</td></tr>
<tr><td><strong>Checksum</strong></td><td>Aadhaar has a check digit. So do IFSC and GSTIN and many others. A single misread character fails it.</td><td>Free</td></tr>
<tr><td><strong>Cross-field</strong></td><td>Date of birth after today. Issue date after expiry date. Age of four on a PAN card.</td><td>Free</td></tr>
<tr><td><strong>Against the source</strong></td><td>Ask the issuing authority whether this number exists and matches this name.</td><td>Per lookup, varies by provider</td></tr>
</table>
''' + note("The first three are free and catch most of it. Do all three before you spend money on the fourth. A field that fails a checksum does not need a paid lookup to tell you it is wrong &mdash; and sending it anyway is a cost you can remove on your first afternoon.") + '''
<p><strong>Connect it to step 7:</strong> each field now carries both a confidence <em>and</em> a
validation result. Step 7 needs both, and they disagree more often than you would expect. A field can
be read clearly and still be wrong; a field can be read poorly and still be correct.</p>
'''

code_route = code('Python — step 7, deciding what to do with each document', r'''# Three outcomes. Never two. A system with only accept and reject will either
# reject good customers or accept bad data, and usually both.

def decide(fields, doc_type, rules):
    hard_fail, weak = [], []

    for name, f in fields.items():
        if name in rules["required"][doc_type]:
            if f["value"] is None:
                hard_fail.append((name, "missing"))
                continue
            if not f["valid"]:                    # from step 6
                hard_fail.append((name, f["invalid_reason"]))
                continue
            if f["score"] < rules["min_score"].get(name, 0.90):
                weak.append((name, f["score"]))

    # A failed CHECKSUM is different from a LOW SCORE. The first means the value
    # is wrong. The second means we are unsure. Do not merge them into one
    # "confidence" number -- you lose the ability to tell the user which it was.
    if hard_fail:
        return {"outcome": "review", "reason": "failed_validation",
                "detail": hard_fail, "show_boxes": True}
    if weak:
        return {"outcome": "review", "reason": "low_confidence",
                "detail": weak, "show_boxes": True}
    return {"outcome": "accept"}

# WHAT TO CHECK
# [ ] "reject" is almost never the right automatic outcome for a document that
#     a real customer uploaded. Route to REVIEW. Let a person reject
# [ ] the review screen shows the image with the box drawn on it, next to the
#     extracted value, in one editable field. Reviewers go 3-5x faster
# [ ] thresholds live in config, are versioned, and are approved. Changing a
#     threshold changes who gets accepted -- treat it as a control change
# [ ] measure the review queue every week. If it is growing faster than volume,
#     something upstream broke and nobody noticed
# [ ] measure the OVERRIDE RATE. If humans accept 95% of what you send them,
#     your thresholds are too tight and you are paying people to click yes
# [ ] every correction a reviewer makes is training data and a bug report.
#     Store the before and after. This is the highest-value data you will
#     generate and most teams throw it away
''')

i_step78 = '''
<h3 id="s-indigo-s7">Step 7 &mdash; Accept, review or reject</h3>
<p><strong>What it does:</strong> turns scores and checks into an actual decision about this document.</p>
''' + code_route + '''
<p><strong>Connect it to step 8:</strong> the decision, the reason and the reviewer's edits all go into
the record. Especially the edits.</p>

<h3 id="s-indigo-s8">Step 8 &mdash; Keep the evidence</h3>
<p><strong>What it does:</strong> stores what happened, so that in two years you can answer "why did
you accept this document?"</p>
<p>This is the step that gets left until last and then never gets built. It is also the one that
regulators and auditors ask about first.</p>
<table>
<tr><th>Store</th><th>Why</th></tr>
<tr><td>The original image</td><td>Everything else is a claim about it.</td></tr>
<tr><td>The full OCR output</td><td>So you can re-run step 5 later without paying for step 4 again.</td></tr>
<tr><td>The extracted fields, with scores and boxes</td><td>What you believed, and how sure you were.</td></tr>
<tr><td>Which engine and which version</td><td>When accuracy shifts, this is the first thing you check.</td></tr>
<tr><td>Which thresholds were in force</td><td>The rules change. The record must say which rules applied that day.</td></tr>
<tr><td>The decision, and who made it</td><td>Automatic, or a named reviewer.</td></tr>
<tr><td>Every correction a human made</td><td>Your best training data and your best bug report.</td></tr>
</table>
''' + warn("Store the record <strong>append-only</strong>. A correction is a new row, never an edit to the old one. The question is not only &ldquo;what do we believe now&rdquo; but &ldquo;what did we believe on the day we opened the account&rdquo;, and an updated row cannot answer the second one.")

i_cost = registry("Document AI — what it costs per 1,000 pages", [
 ("Quality gate (step 2)", "oss",
  "<strong>Free.</strong> OpenCV, thirty lines. Removes more OCR spend than any other decision here."),
 ("Classification (step 3)", "direct",
  "<strong>Free</strong> if you ask the user. <strong>&asymp; $3</strong> per 1,000 for a cloud "
  "classifier. <strong>&asymp; $1.50</strong> if you classify by running plain OCR and keyword matching."),
 ("Plain OCR (step 4)", "direct",
  "<strong>&asymp; $1.50 per 1,000 pages</strong> on AWS, Google and Azure &mdash; matching to the "
  "cent. Falls to <strong>&asymp; $0.60</strong> at high volume (above roughly 1M/month on Azure, "
  "5M on Google). <strong>Price is not a reason to choose between them.</strong>"),
 ("Identity-document API (step 4+5)", "direct",
  "AWS Textract AnalyzeID and equivalents: <strong>&asymp; $10&ndash;25 per 1,000</strong>. Does the "
  "reading and the field extraction together for ID documents."),
 ("Prebuilt and custom models", "direct",
  "Prebuilt <strong>&asymp; $10 per 1,000</strong>. Custom extraction <strong>&asymp; $30 per "
  "1,000</strong> on both Azure and Google."),
 ("Forms and tables", "direct",
  "AWS Textract: tables <strong>&asymp; $15</strong>, forms <strong>&asymp; $50</strong>, "
  "forms+tables+queries <strong>&asymp; $65&ndash;70</strong> per 1,000. <strong>The wrong tool for "
  "an ID card</strong> &mdash; this is for bank statements and application forms."),
 ("Self-hosted (step 4)", "oss",
  "<strong>No per-page fee.</strong> PaddleOCR, docTR, Tesseract. You pay for CPU, and GPU if you "
  "use a vision model. Check the licence of every model you pull &mdash; some are research-only."),
 ("Human review (step 7)", "direct",
  "<strong>The line that decides your business case.</strong> A reviewer costs the same whether the "
  "document was cheap or expensive to read. If 30% of documents go to review, your real cost per "
  "document is dominated by people, not by API calls."),
], "May 2026") + warn("<strong>Features stack, and one document can hit several meters.</strong> A non-standard document typically runs a classifier (&asymp;$3) and then custom extraction (&asymp;$30), so the real cost is the sum of every model that fires &mdash; not a single headline rate. This is the most common mistake in a document-AI cost estimate.") + note("Two more things that quietly distort estimates. Google bills roughly <strong>$0.05 an hour per deployed custom processor version</strong> &mdash; about <strong>$438 a year</strong> whether or not you send it any traffic. And <strong>multi-page documents bill page by page</strong>, so a 40-page file is 40 billable pages even if you only need page one.") + '''
<p>These figures were verified in May 2026 for <a href="/fintech-ai/identity-onboarding/build-sheet/">Build
Sheet 01</a> and are carried here unchanged. Cloud pricing moves. Check the vendor's calculator before
you commit to a number in a business case.</p>
'''

# ---------------------------------------------------------------- AMBER

a_builds = '''
<h3 id="s-amber-week">The weekend version</h3>
<p><strong>Build:</strong> upload form &rarr; OpenCV quality check &rarr; ask the user what the
document is &rarr; Textract AnalyzeID &rarr; format and checksum validation &rarr; anything uncertain
goes to a spreadsheet a person looks at &rarr; store everything in one Postgres table.</p>
<p><strong>You get:</strong> a working product. Genuinely. Two engineers, one weekend, and it handles
real documents.</p>
<p><strong>It breaks when:</strong> volume passes a few hundred a day, or the review spreadsheet gets
more than one person using it.</p>

<h3 id="s-amber-proper">The proper version &mdash; start here if you are serious</h3>
<p><strong>Build:</strong> everything above, plus &mdash; a real review interface that draws the box
on the image &rarr; one adapter per OCR engine so you can switch &rarr; thresholds in versioned
config &rarr; an append-only evidence table &rarr; corrections captured as training data &rarr;
weekly numbers on queue size and override rate.</p>
<p><strong>You get:</strong> something you can run a business on and show an auditor.</p>
<p><strong>Cost shape:</strong> the API bill is small. The reviewers are the cost.</p>
<p><strong>It breaks when:</strong> nothing, for a long time. This is the right build for almost
everyone.</p>

<h3 id="s-amber-big">The enterprise version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; self-hosted OCR for data that cannot leave
your building &rarr; custom models per document type &rarr; a routing layer that picks the cheapest
engine that will work &rarr; full audit and model governance.</p>
<p><strong>Use when:</strong> millions of documents, or a data-residency rule that rules out the cloud
APIs.</p>
<p><strong>It breaks when:</strong> you build it too early. Most teams that start here spend six
months and end up with the proper version anyway, having paid for the detour.</p>
''' + note("If you take one thing from this page: <strong>build the weekend version first, this week.</strong> Run 200 real documents through it. What you learn in those 200 documents will change your design more than any amount of planning, and you will have thrown away almost nothing.")

a_breaks = '''
<p>Ranked by how often we see them, not by how serious they are.</p>
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>High confidence, wrong value</strong></td><td>Confidence measures how clearly the characters were seen, not whether the answer is right.</td><td>Step 6. Checksums and format rules, always, even on 0.99 fields.</td></tr>
<tr><td><strong>Review queue quietly grows</strong></td><td>Something upstream changed &mdash; a new phone camera, a redesigned document, a vendor model update.</td><td>Chart queue size weekly. A rising line is always upstream.</td></tr>
<tr><td><strong>The cost is triple the estimate</strong></td><td>Features stacked. Classifier plus custom extraction plus tables, all on one document.</td><td>Add up every meter that fires, per document type.</td></tr>
<tr><td><strong>Averaged confidence hides a bad read</strong></td><td>A name joined from two words took the mean instead of the minimum.</td><td>Lowest score wins on any joined field.</td></tr>
<tr><td><strong>The model invented a field</strong></td><td>A language model was asked for JSON and filled in a blank.</td><td>Check every value appears in the OCR text. If not, mark it missing.</td></tr>
<tr><td><strong>Cannot explain a decision from last year</strong></td><td>The record was updated in place, or the thresholds were never stored.</td><td>Append-only, with the threshold version on every row.</td></tr>
<tr><td><strong>Works in the demo, fails in the app</strong></td><td>Demo used clean scans. Real users send photos at night, at an angle, with a thumb over the corner.</td><td>Step 2, and test on photos your own team took on their own phones.</td></tr>
</table>
'''

a_next = '''
<p>This page covered one product. The same eight-step shape appears in others, and once you have
built this you will recognise it.</p>
<div class="mod-grid">
<a href="/fintech-ai/identity-onboarding/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 01</div><h3>Identity &amp; Onboarding</h3><p>Every tool in this space with full pricing, plus the face-match and liveness layer that sits next to this one.</p></a>
<a href="/fintech-ai/identity-onboarding/" class="mod-card"><div class="mod-num">MODULE 01</div><h3>Why this is hard</h3><p>The background: why document reading fails, and what verification actually proves.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 06</div><h3>Grounding &amp; refusal</h3><p>The rule that stops a language model inventing a field, written out properly.</p></a>
<a href="/fintech-ai/regulation-india/" class="mod-card"><div class="mod-num">REFERENCE</div><h3>India regulation</h3><p>What you are allowed to store, for how long, and what the KYC rules require.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Document AI inside a regulated process carries KYC, record-keeping and data-protection obligations. Nothing here is legal advice. Have your retention, consent and review process checked by someone qualified before real customer documents go through it.")

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to use this page", g_read),
   ("What Document AI actually is", g_what),
   ("The whole journey, in one table", g_map),
 ],
 'indigo': [
   ("Steps 1 and 2 — getting a usable file", i_step12),
   ("Steps 3 and 4 — what is it, and reading it", i_step34),
   ("The wiring between step 4 and step 5", i_wiring),
   ("Steps 5 and 6 — fields, and checking them", i_step56),
   ("Steps 7 and 8 — deciding, and keeping proof", i_step78),
   ("What it costs", i_cost),
 ],
 'amber': [
   ("Three versions you could build", a_builds),
   ("What goes wrong", a_breaks),
   ("Where to go next", a_next),
 ],
}

TITLE = "Document AI: How to Build It"
META  = ("Build a document AI product step by step: the eight stages, your options at each one, how "
         "to connect them, and what it costs.")
LEAD  = ("A step-by-step guide to building a document AI product. Eight stages, the options at each "
         "one, exactly how each step connects to the next, real costs, and what breaks. Written for "
         "someone who has not built this before.")

print(f"title len: {len(TITLE + ' | Clarigital')}")
print(f"meta len : {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/products/document-ai",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Product Guide 01",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI")],
  lanes  = lanes,
)
