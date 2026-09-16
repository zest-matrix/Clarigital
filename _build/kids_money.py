#!/usr/bin/env python3
"""Session 60 — AI Kids: the 'Money Explorer' track.
Eight sessions on how money and AI actually work, for ages 9-12 with a parent.

Safety position, decided before any content was written:
  * nothing in this track asks a child to enter real card, bank or UPI details
  * no real accounts, no real transactions, no real money at any point
  * every money example is pretend, drawn on paper or typed into a chat
  * the scam session is the most important one and is placed before the project
  * parent present is stated on every session, not just the first
"""
import re, io, os, json

SRC = 'ai-kids/explorer/session-15/index.html'
OUT = 'ai-kids/money'
BASE = 'https://www.clarigital.com'

src = io.open(SRC, encoding='utf-8').read()
STYLE = re.search(r'<style>.*?</style>', src, re.S).group(0)
# Session 61, RULE 4: .kids-out is used by this track's nav but is not defined in
# the source page's CSS. Session 60 patched the OUTPUT; the rebuild regenerated it.
if '.kids-out{' not in STYLE:
    STYLE = STYLE.replace('</style>', '.kids-out{opacity:.55;font-weight:500}\n</style>')
GA4 = re.search(r'<script async src="https://www\.googletagmanager\.com.*?</script>\s*<script>.*?</script>', src, re.S)
GA4 = GA4.group(0) if GA4 else ''
SCRIPTS = [s for s in re.findall(r'<script>(?!.*gtag).*?</script>', src, re.S) if 'toggleParent' in s]
BEHAVIOUR = SCRIPTS[0] if SCRIPTS else '<script>function toggleParent(el){var b=el.nextElementSibling;b.classList.toggle("open");}</script>'

TRACK = "Money Explorer"
N = 12

def nav(active_self=False):
    return ('<body><nav class="kids-nav"><div class="kids-nav-inner">'
            '<a href="/ai-kids/" class="kids-logo"><div class="kids-logo-mark">\U0001F4B0</div>'
            f'<span>{TRACK}</span></a><div class="kids-nav-links">'
            '<a href="/ai-kids/">Home</a><a href="/ai-kids/safety/">Safety First</a>'
            f'<a href="/ai-kids/money/"{" class=\"active\"" if active_self else ""}>{TRACK}</a>'
            '<a href="/ai-kids/parents/">For Parents</a>'
            '<a href="/" class="kids-out">Clarigital \u2197</a></div></div></nav>')

def head(title, desc, canon, crumbs):
    ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(u,n) in enumerate(crumbs)]}
    art = {"@context":"https://schema.org","@type":"Article","headline":title,
           "description":desc,"inLanguage":"en-IN","datePublished":"2026-09-14",
           "dateModified":"2026-09-14","isAccessibleForFree":True,
           "publisher":{"@type":"Organization","name":"Clarigital"},
           "mainEntityOfPage":BASE+canon}
    return f'''<!DOCTYPE html><html lang="en-IN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{canon}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/og-ai-kids.png"><meta property="og:type" content="article">
<meta property="og:url" content="{BASE}{canon}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/og-ai-kids.png">
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(art)}</script>
{GA4}
{STYLE}
</head>'''

def dots(cur):
    d = ''.join(f'<div class="pdot {"done" if i<cur else "current" if i==cur else ""}">{i}</div>'
                for i in range(1, N+1))
    return (f'<div class="wrap" style="padding-top:22px"><div class="progress-dots">{d}</div>'
            f'<p style="text-align:center;font-size:.73rem;color:var(--faint);margin-top:4px">'
            f'Session {cur} of {N} \u2014 {TRACK}</p>')

def parent_panel(learned, questions, watch, safety):
    qs = ''.join(f'<li>{q}</li>' for q in questions)
    return ('<div class="parent-panel"><div class="parent-toggle" onclick="toggleParent(this)">'
            '<span>\U0001F468\u200D\U0001F469\u200D\U0001F467</span><h3>Parent Notes \u2014 tap to expand</h3>'
            '<span class="toggle-arrow" style="margin-left:auto;color:var(--faint)">\u25BC</span></div>'
            '<div class="parent-body">'
            f'<div class="parent-item"><div class="parent-item-label">What they learned</div><p>{learned}</p></div>'
            f'<div class="parent-item"><div class="parent-item-label">Questions to ask</div><ul>{qs}</ul></div>'
            f'<div class="parent-item"><div class="parent-item-label">What to watch for</div><p>{watch}</p></div>'
            f'<div class="parent-item"><div class="parent-item-label">Safety in context</div><p>{safety}</p></div>'
            '</div></div>')

# ------------------------------------------------------------------ CONTENT

S = [
 dict(n=1, emoji="\U0001F4B0", grad="#10B981,#0EA5E9",
  title="What Money Actually Is",
  sub="It is not the coin. It is the record of who has what.",
  goal="Your child works out that most money today is not an object at all \u2014 it is a number in a list that everyone agrees to trust.",
  warm="Ask: &ldquo;If I give you a ten rupee coin, where is the money?&rdquo; They will point at the coin. Then ask: &ldquo;If I send ten rupees to your mum&rsquo;s phone, where is the money now?&rdquo;",
  warm2="&ldquo;Today we find out where money actually lives.&rdquo;",
  main="<p>Take a sheet of paper. Write three names down the left \u2014 your child, you, and a made-up shop. Give everyone a starting number. This is your <strong>ledger</strong>.</p>"
       "<p>Now play. Your child &ldquo;buys&rdquo; something from the shop for 20. Cross out their number, write the new one. Do the same for the shop. Do this five or six times.</p>"
       "<p>Then ask the important question: <em>&ldquo;Nobody moved any coins. So did the money move?&rdquo;</em></p>",
  twist="<p>Tear the paper in half and throw one half away. Ask: &ldquo;How much money does everyone have now?&rdquo;</p>"
        "<p>Nobody knows. That is why real banks keep the list in several places at once, and why nobody is allowed to rub out a line \u2014 they can only add a new one underneath.</p>",
  badge=("\U0001F4D2","Ledger Badge","Worked out that money is a record, not a thing"),
  pl="That money is a shared record rather than a physical object, and that the record only works if everyone trusts it and nobody can secretly change it.",
  pq=["If the shop said you had less money than your list says, who would be right?",
      "Why do you think banks keep more than one copy of the list?",
      "What would happen if someone could rub out a line?"],
  pw="Some children find the idea genuinely unsettling \u2014 that money is &ldquo;just&rdquo; agreement. That reaction is the right one and worth sitting with rather than smoothing over.",
  ps="Nothing in this session touches a real account. Keep it on paper. If your child asks to see your banking app, that is a fine moment to show the balance and close it again \u2014 not to log in together as a habit."),

 dict(n=2, emoji="\U0001F511", grad="#6366F1,#8B5CF6",
  title="How Does It Know It Is You?",
  sub="Three ways a computer checks who you are, and why one is not enough.",
  goal="Your child learns the three kinds of proof \u2014 something you know, something you have, something you are \u2014 and why banks want two of them.",
  warm="Ask: &ldquo;If I phoned you and said I was your cousin, how would you know it was really them?&rdquo; Let them come up with tests.",
  warm2="&ldquo;Computers have exactly the same problem, and only three ways to solve it.&rdquo;",
  main="<p>Write three headings on paper: <strong>Know</strong> \u00b7 <strong>Have</strong> \u00b7 <strong>Are</strong>.</p>"
       "<p>Now sort things into them together. A password? Know. A phone that gets a code? Have. A fingerprint? Are. A face? Are. A secret handshake? Know. A key? Have.</p>"
       "<p>Then ask, for each one: <em>&ldquo;How could someone steal this?&rdquo;</em> A password can be guessed or told. A phone can be taken. A face is harder \u2014 but a photograph of a face is not.</p>",
  twist="<p>Ask your child to invent a way to prove they are them using <strong>two</strong> of the three. Then try to break it.</p>"
        "<p>This is exactly what a bank does, and exactly why it asks for a password <em>and</em> a code.</p>",
  badge=("\U0001F510","Identity Badge","Learned the three kinds of proof and why two beat one"),
  pl="The three authentication factors, and that security comes from combining categories rather than from making any single one longer or cleverer.",
  pq=["Which of the three is easiest for someone to steal?",
      "Why does a code sent to a phone help, if someone already knows the password?",
      "Is a photo of your face the same as your face?"],
  pw="Children often suggest &ldquo;a really long password&rdquo; as the answer. The useful correction is that a second <em>category</em> beats a longer version of the same one.",
  ps="<strong>Say this out loud and make them repeat it: a code that arrives on a phone is never, ever read out to anyone.</strong> Not to a bank, not to a delivery person, not to someone who says there is a problem. Nobody real ever asks."),

 dict(n=3, emoji="\U0001F4C4", grad="#F59E0B,#EF4444",
  title="Teaching a Computer to Read",
  sub="Why reading a bill is much harder than it looks.",
  goal="Your child discovers that a computer does not &ldquo;see&rdquo; a document \u2014 it guesses at shapes, and it tells you how sure it is.",
  warm="Write the same word twice \u2014 once neatly, once in your worst handwriting. Ask: &ldquo;Which one would a computer find harder?&rdquo;",
  warm2="&ldquo;Today we find out what a computer actually sees when it looks at writing.&rdquo;",
  main="<p>Write a pretend shop receipt on paper: shop name, three items, three prices, a total. Make one price deliberately smudged.</p>"
       "<p>Now play the computer. Your child reads it out loud and, after every single item, says how sure they are out of ten.</p>"
       "<p>The smudged one gets a low number. <strong>That number is the whole point.</strong> A real system does the same thing, and anything below its line goes to a human instead of being guessed at.</p>",
  twist="<p>Hand them the receipt upside down. Then at arm&rsquo;s length. Then folded so one item is hidden.</p>"
        "<p>Ask what the computer should do about the hidden one. The right answer is not to guess \u2014 it is to say <em>&ldquo;I could not find it.&rdquo;</em> Saying nothing and saying a made-up number are very different.</p>",
  badge=("\U0001F50D","Reader Badge","Learned that a good computer says how sure it is"),
  pl="That document AI produces a confidence score alongside every value, and that the honest behaviour when confidence is low is to escalate rather than guess.",
  pq=["What should the computer do if it is only 3 out of 10 sure?",
      "Is a wrong answer worse than no answer? When?",
      "How could you make the receipt easier for a computer to read?"],
  pw="The insight to listen for is your child distinguishing &ldquo;I do not know&rdquo; from &ldquo;here is a guess&rdquo;. That distinction is the entire safety argument for AI, in one sentence.",
  ps="If you use a chat AI for this session, photograph the <em>pretend</em> receipt you made together. Never photograph a real bill, statement or card \u2014 real documents have real numbers on them and those do not belong in a chat window."),

 dict(n=4, emoji="\U0001F50E", grad="#0EA5E9,#6366F1",
  title="Spotting the Odd One Out",
  sub="How a computer notices that something does not look right.",
  goal="Your child learns that fraud detection is pattern-spotting, and that a computer being suspicious is not the same as it being correct.",
  warm="Read out a list: samosa 20, chai 10, bus 15, <strong>aeroplane 40,000</strong>, pencil 5. Ask which one jumped out, and why.",
  warm2="&ldquo;You just did what a bank computer does all day.&rdquo;",
  main="<p>Write out a week of pretend spending for an imaginary person \u2014 ten small everyday amounts. Then add three odd ones somewhere in the middle: something huge, something at 3 in the morning, something in a country they have never visited.</p>"
       "<p>Your child is the detective. Which ones look wrong, and <strong>why</strong>? The why matters more than the which.</p>"
       "<p>Then the twist that matters: invent a perfectly innocent reason for each odd one. The huge one was a school trip. The 3am one was a birthday call abroad.</p>",
  twist="<p>Ask: &ldquo;If the computer blocks the card every time something looks odd, what happens to the person on the school trip?&rdquo;</p>"
        "<p>They get stuck, with no money, far from home. So a good system usually <em>asks</em> rather than blocks \u2014 a message, a question, a code \u2014 and only stops things when it is really sure.</p>",
  badge=("\U0001F575\uFE0F","Detective Badge","Learned that suspicious is not the same as guilty"),
  pl="Anomaly detection as pattern comparison, and the real cost of a false alarm \u2014 that blocking a legitimate person is a harm too, not a safe default.",
  pq=["What is the cost of the computer being wrong in each direction?",
      "How would you check, without blocking the person completely?",
      "What makes something &lsquo;normal&rsquo; for one person and odd for another?"],
  pw="Children reach for &ldquo;block it&rdquo; instantly. Getting them to feel the cost of the false alarm is the actual lesson, and it transfers well beyond money.",
  ps="Good moment to explain, plainly, that a real bank will sometimes send a message asking if a payment was really you \u2014 and that the answer is always to check with a parent first, never to tap a link in the message."),

 dict(n=5, emoji="\u2696\uFE0F", grad="#8B5CF6,#EC4899",
  title="Is That Fair?",
  sub="When a computer treats two people differently.",
  goal="Your child works out that a rule can look fair and still land unfairly, and that someone has to check.",
  warm="Ask: &ldquo;If I gave everyone in your class the same size shoes, would that be fair?&rdquo; Let them argue it out.",
  warm2="&ldquo;Same treatment and fair treatment are not always the same thing.&rdquo;",
  main="<p>Make up a rule together for a pretend pocket-money app: <em>&ldquo;You can borrow 100 rupees if you have saved at least 50.&rdquo;</em></p>"
       "<p>Now invent four different children and give each one a different situation \u2014 one gets pocket money weekly, one only on festivals, one shares with a sibling, one has none at all.</p>"
       "<p>Apply the same rule to all four. Ask: <em>&ldquo;The rule was identical for everyone. Did it treat them equally?&rdquo;</em></p>",
  twist="<p>Ask your child to fix the rule. Whatever they come up with, find someone it is unfair to.</p>"
        "<p>That is not a failure \u2014 it is the honest answer. There is no rule with no edges. Which is exactly why people have to keep checking, and why &ldquo;the computer decided&rdquo; is never a good enough reason.</p>",
  badge=("\u2696\uFE0F","Fairness Badge","Learned that the same rule can land differently"),
  pl="That algorithmic fairness is not automatic, that identical treatment can produce unequal outcomes, and that no rule is free of edge cases.",
  pq=["Who does your new rule work badly for?",
      "Should the computer ever be allowed to decide this on its own?",
      "Who should be allowed to say the computer got it wrong?"],
  pw="Resist rescuing them when their fixed rule also turns out unfair. The discovery that there is no perfect rule is the point, and arriving at it themselves makes it stick.",
  ps="Keep the examples imaginary. Using real family finances or real classmates makes this uncomfortable rather than instructive, and children repeat what they hear."),

 dict(n=6, emoji="\U0001F91D", grad="#10B981,#6366F1",
  title="Should a Computer Decide?",
  sub="Who says yes, who says no, and who has to explain.",
  goal="Your child learns the difference between a computer helping someone decide and a computer deciding on its own.",
  warm="Ask: &ldquo;Should a computer choose who gets into your school? Who wins a race? What you have for dinner?&rdquo; Sort them into yes, no, and it depends.",
  warm2="&ldquo;The question is not whether computers are clever. It is who has to explain the answer.&rdquo;",
  main="<p>Play lending. You are the computer, your child is a person asking to borrow 100 pretend rupees. Say no, and give no reason at all.</p>"
       "<p>Let them react. Then swap \u2014 they are the computer, and they must say no <em>and</em> give a reason a person could argue with.</p>"
       "<p>Ask: <em>&ldquo;Which no was easier to accept? Which one could you do something about?&rdquo;</em></p>",
  twist="<p>Now the hard one. They say no, and you ask: &ldquo;Why?&rdquo; \u2014 and they must answer &ldquo;I do not know, the computer said so.&rdquo;</p>"
        "<p>Ask how that feels. That is why real rules say a person must be able to explain a decision about you, and why a reason nobody can give is not a reason.</p>",
  badge=("\U0001F9E0","Explainer Badge","Learned that a decision you cannot explain is not good enough"),
  pl="That explainability is a right rather than a nicety, and that automated decisions about people need a human who can account for them.",
  pq=["What should happen if the computer cannot explain its answer?",
      "Should you be able to ask a person to look again?",
      "Is a fast wrong answer better than a slow right one?"],
  pw="This session often lands harder than expected, because being refused without a reason is something most children have already experienced somewhere.",
  ps="Worth saying plainly: nobody should ever ask your child for money, and no real service lends money to children. If anything online offers them money, coins, or credit, that is a scam \u2014 which is the next session."),

 dict(n=7, emoji="\U0001F6A8", grad="#EF4444,#F59E0B",
  title="Spotting a Scam",
  sub="The most important session in this track.",
  goal="Your child can recognise the four things every scam does, and knows the one rule that stops all of them.",
  warm="Ask: &ldquo;Has anyone ever tried to trick you \u2014 online, in a game, anywhere?&rdquo; Listen properly before moving on.",
  warm2="&ldquo;Every trick in the world does the same four things. Once you can see them, you can see all of them.&rdquo;",
  main="<p>Write the four signs on paper, big:</p>"
       "<p><strong>1. HURRY.</strong> &ldquo;Right now or you lose it.&rdquo; Real things wait.<br>"
       "<strong>2. SECRET.</strong> &ldquo;Do not tell your parents.&rdquo; This one alone is enough. Stop.<br>"
       "<strong>3. TOO GOOD.</strong> Free coins, free money, a prize you never entered.<br>"
       "<strong>4. ASKING.</strong> For a code, a password, a photo, money, or a favour.</p>"
       "<p>Now make up three fake messages together \u2014 a game offering free coins, a text saying a parcel is stuck, a friend&rsquo;s account asking for a code. For each one, your child names which of the four signs are present.</p>",
  twist="<p>Make one that has <em>only one</em> sign. Harder to spot, and much more like the real thing.</p>"
        "<p>Then the rule that covers everything: <strong>&ldquo;If someone asks me for a code, a password, or money \u2014 I stop and I tell a grown-up. Every time. Even if it looks like a friend.&rdquo;</strong> Have them say it. Then say it again tomorrow.</p>",
  safety_block="<strong>Say this together, out loud:</strong> &ldquo;Nobody real will ever ask me for a code. If someone asks me to keep a secret from my parents, that is the sign that I must tell them.&rdquo;",
  badge=("\U0001F6E1\uFE0F","Scam Spotter Badge","Can name the four signs and the one rule"),
  pl="The four structural features of social engineering \u2014 urgency, secrecy, an offer that is too good, and a request \u2014 plus a single rule that generalises to scams they have not seen yet.",
  pq=["Which of the four signs is the most serious on its own?",
      "What do you do if a message looks like it is from a friend?",
      "Why would someone pretend to be in a hurry?"],
  pw="If your child mentions something that has actually happened to them, stop the session and deal with that instead. It matters far more than finishing the activity.",
  ps="<strong>Revisit this session more than once.</strong> Scam awareness fades, and the secrecy sign is the one that protects against far more than fraud. Say the rule again in a month, and again after that."),

 dict(n=8, emoji="\U0001F3E6", grad="#0EA5E9,#10B981",
  title="Where Does the Bank Keep It?",
  sub="Your money is not sitting in a box with your name on it.",
  goal="Your child works out that a bank lends out most of what it holds, which is why it can pay you for keeping money there.",
  warm="Ask: &ldquo;If you give the bank 100 rupees, where does it go? Is there a box with your name on it?&rdquo; Most children think yes.",
  warm2="&ldquo;Today we find out what the bank actually does with it \u2014 and it is stranger than a box.&rdquo;",
  main="<p>You are the bank. Your child and two soft toys are customers. Each &lsquo;deposits&rsquo; 100 pretend rupees. You now hold 300.</p>"
       "<p>Now a fourth person (you again, in a different voice) wants to borrow 200 to buy a bicycle. Lend it out. You are holding 100 and owe 300.</p>"
       "<p>Ask: <em>&ldquo;Is that allowed? What happens if all three of us ask for our money today?&rdquo;</em> Let them worry about it \u2014 the worry is the correct response.</p>",
  twist="<p>Ask why anyone would agree to this. Then explain: the borrower pays a bit extra back, and the bank gives some of that extra to the people who left money there.</p>"
        "<p>That is interest. Now ask the hard one: <em>&ldquo;What if the borrower cannot pay it back?&rdquo;</em> That is exactly the question session 6 was about.</p>",
  badge=("\U0001F3E6","Banking Badge","Worked out that a bank lends out most of what it holds"),
  pl="Fractional reserve banking in its simplest form, and where interest comes from \u2014 plus the honest risk that sits underneath it.",
  pq=["What happens if everyone wants their money on the same day?",
      "Why would the bank pay you for keeping money there?",
      "Who decides whether someone is allowed to borrow?"],
  pw="The moment of unease when they realise the money is not there is the lesson. Do not rush past it into reassurance \u2014 sit in it, then explain the rules that exist because of it.",
  ps="If your child asks whether the bank could lose their money, answer honestly: it can happen, which is why banks are regulated and deposits are insured up to a limit. Vague reassurance teaches them to trust claims rather than rules."),

 dict(n=9, emoji="\U0001F3AF", grad="#F59E0B,#10B981",
  title="Saving Up Is Hard",
  sub="Why waiting is difficult, and how a helper can make it easier.",
  goal="Your child sees that saving is mostly about making a future thing feel real today, and designs something to help.",
  warm="Offer a deal: one biscuit now, or three biscuits after dinner. Whatever they choose, ask them why.",
  warm2="&ldquo;Everyone finds waiting hard. Today we work out how to make it easier.&rdquo;",
  main="<p>Pick something imaginary they want that costs 500 pretend rupees. They get 50 a week.</p>"
       "<p>Draw ten boxes. Colour one in for each week. Ask how it feels looking at ten empty boxes.</p>"
       "<p>Now change one thing at a time and ask whether it helps: seeing a picture of the thing &middot; a bar that fills up &middot; someone cheering at the halfway point &middot; being able to spend it any time, or not.</p>",
  twist="<p>Ask the sharp question: <em>&ldquo;Should the helper make it hard to spend the money early?&rdquo;</em></p>"
        "<p>Let them argue both ways. A helper that makes it impossible is bossy. One that makes it too easy is useless. Real apps make this choice for millions of people, and somebody decided it.</p>",
  badge=("\U0001F3AF","Saver Badge","Designed something that makes waiting easier"),
  pl="That saving behaviour is shaped by design choices, not willpower alone \u2014 and that those choices are made by somebody, on purpose.",
  pq=["Which change helped the most, and why?",
      "Should an app be allowed to stop you spending your own money?",
      "Who should decide \u2014 you, your parent, or the app?"],
  pw="Children who chose the biscuit now are not impatient \u2014 many have learned that promised future things do not always arrive. Worth noticing rather than correcting.",
  ps="Keep the target imaginary. Tying this to a real thing they want turns a design exercise into a negotiation about buying it."),

 dict(n=10, emoji="\u26A0\uFE0F", grad="#EF4444,#8B5CF6",
  title="When the Computer Gets It Wrong",
  sub="It will. The question is what happens next.",
  goal="Your child learns that being wrong is normal for these systems, and that knowing who to tell is the actual skill.",
  warm="Ask: &ldquo;Has a computer, a game or an app ever got something wrong about you?&rdquo; Let them tell the whole story.",
  warm2="&ldquo;Today is not about stopping mistakes. It is about what you do about them.&rdquo;",
  main="<p>Make up three things going wrong: the app says they spent money they did not spend &middot; it blocks something completely normal &middot; it says they saved 500 when they saved 50.</p>"
       "<p>For each one ask three questions, in order: <strong>How would you notice? Who would you tell? What proof do you have?</strong></p>"
       "<p>The third one is the surprise. Proof is what the record from session 1 was for.</p>",
  twist="<p>Now the uncomfortable version: the app insists it is right, and they cannot prove otherwise.</p>"
        "<p>Ask what should happen. The answer is that a <strong>person</strong> has to be able to look, and that &ldquo;the computer says so&rdquo; is never the end of the conversation. Anyone who tells them otherwise is wrong \u2014 including an adult.</p>",
  badge=("\U0001F6E0\uFE0F","Fixer Badge","Knows that being wrong is normal and who to tell"),
  pl="That automated systems fail routinely, that noticing and escalating is the real skill, and that a human must always be reachable behind a machine decision.",
  pq=["How would you even notice that number was wrong?",
      "Who do you tell first?",
      "What if the grown-up says the computer must be right?"],
  pw="The last question matters most. A child who will push back against an adult who defers to a machine has learned something that will serve them for decades.",
  ps="Reinforce here: telling a parent is always the right first step, and no real service ever asks a child to sort out a money problem by themselves or in secret."),

 dict(n=11, emoji="\U0001F441\uFE0F", grad="#8B5CF6,#0EA5E9",
  title="Who Can See What You Bought?",
  sub="Every payment leaves a trail. The trail says a lot.",
  goal="Your child realises that a list of purchases describes a person, and decides who should be allowed to read it.",
  warm="Show them a made-up list of ten things somebody bought in a week. Ask: &ldquo;What kind of person is this? How old? What do they like?&rdquo;",
  warm2="&ldquo;You just worked out a lot about someone you have never met. From a shopping list.&rdquo;",
  main="<p>Your child writes a pretend week of purchases for an invented character \u2014 nothing real, nothing about your family.</p>"
       "<p>Swap. Each of you guesses about the other&rsquo;s character from the list alone. Age, mood, plans, worries.</p>"
       "<p>Then ask: <em>&ldquo;Who should be allowed to read this list?&rdquo;</em> Sort it together \u2014 the bank &middot; the shop &middot; an advert company &middot; a school &middot; a stranger &middot; a parent.</p>",
  twist="<p>Ask what the advert company would do with it. Then ask whether the person would know.</p>"
        "<p>That is why rules exist about asking permission first, telling people what you will use it for, and not quietly using it for something else later.</p>",
  badge=("\U0001F512","Privacy Badge","Learned that a spending list describes a person"),
  pl="That transaction data is personal data, that inference from ordinary records is powerful, and that consent and purpose limits exist for a reason.",
  pq=["What is the most private thing on that list?",
      "Should a shop be allowed to sell the list?",
      "Would you want somebody to ask you first?"],
  pw="Children are often more comfortable sharing than adults expect. The aim is not to frighten them \u2014 it is to make the trail visible so the choice becomes a choice.",
  ps="Use an invented character only. Real family spending is private from siblings and friends too, and this session can otherwise become something repeated at school."),
 dict(n=12, emoji="\U0001F6E0\uFE0F", grad="#10B981,#0EA5E9",
  title="Build Your Own Money Helper",
  sub="Put the whole track together into one thing you made.",
  goal="Your child designs a money helper of their own and decides, deliberately, what it is not allowed to do.",
  warm="Ask: &ldquo;Across these twelve sessions, what surprised you most?&rdquo; Then: &ldquo;What would you want a money helper to do for you?&rdquo;",
  warm2="&ldquo;Today you design it. And you decide the rules it has to follow.&rdquo;",
  main="<p>On paper or with a chat AI, your child designs a pretend money helper. It might track pocket money, split a bill between friends, or save up for something.</p>"
       "<p>Four things it must have, and they come straight from the track:</p>"
       "<p><strong>A record</strong> it never rubs out (session 1). <strong>A way to check it is really them</strong> (session 2). <strong>A reason</strong> it can give whenever it says no (session 6). <strong>A way to tell a person</strong> when it gets something wrong (session 10).</p>"
       "<p>Then the most important part. Ask them to write the list of things it is <strong>never allowed to do</strong>.</p>",
  twist="<p>Try to break it. Ask awkward questions: what if two people say they paid? What if it is not sure? What if someone claims to be them and is in a hurry?</p>"
        "<p>Every good system has a plan for being unsure. Ask what theirs does \u2014 the right answer is ask a person, not guess.</p>",
  badge=("\U0001F3C6","Money Explorer","Finished the whole track and built something"),
  pl="Synthesis \u2014 applying the ledger, identity, confidence, fairness and explainability ideas to a system of their own design, including its limits.",
  pq=["What is your helper not allowed to do, and why?",
      "What does it do when it is not sure?",
      "Which session changed your mind about something?"],
  pw="The &ldquo;never allowed to do&rdquo; list tells you what has actually landed. A child who writes real limits has understood the track; one who writes none has enjoyed it without absorbing it.",
  ps="Before you finish, ask them to say the four scam signs and the one rule from session 7 without looking. If they cannot, do session 7 again. It is the one that matters most."),
]

os.makedirs(OUT, exist_ok=True)
built = []

for s in S:
    n = s['n']
    path = f"{OUT}/session-{n}"
    canon = f"/ai-kids/money/session-{n}/"
    os.makedirs(path, exist_ok=True)
    title = f"{s['title']} \u2014 Money Explorer {n}"
    desc = (f"Session {n} of {N}. {s['sub']} A 25-minute activity for ages 9-12 with a parent. "
            "No real money, no accounts.")[:164]
    safety = (f'<div class="activity-block safety"><div class="block-label safety">Safety</div>'
              f'<p>{s["safety_block"]}</p></div>') if s.get('safety_block') else ''
    body = f'''{head(title, desc, canon, [("/","Home"),("/ai-kids/","AI Kids"),("/ai-kids/money/",TRACK),(canon,s['title'])])}
{nav()}
{dots(n)}
<div class="session-card">
<div class="session-header" style="background:linear-gradient(135deg,{s['grad']})">
  <div class="session-badge-row"><span class="session-num" style="background:rgba(255,255,255,.22);color:#fff">{TRACK} &middot; Session {n} of {N}</span><span class="session-time" style="color:rgba(255,255,255,.78)">&#9201; 25 min &middot; &#128102; Parent present</span></div>
  <h1 style="color:#fff">{s['emoji']} {s['title']}</h1>
  <p style="color:rgba(255,255,255,.88)">{s['sub']}</p>
</div>
<div class="session-body">
  <div class="info-box">&#127919; <strong>Today&apos;s goal:</strong> {s['goal']}</div>
  <h2>&#128293; Warm Up &mdash; 2 minutes</h2>
  <div class="activity-block warmup"><div class="block-label warmup">Warm Up</div><p>{s['warm']}</p><p style="margin-top:7px;font-weight:600;color:var(--text)">{s['warm2']}</p></div>
  <h2>&#129302; The Activity &mdash; 15 minutes</h2>
  <div class="activity-block main"><div class="block-label main">Main Activity</div>{s['main']}</div>
  <h2>&#129513; The Twist &mdash; 5 minutes</h2>
  <div class="activity-block twist"><div class="block-label twist">The Twist</div>{s['twist']}</div>
  {safety}
  <div class="badge-earn"><div class="badge-icon">{s['badge'][0]}</div><h3 style="font-size:.95rem;font-weight:700;color:var(--green);margin-bottom:4px">{s['badge'][1]}</h3><p style="font-size:.82rem;color:var(--muted)">{s['badge'][2]}</p><div style="margin-top:8px;font-size:.73rem;color:var(--faint)">&#10003; Ask your parent to mark this session complete</div></div>
  {parent_panel(s['pl'], s['pq'], s['pw'], s['ps'])}
  <div style="display:flex;justify-content:space-between;gap:10px;margin-top:22px;flex-wrap:wrap">
    {'<a href="/ai-kids/money/session-'+str(n-1)+'/" style="font-size:.8rem;color:var(--muted);text-decoration:none">&larr; Session '+str(n-1)+'</a>' if n>1 else '<a href="/ai-kids/money/" style="font-size:.8rem;color:var(--muted);text-decoration:none">&larr; Track home</a>'}
    {'<a href="/ai-kids/money/session-'+str(n+1)+'/" style="font-size:.8rem;color:var(--green);font-weight:600;text-decoration:none">Session '+str(n+1)+' &rarr;</a>' if n<N else '<a href="/ai-kids/money/" style="font-size:.8rem;color:var(--green);font-weight:600;text-decoration:none">Track home &rarr;</a>'}
  </div>
</div></div></div>
{BEHAVIOUR}
</body></html>'''
    io.open(f"{path}/index.html", 'w', encoding='utf-8').write(body)
    built.append(canon)

# ------------------------------------------------------------------ INDEX
cards = ''.join(
  f'<a href="/ai-kids/money/session-{s["n"]}/" class="session-link">'
  f'<div class="sl-num">{s["n"]}</div><div><div class="sl-title">{s["emoji"]} {s["title"]}</div>'
  f'<div class="sl-sub">{s["sub"]}</div></div></a>' for s in S)

idx_title = "Money Explorer \u2014 AI and Money for Kids"
idx_desc = ("Twelve sessions on how money and AI really work, for ages 9-12 with a parent. "
            "No real money, no accounts, no card details. Free.")
idx = f'''{head(idx_title, idx_desc, "/ai-kids/money/", [("/","Home"),("/ai-kids/","AI Kids"),("/ai-kids/money/",TRACK)])}
{nav(True)}
<div class="wrap" style="padding-top:26px">
<div class="session-card">
<div class="session-header" style="background:linear-gradient(135deg,#10B981,#0EA5E9)">
  <div class="session-badge-row"><span class="session-num" style="background:rgba(255,255,255,.22);color:#fff">12 sessions &middot; Ages 9&ndash;12</span><span class="session-time" style="color:rgba(255,255,255,.78)">&#9201; 25 min each &middot; &#128102; Parent present</span></div>
  <h1 style="color:#fff">&#128176; Money Explorer</h1>
  <p style="color:rgba(255,255,255,.88)">How money and AI actually work &mdash; from what money really is to how to spot a scam.</p>
</div>
<div class="session-body">
<div class="activity-block safety"><div class="block-label safety">Read this first</div>
<p><strong>Nothing in this track uses real money.</strong> No bank accounts, no card numbers, no UPI, no payment apps. Every example is pretend, written on paper or typed into a chat.</p>
<p style="margin-top:8px">A parent is present for every session. Session 7 is about spotting scams and is the most important one here &mdash; do not skip it, and come back to it more than once.</p></div>
<p style="font-size:.88rem;color:var(--muted);line-height:1.7;margin:16px 0">Children grow up with money that they never see. It arrives on a phone and leaves on a phone, and the part in between is invisible. This track makes it visible, and then shows where AI sits inside it &mdash; reading, checking, deciding, and getting things wrong.</p>
<h2>&#128218; The twelve sessions</h2>
<div class="session-list">{cards}</div>
<div class="info-box" style="margin-top:20px">&#128102; <strong>For parents:</strong> each session has a Parent Notes panel with what your child learned, questions to ask, what to watch for, and the safety point in context. Read it before you start.</div>
<div style="margin-top:18px"><a href="/ai-kids/" style="font-size:.82rem;color:var(--muted);text-decoration:none">&larr; All AI Kids tracks</a></div>
</div></div></div>
<style>
.session-list{{display:flex;flex-direction:column;gap:9px;margin-top:12px}}
.session-link{{display:flex;gap:13px;align-items:flex-start;padding:13px 15px;background:var(--card,#fff);border:1px solid var(--border,#E5E7EB);border-radius:12px;text-decoration:none;transition:border-color .18s}}
.session-link:hover{{border-color:var(--green)}}
.sl-num{{flex-shrink:0;width:26px;height:26px;border-radius:50%;background:var(--green);color:#fff;font-size:.78rem;font-weight:700;display:flex;align-items:center;justify-content:center}}
.sl-title{{font-size:.9rem;font-weight:700;color:var(--text);margin-bottom:2px}}
.sl-sub{{font-size:.78rem;color:var(--muted);line-height:1.55}}
</style>
{BEHAVIOUR}
</body></html>'''
io.open(f"{OUT}/index.html", 'w', encoding='utf-8').write(idx)
built.append("/ai-kids/money/")

print(f"built {len(built)} pages")
for b in built: print("  ", b)
