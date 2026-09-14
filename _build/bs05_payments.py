#!/usr/bin/env python3
# Session 49 — Build Sheet 05: Payments & Reconciliation
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

V = VERIFIED   # 'September 2026'

# ---------------------------------------------------------------- GREEN

g_read = f'''
<p>The <a href="/fintech-ai/payments-reconciliation/">Payments and Reconciliation module</a> explains
why money that has obviously moved still will not match. This page is the parts list: what to buy,
what to build, what each one costs per transaction, and where each breaks.</p>
{warn(f"Every price here carries a <strong>Verified {V}</strong> stamp. Payment pricing is the most negotiable number in this section &mdash; published rate cards are the starting position for anyone doing meaningful volume. Treat the figures as budgeting anchors and as a way to tell whether a quote is out of shape.")}
<p>Payments is four jobs, not one. They get bought from different vendors, break in different ways,
and the third one is the one nobody budgets for.</p>
<table>
<tr><th>Job</th><th>What it does</th><th>Can you skip it?</th></tr>
<tr><td><strong>Acceptance</strong></td><td>Take money from a customer: UPI, cards, net banking, wallets.</td><td>No. This is the one everyone buys first and thinks is the whole problem.</td></tr>
<tr><td><strong>Payouts</strong></td><td>Send money out: refunds, vendor settlements, salaries, disbursals.</td><td>Only if money never leaves. Marketplaces, lenders and gig platforms cannot.</td></tr>
<tr><td><strong>Reconciliation</strong></td><td>Prove what you think happened matches what the bank says happened.</td><td>No, and it is not optional in the way people treat it. This is where the finance team's month goes.</td></tr>
<tr><td><strong>Disputes</strong></td><td>Chargebacks, UPI complaints, refund failures, ombudsman escalations.</td><td>No. It arrives whether or not you built for it.</td></tr>
</table>
<p>A gateway integration solves the first. It gives you a partial answer to the second, a data feed
for the third, and a dashboard for the fourth. The gap between "we have a payment gateway" and "we
can close the books" is most of the work on this page.</p>
'''

g_econ = f'''
<p>In every other build sheet in this section, cost is a line item. Here it is a percentage of
revenue, forever, and it is the single number that decides which build you can afford.</p>
<p>Two facts do most of the work.</p>
<p><strong>First: UPI is free to accept, and that is about to stop being universally true.</strong>
MDR on UPI and RuPay debit was set to zero in January 2020 to drive adoption, and it worked &mdash;
UPI now carries roughly 88% of India's digital payments, running past 24 billion transactions and
close to &#8377;30 lakh crore a month. The cost has been carried by banks, NPCI, the payment industry
and a government incentive scheme.</p>
<p>The Taxation and Other Laws (Amendment) Bill, 2026, passed by the Lok Sabha in August 2026, amends
the Payment and Settlement Systems Act, 2007 to let the government notify categories of digital
transactions that may carry charges. The Finance Ministry has said consumers pay nothing and all
person-to-person transfers stay free. What is under discussion is an MDR in the region of
<strong>0.25% to 0.4%</strong>, applying only to <strong>large merchants</strong> (turnover thresholds
around &#8377;1&ndash;1.5 crore have been reported) on <strong>transactions above &#8377;2,000</strong>
&mdash; which would leave roughly 95% of UPI transactions untouched.</p>
{warn("<strong>Rates and thresholds are not notified yet.</strong> The Bill is an enabling provision; the actual categories and rates come later by notification. Do not design a pricing model around a specific number today. Do build the ability to <em>apply a per-rail, per-ticket-size fee</em> and to recompute unit economics when it lands, because if your margin only works at 0% UPI MDR, your margin is a policy position rather than a business model.")}
<p><strong>Second: zero MDR never meant zero cost.</strong> MDR is what the acquiring side charges.
Your payment aggregator's platform fee is a separate commercial term. Published rate cards commonly
show UPI at 0%, and merchants still find a fee on the invoice, because the aggregator is charging for
its own service rather than passing through MDR. Read the contract for the rail-by-rail fee, not the
marketing page.</p>
<p>And the fee attracts <strong>18% GST</strong>. On the fee, not on the transaction value &mdash; so
a 2% platform fee is really 2.36% before anything else. That is not a rounding error at scale and it
is never in the headline number.</p>
'''

g_rank = f'''
<p>The instinct is to rank gateways on TDR. It is the wrong first axis, and the arithmetic shows
why.</p>
<p>Legacy gateways quote 1.6&ndash;1.8% and the modern ones quote around 2%. On &#8377;1 crore of
monthly volume that spread is about &#8377;30,000 a month. Vendor-reported success rates differ by
far more than that &mdash; the modern gateways claim 85&ndash;90% against 65&ndash;75% for older
stacks. Treat those specific figures sceptically, because every one of them is published by a party
with an interest, but the shape of the argument holds: <strong>a 10-point difference in success rate
on &#8377;1 crore of attempted volume is &#8377;10 lakh of orders, not &#8377;30,000 of fees.</strong></p>
<p>So rank on four things you can actually measure during a trial:</p>
<ul>
<li><strong>Success rate on your own traffic</strong>, split by rail, by bank and by ticket size. Not
their number. Yours. Run both gateways in parallel on split traffic for a fortnight.</li>
<li><strong>Settlement timing and what early access costs.</strong> T+1 versus T+2 is working capital.
Instant settlement is a loan priced as a feature &mdash; see the cost block.</li>
<li><strong>Reconciliation data quality.</strong> Does the settlement file carry a stable
identifier that matches your order id, fee breakdown per transaction, and a control total? This is
the field nobody evaluates and the one that decides whether your month-end takes a day or a week.</li>
<li><strong>Failure behaviour.</strong> Webhook reliability, replay tooling, and what happens to your
account when the risk team gets nervous. Sudden account freezes are a documented pattern across
Indian aggregators and they are an existential operational risk, not a support ticket.</li>
</ul>
{note("Add one commercial question to the technical evaluation: <strong>what is the exit path?</strong> Getting a gateway in takes a day. Getting customer card tokens, mandates and subscription state <em>out</em> is the part that takes a quarter, and it is the reason single-gateway merchants accept bad terms at renewal. Ask about token portability before you sign, not after.")}
'''

# ---------------------------------------------------------------- INDIGO

i_mat_accept = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>Razorpay</strong></td><td>The default for Indian online acceptance. Cleanest API and docs, strongest subscription tooling, UPI AutoPay support.</td><td>razorpay.com/docs</td></tr>
<tr><td><strong>Cashfree</strong></td><td>Lowest published TDR of the majors, strong on marketplace payouts and batch disbursal.</td><td>docs.cashfree.com</td></tr>
<tr><td><strong>PayU</strong></td><td>Enterprise and cross-border reach, dedicated account management, established chargeback handling.</td><td>payu.in</td></tr>
<tr><td><strong>CCAvenue / BillDesk</strong></td><td>Legacy breadth of bank acceptance. Lower headline TDR, but setup and annual fees change the total.</td><td>ccavenue.com</td></tr>
<tr><td><strong>Stripe</strong></td><td>The right answer when your customers are mostly international. Not the right answer for a domestic Indian book.</td><td>stripe.com/docs</td></tr>
<tr><td><strong>UPI</strong> <span class="pill p-indirect">indirect</span></td><td>The dominant rail. Reached through a PA or a sponsor bank, never directly.</td><td>npci.org.in</td></tr>
<tr><td><strong>NPCI URCS / UDIR</strong> <span class="pill p-indirect">indirect</span></td><td>UPI dispute resolution and the TCC/RET mechanism. Reached through your sponsor bank or PSP.</td><td>npci.org.in</td></tr>
<tr><td><strong>RBI CMS portal</strong> <span class="pill p-direct">direct</span></td><td>The ombudsman complaint system. Customer-facing &mdash; monitor what reaches it, because it is a supervisory signal about you.</td><td>cms.rbi.org.in</td></tr>
</table>
{note("Notice how much of this is <strong>indirect</strong>. You do not integrate with UPI. You integrate with a payment aggregator or a sponsor bank that integrates with NPCI. Every timing assumption, every dispute window and every settlement file format you build against is <em>theirs</em>, and changes when you switch. Budget for that when you plan a migration.")}
'''

i_mat_recon = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>DuckDB</strong> <span class="pill p-oss">oss</span></td><td>In-process analytical SQL. Joins a month of settlement files against your ledger on a laptop, no warehouse needed. The highest-leverage tool on this page.</td><td>duckdb.org</td></tr>
<tr><td><strong>Polars / pandas</strong> <span class="pill p-oss">oss</span></td><td>Dataframe matching. Polars is materially faster on large settlement files.</td><td>pola.rs</td></tr>
<tr><td><strong>RapidFuzz</strong> <span class="pill p-oss">oss</span></td><td>String similarity for narration-based matching on bank statement lines.</td><td>github.com/rapidfuzz</td></tr>
<tr><td><strong>dbt</strong> <span class="pill p-oss">oss</span></td><td>Versioned, tested transformation logic. Reconciliation rules are exactly the kind of logic that must be testable and reviewable.</td><td>getdbt.com</td></tr>
<tr><td><strong>Apache Arrow / Parquet</strong> <span class="pill p-oss">oss</span></td><td>Columnar archive for settlement files you must retain and re-query years later.</td><td>arrow.apache.org</td></tr>
<tr><td><strong>Osfin / Cointab / Nanonets</strong></td><td>Reconciliation automation with real India market presence and native settlement-file formats.</td><td>osfin.ai</td></tr>
<tr><td><strong>Ledge</strong></td><td>Built for high-volume real-time fintech and marketplace matching. Faster to first production match than the enterprise suites.</td><td>ledge.co</td></tr>
<tr><td><strong>HighRadius / BlackLine / Trintech</strong></td><td>Enterprise record-to-report and financial close. Mature, heavy, audit-oriented, three-to-six-month implementations.</td><td>blackline.com</td></tr>
</table>
'''

code_webhook = code('Python — webhook handling, the three bugs everyone ships', r'''import hmac, hashlib
from flask import request, abort

SECRET = b"your_webhook_secret"

@app.post("/webhooks/payments")
def payments_webhook():
    # BUG 1: verifying the signature against parsed-then-reserialised JSON.
    # The signature is over the RAW BYTES. request.get_json() reorders keys and
    # changes whitespace, so the digest never matches -- or worse, you "fix" it
    # by skipping verification.
    raw = request.get_data()                      # bytes, before any parsing
    sent = request.headers.get("X-Signature", "")
    calc = hmac.new(SECRET, raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calc, sent):       # constant time, not ==
        abort(400)

    ev = json.loads(raw)

    # BUG 2: treating delivery as exactly-once and in-order. It is neither.
    # payment.failed can arrive AFTER payment.captured for the same payment.
    # Order by the event's own timestamp; never by arrival.
    with db.begin():
        prior = db.get_event(ev["id"])
        if prior:
            return "", 200                        # already processed, idempotent
        current = db.get_payment_state(ev["payload"]["payment_id"])
        if current and ev["created_at"] <= current.state_as_of:
            db.record_event(ev["id"], outcome="stale_ignored")
            return "", 200                        # out-of-order, safely dropped

        # BUG 3: trusting the webhook body for the amount. The signature proves
        # it came from the PSP; it does not prove your order is for that amount.
        order = db.get_order(ev["payload"]["order_id"])
        if order.amount_paise != ev["payload"]["amount"]:
            db.flag_for_review(order.id, "amount_mismatch")
            return "", 200                        # 200 stops the retry storm

        db.apply(ev)
        db.record_event(ev["id"], outcome="applied")
    return "", 200

# WHAT TO CHECK
# [ ] signature computed over raw bytes, compared with compare_digest
# [ ] the event id is stored and checked BEFORE any state change, in the same
#     transaction as the state change -- otherwise a retry during processing
#     double-applies
# [ ] out-of-order handling driven by the event timestamp, not arrival order
# [ ] amounts in integer paise. Never float. 0.1 + 0.2 != 0.3
# [ ] non-2xx only for "retry me". A 500 on a malformed event you will never be
#     able to process buys you that event, forever, at increasing intervals
# [ ] webhook handler does NOT call the PSP synchronously. Enqueue and return;
#     a slow handler becomes a retry storm becomes a duplicate storm
# [ ] replay tooling exists and has been used once in anger before you need it
''')

i_accept = f'''
<p>Acceptance integration is well-documented by every vendor and you do not need us to repeat it.
What the vendor docs do not tell you is which three things you will get wrong.</p>
<h3 id="s-indigo-hook">Webhooks: the part that decides whether your ledger is trustworthy</h3>
{code_webhook}
<p><strong>The gotcha nobody documents:</strong> a webhook is a <em>notification that something may
have changed</em>, not a statement of fact about your money. The authoritative record of what you
were actually paid is the settlement file, which arrives later and disagrees more often than teams
expect. Build the ledger so the webhook moves a payment to <code>captured</code> and only the
settlement file moves it to <code>settled</code>. Merging those two states into one is the root of a
large share of reconciliation breaks.</p>

<h3 id="s-indigo-refund">Refunds are not negative payments</h3>
<p>Almost every ledger starts by modelling a refund as a payment with a minus sign. It works until
partial refunds interleave with reversals, and then it stops working permanently.</p>
<p>A refund has its own lifecycle (<code>created</code>, <code>processed</code>,
<code>failed</code>), its own settlement timing that does not line up with the original payment's,
and its own failure mode where the money leaves your escrow and does not arrive with the customer.
A failed refund is not a refund that did not happen &mdash; it is money in flight with a customer
who is already unhappy. Give refunds their own table, their own idempotency key and their own
exception queue.</p>
'''

code_recon = code('SQL — settlement reconciliation with control totals (DuckDB)', r'''-- Run this against the settlement file and your ledger. DuckDB reads the CSV
-- in place; no warehouse, no ingestion pipeline.

-- STEP 1: control totals FIRST, before any matching.
-- A file missing its last 200 rows reconciles with a perfect match rate on the
-- rows that are present. Match rate is silent about what is not in the file.
WITH declared AS (          -- from the file header / manifest, not the rows
  SELECT 48213 AS row_count, 9182734500 AS total_paise
),
actual AS (
  SELECT COUNT(*) AS row_count, SUM(amount_paise) AS total_paise
  FROM read_csv_auto('settlement_2026_09_12.csv')
)
SELECT CASE
  WHEN a.row_count <> d.row_count OR a.total_paise <> d.total_paise
  THEN 'ABORT: file integrity failed' ELSE 'ok' END AS gate,
  d.row_count AS declared_rows, a.row_count AS actual_rows,
  d.total_paise - a.total_paise AS paise_difference
FROM declared d, actual a;

-- STEP 2: match, and record WHICH RULE fired for every row.
SELECT
  COALESCE(l.order_id, s.merchant_ref)            AS order_id,
  CASE
    WHEN l.psp_payment_id = s.psp_payment_id      THEN 'exact_psp_id'
    WHEN l.order_id = s.merchant_ref
         AND l.amount_paise = s.amount_paise      THEN 'ref_plus_amount'
    WHEN l.order_id = s.merchant_ref
         AND ABS(l.amount_paise - s.amount_paise)
             <= s.fee_paise + s.tax_paise         THEN 'net_of_fees'
    ELSE 'unmatched'
  END                                             AS match_rule,
  l.amount_paise AS ledger_paise, s.amount_paise AS settled_paise,
  s.fee_paise, s.tax_paise,
  l.amount_paise - (s.amount_paise + s.fee_paise + s.tax_paise) AS residual_paise
FROM ledger l
FULL OUTER JOIN read_csv_auto('settlement_2026_09_12.csv') s
  ON l.psp_payment_id = s.psp_payment_id OR l.order_id = s.merchant_ref;

-- WHAT TO CHECK
-- [ ] control totals run BEFORE matching and ABORT the run. A silently
--     truncated file is the single most dangerous input here, because every
--     downstream metric looks healthy.
-- [ ] FULL OUTER JOIN, not LEFT. A row in the settlement file that is in no
--     ledger is the interesting case -- money you were paid and cannot explain.
-- [ ] match_rule stored per row. "94% auto-matched" is meaningless without the
--     mix; a jump in net_of_fees means the PSP changed its fee reporting.
-- [ ] know whether your PSP deducts fees PER TRANSACTION or in one aggregate
--     debit. It changes the matching logic completely and it differs by PSP and
--     sometimes by plan within one PSP.
-- [ ] residual_paise must be exactly 0 on a clean match. Any tolerance you add
--     here is a control change: version it, date it, get it approved.
-- [ ] time zone. Settlement files are cut on IST business days. Aggregating in
--     UTC moves 5.5 hours of transactions into the wrong settlement day.
-- [ ] a debit with no credit inside the RBI reversal window is NOT a break yet.
--     Age it before you escalate it.
''')

i_recon = f'''
<p>Reconciliation is not a product you buy first. It is a query you run, and the useful realisation
is how far a single tool gets you.</p>
<h3 id="s-indigo-duck">DuckDB is the answer for most teams for longer than they expect</h3>
<p>Settlement reconciliation is a join between two files. Until you are doing millions of
transactions a day, that join runs in seconds in an in-process analytical database against CSVs on
disk. No warehouse, no ingestion pipeline, no vendor. Teams routinely buy a platform to do something
their data volume does not justify, and then discover that the platform still needs them to define
every matching rule.</p>
{code_recon}
<p><strong>The gotcha nobody documents:</strong> whether fees are deducted <em>per transaction</em>
or as a <em>single aggregate debit</em> at the end of the cycle. It varies by aggregator, and
sometimes by plan within one aggregator. Per-transaction deduction means your settled amount never
equals your ledger amount and every match must be net-of-fees. Aggregate deduction means the
transactions match exactly and there is one large unexplained debit that belongs to no order at all.
Building for one and receiving the other is a full rewrite of the matching layer. Ask before you
integrate, and ask for a sample file.</p>

<h3 id="s-indigo-ledger">Build the ledger so breaks cannot happen</h3>
<p>Most reconciliation work is compensating for a ledger that allowed the break in the first place.
Four decisions remove more exceptions than any matching engine:</p>
<ul>
<li><strong>Integer minor units.</strong> Paise, as integers, everywhere. Floats in money columns are
the single most avoidable defect in fintech.</li>
<li><strong>A caller-supplied idempotency key with a UNIQUE constraint.</strong> Not generated by
you on receipt &mdash; supplied by the caller, so a retry of the same intent collapses to one
record at the database level rather than in application logic.</li>
<li><strong><code>effective_at</code> separate from <code>recorded_at</code>.</strong> The two clocks
from the module. When the money moved, and when you learned it moved. Collapsing these makes
late-arriving settlement data look like an error.</li>
<li><strong>Append-only.</strong> A correction is a new entry, never an update. The ability to
reconstruct what you believed on a given date is the entire audit trail.</li>
</ul>
'''

code_payout = code('Python — payouts, where the retry logic decides whether you pay twice', r'''import uuid, requests

def disburse(order_id, account, amount_paise, attempt_state):
    # The idempotency key is derived from the INTENT, not from the attempt.
    # Same intent retried -> same key -> PSP returns the original payout.
    # A fresh uuid4() per retry is how platforms pay the same person twice.
    key = f"payout:{order_id}"

    r = requests.post(
        "https://api.psp.example/v1/payouts",
        json={"account": account, "amount": amount_paise,
              "currency": "INR", "reference": order_id},
        headers={"Idempotency-Key": key, "Authorization": f"Bearer {TOKEN}"},
        timeout=(3, 30),
    )

    # A TIMEOUT IS NOT A FAILURE. It is an unknown. The payout may have been
    # created. Never retry a timeout as a fresh request without the same key,
    # and never mark it failed without asking the PSP what happened.
    if r.status_code >= 500 or r.status_code == 408:
        return reconcile_unknown(key, order_id)

    r.raise_for_status()
    return r.json()

def reconcile_unknown(key, order_id):
    """Ask, do not assume. Query by YOUR reference, not the PSP's id --
    you may never have received the PSP's id."""
    q = requests.get("https://api.psp.example/v1/payouts",
                     params={"reference": order_id}, timeout=(3, 30))
    hits = q.json().get("items", [])
    if hits:
        return hits[0]                 # it existed all along
    return {"status": "unknown", "action": "queue_for_human"}

# WHAT TO CHECK
# [ ] idempotency key derived from the intent and STORED before the call, not
#     after. If the process dies mid-request you must be able to recover the key
# [ ] separate connect and read timeouts. A single timeout value means a slow
#     PSP holds your worker pool
# [ ] timeouts and 5xx go to an UNKNOWN state, never to failed. "Failed" is a
#     conclusion; only the PSP can give you that
# [ ] queryable by your own reference, not only by the PSP's identifier
# [ ] a daily sweep that lists PSP payouts with no matching local record. This
#     is how you find the ones you paid and never booked
# [ ] beneficiary account validated (penny drop or name match) BEFORE the first
#     payout, not after the first complaint
# [ ] payouts and refunds are different flows even though both send money out.
#     A refund is tied to a payment and a customer right; a payout is not
''')

i_payout = f'''
<p>Payouts feel like acceptance in reverse. They are not. Acceptance failures cost you a sale;
payout failures cost you money you have already sent, and the recovery path runs through a bank.</p>
{code_payout}
<p><strong>The gotcha nobody documents:</strong> the timeout. Every payments team knows to use
idempotency keys and most still treat a request timeout as a failure and retry with a fresh key.
The PSP received the first request. It created the payout. Your side recorded a failure, retried,
and created a second one. This is the single most expensive bug in this build sheet, and it only
ever shows up under load, which is exactly when you are least able to investigate it.</p>

<h3 id="s-indigo-pa">If you are the aggregator: the 2025 Directions</h3>
<p>Everything above assumes you use a PA. If you <em>are</em> one, or you are close enough to look
like one, the rules changed materially and recently.</p>
<p>The <strong>RBI (Regulation of Payment Aggregators) Directions, 2025</strong>, notified
15 September 2025 and effective immediately, repealed and replaced the 2020 PA-PG Guidelines, the
2021 clarifications and the separate cross-border circular. The shape:</p>
<table>
<tr><th>Item</th><th>Requirement</th></tr>
<tr><td><strong>Categories</strong></td><td><strong>PA-O</strong> online · <strong>PA-P</strong> physical (proximity) · <strong>PA-CB</strong> cross-border. <strong>PA-P is newly regulated</strong> &mdash; entities doing only PA-P had to apply by 31 Dec 2025 or wind down by 28 Feb 2026.</td></tr>
<tr><td><strong>Net worth</strong></td><td>&#8377;15 crore at application, rising to &#8377;25 crore and maintained on an ongoing basis.</td></tr>
<tr><td><strong>Escrow</strong></td><td>With a Scheduled Commercial Bank. Your own funds must not sit in it. Day-end balance must equal the amount realised. Pre-funding is permitted for domestic PAs only, and pre-funded amounts cannot be withdrawn.</td></tr>
<tr><td><strong>PA-CB</strong></td><td>Separate <strong>InCA</strong> (inward) and <strong>OCA</strong> (outward) accounts, never commingled. Per-transaction cap of <strong>&#8377;25 lakh</strong>. No direct dealing in foreign currency except through an authorised dealer. No interest on international balances.</td></tr>
<tr><td><strong>Settlement</strong></td><td>Liberalised from a fixed regulatory timeline to what the PA&ndash;merchant agreement provides, as long as it is fair, equitable and the timelines are transparently disclosed.</td></tr>
<tr><td><strong>Card data</strong></td><td>Only issuers and card networks may store card details. Everyone else tokenises or deletes.</td></tr>
<tr><td><strong>Reporting</strong></td><td>Monthly transaction statistics to RBI; quarterly auditor's certificate on escrow balances. FIU-IND registration required &mdash; see <a href="/fintech-ai/aml-compliance/build-sheet/">Build Sheet 04</a>.</td></tr>
</table>
{warn("<strong>A deadline lands this week.</strong> Merchants onboarded up to 31 December 2025 had to be brought into line with the new customer due diligence requirements by <strong>15 September 2026</strong>. There is no equivalent leeway for merchants onboarded from 1 January 2026 onwards. Acquiring banks now also need their own policy for merchants acquired by non-bank PAs, and must be able to pull the PA's due-diligence records on demand &mdash; so this reaches your bank relationship, not only your compliance file.")}
'''

# ---------------------------------------------------------------- COST

cost_rows = [
 ("UPI acceptance &mdash; MDR", "direct",
  "<strong>0% since January 2020</strong> by mandate. The Taxation and Other Laws (Amendment) Bill, "
  "2026 enables a change: reported discussion of <strong>0.25&ndash;0.4%</strong> on large merchants "
  "for tickets above &#8377;2,000, leaving ~95% of transactions out of scope. <strong>Rates and "
  "thresholds are not notified yet.</strong>"),
 ("UPI acceptance &mdash; your PA's fee", "direct",
  "Separate from MDR and <strong>not always zero</strong>. Published cards commonly show 0%; "
  "contracts sometimes carry a platform fee regardless. At volume, UPI is negotiable well below 1%. "
  "Confirm the rail-by-rail rate in writing."),
 ("Domestic cards, net banking, wallets", "direct",
  "&asymp; <strong>2%</strong> at Razorpay-class pricing. Cashfree publishes lower &mdash; figures "
  "around <strong>1.75&ndash;1.95%</strong> are commonly cited. High-volume card pricing sometimes "
  "moves to a flat per-transaction fee (&asymp; &#8377;9) instead of a percentage, which is far "
  "cheaper on large tickets."),
 ("Premium methods", "direct",
  "&asymp; <strong>3%</strong> for Amex, Diners, EMI and cardless EMI. International cards &asymp; "
  "<strong>3%</strong>, and optional chargeback protection adds roughly <strong>1%</strong> on top."),
 ("Legacy gateways", "direct",
  "Headline <strong>1.6&ndash;1.8%</strong> &mdash; but setup fees of <strong>&#8377;5,000&ndash;"
  "50,000</strong> and annual maintenance of <strong>&#8377;2,400&ndash;9,999</strong> are commonly "
  "reported, and the success-rate gap usually costs more than the TDR saves."),
 ("GST on the fee", "direct",
  "<strong>18%, on the fee only</strong>, not the transaction value. A 2% platform fee is 2.36% "
  "all-in. Never in the headline number."),
 ("Settlement timing", "direct",
  "T+1 or T+2 by default depending on provider and plan. <strong>Instant settlement</strong> "
  "(minutes) is a paid add-on. Price it as what it is: <strong>a very short-term loan against your "
  "own receivables</strong>. An extra 0.1% to get money one day early is roughly 36% annualised."),
 ("Cross-border receipt", "direct",
  "Headline &asymp; 3%, but all-in cost including FX spread and partner bank fees is frequently "
  "reported at <strong>5&ndash;7%</strong>. The spread is where the money is and it is rarely quoted."),
 ("Reconciliation &mdash; build", "oss",
  "<strong>Infrastructure only.</strong> DuckDB, Polars and dbt cost nothing. The real cost is "
  "engineering time to write and maintain the matching rules, and it is genuinely modest for a "
  "single-PSP book."),
 ("Reconciliation &mdash; buy", "direct",
  "India-focused automation (Osfin, Cointab, Nanonets) is quote-based and mid-market. Enterprise "
  "close suites (BlackLine, HighRadius, Trintech) are six figures annually with "
  "<strong>three-to-six-month implementations</strong>."),
 ("Disputes and chargebacks", "direct",
  "A per-case fee from the PSP whether or not you win, plus analyst time. <strong>The cost that "
  "dominates is not the fee</strong> &mdash; it is the excessive-chargeback programmes run by the "
  "card networks, where breaching a ratio threshold brings monitoring, fines and the risk of losing "
  "acceptance entirely."),
]

i_cost = f'''
{registry("Payments &mdash; cost per unit", cost_rows, V)}
{warn("<strong>Model cost per successful order, not cost per transaction.</strong> A gateway at 1.75% with an 80% success rate costs you more per completed order than one at 2% with 90%, before you count the customer who abandoned and did not come back. Compute: <em>(fee &times; 1.18 GST) &divide; success rate</em>, per rail, on your own traffic mix. That single number reorders most gateway shortlists, and it is the number no vendor will compute for you.")}
<p>Three cost lines that arrive after the contract: chargeback handling fees on disputes you win,
per-refund fees at some providers, and the working-capital cost of settlement timing, which is real
money and never appears on any rate card.</p>
'''

# ---------------------------------------------------------------- AMBER

a_combos = f'''
<table>
<tr><th>Combination</th><th>Works because</th></tr>
<tr><td>Two gateways with rule-based routing</td><td>Redundancy against outages, leverage at renewal, and real A/B data on success rate. The single highest-return architectural decision on this page.</td></tr>
<tr><td>Webhook moves to <code>captured</code>, settlement file moves to <code>settled</code></td><td>Two clocks, two states. Most reconciliation breaks are the two collapsed into one.</td></tr>
<tr><td>Append-only ledger + DuckDB matching</td><td>The ledger prevents the break; the query finds the ones that got through. Neither needs a vendor.</td></tr>
<tr><td>Domestic PA + specialist cross-border provider</td><td>Different problems. A domestic aggregator bolting on international acceptance is usually the most expensive way to receive foreign money.</td></tr>
<tr><td>Control totals + exception aging</td><td>Totals catch what is missing from the file; aging catches what you stopped looking at. Match rate alone catches neither.</td></tr>
<tr><td>Tokenisation at the network + your own subscription state</td><td>Card data stays where regulation requires it, and the mandate state stays portable enough that you can actually switch.</td></tr>
</table>
<h3 id="s-amber-conflict">Combinations that conflict</h3>
<ul>
<li><strong>One gateway and no fallback.</strong> Every Indian aggregator has had outages, and the freeze pattern is documented. A single point of failure on revenue is a business risk, not an engineering preference.</li>
<li><strong>Treating the webhook as the source of truth for money.</strong> It is a notification. The settlement file is the fact.</li>
<li><strong>Refunds modelled as negative payments.</strong> Works until partial refunds and reversals interleave, then never works again.</li>
<li><strong>A fresh idempotency key on retry.</strong> This is how you pay a supplier twice.</li>
<li><strong>Buying an enterprise close suite for a single-PSP book.</strong> Three-to-six months of implementation to automate a join you could write today.</li>
<li><strong>Widening tolerances to raise the auto-match rate.</strong> The number improves and the control degrades. If match rate jumps and exception <em>value</em> does not fall proportionately, someone moved a tolerance.</li>
<li><strong>Reconciling in UTC.</strong> Settlement files cut on IST business days. Five and a half hours of transactions land in the wrong day, every day.</li>
</ul>
'''

a_builds = f'''
<h3 id="s-amber-exp">Strong and expensive</h3>
<p><strong>Build:</strong> two payment aggregators with an orchestration layer routing by rail, bank
and ticket size, plus a specialist cross-border provider, plus an enterprise reconciliation and close
platform, plus a dedicated disputes function.</p>
<p><strong>Use when:</strong> volume is high enough that a point of success rate is worth more than
the entire tooling budget, and you have a finance team with a statutory close to meet.</p>
<p><strong>Cost shape:</strong> blended TDR plus six figures a year in close tooling plus headcount.</p>
<p><strong>Trade:</strong> the orchestration layer becomes its own system to maintain, and the close
suite takes three to six months before it matches a single transaction.</p>

<h3 id="s-amber-def">Strong and reasonable &mdash; the default</h3>
<p><strong>Build:</strong> primary aggregator plus a second one kept live at low volume for
failover and leverage &rarr; an append-only ledger with integer paise, caller-supplied idempotency
keys and the two clocks separated &rarr; settlement reconciliation in DuckDB or dbt, run daily,
rules in version control &rarr; an exception queue with named owners and aging &rarr; disputes handled
in-house against a written playbook.</p>
<p><strong>Use when:</strong> you have engineers and payments are core rather than incidental. This
covers most fintechs, marketplaces and subscription businesses in India.</p>
<p><strong>Cost shape:</strong> TDR plus GST, and essentially nothing for the reconciliation stack
beyond the engineering time to write the rules.</p>
<p><strong>Trade:</strong> you own the matching rules, which means you must test them like code.
That is the right trade, because those rules encode your specific commercial arrangements and no
vendor knows them better than you do.</p>
{note("Why the second gateway is in the <em>default</em> build rather than the expensive one. It is not primarily about redundancy. It is that running 5% of traffic through an alternative is the only way to get an honest success-rate comparison, and the only leverage you have at renewal. The cost of keeping it live is close to zero; the cost of not having it is discovered on the day you need it.")}

<h3 id="s-amber-lean">Strong and lean</h3>
<p><strong>Build:</strong> one aggregator on published pricing &rarr; the same ledger discipline,
which costs nothing extra if you do it from day one &rarr; a single scheduled DuckDB query against
the daily settlement file, with control totals &rarr; exceptions in a spreadsheet with an owner and
a date.</p>
<p><strong>Use when:</strong> pre-revenue or early, and every hour spent on payments infrastructure
is an hour not spent on the product.</p>
<p><strong>Cost shape:</strong> TDR only.</p>
<p><strong>Trade:</strong> no failover and manual exception handling. Acceptable. <strong>What is not
acceptable at any scale is the ledger shortcut</strong> &mdash; floats, no idempotency key, one
timestamp. Those cost nothing to get right on day one and are close to unfixable once there is a
year of data behind them.</p>
{warn("Whichever grade you pick: do not automate reconciliation and remove human sign-off in the same project. Speed belongs on matching. Accountability stays on approval. A system that closes the books with nobody accountable for the number is worse than the slow manual process it replaced.")}
'''

a_next = f'''
<p>Two numbers to watch that are not in anyone's dashboard by default.</p>
<p><strong>Exception aging, as a distribution.</strong> Not the average. No unmatched item older than
30 days without a documented owner and a plan. The average hides the one item from March that nobody
has looked at since.</p>
<p><strong>Complaint rate reaching the ombudsman.</strong> UPI complaint volume passed 1.2 million a
month in early 2026, around 60% of it "debited but not credited". RB-IOS 2026 replaced the 2021
scheme from 1 July 2026, with awards up to &#8377;30 lakh for consequential loss and &#8377;3 lakh
for time, expense and harassment. What reaches the RBI CMS portal about you is a supervisory signal,
and it is visible to your regulator before it is visible to you unless you are watching for it.</p>
<h3 id="s-amber-next">What this feeds</h3>
<div class="mod-grid">
<a href="/fintech-ai/fraud-risk/" class="mod-card"><div class="mod-num">MODULE 03</div><h3>Fraud &amp; Risk</h3><p>Authorisation latency, step-up rather than block, and the chargeback evidence pack. Shares a queue with disputes.</p></a>
<a href="/fintech-ai/aml-compliance/" class="mod-card"><div class="mod-num">MODULE 04</div><h3>AML &amp; Compliance</h3><p>Real-time payment screening runs inside this latency budget, and FIU-IND registration is a PA obligation.</p></a>
<a href="/fintech-ai/customer-operations/" class="mod-card"><div class="mod-num">MODULE 06</div><h3>Customer Operations</h3><p>"Where is my refund" is the highest-volume contact reason in Indian fintech. Reconciliation quality is support volume.</p></a>
<a href="/fintech-ai/build-playbook/licensing-and-access/" class="mod-card"><div class="mod-num">PLAYBOOK</div><h3>Licensing &amp; Access</h3><p>PA authorisation, net worth thresholds and timelines if you are becoming the aggregator rather than using one.</p></a>
</div>
{warn("Everything on this page is illustrative. Payment systems move customer money and carry statutory obligations under the Payment and Settlement Systems Act and the RBI PA Directions. Nothing here is legal or financial advice. Have your settlement design, your escrow arrangements and your dispute workflow reviewed by qualified counsel before they touch a real rupee.")}
'''

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to read this build sheet", g_read),
   ("The economics that decide everything", g_econ),
   ("How to rank gateways — and how not to", g_rank),
 ],
 'indigo': [
   ("Raw materials — acceptance and rails", i_mat_accept),
   ("Raw materials — reconciliation and ledger", i_mat_recon),
   ("How to use each one — accepting money", i_accept),
   ("How to use each one — reconciliation", i_recon),
   ("How to use each one — payouts and the PA rules", i_payout),
   ("Cost per unit", i_cost),
 ],
 'amber': [
   ("Best combinations", a_combos),
   ("Three recommended builds", a_builds),
   ("What next", a_next),
 ],
}

TITLE = "Payments and Reconciliation Build Sheet"
META  = ("Every payment rail, gateway and reconciliation tool: how to use each one, what it really "
         "costs per transaction, and three recommended builds.")
LEAD  = ("Every gateway, rail and reconciliation tool a payments stack needs. What each one is for, "
         "the first working call, the gotcha nobody documents, real cost per transaction, and three "
         "recommended builds at three budgets.")

print(f"title len: {len(TITLE + ' | Clarigital')}")
print(f"meta len : {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/payments-reconciliation/build-sheet",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Build Sheet 05",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI"),
            ("/fintech-ai/payments-reconciliation/", "Payments and Reconciliation")],
  lanes  = lanes,
)
