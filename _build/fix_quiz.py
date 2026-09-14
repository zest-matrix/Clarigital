#!/usr/bin/env python3
"""Session 47b — repair the course quiz. Six defects, 68 pages.
Every change is verified BEFORE the file is written."""
import glob, re, io

OLD_TOGGLE = """function toggleQuiz(id){
  var body=document.getElementById(id);
  var icon=document.getElementById(id+'-icon');
  body.classList.toggle('open');
  if(icon)icon.textContent=body.classList.contains('open')?'\u25b4':'\u25be';
}"""

NEW_JS = """function toggleQuiz(id){
  var body=document.getElementById(id);
  if(!body)return;
  var open=body.classList.toggle('open');
  var icon=document.getElementById(id+'-icon');
  if(!icon){
    var sec=body.parentNode;
    var btn=sec?sec.querySelector('.quiz-toggle'):null;
    if(btn)icon=btn.querySelector('.qt-arrow');
  }
  if(icon)icon.textContent=open?'\u25b4':'\u25be';
  var btn2=body.parentNode?body.parentNode.querySelector('.quiz-toggle'):null;
  if(btn2)btn2.setAttribute('aria-expanded',open?'true':'false');
}
function checkAnswer(btn,ok){
  var q=btn.closest?btn.closest('.quiz-q'):null;
  if(!q)return;
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){opts[i].classList.remove('correct','wrong');opts[i].disabled=true;}
  btn.classList.add(ok?'correct':'wrong');
  var fb=q.querySelector('.quiz-feedback');
  if(fb){
    fb.textContent=ok?'Correct.':'Not quite. The right answer is highlighted above.';
    fb.className='quiz-feedback '+(ok?'ok':'no');
    if(!ok){
      for(var j=0;j<opts.length;j++){
        if(opts[j].getAttribute('onclick')&&opts[j].getAttribute('onclick').indexOf('true')>-1){
          opts[j].classList.add('correct');
        }
      }
    }
  }
}"""

OLD_CSS = ".quiz-body{display:none;padding-top:16px}\n.quiz-body.open{display:block}"
NEW_CSS = (
  # RULE 6: content renders without JavaScript. Collapse only when JS is present.
  ".quiz-body{display:block;padding-top:16px}\n"
  "html.js .quiz-body{display:none}\n"
  "html.js .quiz-body.open{display:block}\n"
  # markup emits .quiz-opts / .quiz-feedback / .qt-arrow; none of them had any CSS
  ".quiz-opts{display:flex;flex-direction:column;gap:7px}\n"
  ".quiz-feedback{font-size:.82rem;margin-top:10px;line-height:1.6;color:var(--muted)}\n"
  ".quiz-feedback.ok{color:var(--green)}\n"
  ".quiz-feedback.no{color:var(--amber)}\n"
  ".quiz-opt.wrong{background:rgba(239,68,68,.12);border-color:rgba(239,68,68,.35);color:#F87171}\n"
  ".quiz-opt:disabled{cursor:default}\n"
  ".qt-arrow{color:var(--muted);font-size:.75rem;flex-shrink:0}"
)

stats = {k: 0 for k in ('js', 'css', 'bools', 'inline', 'skipped', 'written')}
bool_total = 0
problems = []

files = sorted(glob.glob('courses/**/index.html', recursive=True))

for f in files:
    h = io.open(f, encoding='utf-8').read()
    if 'quiz-toggle' not in h:
        continue
    orig = h

    # --- 1. JS: replace toggleQuiz, add checkAnswer -----------------------
    if OLD_TOGGLE in h:
        assert h.count(OLD_TOGGLE) == 1, f"{f}: toggleQuiz appears {h.count(OLD_TOGGLE)}x"
        h = h.replace(OLD_TOGGLE, NEW_JS)
        stats['js'] += 1
    elif 'function checkAnswer' not in h:
        problems.append(f"{f}: toggleQuiz not in expected form and no checkAnswer")

    # --- 2. CSS ----------------------------------------------------------
    if OLD_CSS in h:
        assert h.count(OLD_CSS) == 1, f"{f}: quiz CSS appears {h.count(OLD_CSS)}x"
        h = h.replace(OLD_CSS, NEW_CSS)
        stats['css'] += 1
    elif '.quiz-opts{' not in h:
        problems.append(f"{f}: quiz CSS block not found")

    # --- 3. Python booleans leaked into JavaScript ------------------------
    n = len(re.findall(r'checkAnswer\(this,(?:True|False)\)', h))
    if n:
        h = h.replace('checkAnswer(this,True)', 'checkAnswer(this,true)')
        h = h.replace('checkAnswer(this,False)', 'checkAnswer(this,false)')
        assert 'checkAnswer(this,True)' not in h and 'checkAnswer(this,False)' not in h
        stats['bools'] += 1
        bool_total += n

    # --- 4. inline display:none (beats the class, and breaks rule 6) ------
    pat = r'(<div class="quiz-body" id="[^"]+") style="display:none"'
    m = len(re.findall(pat, h))
    if m:
        h = re.sub(pat, r'\1', h)
        stats['inline'] += m

    # --- VERIFY BEFORE WRITING -------------------------------------------
    if h == orig:
        stats['skipped'] += 1
        continue
    b_o = re.sub(r'<script.*?</script>', '', orig[orig.find('<body'):], flags=re.S)
    b_n = re.sub(r'<script.*?</script>', '', h[h.find('<body'):], flags=re.S)
    assert b_n.count('<div') == b_n.count('</div>'), f"{f}: div imbalance"
    assert b_n.count('<div') == b_o.count('<div'), f"{f}: div count changed"
    assert h.count('<head>') == 1 and h.count('</html>') == 1, f"{f}: structure"
    assert 'True)' not in h.replace('isAccessibleForFree', ''), f"{f}: stray python bool"

    io.open(f, 'w', encoding='utf-8').write(h)
    stats['written'] += 1

print(f"course pages touched          : {stats['written']}")
print(f"  toggleQuiz replaced         : {stats['js']}")
print(f"  checkAnswer now defined     : {stats['js']}")
print(f"  CSS block rewritten         : {stats['css']}")
print(f"  pages with bools fixed      : {stats['bools']}  ({bool_total} occurrences)")
print(f"  inline display:none removed : {stats['inline']}")
print(f"  unchanged                   : {stats['skipped']}")
if problems:
    print("\nPROBLEMS:")
    for p in problems:
        print("  ", p)
