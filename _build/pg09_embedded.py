#!/usr/bin/env python3
# Session 81 — PRODUCT GUIDE 09: Embedded insurance
# First page on this site under IRDAI. Verified September 2026.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product: selling an insurance policy inside a journey the
customer came for something else. A phone with screen cover at checkout. Trip cover in a booking flow.
Hospital cash alongside a loan. The insurance is two taps, and everything difficult about it sits
behind those two taps.</p>
<p>This is the first page on this site under <strong>IRDAI</strong> rather than RBI or SEBI. If you
have built a lending or payments product, almost none of your regulatory instincts transfer.</p>
''' + warn("<strong>1 January 2027 is a hard date and two different regulators land on it.</strong> From that day the <strong>IRDAI (Insurance Intermediaries) (Amendment) Regulations, 2026</strong> (notified 30 July 2026) require every proposal form, policy and certificate of insurance to carry the name and functional identity of the person who sold it. The same day, the <strong>RBI Responsible Business Conduct (Second Amendment) Directions, 2026</strong> (notified 15 June 2026) take effect for banks and NBFCs, banning compulsory bundling and dark patterns. <strong>Both changes land on the checkout screen, not in the policy document.</strong>")

g_what = '''
<p>Embedded insurance is <strong>distribution</strong>. You are not the insurer, you do not carry the
risk, you do not decide claims, and in most designs the money is not yours for more than a day. What
you own is the moment the customer is offered cover, and the obligations that attach to that moment.</p>
<p>Four roles. Work out which one you are before anything else, because every later answer depends
on it:</p>
<table>
<tr><th>Role</th><th>What it does</th><th>What it needs</th></tr>
<tr><td><strong>Insurer</strong></td><td>Underwrites, prices, files the product, pays claims.</td><td>An insurance licence. Almost certainly not you.</td></tr>
<tr><td><strong>Intermediary</strong></td><td>Solicits and procures the policy, and services the policyholder.</td><td><strong>IRDAI registration</strong> &mdash; corporate agent, broker or insurance marketing firm.</td></tr>
<tr><td><strong>Platform</strong></td><td>Owns the surface the customer is standing on.</td><td>Nothing, on its own. <strong>Which is the trap.</strong></td></tr>
<tr><td><strong>Master policyholder</strong></td><td>Holds a group policy under which members are covered.</td><td>A group that <strong>already exists</strong>. See step 2.</td></tr>
</table>
''' + warn("<strong>The three designs most teams reach for first are the three that do not work.</strong><br><br><strong>1. Referral for a revenue share.</strong> &ldquo;We just send traffic, the insurer does the selling.&rdquo; If you are presenting products, taking the customer through a choice and being paid for the outcome, you are soliciting insurance for remuneration. That needs registration, whatever the contract calls it.<br><br><strong>2. A group policy covering &lsquo;our customers&rsquo;.</strong> Buy one master policy, enrol buyers into it as they arrive, no intermediary licence required. The <strong>Protection of Policyholders&rsquo; Interests Regulations, 2024</strong> closed this: the group must be in existence <em>before</em> the policy is issued, and a master policyholder obtains cover only after the group has been formed and its members enrolled. You cannot constitute a group out of people who have not bought anything yet.<br><br><strong>3. Cover folded in so it cannot be declined.</strong> Barred for a corporate agent selling insurance alongside a principal product, and from 1 January 2027 barred outright for banks and NBFCs under the RBI Directions.") + '''
<p><strong>What embedded insurance is not:</strong></p>
<ul>
<li><strong>Not a feature.</strong> It is a regulated activity with a registration, a net worth, a
named officer and an annual fee.</li>
<li><strong>Not a payments integration.</strong> The premium is not revenue and the settlement clock
is not yours. Step 5.</li>
<li><strong>Not finished at issuance.</strong> Servicing the policyholder is a separate, explicitly
non-delegable obligation. Step 8.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Are you allowed to sell it?</strong></td><td>Answer this before designing a screen.</td></tr>
<tr><td>2</td><td><strong>Pick the structure</strong></td><td>Corporate agent, broker, marketing firm &mdash; or someone else&rsquo;s licence.</td></tr>
<tr><td>3</td><td><strong>Product and insurer</strong></td><td>What can be embedded, and how many insurers you may hold.</td></tr>
<tr><td>4</td><td><strong>The offer on the page</strong></td><td>Consent, disclosure, and the patterns now banned.</td></tr>
<tr><td>5</td><td><strong>Take the money</strong></td><td><strong>24 hours, in full, no netting.</strong> The step that gets penalised.</td></tr>
<tr><td>6</td><td><strong>Issue and deliver</strong></td><td>Electronic policy, and from 2027 a named seller on it.</td></tr>
<tr><td>7</td><td><strong>Free look, cancellation, refund</strong></td><td>The refund that must not flow back through you.</td></tr>
<tr><td>8</td><td><strong>Service the policyholder</strong></td><td>Grievances and claims support. Non-delegable.</td></tr>
</table>
''' + note("<strong>Steps 1, 5, 7 and 8 are the ones people skip, and they are the ones an inspection looks at.</strong> Steps 3 and 4 are where the product feels like a product. A build that does 3 and 4 beautifully and skips the rest is a nicely designed checkout add-on that somebody is going to be fined for.")

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Are you allowed to sell it?</h3>
<p>Soliciting or procuring insurance for remuneration requires registration with IRDAI. There is no
de minimis, no pilot exemption and no version of this that waits until you have traction.</p>
<p>The one useful shortcut: <strong>every insurer must offer a search tool on its own website letting
anyone verify which distribution channels are authorised to sell its policies.</strong> That
requirement came in with the 2024 policyholder regulations. Before you sign anything with a partner
who says they will handle the licensing, go and look yourself.</p>

<h3 id="s-indigo-s2">Step 2 &mdash; Pick the structure</h3>
<table>
<tr><th>Route</th><th>You represent</th><th>Suits</th><th>Cost of entry</th></tr>
<tr><td><strong>Corporate agent</strong></td><td>The insurer</td><td>Most embedded products. A fixed panel, one integration each.</td><td><strong>&#8377;50 lakh net worth</strong>, held at all times</td></tr>
<tr><td><strong>Insurance broker</strong></td><td><strong>The customer</strong></td><td>Genuine comparison across the market, with a written recommendation.</td><td>Higher capital, higher duty</td></tr>
<tr><td><strong>Insurance marketing firm</strong></td><td>The insurer, area-restricted</td><td>Smaller, regional distribution.</td><td>Lower, and narrower in scope</td></tr>
<tr><td><strong>Someone else&rsquo;s licence</strong></td><td>Nobody &mdash; you are a vendor</td><td>Testing demand before committing.</td><td><strong>You may not be paid for the sale</strong></td></tr>
</table>
<p><strong>Corporate agent, in numbers.</strong> Up to <strong>nine life, nine general and nine health
insurers</strong>; a composite corporate agent may hold up to <strong>27 arrangements in total</strong>.
A corporate agent (general) is limited to retail lines plus commercial lines with a total sum insured
<strong>not exceeding &#8377;5 crore per risk</strong>. Net worth <strong>&#8377;50 lakh at all
times</strong> for an entity doing insurance intermediation exclusively, and where you have another
business, the two must be kept at <strong>arm&rsquo;s length</strong>. A principal officer who is a
graduate, has completed <strong>50 hours</strong> of Insurance Institute of India training and passed
the examination. Any tie-up entered into, modified or terminated must be disclosed to IRDAI
<strong>within 30 days</strong>.</p>
''' + warn("<strong>Registration is now continuous, and that created a deadline rather than removing one.</strong> The <strong>Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Act, 2025</strong> came into force on <strong>5 February 2026</strong> and replaced three-year renewals with registration that runs until it is surrendered, suspended or cancelled, against an annual fee of <strong>the higher of &#8377;10,000 or 0.04% of commission and other receipts from insurers in the preceding financial year</strong>. <strong>Existing three-year registrants must apply for a fresh certificate by 31 January 2027</strong>, with late applications accepted to <strong>31 March 2027</strong> on reasons and an additional <strong>&#8377;750</strong>. Miss that and the entity ceases to act as an intermediary and must register from scratch. If your embedded product runs on a partner&rsquo;s registration, this deadline is theirs and the outage is yours &mdash; ask them for the date they filed.")

i_step34 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; Product and insurer</h3>
<p>Embedded works when the cover is <strong>small, specific and obviously connected to what the
customer is already doing</strong>. Screen damage on a phone. Delay and cancellation on a trip.
Shipment cover on a consignment. Hospital cash beside a loan. The further the cover drifts from the
purchase, the more it looks like an unrelated financial product sold on impulse &mdash; which is
precisely how the mis-selling definitions are drawn.</p>
''' + note("<strong>Your commission is not a commercial negotiation, it is a regulatory envelope.</strong> Since the product-level caps were removed in 2023 and consolidated into the <strong>Expenses of Management (including Commission) Regulations, 2024</strong>, an insurer sets what it pays you within an overall ceiling: <strong>30% of gross written premium for a general insurer, 35% for a standalone health insurer</strong>, and segment-level limits for life. An insurer that wants your distribution badly still cannot pay you out of a bucket that is full. Enforcement is real: one standalone health insurer was restricted from opening new branches for six months over a breach in FY25.") + '''

<h3 id="s-indigo-s4">Step 4 &mdash; The offer on the page</h3>
<p>This is the step that changes on 1 January 2027, and the changes are in your interface, not in
your contracts.</p>
<table>
<tr><th>Pattern</th><th>Status</th></tr>
<tr><td>Cover pre-ticked, customer unticks to decline</td><td><strong>Banned</strong> &mdash; pre-selected add-on</td></tr>
<tr><td>&ldquo;No thanks&rdquo; rendered small, grey or below the fold</td><td><strong>Banned</strong> &mdash; hidden decline</td></tr>
<tr><td>Countdown timer on the insurance offer</td><td><strong>Banned</strong> &mdash; false urgency</td></tr>
<tr><td>Premium appearing only at the payment screen</td><td><strong>Banned</strong> &mdash; drip pricing</td></tr>
<tr><td>Cover required to complete the main purchase</td><td><strong>Banned</strong> &mdash; compulsory bundling and forced action</td></tr>
<tr><td>Cover required, but the customer may buy it anywhere</td><td><strong>Permitted</strong> where it is a genuine risk mitigant</td></tr>
<tr><td>Cancelling the cover is harder than buying it</td><td><strong>Banned</strong> &mdash; subscription trap</td></tr>
</table>
<p>Those come from the RBI Directions and bind banks and NBFCs. <strong>If you are neither, they do
not bind you and you should build to them anyway</strong> &mdash; IRDAI reached the same conclusion
by a different route when it penalised a distributor for ranking products as &ldquo;top&rdquo; and
&ldquo;best&rdquo; with no objective basis, and your insurer partner is bound even where you are not.</p>
'''

code_offer = code('Python — steps 4 and 5, the offer and the premium that is not yours', r'''from datetime import datetime, timedelta
from decimal import Decimal

# STEP 4. THE OFFER.
# The rule is not "get consent", it is "be able to show what they saw".
# Store the RENDERED offer, not the inputs that produced it. Six months from
# now the premium table, the wording and the layout will all have changed, and
# the question in a complaint is always: what did this person actually see.

def render_offer(quote, product):
    return {
        "default_selected": False,          # NEVER pre-tick. Not a growth lever.
        "decline_equally_prominent": True,  # same size, same weight, same row
        "premium_shown_inclusive": quote["premium_paise"],   # no drip pricing
        "gst_shown_separately": quote["gst_paise"],
        "insurer_named": product["insurer_legal_name"],      # not your brand
        "your_role_disclosed": "corporate_agent",            # say what you are
        "cis_url": product["customer_information_sheet_url"],
        "no_countdown": True,
        "main_purchase_blocked_if_declined": False,          # assert, don't hope
    }

def record_consent(session, offer):
    assert offer["default_selected"] is False, "pre-selected cover is a defect"
    return {
        "customer_id": session["customer_id"],
        "at": datetime.utcnow().isoformat(),
        "action": "ACCEPTED",                 # explicit, affirmative, logged
        "offer_snapshot_hash": sha256_of(offer),   # what they saw
        "offer_snapshot_blob": offer,              # keep the blob, not a recipe
        "channel": session["channel"],
    }

# STEP 5. THE PREMIUM. THIS IS THE ONE.
# Section 64VB, Insurance Act 1938: the insurer may not assume risk until the
# premium is received. Sub-section (4): where you collect premium on the
# insurer's behalf you must deposit or dispatch it to the insurer IN FULL,
# WITHOUT DEDUCTING YOUR COMMISSION, WITHIN 24 HOURS of collection, excluding
# bank and postal holidays.
#
# Your PSP settles T+2. Your finance system nets fees. Both are wrong here,
# and both are wrong by default rather than by anyone's decision.

REMIT_HOURS = 24

def remittance_due(collected_at, holidays):
    due, remaining = collected_at, timedelta(hours=REMIT_HOURS)
    while remaining > timedelta(0):
        due += timedelta(hours=1)
        if due.date() not in holidays:       # bank and postal holidays excluded
            remaining -= timedelta(hours=1)
    return due

def build_remittance(collections, commission_ledger):
    """One job: move the gross premium. Commission is settled separately."""
    gross = sum(Decimal(c["premium_paise"]) for c in collections)
    netted = sum(Decimal(c.get("commission_withheld_paise", 0)) for c in collections)
    assert netted == 0, "commission may not be deducted from premium remitted"
    commission_ledger.accrue(collections)    # invoice the insurer, separately
    return {"to": "insurer", "amount_paise": gross, "basis": "gross"}

def cover_status(policy, remittance):
    # What the customer is told must track what is legally true.
    if not remittance or not remittance["confirmed_by_insurer"]:
        return "COVER_PENDING"               # not "Insured". Not a tick.
    return "COVER_ACTIVE"

# WHAT TO CHECK
# [ ] measure remittance age as a QUEUE with an owner, in hours, not as a
#     month-end reconciliation. A regulator sampled 67 policies and found
#     delays beyond 30 days; the same order covered 8,971 policies at 5-24
#     days and roughly 77,033 that simply took longer than three working days,
#     because three working days was the design
# [ ] never net commission out of premium. Accrue it and invoice separately
# [ ] the premium account is not a revenue account. It should not appear in
#     your cash position, your runway, or any sweep
# [ ] do not render "Insured" before the insurer confirms receipt. A tick in
#     your UI does not attach risk; Section 64VB does
# [ ] a payment that succeeds at your PSP and fails to remit is an OPEN
#     obligation, not a resolved transaction
# [ ] reconcile in IST against the insurer's own receipt confirmation, never
#     against your settlement file
''')

i_step5 = '''
<h3 id="s-indigo-s5">Step 5 &mdash; Take the money, and understand whose it is</h3>
''' + code_offer + '''
<p><strong>The gotcha that defines this product:</strong> <strong>the premium is not your money and
the clock is 24 hours, not your settlement cycle.</strong> Every embedded checkout has the same
shape &mdash; the customer pays you, your payment gateway settles to you in a day or two, your
finance system nets what you are owed, and the balance goes out. Each of those three steps is
sensible. Together they breach a 1938 statute.</p>
<p>This is not a theoretical exposure. In an order dated <strong>4 August 2025</strong>, IRDAI fined
a large online distributor <strong>&#8377;5 crore</strong> under section 102 of the Insurance Act
across <strong>eleven charges</strong>, six of which carried <strong>&#8377;1 crore each</strong>.
Premium remittance was one of them. The finding was not that something went wrong occasionally: the
firm collected through <strong>its own payment gateway into its own nodal account</strong>, and
<strong>a minimum of three working days to remit was how the system was built.</strong> A sample of
67 policies showed delays of more than <strong>30 days</strong>. Another <strong>8,971</strong> ran
<strong>5 to 24 days</strong> late. Roughly <strong>77,033</strong> simply took longer than three
working days.</p>
''' + note("<strong>The inspection was in June 2020. The show-cause notice came in October 2024. The order came in August 2025.</strong> Five years from the look to the bill. Whatever your embedded product is doing today is being assessed against rules you will be judged on years from now, and &ldquo;nobody has said anything&rdquo; is not evidence of anything at all.")

code_after = code('Python — steps 6 to 8, issuance, refunds and the servicing you cannot outsource', r'''# STEP 6. ISSUE AND DELIVER.
# Policies are issued in electronic form. From 1 January 2027 the proposal
# form, the policy and the certificate of insurance must each carry the name
# and functional identity of the person who sold it, plus the mobile number
# and email of the office through which it was sold.
#
# For an embedded product this is a SCHEMA CHANGE, not a compliance task. A
# checkout has no salesperson. You now need a defined, named, resolvable
# identity attached to every sale, and a policy-wise sales record the
# regulator can reach remotely.

def sale_attribution(session, staff_registry):
    """Every policy needs an answer to 'who sold this'. Decide it now."""
    person = staff_registry.resolve(session)     # specified person / POS person
    assert person is not None, "unattributed sale: do not issue"
    assert person["certificate_active"], "seller certificate lapsed"
    return {
        "seller_name": person["name"],
        "functional_identity": person["irdai_role"],  # e.g. specified person
        "office_mobile": person["office"]["mobile"],
        "office_email": person["office"]["email"],
    }

# STEP 7. FREE LOOK, CANCELLATION AND REFUND.
# Free look is 30 days for health, and for life policies with a term of a year
# or more, from receipt of the policy document. Separately, a retail
# policyholder may cancel at any time and receive a refund for the unexpired
# period.
#
# Section 64VB(3): a refund of premium is paid by the INSURER DIRECTLY to the
# INSURED, and shall in no case be credited to the account of the agent.

def cancellation(policy, reason, your_psp):
    route = {"payer": "insurer", "payee": "policyholder_bank_account"}
    # The one line that matters. Your checkout refunds the cart. The insurance
    # line is not part of the cart for this purpose.
    assert route["payer"] != "platform", "premium refunds do not flow through you"
    your_psp.exclude_line(policy["order_line_id"], reason="statutory_refund_route")
    return {"route": route, "clawback": "commission_reversed_via_insurer_ledger"}

# STEP 8. SERVICING. NON-DELEGABLE.
def grievance_channels(config):
    """A generic support queue is not an insurance grievance channel."""
    required = [
        config["insurance_specific_web_page"],   # published, findable
        config["ivr_option_for_insurance"],      # an actual option on the line
        config["named_grievance_officer"],
        config["turnaround_and_escalation_published"],
        config["route_to_insurer_and_ombudsman_published"],
    ]
    assert all(required), "CRM tagging is not a grievance framework"
    return required

# WHAT TO CHECK
# [ ] decide the seller identity model before 1 January 2027, not after. It
#     touches your proposal payload, your policy record and your sales log
# [ ] a lapsed specified-person certificate must block issuance, not warn
# [ ] refunds never leave your accounts. Exclude the insurance line from cart
#     refunds explicitly, in code, with a test
# [ ] renewal notices are an obligation, not a marketing campaign, and their
#     absence has been penalised
# [ ] publish the insurance grievance route on the website AND put it on the
#     phone line. Both have been found missing, in the same order
# [ ] keep policy-wise sales records in a form a regulator can access
#     remotely, including the call or session record where one exists
''')

i_step68 = '''
<h3 id="s-indigo-s6">Steps 6 to 8 &mdash; Issue, refund, service</h3>
''' + code_after + '''
<p><strong>The gotcha that costs the most to retrofit:</strong> <strong>servicing the policyholder is
a distinct and non-delegable obligation, and your existing support stack almost certainly does not
discharge it.</strong> In September 2026 IRDAI imposed a <strong>&#8377;1 crore</strong> penalty on a
bank acting as a corporate agent. Part of the reasoning is worth reading closely, because it
describes a setup most platforms have: an internal CRM-based tracking system and a generic
customer-service escalation path, <strong>without a policyholder-facing, insurance-specific channel
and disclosure</strong>, does not meet regulation 20(1) of the Corporate Agents Regulations, which
places a distinct and non-delegable duty on the corporate agent to service and protect the interests
of insurance policyholders. There was no insurance option on the toll-free IVR and no insurance
grievance disclosure on the website.</p>
<p>Read that as a specification. A tag in Zendesk is not a channel. <strong>An insurance grievance
route has to be published where a policyholder can find it, reachable by phone, owned by a named
person, and disclosed on your website alongside your registration number and your role.</strong></p>

<h3 id="s-indigo-s2027">What changes on 1 January 2027, in one place</h3>
<table>
<tr><th>Change</th><th>Source</th><th>What it touches</th></tr>
<tr><td><strong>Named seller on every proposal, policy and certificate</strong></td><td>IRDAI Intermediaries Amendment 2026</td><td>Your proposal payload and policy schema</td></tr>
<tr><td><strong>Policy-wise sales records remotely accessible to the regulator</strong></td><td>IRDAI Intermediaries Amendment 2026</td><td>Your data model and retention</td></tr>
<tr><td><strong>Professional indemnity cover</strong> where intermediation is more than half your revenue</td><td>IRDAI Intermediaries Amendment 2026</td><td>Your own insurance programme</td></tr>
<tr><td><strong>Fresh certificate by 31 January 2027</strong> (grace to 31 March, &#8377;750)</td><td>SBSR Act 2025 read with the 2026 amendment</td><td>Whether you may trade at all</td></tr>
<tr><td><strong>No compulsory bundling of third-party products</strong></td><td>RBI RBC (Second Amendment) 2026</td><td>Your checkout flow</td></tr>
<tr><td><strong>Dark patterns prohibited</strong></td><td>RBI RBC (Second Amendment) 2026</td><td>Your interface</td></tr>
<tr><td><strong>Full compensation for mis-selling</strong></td><td>RBI RBC (Second Amendment) 2026</td><td>Your refund and complaints path</td></tr>
<tr><td><strong>Responsibility for DSAs, sub-agents and representatives</strong></td><td>RBI RBC (Second Amendment) 2026</td><td>Your partner and affiliate programme</td></tr>
</table>
''' + note("<strong>One useful loosening in the same RBI Directions:</strong> an NBFC may distribute insurance <strong>without prior RBI approval</strong>, subject to its IRDAI registration. If you are an NBFC that shelved embedded insurance because of the approval step, the step has gone. The IRDAI registration has not.")

i_cost = registry("Embedded insurance &mdash; what it costs", [
 ("Corporate agent registration", "direct",
  "Non-refundable application fee <strong>&#8377;10,000</strong>, registration fee "
  "<strong>&#8377;25,000</strong>, and <strong>&#8377;500</strong> per certificate for the principal "
  "officer, each specified person and each authorised verifier. Trivial next to what sits underneath it."),
 ("Net worth", "direct",
  "<strong>&#8377;50 lakh, maintained at all times</strong>, for an entity doing insurance "
  "intermediation exclusively. This is locked capital, not a one-off fee, and where you have another "
  "business the two must be at arm&rsquo;s length."),
 ("Annual fee", "direct",
  "Under the continuous-registration regime, <strong>the higher of &#8377;10,000 or 0.04% of "
  "commission and other receipts from insurers in the preceding financial year</strong>. It scales "
  "with you, which most licence fees do not."),
 ("Principal officer and certified sellers", "direct",
  "A graduate principal officer with <strong>50 hours</strong> of Insurance Institute of India "
  "training and the examination passed, plus certification for every specified person. <strong>From "
  "1 January 2027 every policy names one of them</strong>, so this headcount becomes a function of "
  "your sales volume rather than a fixed compliance cost."),
 ("Professional indemnity insurance", "direct",
  "Required where insurance intermediation is more than half of your revenue. Price it before you "
  "assume the economics work at scale."),
 ("Your commission", "indirect",
  "Paid by the insurer out of its <strong>Expenses of Management</strong> envelope &mdash; "
  "<strong>30%</strong> of gross written premium for a general insurer, <strong>35%</strong> for a "
  "standalone health insurer, segmental for life. Not a number your partner is free to set."),
 ("The premium float", "indirect",
  "<strong>Zero, by law.</strong> Twenty-four hours, in full, without netting commission. If a "
  "business case anywhere in your model assumes working capital from held premium, delete it."),
 ("Servicing", "direct",
  "A published insurance grievance route, an option on the phone line, a named officer, renewal "
  "notices, and policy-wise records reachable by the regulator. <strong>Non-delegable, which means "
  "it cannot be outsourced to the insurer and called done.</strong>"),
], "September 2026") + note("<strong>The cost nobody models is attribution.</strong> An embedded checkout has no salesperson, and from 1 January 2027 every policy needs one. Whether that is a small certified team behind the flow or a defined functional identity, it is a decision with a headcount attached, and it is easier to make in 2026 than in a hurry in January.")

a_builds = '''
<h3 id="s-amber-week">Test demand without a licence</h3>
<p><strong>Build:</strong> a plain link or handoff to the insurer or to a licensed partner, with no
selection, no recommendation and <strong>no payment to you for the outcome</strong>. Measure how many
people click.</p>
<p><strong>You get:</strong> an honest demand signal for the cost of a week. <strong>You do not get
revenue</strong>, and the moment you take a per-policy fee you have changed what you are.</p>

<h3 id="s-amber-proper">Distribute on someone else&rsquo;s registration</h3>
<p><strong>Build:</strong> integrate with a licensed intermediary who owns the registration, the
specified persons and the grievance route &rarr; your surface, their compliance &rarr; premium moves
to them or to the insurer, never into your account.</p>
<p><strong>Trade:</strong> thinner economics, and <strong>their 31 January 2027 filing is your
availability risk</strong>. Ask for the date, in writing, and ask again in December.</p>

<h3 id="s-amber-big">Hold your own registration</h3>
<p><strong>Build:</strong> corporate agent registration &rarr; &#8377;50 lakh net worth &rarr;
principal officer and certified specified persons &rarr; a panel of up to nine insurers per line
&rarr; consent and offer-snapshot storage &rarr; a 24-hour premium remittance queue with an owner
&rarr; seller attribution on every policy &rarr; a published insurance grievance channel.</p>
<p><strong>It breaks when:</strong> the team treats it as a payments integration with a compliance
review at the end. The four steps that carry the penalties &mdash; permission, premium, refunds and
servicing &mdash; are all outside the part that looks like the product.</p>
''' + note("If you take one thing from this page: <strong>the premium is not yours, and it has to be with the insurer within 24 hours, in full, without your commission taken out.</strong> Build the remittance queue before you build the offer screen. Everything else on this page can be retrofitted; that one is in the plumbing.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Premium sits for two or three days</strong></td><td>PSP settlement cycle treated as the remittance clock.</td><td>24 hours from collection, excluding bank and postal holidays.</td></tr>
<tr><td><strong>Commission netted out of premium</strong></td><td>Finance nets fees everywhere else.</td><td>Remit gross. Accrue and invoice commission separately.</td></tr>
<tr><td><strong>UI says &ldquo;Insured&rdquo; before the insurer has the money</strong></td><td>Optimistic state after a successful card charge.</td><td>Cover pending until the insurer confirms receipt.</td></tr>
<tr><td><strong>Cart refund returns the premium</strong></td><td>The insurance line is just another order line.</td><td>Refunds come from the insurer to the customer. Exclude the line.</td></tr>
<tr><td><strong>Cover pre-ticked to lift attach rate</strong></td><td>It works, which is exactly the problem.</td><td>Unticked default. Decline as prominent as accept.</td></tr>
<tr><td><strong>&ldquo;Best&rdquo; or &ldquo;Top&rdquo; labels on a product</strong></td><td>Ordinary e-commerce merchandising.</td><td>Objective, disclosed criteria, or no label.</td></tr>
<tr><td><strong>Insurance complaints go to the general support queue</strong></td><td>One helpdesk for everything.</td><td>Published insurance channel, IVR option, named officer.</td></tr>
<tr><td><strong>Policies with no identifiable seller</strong></td><td>A checkout has no salesperson.</td><td>Attribution model decided before 1 January 2027.</td></tr>
<tr><td><strong>A group policy covering future customers</strong></td><td>Group treated as a marketing segment.</td><td>The group must exist and be enrolled before the policy issues.</td></tr>
<tr><td><strong>Partner&rsquo;s registration lapses</strong></td><td>Nobody tracked their 31 January 2027 filing.</td><td>Track it like a certificate expiry, because it is one.</td></tr>
</table>
'''

SRC=[('official','Insurance Act, 1938 &mdash; section 64VB','the rule that no risk attaches until the insurer receives the premium; that a refund is paid by the insurer directly to the insured and never credited to the agent; and that premium collected on an insurer&rsquo;s behalf must be deposited or dispatched in full, without deduction of commission, within 24 hours excluding bank and postal holidays. Section 102 is the penalty provision referred to below.','https://www.indiacode.nic.in'),
 ('official','IRDAI (Insurance Intermediaries) (Amendment) Regulations, 2026','notified 30 July 2026, amending the Corporate Agents Regulations 2015, Insurance Brokers Regulations 2018, Insurance Marketing Firm Regulations 2015, Web Aggregators Regulations 2017 and CPSC-SPV Regulations 2019. Continuous registration and the annual fee, the 31 January 2027 and 31 March 2027 dates, seller tagging on the proposal, policy and certificate from 1 January 2027, remotely accessible policy-wise sales records, and professional indemnity cover.','https://irdai.gov.in'),
 ('official','IRDAI (Protection of Policyholders&rsquo; Interests, Operations and Allied Matters of Insurers) Regulations, 2024','notified 1 April 2024 with master circulars of 19 June 2024 and 5 September 2024, consolidating eight regulations and 41 circulars and applying to distribution channels as well as insurers. The requirement that a group exist before the policy issues, the 30-day free look, cancellation with a refund for the unexpired period, electronic issuance, and the insurer-side search tool for verifying authorised distribution channels.','https://irdai.gov.in'),
 ('official','IRDAI corporate agent registration requirements and fee schedule','the &#8377;50 lakh net worth held at all times, the &#8377;10,000 application and &#8377;25,000 registration fees, &#8377;500 per principal officer, specified person and authorised verifier certificate, the nine-insurer per line and 27-in-total tie-up limits, the &#8377;5 crore per risk commercial-lines limit, the 30-day tie-up disclosure and the principal officer training requirement.','https://irdai.gov.in'),
 ('official','RBI Responsible Business Conduct (Second Amendment) Directions, 2026','drafted 11 February 2026 and notified 15 June 2026, effective 1 January 2027, in mirror versions for commercial banks and NBFCs. The prohibition on compulsory bundling of third-party products, the ban on dark patterns, the mis-selling definition and compensation mechanism, responsibility for DSAs and sub-agents, and the removal of prior RBI approval for NBFC insurance distribution.','https://www.rbi.org.in'),
 ('official','IRDAI penalty orders','the &#8377;5 crore order of 4 August 2025 under section 102 of the Insurance Act, with eleven charges and the premium remittance and policy tagging findings; and the September 2026 &#8377;1 crore corporate agent order holding that a CRM-based tracking system and generic customer-service escalation do not discharge the distinct and non-delegable servicing duty under regulation 20(1).','https://irdai.gov.in'),
 ('industry','Expenses of Management enforcement and market context','the six-month branch expansion restriction on a standalone health insurer for an FY25 EoM breach, insurance penetration at 3.7% of GDP in 2024-25 against a global 7.3%, and reported commission outflows of about &#8377;60,800 crore for life and &#8377;47,266 crore for non-life in 2024-25. Directional context, not figures to build on.',''),
 ('industry','Bima Sugam status reporting','the phased rollout by Bima Sugam India Federation under the 2024 Insurance Electronic Marketplace Regulations, and IRDAI&rsquo;s statement that motor, health and term products should be live by the end of September 2026. The platform has missed several previous dates and its commercial model is reported rather than notified &mdash; confirm before designing around it.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. The intermediaries amendment is six weeks old and the two 1 January 2027 '
 'regimes are not yet in force. Verify against the notified text before you build to any date here.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 06</div><h3>Customer Operations</h3><p>Grievance handling, contact windows and the conduct rules an insurance channel inherits.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Escrow, settlement files and why a webhook is a notification rather than a fact.</p></a>
<a href="/fintech-ai/products/bnpl-checkout/" class="mod-card"><div class="mod-num">GUIDE 03</div><h3>BNPL Checkout</h3><p>The other regulated product that lives inside somebody else&rsquo;s checkout screen.</p></a>
<a href="/fintech-ai/regulation-india/" class="mod-card"><div class="mod-num">SPINE</div><h3>India regulation</h3><p>RBI, SEBI and IRDAI, and which one owns the question you are asking.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Insurance distribution is a registered activity and the obligations described here sit on a registered intermediary, not on a technology vendor. Nothing here is legal advice. Have your structure, your premium handling and your grievance framework reviewed by qualified counsel, and confirm every date against the notified text, before the first policy is sold.")

lanes={'green':[("How to use this page",g_read),("What embedded insurance actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — permission, and the structure",i_step12),
           ("Steps 3 and 4 — product, insurer and the offer",i_step34),
           ("Step 5 — the premium, and the 24-hour clock",i_step5),
           ("Steps 6 to 8 — issue, refund, service",i_step68),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Embedded Insurance: How to Build It"
META=("Build an embedded insurance product step by step: who may sell it, the 24-hour premium rule, "
      "and what changes on 1 January 2027.")
LEAD=("A step-by-step guide to selling insurance inside your own checkout in India. Eight stages, the "
      "options at each one, exactly how each step connects to the next, real costs, and what breaks. "
      "Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/embedded-insurance",title=TITLE,meta=META,lead=LEAD,label="Product Guide 09",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/embedded-insurance/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h)
    assert m, "no <body> tag found"
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h)
    assert t, "no page-hero div found"
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

# ---- Link it from two modules, per the established pattern. --------------
# Rule 5: match the ELEMENT, assert the index, verify the write.
NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Selling cover inside '
  'your own checkout? The eight steps, who is allowed to sell, and what changes on 1 January 2027: '
  '<a href="/fintech-ai/products/embedded-insurance/"><strong>Embedded Insurance: How to Build It '
  '&rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('customer-operations', 'payments-reconciliation'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/embedded-insurance' in src:
        print('  = already linked from /' + mod + '/'); continue
    n = src.count(ANCHOR)
    assert n == 1, 'anchor appears ' + str(n) + ' times in ' + p + ' — refusing to write'
    i = src.find(ANCHOR)
    assert i != -1, 'anchor not found in ' + p
    out = src[:i] + NOTE_BLOCK + src[i:]
    assert NOTE_BLOCK.count('<div') == 1 and NOTE_BLOCK.count('</div>') == 1, 'block shape changed'
    assert out.count('<div') == src.count('<div') + 1, 'div count moved unexpectedly'
    assert out.count('</div>') == src.count('</div>') + 1, 'close-div count moved unexpectedly'
    assert len(out) == len(src) + len(NOTE_BLOCK), 'length changed by more than the block'
    _io.open(p, 'w', encoding='utf-8').write(out)
    print('  + linked from /' + mod + '/')
