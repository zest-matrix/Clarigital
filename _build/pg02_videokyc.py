#!/usr/bin/env python3
# Session 70 — PRODUCT GUIDE 02: Video KYC (V-CIP)
import sys; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product, start to finish. The
<a href="/fintech-ai/identity-onboarding/">Identity module</a> explains why verification is hard. The
<a href="/fintech-ai/identity-onboarding/build-sheet/">build sheet</a> lists every tool with prices.
This page tells you which eight steps there are and how to connect them.</p>
<p>It is written for someone who has not built this before.</p>
''' + warn("<strong>Read this before anything else.</strong> Video KYC in India is not a video call with some checks bolted on. It is a <strong>regulated process</strong> where the <em>product</em> is the compliance. Build the video first and the controls later and you will rebuild it. Several of the requirements below &mdash; a proprietary app, infrastructure in your own premises, a concurrent audit before activation &mdash; are architecture decisions, not features.")

g_what = '''
<p>Video KYC lets you open an account for someone who never walks into a branch. A trained officer of
your firm talks to the customer on a live video call, software reads their documents, matches their
face, and confirms a real person is present.</p>
<p>In India it is called <strong>V-CIP</strong> &mdash; Video-based Customer Identification Process
&mdash; and it sits in <strong>Para 19</strong> of the RBI KYC Master Direction.</p>
<p><strong>Why it matters commercially:</strong> a compliant V-CIP session is treated as
<strong>face-to-face</strong>. That is only true of three things &mdash; a physical meeting, digital
KYC with a physical meet, and V-CIP. It means <strong>full CDD, no enhanced-due-diligence
classification, and none of the transaction caps</strong> that apply to OTP-based eKYC.</p>
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not a Zoom call.</strong> The application must be proprietary. Zoom, Teams and Meet are
explicitly out.</li>
<li><strong>Not a liveness check with video attached.</strong> The human officer is a required
control, not a cost to be automated away.</li>
<li><strong>Not finished when the call ends.</strong> A separate team must audit the session
<em>before</em> the account is activated.</li>
</ul>
'''

g_map = '''
<p>Eight steps. Read this once and the rest is detail.</p>
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Can they even start?</strong></td><td>Right device, in India, real connection. Check before you waste an officer's time.</td></tr>
<tr><td>2</td><td><strong>Get consent, on the record</strong></td><td>Recorded, timestamped, and impossible to alter later.</td></tr>
<tr><td>3</td><td><strong>Capture the documents</strong></td><td>Live capture. An uploaded scan does not count.</td></tr>
<tr><td>4</td><td><strong>Prove a real person is there</strong></td><td>Not a photo, not a video, not a deepfake, not a virtual camera.</td></tr>
<tr><td>5</td><td><strong>Match the face to the document</strong></td><td>Is the person on the call the person on the ID?</td></tr>
<tr><td>6</td><td><strong>The conversation</strong></td><td>A trained officer asks questions that cannot be rehearsed.</td></tr>
<tr><td>7</td><td><strong>Decide</strong></td><td>Approve, re-do, or refuse. Three outcomes, never two.</td></tr>
<tr><td>8</td><td><strong>Audit, then activate</strong></td><td>A different team checks the session. Only then does the account open.</td></tr>
</table>
''' + note("Steps 1, 2 and 8 are the ones teams skip, and they are the ones an inspection looks at. A build that does 3&ndash;6 beautifully and skips 8 is not a video KYC product &mdash; it is a video call with face matching.")

code_gate = code('Python — step 1, the pre-flight gate', r'''from ipaddress import ip_address

# RBI requires the customer to be IN INDIA, the app to reject foreign IPs, and
# to detect IP spoofing. Check all of it BEFORE an officer joins the call --
# an officer's time is the most expensive thing in this pipeline.

def preflight(session):
    fail = []

    # 1. GEOTAG. Live GPS from the device, not an IP-derived guess.
    gps = session.get("gps")
    if not gps:
        fail.append("no_gps")                    # permission denied or spoofed
    elif not (6.0 <= gps["lat"] <= 37.5 and 68.0 <= gps["lon"] <= 97.5):
        fail.append("outside_india")             # rough India bounding box

    # 2. IP. Must resolve to India, and must not look like a tunnel.
    ip = session.get("ip")
    if not ip or session["ip_country"] != "IN":
        fail.append("foreign_ip")
    if session.get("is_vpn") or session.get("is_proxy") or session.get("is_hosting"):
        fail.append("ip_spoof_suspected")        # datacentre ASN on a phone = no

    # 3. DO THE TWO AGREE? GPS in Mumbai and IP in Frankfurt is the
    #    interesting case, and it is the one a spoofer produces.
    if "outside_india" not in fail and "foreign_ip" not in fail:
        if session.get("ip_distance_km", 0) > 500:
            fail.append("gps_ip_mismatch")

    # 4. Can the call actually work? A session that dies at step 6 wastes the
    #    officer AND the customer, and they rarely come back.
    if session.get("bandwidth_kbps", 0) < 400: fail.append("bandwidth_too_low")
    if not session.get("camera_ok"): fail.append("no_camera")
    if not session.get("mic_ok"): fail.append("no_mic")

    return {"proceed": not fail, "reasons": fail}

# WHAT TO CHECK
# [ ] GPS is captured live at the START and recorded INTO the video, not read
#     once and stored beside it. The recording itself must carry the coordinates
# [ ] tell the customer WHICH check failed, in plain words. "Please enable
#     location" gets you a session; "Verification failed" gets you a complaint
# [ ] a bounding box is a coarse first filter, not a border. Use it to reject
#     obvious cases fast, and a proper geocoder for the record
# [ ] datacentre and hosting ASNs on a consumer session are the strongest
#     spoofing signal you get. Treat hosting-provider IPs as disqualifying
# [ ] failures are LOGGED with the reason. The distribution tells you whether
#     you have a fraud problem or a UX problem, and they look identical in a
#     total
# [ ] never let a failed pre-flight silently fall back to a different KYC route.
#     That decision is a compliance decision, not an error handler
''')

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Can they even start?</h3>
<p><strong>What it does:</strong> confirms the customer is in India, on a real connection, with a
working camera, before anyone joins the call.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Effort</th><th>Pick this when</th></tr>
<tr><td><strong>A. Browser APIs only</strong></td><td>Geolocation API plus a getUserMedia test.</td><td>A day</td><td>Start here. It catches the honest failures, which are most of them.</td></tr>
<tr><td><strong>B. Add IP intelligence</strong></td><td>A lookup service that tells you country, ASN, and whether the IP is VPN, proxy or hosting.</td><td>Days, small per-lookup fee</td><td>As soon as you are live. Required to detect spoofing.</td></tr>
<tr><td><strong>C. Full device intelligence</strong></td><td>Device fingerprint, emulator detection, rooted-device checks.</td><td>Weeks, licensed</td><td>Volume is high enough that organised attempts are worth defending against.</td></tr>
</table>
''' + code_gate + '''
<p><strong>Connect it to step 2:</strong> a session that passes gets a session id and a recording
handle. Everything after this writes into that one recording &mdash; consent, documents, face, the
conversation. One file, one timeline, one set of timestamps.</p>

<h3 id="s-indigo-s2">Step 2 &mdash; Consent, on the record</h3>
<p><strong>What it does:</strong> captures the customer agreeing, in a form you cannot later be
accused of editing.</p>
<p>The requirement has three parts and teams usually build one: consent must be
<strong>recorded</strong>, <strong>auditable</strong>, and <strong>alteration-proof</strong>.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Pick this when</th></tr>
<tr><td><strong>A. Spoken, inside the recording</strong></td><td>The officer asks, the customer says yes, it is in the video.</td><td>Always. This is the baseline and it satisfies &ldquo;recorded&rdquo;.</td></tr>
<tr><td><strong>B. Hash the recording</strong></td><td>Store a cryptographic hash of the file when the session closes.</td><td>Always. This is what makes &ldquo;alteration-proof&rdquo; a fact rather than a claim.</td></tr>
<tr><td><strong>C. External timestamping</strong></td><td>A trusted timestamp authority signs the hash.</td><td>When you need to prove the file existed at a time, not just that it is unchanged.</td></tr>
</table>
''' + warn("<strong>The gotcha nobody documents:</strong> &ldquo;alteration-proof&rdquo; is usually implemented as <em>we do not have a feature that edits it</em>. That is not the same thing and it will not survive a question from an auditor. <strong>Hash the file on close, store the hash somewhere the video pipeline cannot write to, and re-verify it on retrieval.</strong> It costs almost nothing and it converts a policy claim into arithmetic.")

code_live = code('Python — step 4, and the question that dates your whole build', r'''# Liveness has three generations, and most products are stuck in the first two.
#
#   2019: is this a PHOTO?          -- beaten by playing a video
#   2021: is this a VIDEO REPLAY?   -- beaten by a deepfake
#   2026: is this a DEEPFAKE, and is it even coming from the CAMERA?
#
# The 2026 question is INJECTION. An attacker does not hold a screen up to the
# lens -- they replace the camera feed with a virtual camera driver and send a
# synthetic face straight into your app. Every pixel-level liveness check in the
# world passes, because the pixels are perfect.

def assess_liveness(signals):
    checks = {
        # presentation attack: something held up to a real camera
        "pad_score":        signals["pad_score"] >= 0.90,
        # injection attack: the frames never came from a camera at all
        "camera_is_real":   signals["virtual_camera_detected"] is False,
        "driver_signed":    signals["camera_driver_trusted"],
        "frame_timing_ok":  signals["frame_interval_variance"] > 0.0001,
        # a synthetic stream is often TOO regular. Real cameras jitter.
        "sensor_noise_ok":  signals["sensor_noise_present"],
    }
    failed = [k for k, v in checks.items() if not v]
    if "camera_is_real" in failed or "driver_signed" in failed:
        return {"outcome": "reject_hard", "reason": "injection_suspected",
                "escalate": True}
    if failed:
        return {"outcome": "retry", "reason": failed, "attempts_allowed": 2}
    return {"outcome": "pass"}

# WHAT TO CHECK
# [ ] ASK EVERY VENDOR: "do you detect virtual-camera injection?" The answer
#     tells you whether you are buying a 2021 product or a 2026 one. It is the
#     single most useful question in this whole procurement
# [ ] ask for iBeta PAD certification and the LEVEL. Level 1 is photos and
#     screens; Level 2 is masks. Neither covers injection -- that is separate
# [ ] DO NOT require blinking or smiling. RBI's FAQ (Q20) says specific facial
#     gestures are not mandatory, and accommodation is required for customers
#     who cannot perform them. A gesture-gated flow excludes disabled customers
#     and is a conduct problem as well as an accessibility one
# [ ] an injection signal is a HARD reject and an escalation, not a retry. A
#     retry just tells the attacker which check fired
# [ ] log the raw scores, not the verdict. Thresholds change; the evidence of
#     what you saw should not have to be recomputed
# [ ] rehearse a failure. If your liveness vendor is down, what happens? The
#     answer must not be "approve anyway"
''')

i_step34 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; Capture the documents</h3>
<p><strong>What it does:</strong> gets the identity documents into the session, live.</p>
<p><strong>Live capture is mandatory.</strong> An uploaded scan does not meet the standard, however
clear it is. The document has to be shown to the camera during the session.</p>
<table>
<tr><th>Route</th><th>What it gives you</th><th>Note</th></tr>
<tr><td><strong>DigiLocker / offline Aadhaar XML</strong></td><td>The issued record, already verified.</td><td>XML or QR must be <strong>no older than three days</strong>.</td></tr>
<tr><td><strong>Live PAN capture</strong></td><td>An image verified against the authorised database.</td><td>Verification against the database, not just a reading of the card.</td></tr>
<tr><td><strong>Other OVD via live capture</strong></td><td>For customers without the above.</td><td>Reading and structuring is <a href="/fintech-ai/products/document-ai/">Document AI</a> &mdash; the same eight steps, inside this one.</td></tr>
</table>
''' + warn("<strong>The Aadhaar number must be redacted in your records.</strong> Not masked in the UI &mdash; redacted in what you store. Teams capture a clean frame of the Aadhaar card into the video recording and then discover the recording itself now contains the full number, retained for years. <strong>Decide where redaction happens before you record anything</strong>, because you cannot un-record.") + '''

<h3 id="s-indigo-s4">Step 4 &mdash; Prove a real person is there</h3>
<p><strong>What it does:</strong> confirms the face on the call belongs to a living human who is
actually present.</p>
''' + code_live + '''
<p><strong>The gotcha nobody documents:</strong> injection. Every liveness product sold before about
2023 answers the question <em>&ldquo;does this look like a real face?&rdquo;</em>. A virtual camera
makes that question meaningless, because the synthetic face is a perfect one. The question that
matters in 2026 is <em>&ldquo;did these frames come from a physical camera on this device?&rdquo;</em>
&mdash; and it is answered with driver checks, frame-timing analysis and sensor-noise detection, not
with a better face model.</p>
'''

i_step56 = '''
<h3 id="s-indigo-s5">Step 5 &mdash; Match the face to the document</h3>
<p><strong>What it does:</strong> compares the live face with the photo on the identity document.</p>
<table>
<tr><th>Option</th><th>What it is</th><th>Pick this when</th></tr>
<tr><td><strong>A. Vendor API</strong></td><td>Send both images, get a similarity score.</td><td>Almost always. This is a commodity and not where your effort belongs.</td></tr>
<tr><td><strong>B. Self-hosted model</strong></td><td>Run face matching on your own infrastructure.</td><td>Residency rules make sending faces out impossible, or volume justifies it.</td></tr>
</table>
<p>The technical work is small. The <em>policy</em> work is not, and it is yours:</p>
<ul>
<li><strong>Set the threshold deliberately, and write down why.</strong> It trades false accepts
against false rejects and both are harms.</li>
<li><strong>Test on your own population.</strong> Face matching accuracy varies by skin tone, age and
gender across every published evaluation. A threshold tuned on a vendor's demo set is a threshold
tuned on somebody else's customers.</li>
<li><strong>A low score is a human decision, not an automatic refusal.</strong> The officer is on the
call already. That is the point of them.</li>
</ul>

<h3 id="s-indigo-s6">Step 6 &mdash; The conversation</h3>
<p><strong>What it does:</strong> a trained officer of your firm talks to the customer and forms a
judgement.</p>
<p>This step cannot be automated away. The officer must be <strong>your</strong> trained official,
must run a <strong>randomised</strong> set of questions so nothing can be pre-rehearsed, and must be
able to act on anything that looks wrong.</p>
''' + note("<strong>Design the question bank as data, not as a script in someone's head.</strong> A pool of questions, drawn at random, with the drawn set recorded against the session. Then &ldquo;were the questions randomised&rdquo; has an answer you can produce, and a coached applicant cannot be fed the list. This is cheap to build on day one and awkward to retrofit.") + '''
<p>Give the officer a single screen with everything already on it: the document reading, the face
match score, the liveness result, the pre-flight signals. An officer hunting through tabs during a
live call is the most common cause of a rushed judgement.</p>
'''

code_audit = code('Python — steps 7 and 8, and the one nobody budgets for', r'''from datetime import datetime, timedelta, timezone
IST = timezone(timedelta(hours=5, minutes=30))

# THREE OUTCOMES. A two-outcome system either rejects good customers or
# approves bad sessions, and usually both.

def officer_decision(session, checks, officer):
    if checks["liveness"]["outcome"] == "reject_hard":
        return {"outcome": "reject", "reason": "injection_suspected",
                "reviewable": True}       # a person can still overturn it
    if not checks["documents_valid"] or checks["face_match"] < session["threshold"]:
        return {"outcome": "redo", "reason": "quality_or_match",
                "guidance": "explain WHICH part, in plain words"}
    return {"outcome": "recommend_approve", "by": officer["id"],
            "at": datetime.now(IST).isoformat()}

# STEP 8. The officer RECOMMENDS. A DIFFERENT team approves. The account does
# not exist until that second team has looked. This is a hard requirement and
# it is the step product teams discover three weeks before launch.

def concurrent_audit(session, auditor):
    assert auditor["team"] != session["officer_team"], "auditor must be independent"
    findings = []
    for need in ("recording_present", "gps_in_recording", "timestamps_present",
                 "consent_captured", "officer_credentials_recorded",
                 "questions_randomised", "aadhaar_redacted", "hash_matches"):
        if not session.get(need):
            findings.append(need)
    return {"activate": not findings, "findings": findings,
            "auditor": auditor["id"], "at": datetime.now(IST).isoformat()}

# WHAT TO CHECK
# [ ] the auditor is a DIFFERENT TEAM. Asserted in code, not in a policy
#     document. This is the most commonly faked control in the whole process
# [ ] account activation is gated on the audit result. If an account can exist
#     before the audit, the audit is decorative
# [ ] "redo" tells the customer which part failed. A blank retry produces the
#     same failure and then an abandoned application
# [ ] the hash from step 2 is re-verified HERE, at audit time. Checking it only
#     at write time proves nothing about the intervening days
# [ ] audit capacity is planned as a number. It is a person per N sessions and
#     it does not scale by deploying more servers -- this is the line that
#     silently caps your onboarding volume
# [ ] measure the audit FAILURE rate weekly. Near zero means the audit is a
#     rubber stamp; rising means something upstream broke
# [ ] rejections are reviewable by a human on request. "The system said no" is
#     not an answer you can give a customer about their bank account
''')

i_step78 = '''
<h3 id="s-indigo-s7">Steps 7 and 8 &mdash; Decide, audit, then activate</h3>
''' + code_audit + '''
<p><strong>The gotcha nobody documents:</strong> the concurrent audit is a
<strong>capacity constraint, not a feature</strong>. Every session must be reviewed by an independent
team before the account activates. That is a person, reviewing recordings, at some rate per hour.
Your onboarding throughput is capped by that number and no amount of infrastructure changes it.
Teams model gateway costs and liveness costs carefully and then discover the ceiling on launch week.
<strong>Work out your audit rate before you forecast volume.</strong></p>
'''

i_cost = registry("Video KYC &mdash; what it costs", [
 ("V-CIP platform, per verification", "direct",
  "Published entry pricing from around <strong>&#8377;10 per verification</strong> for an API "
  "covering V-CIP, liveness, PAN, Aadhaar XML and DigiLocker. Enterprise deals are negotiated per "
  "volume and usually bundle the components."),
 ("Liveness and injection detection", "direct",
  "Sometimes bundled, sometimes a separate meter. <strong>Ask whether injection detection is "
  "included or an add-on</strong> &mdash; the ones that charge separately are often the ones that "
  "actually have it."),
 ("Document reading", "direct",
  "See <a href=\"/fintech-ai/products/document-ai/\">Document AI</a>. Plain OCR is about $1.50 per "
  "1,000 pages; identity-document APIs are $10&ndash;25."),
 ("IP intelligence", "direct",
  "Per-lookup, small. Required rather than optional &mdash; foreign-IP rejection and spoof detection "
  "are explicit requirements."),
 ("The officer", "direct",
  "A trained employee of <em>your</em> firm, on a live call, for the length of the session. "
  "<strong>Not outsourceable in the way a contact centre is</strong>, because the training and the "
  "judgement are regulatory requirements."),
 ("The concurrent auditor", "direct",
  "<strong>A second person, on a different team, for every single session.</strong> The line nobody "
  "budgets and the one that caps throughput."),
 ("Storage", "direct",
  "Encrypted video, retained, <strong>in India</strong>, with tamper evidence. Video is large and "
  "retention is long; this grows quietly and is rarely in the first model."),
], "September 2026") + warn("<strong>Model cost per COMPLETED onboarding, not per session.</strong> Sessions fail &mdash; bad connections, failed liveness, documents that will not read, customers who drop. If 30% of sessions do not complete, your real cost per customer is the session cost divided by 0.7, plus the officer and auditor time spent on the ones that failed. That is a very different number from the vendor's per-verification rate.")

a_builds = '''
<h3 id="s-amber-week">The two-week version</h3>
<p><strong>Build:</strong> browser pre-flight &rarr; a bought V-CIP platform that handles video,
liveness, capture and face match &rarr; your own officer console &rarr; a simple audit queue &rarr;
Postgres for the evidence record.</p>
<p><strong>You get:</strong> something compliant enough to test with real customers under supervision.</p>
<p><strong>It breaks when:</strong> volume passes what one auditor can review in a day.</p>

<h3 id="s-amber-proper">The proper version &mdash; start here if you are serious</h3>
<p><strong>Build:</strong> everything above, plus &mdash; IP intelligence with spoof detection &rarr;
injection detection confirmed with the vendor <em>in writing</em> &rarr; a randomised question bank
as data &rarr; hashing at session close and re-verification at audit &rarr; an officer console with
every signal on one screen &rarr; audit capacity modelled as a number &rarr; weekly metrics on
completion rate, audit failure rate and reason distribution.</p>
<p><strong>Trade:</strong> you own the orchestration, the evidence and the thresholds. That is the
right trade &mdash; those three are what an inspection examines, and none of them is something a
vendor can hold for you.</p>

<h3 id="s-amber-big">The enterprise version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; self-hosted face match and liveness for
residency &rarr; device intelligence &rarr; a dedicated audit function with its own tooling &rarr;
full model governance on the matching thresholds.</p>
<p><strong>It breaks when:</strong> you build it before you have run a thousand real sessions and
learned where your own failures actually are.</p>
''' + note("If you take one thing from this page: <strong>work out your concurrent-audit rate in week one.</strong> Everything else on this page can be bought, tuned or fixed later. That number is a hard ceiling on how many customers you can onboard per day, it is set by people rather than technology, and almost nobody discovers it until they need the capacity.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Liveness passes a deepfake</strong></td><td>The product answers &ldquo;is this a real face&rdquo;, not &ldquo;did this come from a camera&rdquo;.</td><td>Injection detection. Ask the vendor the question directly.</td></tr>
<tr><td><strong>The recording contains an un-redacted Aadhaar</strong></td><td>Redaction was designed for the UI, not for the stored video.</td><td>Decide redaction before you record. You cannot un-record.</td></tr>
<tr><td><strong>Onboarding volume hits a wall</strong></td><td>The concurrent audit is one person per N sessions.</td><td>Model audit capacity before forecasting volume.</td></tr>
<tr><td><strong>Disabled customers cannot complete</strong></td><td>The flow requires blinking or smiling.</td><td>Not mandatory per the RBI FAQ. Remove the gesture gate.</td></tr>
<tr><td><strong>&ldquo;Alteration-proof&rdquo; cannot be demonstrated</strong></td><td>It meant &ldquo;we have no edit feature&rdquo;.</td><td>Hash on close, store it out of reach, re-verify at audit.</td></tr>
<tr><td><strong>Sessions die at step 6</strong></td><td>No bandwidth check at step 1.</td><td>Pre-flight. The officer's time is the expensive part.</td></tr>
<tr><td><strong>Audit failure rate is near zero</strong></td><td>It is a rubber stamp.</td><td>Sample and re-review. A control nobody fails is not a control.</td></tr>
</table>
'''

a_next = '''
<div class="mod-grid">
<a href="/fintech-ai/products/document-ai/" class="mod-card"><div class="mod-num">GUIDE 01</div><h3>Document AI</h3><p>Step 3 of this page is that whole product, nested inside this one. Eight steps, same shape.</p></a>
<a href="/fintech-ai/identity-onboarding/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 01</div><h3>Identity &amp; Onboarding</h3><p>Every tool with prices, including the face-match and liveness vendors.</p></a>
<a href="/fintech-ai/aml-compliance/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 04</div><h3>AML &amp; Compliance</h3><p>Screening runs on the name this process captured. Wrong name in, wrong screen out.</p></a>
<a href="/fintech-ai/regulation-india/" class="mod-card"><div class="mod-num">REFERENCE</div><h3>India regulation</h3><p>The KYC Master Direction, retention rules and what counts as face-to-face.</p></a>
</div>
''' + warn("This page is a guide, not a specification. V-CIP is a regulated process and a non-compliant onboarding is a supervisory matter, not a bug. Nothing here is legal advice. Have your flow, your retention and your audit process reviewed by qualified counsel and your compliance officer before a real customer joins a call.")

SRC = [
 ('official','RBI KYC Master Direction, Para 19','the V-CIP framework: trained official, live recording, geo-tagging, liveness, IP control, concurrent audit and the face-to-face equivalence.','https://www.rbi.org.in'),
 ('official','RBI sector-specific KYC Master Directions, 28 November 2025','the replacement of the 2016 Direction and the extension of V-CIP to ten institution types including payment aggregators.','https://www.rbi.org.in'),
 ('official','RBI KYC FAQs','Q20 — specific facial gestures such as blinking or smiling are not mandatory for the liveness check, with accommodation required.','https://www.rbi.org.in'),
 ('official','UIDAI','offline Aadhaar XML and QR, the three-day freshness limit, and the redaction requirement.','https://uidai.gov.in'),
 ('official','DigiLocker','issued-document retrieval as an OVD route inside the session.','https://www.digilocker.gov.in'),
 ('industry','V-CIP platform pricing and capability reporting','the ~₹10 per verification entry point, iBeta PAD levels, and the injection-detection question. Vendor-published and third-party compiled; confirm in writing.',''),
]
CSSRC = None
import re as _re
_src = open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC = _re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}', _src, _re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'
            +(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>'
            for k,n,w,u in SRC)
a_src = ('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check '
 'it. Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. V-CIP rules changed materially in 2025; the date is part of the claim.</p></div>')

lanes = {
 'green': [("How to use this page", g_read),("What Video KYC actually is", g_what),
           ("The whole journey, in one table", g_map)],
 'indigo':[("Steps 1 and 2 — can they start, and consent", i_step12),
           ("Steps 3 and 4 — documents, and proving a real person", i_step34),
           ("Steps 5 and 6 — face match and the conversation", i_step56),
           ("Steps 7 and 8 — decide, audit, activate", i_step78),
           ("What it costs", i_cost)],
 'amber': [("Three versions you could build", a_builds),("What goes wrong", a_breaks),
           ("Where to go next", a_next + a_src)],
}

TITLE="Video KYC: How to Build It"
META=("Build a video KYC product step by step: the eight stages, your options at each one, how to "
      "connect them, and what RBI actually requires.")
LEAD=("A step-by-step guide to building a V-CIP video KYC product. Eight stages, the options at each "
      "one, exactly how each step connects to the next, real costs, and what breaks. Written for "
      "someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/video-kyc", title=TITLE, meta=META, lead=LEAD,
     label="Product Guide 02",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")], lanes=lanes)

# ensure the sources CSS is present
import io as _io
f='fintech-ai/products/video-kyc/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h:
    _io.open(f,'w',encoding='utf-8').write(h.replace('</style>',CSSRC+'\n</style>',1))
    print("sources CSS added")
