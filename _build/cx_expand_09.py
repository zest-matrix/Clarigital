#!/usr/bin/env python3
"""cx_expand_09.py — Session 101. Clears the WRITE backlog: 24 pages.

THE REASON THIS SESSION IS DIFFERENT
S100 deferred two pages on a third template. Listing the remaining 24 showed
**18 of them use that template**, so the backlog was a template problem rather
than a content one. This script solves it.

THE THIRD TEMPLATE
`art-body` of three lane-sections (`lane-green`, `lane-indigo`, `lane-red`),
h2 ids numbered per lane as `s-{lane}-{n}`, and a `pg-toc` sidebar whose links
point at those ids. Adding an h2 without a TOC entry produces a page whose own
navigation omits one of its sections -- the derived-artefact defect class QA #7
and QA #8 both found.

So `splice_toc_atlas()` does three things together: appends the sections to the
end of the red lane with correctly numbered ids, inserts matching links after
the last red TOC entry, and then ASSERTS that every h2 id on the page appears
in the TOC. That last assertion is the one that matters -- it is the check the
defect would have failed.

ON CONTENT FOR TOOL PAGES
The 18 tool guides get sections about using a tool of that KIND well --
evaluation, adoption, what goes wrong -- rather than feature claims. Feature
detail on fast-moving AI tools goes stale between sessions and cannot be
verified from here; the existing pages already carry it and are dated. Durable
material is the honest contribution.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

GSC = ('official', 'Google Search Central documentation',
       'crawler access, structured data eligibility and the AI feature guidance referenced here',
       'developers.google.com')
FTC = ('official', 'FTC Endorsement Guides',
       'the disclosure obligations attaching to affiliate content', 'ftc.gov')
ASCI = ('official', 'ASCI Guidelines for Influencer Advertising in Digital Media',
        'the disclosure obligations for affiliate content aimed at Indian audiences', 'ascionline.in')

S = lambda t, c: (t, c)

# ---------------------------------------------------------------- shared text
EVAL = S('Evaluating It Against Your Own Work', '''
<p>Vendor demonstrations are built on material the tool handles well, so the only evaluation that
predicts anything is one run on your own inputs.</p>
<p><strong>Assemble twenty real examples before the trial starts</strong>, including the awkward ones —
the messy input, the edge case, the one that went wrong last month. A set of clean examples measures a
situation you do not have.</p>
<p><strong>Define what good looks like in writing</strong>, before you see any output. Deciding
afterwards is choosing the answer rather than measuring it, and it is what makes most tool trials
inconclusive.</p>
<p><strong>Time the whole task, not the tool.</strong> A tool that halves the generation step and adds
a verification step has not saved anything. Measure the end-to-end time including checking and
correction, because that is the number your team experiences.</p>
<p><strong>Have two people run the same examples.</strong> Tolerance for a given failure varies more
between people than between tools, and a decision made by one enthusiast rarely survives contact with
the team.</p>
<p><strong>And price the failure, not just the licence.</strong> What does a wrong output cost here —
a correction, an apology, a customer? That number decides how much checking you need, which is usually
the real cost of adoption.</p>
''')

ADOPT = S('Adoption, Which Is Where Tools Fail', '''
<p>Most tool decisions are made on capability and lost on adoption. The pattern is consistent enough to
plan around.</p>
<p><strong>Name an owner.</strong> Not a committee and not "the team" — one person responsible for the
configuration, the questions, and whether it is still earning its licence in six months. Tools without
an owner decay into a subscription nobody cancels.</p>
<p><strong>Start with one workflow, not the whole team.</strong> A narrow deployment that works spreads
on its own; a broad one that half-works produces a reputation the tool never recovers from.</p>
<p><strong>Write down what it is not for.</strong> The boundary matters more than the capability,
because the damage comes from use outside the intended case — and nobody is told where that edge is
unless someone writes it down.</p>
<p><strong>Keep the manual path working.</strong> For at least one cycle. A team that cannot fall back
is a team that cannot report a problem honestly.</p>
<p><strong>Review it on a date you set in advance.</strong> Three months, against the criteria you
wrote at the start. <strong>A tool nobody has reviewed is a tool nobody has decided to keep</strong> —
and the review is the only thing that ever removes one.</p>
''')

TRANSCRIBE = S('What Determines Transcription Accuracy in Practice', '''
<p>Accuracy figures quoted for speech models are measured on clean benchmark audio. Your accuracy is
determined mostly by things upstream of the model.</p>
<p><strong>Audio quality dominates.</strong> A single good microphone per speaker beats any model
improvement. Room echo, overlapping speech and a laptop microphone across a table cost more accuracy
than the gap between any two vendors.</p>
<p><strong>Domain vocabulary is the second factor.</strong> Product names, drug names, place names,
acronyms and people's names are where errors concentrate, and they are exactly the words that matter.
Most systems accept a custom vocabulary or keyword boost — supplying one is the highest-return
configuration step and it is routinely skipped.</p>
<p><strong>Accent and code-switching matter more than vendors admit</strong>, and in Indian contexts
particularly, where a single meeting may move between languages mid-sentence. Test on your own
speakers rather than on a demo.</p>
<p><strong>Speaker separation degrades faster than the words do.</strong> A transcript with accurate
text and wrong attribution is worse than a slightly less accurate one that knows who spoke.</p>
<p><strong>Measure on your own recordings and count the errors that matter</strong> — a misheard filler
word is not the same defect as a misheard figure.</p>
''')

CODEAGENT = S('Working With a Coding Agent Without Losing the Thread', '''
<p>The failure mode is not bad code. It is a large volume of plausible code that nobody has
understood, arriving faster than it can be reviewed.</p>
<p><strong>Keep the unit of work small.</strong> One change, one purpose, reviewable in a sitting. An
agent asked for a large refactor returns something you will approve because reading it properly costs
more than the work saved — which is how unreviewed code enters a codebase.</p>
<p><strong>Make the tests the specification.</strong> An agent working against a failing test has an
objective definition of done; one working against a description has your interpretation of its
interpretation.</p>
<p><strong>Commit in small steps and keep the history clean.</strong> The ability to bisect is what
makes an agent's output safe to accept, and it is the first thing lost when a session produces one
enormous commit.</p>
<p><strong>Read the diff, not the summary.</strong> The summary is generated from the same process that
produced the change, and it is confident about both.</p>
<p><strong>And watch the dependency additions.</strong> An agent will reach for a library to solve a
problem, and a new dependency is a decision with a long tail that nobody made deliberately.</p>
''')

MEETINGS = S('Consent, Retention and Who Can Read the Notes', '''
<p>A meeting recorder creates a permanent, searchable record of conversations people believed were
ephemeral, and the governance questions arrive after adoption rather than before.</p>
<p><strong>Consent is not a settings toggle.</strong> Recording rules vary by jurisdiction and several
require all parties to agree, not just the host. For external meetings, say it out loud at the start
rather than relying on a notification banner people do not read.</p>
<p><strong>Decide retention deliberately.</strong> Indefinite is a decision, and usually the wrong one:
a two-year archive of internal conversation is a disclosure liability in any dispute. Set a period and
enforce it.</p>
<p><strong>Work out who can search it.</strong> A tool where any colleague can retrieve any meeting is
a different organisation from one where access follows the participants. This is the question that
causes trouble later and is easiest to set at the start.</p>
<p><strong>Exclude the meetings that should not be recorded</strong> — performance conversations,
grievances, anything legally privileged — and make that a default rather than a reminder.</p>
<p><strong>And treat the summary as a draft.</strong> A generated action item attributed to the wrong
person, circulated automatically, is a small and recurring source of avoidable friction.</p>
''')

VIDEOTOOL = S('Where Automated Editing Earns Its Place', '''
<p>Automated video tools produce a competent first cut quickly, and the value depends entirely on what
happens next.</p>
<p><strong>They are strong at</strong> the mechanical work: finding the segments, cutting to length,
burning captions, reformatting aspect ratio. This is genuinely tedious and genuinely automatable.</p>
<p><strong>They are weak at judgement</strong> — which moment is actually the interesting one, where a
cut lands emotionally, when a pause should be kept. A tool optimising for engagement patterns produces
clips that look like every other clip.</p>
<p>So the workable pattern is <strong>automate the cut, decide the selection.</strong> Let the tool
propose, and have a person choose which of the proposals to publish. The time saved is real; the
selection is where your channel sounds like yours rather than like the tool.</p>
<p><strong>Check the captions rather than trusting them</strong>, particularly for names, figures and
anything technical. Burned-in captions are permanent and a wrong figure on screen is worse than no
caption.</p>
<p><strong>And keep the source.</strong> Automated output is disposable; the recording is the asset,
and a workflow that discards the original in favour of the export loses the ability to recut later.</p>
''')

MODELPICK = S('Placing It Against the Alternatives', '''
<p>Model choice is a routing decision rather than a ranking one, and the useful question is which part
of your traffic this is right for.</p>
<p><strong>Route by task, not by preference.</strong> Most requests in most applications are not hard.
Classification, extraction and formatting rarely need the most capable available option, and sending
everything to the top tier is the largest and most common overspend.</p>
<p><strong>Test on your own evaluation set</strong>, not on published benchmarks. A benchmark measures a
task that is not yours, and the ordering between models frequently reverses on specific work.</p>
<p><strong>Weigh the things that are not capability.</strong> Where the data goes and under whose terms.
Latency at your percentile, not the average. Whether the model can change underneath you, and whether
that matters for reproducibility. Rate limits at your peak rather than your mean.</p>
<p><strong>Assume you will move.</strong> Keep the provider behind an interface, keep prompts in
version control, and keep an evaluation set that runs against any of them. The cost of switching is
paid once at design time or repeatedly afterwards.</p>
<p><strong>And re-check on a schedule.</strong> This ordering changes faster than any procurement cycle,
so a decision made a year ago and never revisited is a decision that has quietly expired.</p>
''')

VOICEAGENT = S('Designing a Voice Agent People Do Not Hang Up On', '''
<p>Voice removes every affordance text gives you. There is no scrollback, no visible options, and no
way to skim — so the design constraints are different in kind, not degree.</p>
<p><strong>Say what it is in the first sentence.</strong> That the caller is speaking to an automated
system, and what it can do. Concealing it produces the complaint, and in several jurisdictions
disclosure is a requirement rather than a courtesy.</p>
<p><strong>Give a route to a human immediately and repeatedly.</strong> The single largest source of
anger with voice systems is the feeling of being trapped. An easy exit reduces escalations rather than
increasing them, which is the opposite of what most deployments assume.</p>
<p><strong>Handle interruption.</strong> People talk over systems; an agent that cannot be interrupted
feels broken within two turns.</p>
<p><strong>Keep turns short.</strong> A paragraph of speech is unlistenable. One idea, then stop.</p>
<p><strong>Confirm before acting</strong>, reading back anything consequential — an amount, a date, an
address — because a misheard digit in voice has no visible correction step.</p>
<p><strong>And measure abandonment and transfer rate, not containment.</strong> Containment rewards
trapping people, which is exactly the behaviour to avoid.</p>
''')

ENTSEARCH = S('Why Enterprise Search Projects Disappoint', '''
<p>The technology is rarely the problem. Three organisational conditions decide the outcome and none of
them is on the vendor's checklist.</p>
<p><strong>Permissions have to be right first.</strong> A search tool that respects your existing access
controls will faithfully expose whatever they already got wrong — and the discovery that a shared drive
was open to everyone usually arrives via search results. Audit before connecting, not after.</p>
<p><strong>The corpus has to be worth searching.</strong> Indexing five years of outdated documents
produces confident answers from superseded material. <strong>A good answer from a stale document is
worse than no answer</strong>, because it is believed. Decide what is authoritative and index that.</p>
<p><strong>Someone has to own the gaps.</strong> Search reveals what is not written down, which is
valuable and actionable only if a person is responsible for acting on it.</p>
<p><strong>And measure it on questions answered, not queries run.</strong> Query volume rises when
search works badly. Sample real queries, check whether the answer was right, and track that — it is
manual, it is the only honest measure, and it is what nobody does.</p>
''')

GTMDATA = S('Data Quality, Enrichment and the Limits of Both', '''
<p>Enrichment tools aggregate from many sources and the aggregate inherits every source's staleness.
Treating the output as fact is where these projects go wrong.</p>
<p><strong>Job titles and headcounts decay fastest</strong> — people move, companies restructure — and a
sequence addressing someone by a role they left is worse than a generic one.</p>
<p><strong>Match rates vary enormously by segment.</strong> Coverage is strong for large companies in
large markets and thin for small businesses and non-Western markets. Check the rate for <em>your</em>
segment before building a process that assumes coverage.</p>
<p><strong>Waterfall enrichment reports the first hit, not the best one.</strong> Knowing which source
supplied a field matters when the field turns out to be wrong.</p>
<p><strong>And verification is a separate step from enrichment.</strong> An email that exists is not an
email that is monitored.</p>
<p>On the legal position: <strong>enriched personal data is still personal data.</strong> Obtaining it
from a vendor does not supply a basis for processing it, and under a consent-based regime such as
India's DPDP framework there is no legitimate-interest fallback. <strong>The obligation follows the
data, not the contract that delivered it.</strong></p>
''')

# ------------------------------------------------------------------- the pages
TOOLS = {
 'ai-atlas/specialist-tools/images-design/krea': [EVAL, ADOPT],
 'ai-atlas/specialist-tools/images-design/recraft': [EVAL, ADOPT],
 'ai-atlas/specialist-tools/voice-audio/assemblyai': [TRANSCRIBE, EVAL],
 'ai-atlas/specialist-tools/voice-audio/deepgram': [TRANSCRIBE, EVAL],
 'ai-atlas/tools/amazon-nova': [MODELPICK, EVAL],
 'ai-atlas/tools/kimi': [MODELPICK, EVAL],
 'ai-atlas/tools/manus': [MODELPICK, ADOPT],
 'ai-atlas/tools/apple-intelligence': [MODELPICK, ADOPT],
 'ai-atlas/specialist-tools/business-productivity/fathom': [MEETINGS, ADOPT],
 'ai-atlas/specialist-tools/business-productivity/granola': [MEETINGS, ADOPT],
 'ai-atlas/specialist-tools/business-productivity/glean': [ENTSEARCH, ADOPT],
 'ai-atlas/specialist-tools/business-productivity/clay': [GTMDATA, ADOPT],
 'ai-atlas/specialist-tools/video/captions': [VIDEOTOOL, EVAL],
 'ai-atlas/specialist-tools/video/opus-clip': [VIDEOTOOL, EVAL],
 'ai-atlas/specialist-tools/coding/aider': [CODEAGENT, EVAL],
 'ai-atlas/specialist-tools/coding/cline': [CODEAGENT, EVAL],
 'ai-atlas/specialist-tools/coding/devin': [CODEAGENT, ADOPT],
 'ai-atlas/specialist-tools/voice-agents/bland-ai': [VOICEAGENT, EVAL],
}

CODEX = {
'codex/seo/ai-search/ranking-in-ai-assistants': dict(sources=[GSC], sections=[
 S('What You Can Control, and What You Cannot', '''
<p>Visibility in an assistant is not a ranking you can optimise in the way a search result is, and
being precise about the boundary saves a great deal of wasted effort.</p>
<p><strong>What you can influence:</strong> whether your content is crawlable by the relevant agents;
whether it is structured so an answer can be extracted without the surrounding page; whether your
claims are specific and checkable rather than hedged; and whether other sources that assistants rely on
— reference sites, industry publications, community discussions — say accurate things about you.</p>
<p><strong>What you cannot:</strong> which sources a given assistant draws on, how it weights them,
whether it cites at all, and what it says about you when it does not cite. Different assistants make
different choices and change them without notice.</p>
<p><strong>The practical consequence</strong> is that the durable work is the same work that makes a
page good: accurate, specific, structured and current. <strong>A team being sold assistant
optimisation as a distinct practice with distinct tooling should ask which part is not already in
their content brief.</strong></p>
'''),
 S('Monitoring Without a Rank Tracker', '''
<p>There is no console for this, so monitoring is manual and should be treated as a scheduled task
rather than a tool purchase.</p>
<p><strong>Write down twenty questions</strong> a prospective customer would actually ask in your
category, including your brand name and your competitors'.</p>
<p><strong>Ask them across the assistants your audience uses</strong>, monthly, from a clean session so
personalisation does not colour the result.</p>
<p><strong>Record three things:</strong> whether you appeared, whether what was said was accurate, and
who was cited instead.</p>
<p>That third column is the useful one. <strong>It tells you which sources the assistants trust in your
category</strong>, and being accurately represented on those sources is more tractable than trying to
influence the assistant directly.</p>
<p><strong>Correct inaccuracies at the source.</strong> If an assistant repeats something wrong about
your pricing or your product, the fix is usually a stale page somewhere — yours or a third party's —
rather than anything to do with the assistant.</p>
''')]),

'codex/seo/ai-search/generative-engine-optimisation': dict(sources=[GSC], sections=[
 S('Separating the Practice From the Marketing', '''
<p>GEO is sold as a new discipline and is mostly an old one with a new acronym. The honest split is
worth making before anyone buys tooling.</p>
<p><strong>Genuinely different:</strong> the unit of success is a citation rather than a click;
extraction matters more than ranking, so structure carries more weight than it used to; and
measurement is manual because there is no console.</p>
<p><strong>Not different at all:</strong> being crawlable, being accurate, being specific, being
current, being well structured, and being cited by other credible sources. That is the entire
substance of most GEO advice and it was in the SEO brief already.</p>
<p><strong>The test for any GEO recommendation:</strong> would this have been good advice three years
ago? If yes, it is SEO. If it involves stuffing a page with phrases meant for a model rather than a
reader, it is the 2010s keyword density argument wearing new clothes, and it will age the same way.</p>
'''),
 S('The Business Model Question Nobody Raises First', '''
<p>Before optimising to be the source of an answer, establish whether being that source is worth
anything to you.</p>
<p><strong>If your revenue depends on pageviews</strong> — advertising, affiliate, anything monetised
per visit — then succeeding at GEO on informational content means your material is used and your visit
is not. That is optimising against yourself, and it is worth saying out loud in the strategy meeting
rather than discovering in the traffic report.</p>
<p><strong>If your revenue depends on being chosen later</strong> — software, services, considered
purchases — then a citation at the moment of a question is genuinely valuable even with no click,
because it puts you in the consideration set.</p>
<p>So the strategic move differs by model. <strong>Publishers should be shifting effort toward content
that cannot be answered in a box</strong> — judgement, comparison, tools, anything requiring trust in a
named source. <strong>Everyone else should be making sure that what the assistants say about them is
accurate</strong>, which is a different and more tractable objective than visibility.</p>
''')]),

'codex/seo/ai-search/llms-txt-seo': dict(sources=[GSC], sections=[
 S('Deciding Your Crawler Policy Deliberately', '''
<p>Crawler access is a business decision presented as a technical one, and most sites have not made it
— they have inherited a default.</p>
<p>The positions available, and who each suits:</p>
<p><strong>Open to everything.</strong> Maximum visibility, no control over training use. Suits anyone
whose content is marketing rather than product.</p>
<p><strong>Allow retrieval, block training</strong>, where the distinction is respected. Several
crawlers are separable — one fetches to answer a live question, another collects for training — and
allowing the first while blocking the second is a coherent position. It depends on voluntary
compliance.</p>
<p><strong>Block everything.</strong> Protects the material and removes you from the answers, including
the ones where being named would have helped.</p>
<p><strong>The decision belongs to whoever owns the commercial model</strong>, not to whoever edits
`robots.txt`. Write down what you chose and why, because the person who inherits the file cannot infer
the intent from the syntax.</p>
'''),
 S('What llms.txt Is and Is Not', '''
<p>The proposal is a plain-text file at the site root that points to the pages you consider
authoritative, in a form easy to read without rendering.</p>
<p><strong>What it is:</strong> a curation signal — here is the canonical version, here is the current
documentation, ignore the archived variants. For a site with a large surface and a small authoritative
core, that is a genuinely useful thing to state.</p>
<p><strong>What it is not:</strong> a standard anyone is obliged to honour, a ranking mechanism, or a
substitute for `robots.txt`. It grants no access and removes none; it is advisory to whoever chooses
to read it.</p>
<p><strong>Is it worth doing?</strong> It costs an afternoon, it cannot hurt, and adoption is uneven
enough that the honest expectation is little measurable effect. That is a reasonable basis for doing
it and a poor basis for a project plan.</p>
<p><strong>The one caution:</strong> like every other derived file on a site, it goes stale. An
`llms.txt` pointing at pages that have moved is worse than none — so generate it rather than writing
it, and regenerate it when the site changes.</p>
''')]),

'codex/seo/ai-search/ai-overviews-optimisation': dict(sources=[GSC], sections=[
 S('Reading the Traffic Change Correctly', '''
<p>The pattern reported most often is impressions holding while clicks fall, and interpreting it
correctly determines whether you respond usefully or expensively.</p>
<p><strong>Segment before concluding anything.</strong> The effect is heavily concentrated in
informational queries with short factual answers. Transactional and navigational performance is often
unchanged, and a blended figure conceals both.</p>
<p><strong>Compare query by query, not in aggregate.</strong> Identify the specific queries where an
overview now appears and measure those against themselves over time. That is the only comparison that
isolates the cause.</p>
<p><strong>Do not respond by rewriting titles.</strong> A falling CTR on a query whose answer is now
displayed is not a title problem, and title work is where teams spend the first month for no return.</p>
<p><strong>Watch branded search and direct traffic</strong> as the indirect signal that appearing
without a click still does something.</p>
<p>And be honest in the reporting: <strong>some of this traffic is not coming back</strong>, and a plan
built on recovering it will keep failing.</p>
'''),
 S('Where the Effort Actually Pays', '''
<p>Two responses have evidence behind them and one does not.</p>
<p><strong>Be extractable.</strong> Answer in the first sentence under a heading, keep paragraphs
self-contained, state definitions plainly, and use specific checkable claims. This is what gets a page
used as a source, and it is better writing regardless.</p>
<p><strong>Shift the content mix.</strong> Toward questions that cannot be answered in a box —
comparisons with trade-offs, judgement calls, tools that need the user's own numbers, anything where
currency matters and a cached answer may be stale. This is the strategic response and it is slower than
anyone wants.</p>
<p><strong>What does not pay:</strong> trying to be excluded. Blocking the feature generally means
losing the organic result alongside it, which trades a reduced click rate for none.</p>
<p><strong>And measure the right thing.</strong> If you are being cited without being visited, the
metric that matters is whether people arrive later by name — so branded search volume and direct
traffic become the scoreboard, not sessions on the page.</p>
''')]),

'codex/affiliate-marketing/content-affiliate-marketing': dict(sources=[FTC, ASCI], sections=[
 S('Writing Reviews That Are Worth Trusting', '''
<p>The commercial incentive in affiliate content is obvious to readers, so credibility has to be
earned structurally rather than claimed.</p>
<p><strong>Say what you did not like.</strong> A review with no drawbacks reads as an advertisement,
and a specific, fair criticism does more for trust than any amount of enthusiasm.</p>
<p><strong>Recommend against something.</strong> A comparison where every option is excellent for
somebody is a comparison that has made no decision. Naming who should not buy a product is the
strongest available credibility signal.</p>
<p><strong>Be specific about the testing.</strong> How long, under what conditions, with what
alternatives. <em>"We tested this"</em> is a claim; <em>"we used it daily for six weeks alongside two
alternatives"</em> is evidence.</p>
<p><strong>Show the failure cases.</strong> The conditions where it did not work are the most useful
paragraph on the page and the most commonly omitted.</p>
<p><strong>And keep the commission out of the ordering.</strong> If the highest-paying product is
always first, readers work it out, and the credibility you spent years building is spent in one
comparison table.</p>
'''),
 S('Maintenance, Which Is the Whole Business', '''
<p>Affiliate content is an asset that decays. Products change, prices move, links break, and a review
that was accurate two years ago is now actively misleading — while still ranking.</p>
<p>The maintenance that matters, in order of return:</p>
<p><strong>Check that links still work and still pay.</strong> A dead or expired affiliate link earns
nothing and the page keeps sending traffic through it. Audit quarterly; this alone recovers more
revenue than most new content.</p>
<p><strong>Re-verify the facts on your highest-traffic pages.</strong> Specifications, prices, what is
in the box. Wrong details are what readers notice and what destroys trust fastest.</p>
<p><strong>Update rather than republish.</strong> A page with accumulated links and history is an
asset; replacing it with a new URL spends that asset to save an edit.</p>
<p><strong>Date your reviews visibly</strong> and say when they were last checked. Readers reward it
and it is the honest thing to do.</p>
<p><strong>And disclose in the content</strong>, near the recommendation, not only in a footer — the
obligation attaches to the relationship, and it survives the reader arriving mid-page from a search
result.</p>
''')]),

'ai-atlas/concepts/rag': dict(sources=[], sections=[
 S('Diagnosing a RAG System That Answers Badly', '''
<p>When a retrieval system gives a poor answer there are three distinct failure points, and fixing the
wrong one is the usual outcome.</p>
<p><strong>The document was never retrieved.</strong> Check first, always: search the index manually
for the passage that should have answered it. If it is not in the results, the problem is retrieval —
chunking, embedding, or the query — and no prompt change will fix it.</p>
<p><strong>It was retrieved and ignored.</strong> The passage is in the context and the answer
contradicts it. This is a prompting or model problem, and often a position problem — material in the
middle of a long context is used less reliably than material at either end.</p>
<p><strong>It was retrieved, used, and the source was wrong.</strong> The system worked perfectly and
the corpus was stale. <strong>This is the most dangerous failure because it is invisible</strong> — the
answer is confident, well-sourced and wrong, and the citation makes it more believable.</p>
<p><strong>Always check in that order.</strong> Teams routinely rewrite prompts for a retrieval problem
and re-tune retrieval for a stale-document problem.</p>
'''),
 S('The Corpus Is the Product', '''
<p>Most RAG effort goes into the pipeline and most of the quality comes from the documents. The ratio
should be closer to the reverse.</p>
<p><strong>Decide what is authoritative</strong> and index only that. Indexing everything means
indexing three superseded versions of the policy, and the system has no way to prefer the current one.</p>
<p><strong>Remove rather than add.</strong> The highest-return maintenance in most deployments is
deleting outdated documents, and it is never anyone's job.</p>
<p><strong>Date everything and surface the date in the answer</strong>, so a reader can judge currency
themselves.</p>
<p><strong>Cite to a location a person can open.</strong> A citation that cannot be checked is
decoration, and it increases trust without increasing reliability — the worst combination.</p>
<p><strong>And close the loop.</strong> When a user reports a bad answer, the question is which of the
three failure points it was, and the answer should change either the corpus or the pipeline. A system
with no feedback path degrades silently as the documents age around it.</p>
''')]),
}

# --------------------------------------------------------------- splice logic
ANCHORS = ['</div>\n    <aside class="guide-sidebar">',
           '\n\n    </main>\n    <aside class="art-sidebar">']
TOC_ANCHOR = '<div class="art-sidebar">'
_TPL = io.open('_build/codex_style.txt', encoding='utf-8').read()
SRCS_CSS = '\n' + _TPL[_TPL.index('.srcs{'):_TPL.index('.srcs a{word-break:break-word}') + len('.srcs a{word-break:break-word}')]
MD = re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')


def splice_toc_atlas(h, sections):
    """Append sections to the end of the red lane AND add matching TOC links.

    Asserts afterwards that every h2 id on the page appears in the TOC -- the
    check the deferred defect would have failed."""
    ids = re.findall(r'<h2[^>]*id="s-red-(\d+)"', h)
    assert ids, 'no red-lane h2 ids found'
    n = max(int(x) for x in ids) + 1
    block = ''.join('<h2 id="s-red-%d">%s</h2>\n%s\n' % (n + k, t, c)
                    for k, (t, c) in enumerate(sections))
    i = h.find(TOC_ANCHOR)
    assert i != -1 and h.count(TOC_ANCHOR) == 1, 'art-sidebar anchor'
    # the lane closes with two </div> immediately before the sidebar
    close = '</div>\n</div>\n'
    assert h[i - len(close):i] == close, 'unexpected lane close: %r' % h[i - 30:i]
    out = h[:i - len(close)] + block + h[i - len(close):]
    # TOC: insert after the last existing s-red link
    last = None
    for m in re.finditer(r'<a href="#s-red-\d+"[^>]*>.*?</a>', out, re.S):
        last = m
    assert last, 'no red TOC links'
    links = ''.join('<a href="#s-red-%d">%s</a>' % (n + k, t)
                    for k, (t, _) in enumerate(sections))
    out = out[:last.end()] + links + out[last.end():]
    # THE ASSERTION THAT MATTERS
    page_ids = set(re.findall(r'<h2[^>]*id="([^"]+)"', out))
    toc_ids = set(re.findall(r'<a href="#([^"]+)"', out))
    missing = page_ids - toc_ids
    assert not missing, 'h2 ids absent from the TOC: %s' % sorted(missing)
    return out


ALL = {}
for p, secs in TOOLS.items():
    ALL[p] = dict(sources=[], sections=secs)
ALL.update(CODEX)

done = 0
for path, cfg in ALL.items():
    f = path + '/index.html'
    assert os.path.exists(f), 'missing ' + f
    src = io.open(f, encoding='utf-8').read()
    if cfg['sections'][0][0] in src:
        print('  = already expanded: ' + path); continue
    add = ''.join('<h2>%s</h2>\n%s\n' % (t, c) for t, c in cfg['sections'])
    add += sources_block(cfg['sources'])
    assert not MD.findall(re.sub(r'<[^>]+>', ' ', add)), '%s: markdown' % f
    if 'pg-toc' in src:
        out = splice_toc_atlas(src, cfg['sections'])
        tag = 'toc-atlas'
    else:
        found = [a for a in ANCHORS if src.count(a) == 1]
        assert len(found) == 1, '%s: matched %d anchors' % (f, len(found))
        i = src.find(found[0])
        out = src[:i] + add + src[i:]
        tag = 'codex' if 'guide-sidebar' in found[0] else 'atlas'
    for t in ('<div', '</div>', '<ul', '</ul>', '<ol', '</ol>'):
        assert out.count(t) == src.count(t) + add.count(t), '%s: %s moved' % (f, t)
    assert len(re.findall(r'<h1[\s>]', out)) == 1
    assert out.count('</html>') == 1 and out.count('</body>') == 1
    # +2 sections, +1 more if a sources block was appended (it emits an <h2>)
    expect = 2 + (1 if cfg['sources'] else 0)
    assert len(re.findall(r'<h2[\s>]', out)) == len(re.findall(r'<h2[\s>]', src)) + expect, \
        '%s: h2 delta not %d' % (f, expect)
    if cfg['sources'] and '.srcs{' not in out:
        assert out.count('</style>') == 1
        out = out.replace('</style>', SRCS_CSS + '\n</style>', 1)
    io.open(f, 'w', encoding='utf-8').write(out)
    done += 1
    print('  ✅ %-52s [%s] +%d words' % (path[:52], tag,
          len(re.sub(r'<[^>]+>', ' ', add).split())))
print('\n%d pages expanded' % done)
