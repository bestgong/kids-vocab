#!/usr/bin/env python3
"""Generate kids vocab HTML page from vocabulary.json"""
import json, random

with open('/workspace/kids_vocab/vocabulary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
books = data['books']

quiz_data = []
for w in words:
    if not w.get('examples'):
        continue
    ex = random.choice(w['examples'])
    blank_ex = ex.replace(w['word'], '______', 1) if w['word'] in ex else '______ ' + ex
    others = [ow['word'] for ow in words if ow['word'] != w['word'] and len(ow['word']) > 1]
    if len(others) < 3:
        continue
    wrong_opts = random.sample(others, 3)
    options = wrong_opts + [w['word']]
    random.shuffle(options)
    quiz_data.append({'word': w['word'], 'meaning': w['meaning'], 'blank': blank_ex, 'answer': w['word'], 'options': options, 'books': w.get('books', [])})

data_json = json.dumps(data, ensure_ascii=False)
quiz_json = json.dumps(quiz_data, ensure_ascii=False)

html_parts = []
html_parts.append('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>小朋友英语词汇学习</title>')
html_parts.append('<style>\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody { font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #fce4ec 0%, #e8f5e9 30%, #e3f2fd 60%, #fff9c4 100%); min-height: 100vh; }\n.header { background: linear-gradient(135deg, #ff6b6b, #ffa502); padding: 16px 24px; color: white; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 20px rgba(255,107,107,0.3); position: sticky; top: 0; z-index: 100; }\n.header h1 { font-size: 1.6em; }\n.header-stats { display: flex; gap: 12px; font-size: 0.85em; flex-wrap: wrap; }\n.header-stats span { background: rgba(255,255,255,0.25); padding: 5px 12px; border-radius: 20px; }\n.tabs { display: flex; gap: 8px; padding: 16px 24px 0; justify-content: center; flex-wrap: wrap; }\n.tab { padding: 10px 22px; border-radius: 25px; border: none; font-size: 1em; cursor: pointer; transition: all 0.3s; font-weight: 600; background: white; color: #666; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }\n.tab:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }\n.tab.active { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; }\n.tab.highlight { background: linear-gradient(135deg, #fd79a8, #e84393); color: white; animation: glowPulse 2s infinite; }\n@keyframes glowPulse { 0%,100% { box-shadow: 0 2px 8px rgba(253,121,168,0.3); } 50% { box-shadow: 0 4px 24px rgba(253,121,168,0.6); } }\n.main { max-width: 900px; margin: 20px auto; padding: 0 20px; }\n.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; margin-top: 16px; }\n.book-card { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); transition: all 0.3s; cursor: pointer; border: 2px solid transparent; }\n.book-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); border-color: #6c5ce7; }\n.book-card h3 { font-size: 1.1em; color: #2d3436; margin-bottom: 4px; }\n.book-card .cn-title { color: #636e72; font-size: 0.9em; margin-bottom: 8px; }\n.book-card .word-count { display: inline-block; background: #dfe6e9; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; color: #636e72; }\n.book-card .level-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; color: white; margin-left: 6px; }\n.panel { display: none; }\n.panel.active { display: block; }\n.word-list { margin-top: 16px; }\n.word-item { background: white; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }\n.word-en { font-size: 1.3em; font-weight: 700; color: #2d3436; }\n.word-pos { display: inline-block; background: #6c5ce7; color: white; padding: 2px 8px; border-radius: 8px; font-size: 0.7em; margin-left: 8px; vertical-align: middle; }\n.word-cn { color: #636e72; margin-top: 4px; font-size: 0.95em; }\n.word-ex { color: #b2bec3; margin-top: 6px; font-size: 0.88em; font-style: italic; line-height: 1.5; }\n.word-books { display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }\n.book-tag { background: #dfe6e9; padding: 2px 8px; border-radius: 10px; font-size: 0.75em; color: #636e72; }\n.search-bar { margin: 16px auto; max-width: 500px; }\n.search-bar input { width: 100%; padding: 12px 20px; border-radius: 25px; border: 2px solid #dfe6e9; font-size: 1em; outline: none; }\n.search-bar input:focus { border-color: #6c5ce7; }\n.back-btn { background: #dfe6e9; border: none; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 0.9em; margin-bottom: 16px; }\n.back-btn:hover { background: #b2bec3; }\n.book-header { background: white; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }\n.book-header h2 { font-size: 1.5em; color: #2d3436; }\n.book-header .cn { color: #636e72; font-size: 1.1em; }\n.quiz-container { background: white; border-radius: 16px; padding: 24px; margin-top: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }\n.quiz-progress { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }\n.quiz-bar { flex: 1; height: 8px; background: #dfe6e9; border-radius: 4px; overflow: hidden; }\n.quiz-bar-fill { height: 100%; background: linear-gradient(90deg, #6c5ce7, #a29bfe); transition: width 0.5s; border-radius: 4px; }\n.quiz-score { font-weight: 700; color: #6c5ce7; font-size: 1.1em; }\n.quiz-question { font-size: 1.1em; margin-bottom: 8px; color: #2d3436; }\n.quiz-sentence { background: #f8f9fa; padding: 16px; border-radius: 12px; margin-bottom: 16px; font-size: 1.15em; color: #2d3436; line-height: 1.6; }\n.quiz-sentence .blank { border-bottom: 2px dashed #6c5ce7; padding: 0 8px; font-weight: 600; color: #6c5ce7; }\n.quiz-options { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }\n.quiz-opt { padding: 12px 16px; border: 2px solid #dfe6e9; border-radius: 12px; background: white; cursor: pointer; font-size: 1em; transition: all 0.2s; text-align: center; font-weight: 500; }\n.quiz-opt:hover { border-color: #6c5ce7; background: #f3f0ff; }\n.quiz-opt.correct { border-color: #00b894; background: #e6fff9; color: #00b894; font-weight: 700; }\n.quiz-opt.wrong { border-color: #ff7675; background: #ffe6e6; color: #ff7675; }\n.quiz-opt.disabled { pointer-events: none; opacity: 0.7; }\n.quiz-next { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; border: none; padding: 12px 28px; border-radius: 25px; font-size: 1em; cursor: pointer; display: none; margin: 0 auto; font-weight: 600; }\n.quiz-next:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(108,92,231,0.4); }\n.quiz-result { text-align: center; padding: 40px 20px; }\n.quiz-result h2 { font-size: 2em; color: #6c5ce7; margin-bottom: 16px; }\n.quiz-result .score-big { font-size: 3em; font-weight: 800; background: linear-gradient(135deg, #6c5ce7, #e84393); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }\n.quiz-result .wrong-list { text-align: left; margin-top: 20px; }\n.quiz-result .wrong-item { background: #ffe6e6; padding: 10px 14px; border-radius: 10px; margin-bottom: 8px; color: #d63031; }\n.quiz-filter { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }\n.quiz-filter-btn { padding: 6px 14px; border-radius: 16px; border: 1px solid #dfe6e9; background: white; cursor: pointer; font-size: 0.85em; }\n.quiz-filter-btn:hover, .quiz-filter-btn.active { border-color: #6c5ce7; background: #f3f0ff; color: #6c5ce7; }\n.sm2-badge { display: inline-block; padding: 2px 8px; border-radius: 8px; font-size: 0.7em; margin-left: 6px; }\n.sm2-new { background: #74b9ff; color: white; }\n.sm2-learning { background: #fdcb6e; color: #2d3436; }\n.sm2-review { background: #55efc4; color: #2d3436; }\n.sm2-mastered { background: #00b894; color: white; }\n.footer { text-align: center; padding: 40px 20px; color: #b2bec3; font-size: 0.85em; }\n</style>')
html_parts.append('</head>\n<body>')
html_parts.append('<div class="header"><h1>小朋友英语词汇学习</h1><div class="header-stats"><span>' + str(len(books)) + '本读物</span><span>' + str(len(words)) + '个词</span><span>' + str(len(quiz_data)) + '道题</span></div></div>')
html_parts.append('<div class="tabs"><button class="tab active" onclick="showPanel(\'books\')">词汇本</button><button class="tab" onclick="showPanel(\'all-words\')">全部单词</button><button class="tab highlight" onclick="showPanel(\'quiz\')">测试题</button></div>')
html_parts.append('<div class="main"><div id="panel-books" class="panel active"><div class="search-bar"><input type="text" placeholder="搜索书名或单词..." oninput="filterBooks(this.value)"></div><div class="card-grid" id="book-grid"></div></div><div id="panel-book-detail" class="panel"><button class="back-btn" onclick="showPanel(\'books\')">返回书架</button><div id="book-detail"></div></div><div id="panel-all-words" class="panel"><div class="search-bar"><input type="text" placeholder="搜索英文或中文..." oninput="filterWords(this.value)"></div><div class="word-list" id="all-words-list"></div></div><div id="panel-quiz" class="panel"><div class="quiz-filter" id="quiz-filter"></div><div id="quiz-area"></div></div></div>')
html_parts.append('<div class="footer">小朋友英语词汇学习 SM-2间隔重复 ' + str(len(books)) + '本分级读物 ' + str(len(words)) + '词</div>')

js = '''<script>
const DATA = ''' + data_json + ''';
const QUIZ = ''' + quiz_json + ''';
const BOOKS_MAP = {};
DATA.books.forEach(b => { BOOKS_MAP[b.title] = b; });
function getSM2() { return JSON.parse(localStorage.getItem('kids_vocab_sm2') || '{}'); }
function saveSM2(sm2) { localStorage.setItem('kids_vocab_sm2', JSON.stringify(sm2)); }
function getWordState(word) { const s = getSM2(); return s[word] || {interval:0, repetition:0, efactor:2.5, nextDate:'', status:'new'}; }
function setWordState(word, state) { const s = getSM2(); s[word] = state; saveSM2(s); }
function showPanel(id) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-'+id).classList.add('active');
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  if(id==='books'||id==='book-detail') document.querySelectorAll('.tab')[0].classList.add('active');
  else if(id==='all-words') document.querySelectorAll('.tab')[1].classList.add('active');
  else if(id==='quiz') { document.querySelectorAll('.tab')[2].classList.add('active'); initQuiz(); }
}
function renderBooks(filter) {
  filter = filter || '';
  const grid = document.getElementById('book-grid');
  grid.innerHTML = '';
  DATA.books.forEach((b, i) => {
    const wds = DATA.words.filter(w => (w.books||[]).includes(b.title));
    if(filter && !b.title.toLowerCase().includes(filter.toLowerCase()) && !(b.cn||'').includes(filter) && !wds.some(w=>w.word.toLowerCase().includes(filter.toLowerCase()))) return;
    const level = i < 11 ? 'L1-Phonics' : i < 30 ? 'L1-Elephant&Piggie' : i < 42 ? 'L2-First Reading' : 'L1-Little Critter';
    const badge_color = i >= 42 ? '#6c5ce7' : i >= 30 ? '#e17055' : i >= 11 ? '#00b894' : '#0984e3';
    grid.innerHTML += '<div class="book-card" onclick="showBookDetail(\\''+b.title.replace(/'/g,"\\\\'")+'\\')"><h3>'+b.title+'</h3><div class="cn-title">'+(b.cn||'')+'</div><span class="word-count">'+wds.length+'词</span><span class="level-badge" style="background:'+badge_color+'">'+level+'</span></div>';
  });
}
function filterBooks(v) { renderBooks(v); }
function showBookDetail(title) {
  const b = BOOKS_MAP[title];
  const wds = DATA.words.filter(w => (w.books||[]).includes(title));
  const detail = document.getElementById('book-detail');
  detail.innerHTML = '<div class="book-header"><h2>'+b.title+'</h2><div class="cn">'+(b.cn||'')+'</div></div>';
  wds.forEach(w => {
    const st = getWordState(w.word);
    const badge = st.status==='mastered'?'<span class="sm2-badge sm2-mastered">已掌握</span>':st.status==='review'?'<span class="sm2-badge sm2-review">复习</span>':st.status==='learning'?'<span class="sm2-badge sm2-learning">学习中</span>':'<span class="sm2-badge sm2-new">新词</span>';
    detail.innerHTML += '<div class="word-item"><div><span class="word-en">'+w.word+'</span><span class="word-pos">'+w.pos+'</span>'+badge+'</div><div class="word-cn">'+w.meaning+'</div>'+(w.examples||[]).map(e=>'<div class="word-ex">'+e+'</div>').join('')+'</div>';
  });
  showPanel('book-detail');
}
function renderAllWords(filter) {
  filter = filter || '';
  const list = document.getElementById('all-words-list');
  list.innerHTML = '';
  DATA.words.forEach(w => {
    if(filter && !w.word.toLowerCase().includes(filter.toLowerCase()) && !w.meaning.includes(filter)) return;
    const st = getWordState(w.word);
    const badge = st.status==='mastered'?'<span class="sm2-badge sm2-mastered">已掌握</span>':st.status==='review'?'<span class="sm2-badge sm2-review">复习</span>':st.status==='learning'?'<span class="sm2-badge sm2-learning">学习中</span>':'<span class="sm2-badge sm2-new">新词</span>';
    list.innerHTML += '<div class="word-item"><div><span class="word-en">'+w.word+'</span><span class="word-pos">'+w.pos+'</span>'+badge+'</div><div class="word-cn">'+w.meaning+'</div>'+(w.examples||[]).slice(0,2).map(e=>'<div class="word-ex">'+e+'</div>').join('')+'<div class="word-books">'+(w.books||[]).map(b=>'<span class="book-tag">'+b+'</span>').join('')+'</div></div>';
  });
}
function filterWords(v) { renderAllWords(v); }
let quizQueue=[], quizIdx=0, quizCorrect=0, quizWrong=[], quizBookFilter='';
function initQuiz() {
  const filterDiv = document.getElementById('quiz-filter');
  let filterHTML = '<button class="quiz-filter-btn active" onclick="setQuizFilter(this,\\'\\')">全部</button>';
  DATA.books.forEach(b => { filterHTML += '<button class="quiz-filter-btn" onclick="setQuizFilter(this,\\''+b.title.replace(/'/g,"\\\\'")+'\\')">'+(b.cn||b.title)+'</button>'; });
  filterDiv.innerHTML = filterHTML;
  startQuiz();
}
function setQuizFilter(btn, book) {
  document.querySelectorAll('.quiz-filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  quizBookFilter = book;
  startQuiz();
}
function startQuiz() {
  let pool = QUIZ;
  if(quizBookFilter) pool = QUIZ.filter(q => (q.books||[]).includes(quizBookFilter));
  quizQueue = [...pool].sort(() => Math.random()-0.5).slice(0, 20);
  quizIdx = 0; quizCorrect = 0; quizWrong = [];
  renderQuizQuestion();
}
function renderQuizQuestion() {
  const area = document.getElementById('quiz-area');
  if(quizIdx >= quizQueue.length) { renderQuizResult(); return; }
  const q = quizQueue[quizIdx];
  const pct = Math.round((quizIdx/quizQueue.length)*100);
  const blankHTML = q.blank.replace('______','<span class="blank">______</span>');
  let optsHTML = '';
  q.options.forEach(o => { optsHTML += '<button class="quiz-opt" onclick="checkAnswer(this,\\''+o.replace(/'/g,"\\\\'")+'\\',\\''+q.answer.replace(/'/g,"\\\\'")+'\\')">'+o+'</button>'; });
  area.innerHTML = '<div class="quiz-container"><div class="quiz-progress"><div class="quiz-bar"><div class="quiz-bar-fill" style="width:'+pct+'%"></div></div><div class="quiz-score">'+quizIdx+'/'+quizQueue.length+'</div></div><div class="quiz-question">选择正确的单词填入空白处：</div><div class="quiz-sentence">'+blankHTML+'</div><div class="quiz-options">'+optsHTML+'</div><button class="quiz-next" id="quiz-next" onclick="nextQuestion()">下一题</button></div>';
}
function checkAnswer(btn, chosen, answer) {
  const opts = document.querySelectorAll('.quiz-opt');
  opts.forEach(o => { o.classList.add('disabled'); if(o.textContent === answer) o.classList.add('correct'); if(o.textContent === chosen && chosen !== answer) o.classList.add('wrong'); });
  if(chosen === answer) {
    quizCorrect++;
    const st = getWordState(answer);
    st.repetition = (st.repetition||0) + 1;
    st.efactor = Math.max(1.3, (st.efactor||2.5) + 0.1);
    st.interval = st.repetition < 2 ? 1 : Math.round(st.interval * st.efactor);
    st.status = st.repetition >= 5 ? 'mastered' : st.repetition >= 2 ? 'review' : 'learning';
    const d = new Date(); d.setDate(d.getDate()+st.interval);
    st.nextDate = d.toISOString().slice(0,10);
    setWordState(answer, st);
  } else {
    quizWrong.push({word:answer, chosen:chosen});
    const st = getWordState(answer);
    st.repetition = 0; st.interval = 0; st.efactor = Math.max(1.3, (st.efactor||2.5) - 0.2);
    st.status = 'learning';
    setWordState(answer, st);
  }
  document.getElementById('quiz-next').style.display = 'block';
}
function nextQuestion() { quizIdx++; renderQuizQuestion(); }
function renderQuizResult() {
  const area = document.getElementById('quiz-area');
  const pct = quizQueue.length ? Math.round(quizCorrect/quizQueue.length*100) : 0;
  let html = '<div class="quiz-result"><h2>测试完成！</h2><div class="score-big">'+pct+'%</div><p style="margin-top:8px;color:#636e72">答对 '+quizCorrect+'/'+quizQueue.length+' 题</p>';
  if(quizWrong.length) {
    html += '<div class="wrong-list"><h3 style="margin-bottom:10px;color:#d63031">错题回顾</h3>';
    quizWrong.forEach(w => { html += '<div class="wrong-item"><strong>'+w.word+'</strong> - 你选了 "'+w.chosen+'"</div>'; });
    html += '</div>';
  }
  html += '<button class="quiz-next" style="display:block;margin-top:24px" onclick="startQuiz()">再做一组</button></div>';
  area.innerHTML = html;
}
renderBooks();
renderAllWords();
</script>'''

html_parts.append(js)
html_parts.append('\n</body>\n</html>')

with open('/workspace/kids_vocab/index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print(f"HTML: {len(books)} books, {len(words)} words, {len(quiz_data)} quiz")
