#!/usr/bin/env python3
"""Generate kids vocab HTML page from vocabulary.json - Performance optimized"""
import json, random

with open('/workspace/kids_vocab/vocabulary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
books = data['books']

# Pre-build book->words index
book_words = {}
for b in books:
    book_words[b['title']] = [w for w in words if b['title'] in w.get('books', [])]

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
bw_json = json.dumps(book_words, ensure_ascii=False)

html = []
html.append('<!DOCTYPE html>')
html.append('<html lang="zh-CN">')
html.append('<head>')
html.append('<meta charset="UTF-8">')
html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
html.append('<title>小朋友英语词汇学习</title>')
html.append('<style>')
html.append('* { margin: 0; padding: 0; box-sizing: border-box; }')
html.append('body { font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #fce4ec 0%, #e8f5e9 30%, #e3f2fd 60%, #fff9c4 100%); min-height: 100vh; }')
html.append('.header { background: linear-gradient(135deg, #ff6b6b, #ffa502); padding: 16px 24px; color: white; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 20px rgba(255,107,107,0.3); position: sticky; top: 0; z-index: 100; }')
html.append('.header h1 { font-size: 1.6em; }')
html.append('.header-stats { display: flex; gap: 12px; font-size: 0.85em; flex-wrap: wrap; }')
html.append('.header-stats span { background: rgba(255,255,255,0.25); padding: 5px 12px; border-radius: 20px; }')
html.append('.tabs { display: flex; gap: 8px; padding: 16px 24px 0; justify-content: center; flex-wrap: wrap; }')
html.append('.tab { padding: 10px 22px; border-radius: 25px; border: none; font-size: 1em; cursor: pointer; transition: all 0.3s; font-weight: 600; background: white; color: #666; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }')
html.append('.tab:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }')
html.append('.tab.active { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; }')
html.append('.tab.highlight { background: linear-gradient(135deg, #fd79a8, #e84393); color: white; animation: glowPulse 2s infinite; }')
html.append('@keyframes glowPulse { 0%,100% { box-shadow: 0 2px 8px rgba(253,121,168,0.3); } 50% { box-shadow: 0 4px 24px rgba(253,121,168,0.6); } }')
html.append('.main { max-width: 900px; margin: 20px auto; padding: 0 20px; }')
html.append('.panel { display: none; }')
html.append('.panel.active { display: block; }')
html.append('.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; margin-top: 16px; }')
html.append('.book-card { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); transition: all 0.3s; cursor: pointer; border: 2px solid transparent; }')
html.append('.book-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); border-color: #6c5ce7; }')
html.append('.book-card h3 { font-size: 1.1em; color: #2d3436; margin-bottom: 4px; }')
html.append('.cn-title { color: #636e72; font-size: 0.9em; margin-bottom: 8px; }')
html.append('.word-count { background: #dfe6e9; color: #2d3436; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; margin-right: 6px; }')
html.append('.level-badge { color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75em; }')
html.append('.search-bar { margin: 16px 0; }')
html.append('.search-bar input { width: 100%; padding: 12px 20px; border: 2px solid #dfe6e9; border-radius: 25px; font-size: 1em; outline: none; transition: border-color 0.3s; }')
html.append('.search-bar input:focus { border-color: #6c5ce7; }')
html.append('.word-item { background: white; border-radius: 12px; padding: 14px 18px; margin-bottom: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }')
html.append('.word-en { font-size: 1.15em; font-weight: 700; color: #2d3436; margin-right: 8px; }')
html.append('.word-pos { color: #6c5ce7; font-size: 0.85em; font-weight: 600; margin-right: 8px; }')
html.append('.word-cn { color: #636e72; margin-top: 4px; font-size: 0.95em; }')
html.append('.word-ex { color: #b2bec3; font-size: 0.85em; margin-top: 4px; font-style: italic; padding-left: 12px; border-left: 2px solid #dfe6e9; }')
html.append('.word-books { margin-top: 6px; display: flex; gap: 4px; flex-wrap: wrap; }')
html.append('.book-tag { background: #dfe6e9; color: #636e72; padding: 2px 8px; border-radius: 10px; font-size: 0.75em; }')
html.append('.sm2-badge { font-size: 0.7em; padding: 2px 8px; border-radius: 10px; margin-left: 6px; }')
html.append('.sm2-new { background: #dfe6e9; color: #636e72; }')
html.append('.sm2-learning { background: #ffeaa7; color: #d63031; }')
html.append('.sm2-review { background: #81ecec; color: #00cec9; }')
html.append('.sm2-mastered { background: #55efc4; color: #00b894; }')
html.append('.back-btn { background: white; border: 2px solid #6c5ce7; color: #6c5ce7; padding: 8px 20px; border-radius: 20px; cursor: pointer; font-size: 0.95em; margin-bottom: 16px; }')
html.append('.back-btn:hover { background: #6c5ce7; color: white; }')
html.append('.book-header { margin-bottom: 16px; }')
html.append('.book-header h2 { font-size: 1.5em; color: #2d3436; }')
html.append('.book-header .cn { color: #636e72; font-size: 1.1em; }')
html.append('.quiz-filter { display: flex; gap: 6px; flex-wrap: wrap; margin: 16px 0; }')
html.append('.quiz-filter-btn { padding: 6px 14px; border-radius: 16px; border: 1px solid #dfe6e9; background: white; color: #636e72; cursor: pointer; font-size: 0.85em; transition: all 0.2s; }')
html.append('.quiz-filter-btn.active { background: #6c5ce7; color: white; border-color: #6c5ce7; }')
html.append('.quiz-container { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }')
html.append('.quiz-progress { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }')
html.append('.quiz-bar { flex: 1; height: 8px; background: #dfe6e9; border-radius: 4px; overflow: hidden; }')
html.append('.quiz-bar-fill { height: 100%; background: linear-gradient(90deg, #6c5ce7, #a29bfe); border-radius: 4px; transition: width 0.3s; }')
html.append('.quiz-score { font-weight: 700; color: #6c5ce7; min-width: 50px; text-align: right; }')
html.append('.quiz-question { font-size: 1.1em; color: #2d3436; margin-bottom: 12px; font-weight: 600; }')
html.append('.quiz-sentence { font-size: 1.15em; color: #2d3436; margin-bottom: 24px; line-height: 1.6; padding: 16px; background: #f8f9fa; border-radius: 12px; }')
html.append('.blank { color: #6c5ce7; font-weight: 700; border-bottom: 2px solid #6c5ce7; padding: 0 4px; }')
html.append('.quiz-options { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }')
html.append('.quiz-opt { padding: 14px; border: 2px solid #dfe6e9; border-radius: 12px; background: white; font-size: 1.05em; cursor: pointer; transition: all 0.2s; }')
html.append('.quiz-opt:hover:not(.disabled) { border-color: #6c5ce7; background: #f8f7ff; }')
html.append('.quiz-opt.correct { border-color: #00b894; background: #55efc4; color: white; }')
html.append('.quiz-opt.wrong { border-color: #d63031; background: #fab1a0; color: white; }')
html.append('.quiz-opt.disabled { cursor: default; opacity: 0.7; }')
html.append('.quiz-next { display: none; background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; border: none; padding: 12px 30px; border-radius: 25px; font-size: 1em; cursor: pointer; margin-top: 12px; }')
html.append('.quiz-next:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(108,92,231,0.4); }')
html.append('.quiz-result { text-align: center; }')
html.append('.score-big { font-size: 4em; font-weight: 800; background: linear-gradient(135deg, #6c5ce7, #e84393); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 16px 0; }')
html.append('.wrong-list { margin-top: 20px; text-align: left; }')
html.append('.wrong-item { background: #ffeaa7; padding: 8px 14px; border-radius: 8px; margin-bottom: 6px; font-size: 0.95em; }')
html.append('.footer { text-align: center; padding: 24px; color: #b2bec3; font-size: 0.85em; }')
html.append('.load-more { display: block; margin: 16px auto; padding: 10px 30px; border-radius: 20px; border: 2px solid #6c5ce7; background: white; color: #6c5ce7; font-size: 1em; cursor: pointer; }')
html.append('.load-more:hover { background: #6c5ce7; color: white; }')
html.append('</style>')
html.append('</head>')
html.append('<body>')
html.append('<div class="header"><h1>小朋友英语词汇学习</h1><div class="header-stats"><span>' + str(len(books)) + '本读物</span><span>' + str(len(words)) + '个词</span><span>' + str(len(quiz_data)) + '道题</span></div></div>')
html.append('<div class="tabs"><button class="tab active" onclick="showPanel(\'books\')">词汇本</button><button class="tab" onclick="showPanel(\'all-words\')">全部单词</button><button class="tab highlight" onclick="showPanel(\'quiz\')">测试题</button></div>')
html.append('<div class="main">')
html.append('<div id="panel-books" class="panel active"><div class="search-bar"><input type="text" placeholder="搜索书名或单词..." oninput="filterBooks(this.value)"></div><div class="card-grid" id="book-grid"></div></div>')
html.append('<div id="panel-book-detail" class="panel"><button class="back-btn" onclick="showPanel(\'books\')">返回书架</button><div id="book-detail"></div></div>')
html.append('<div id="panel-all-words" class="panel"><div class="search-bar"><input type="text" placeholder="搜索英文或中文..." oninput="filterWords(this.value)"></div><div class="word-list" id="all-words-list"></div><button class="load-more" id="load-more-btn" onclick="loadMoreWords()" style="display:none">加载更多</button></div>')
html.append('<div id="panel-quiz" class="panel"><div class="quiz-filter" id="quiz-filter"></div><div id="quiz-area"></div></div>')
html.append('</div>')
html.append('<div class="footer">小朋友英语词汇学习 SM-2间隔重复 ' + str(len(books)) + '本分级读物 ' + str(len(words)) + '词</div>')

# JavaScript - Performance optimized
js_code = '<script>\n'
js_code += 'const DATA = ' + data_json + ';\n'
js_code += 'const QUIZ = ' + quiz_json + ';\n'
js_code += 'const BW = ' + bw_json + ';\n'
js_code += """const BOOKS_MAP = {};
DATA.books.forEach(b => { BOOKS_MAP[b.title] = b; });

// SM2 helpers - cache parsed state
let _sm2Cache = null;
function getSM2() {
  if (!_sm2Cache) _sm2Cache = JSON.parse(localStorage.getItem('kids_vocab_sm2') || '{}');
  return _sm2Cache;
}
function saveSM2() { localStorage.setItem('kids_vocab_sm2', JSON.stringify(_sm2Cache)); }
function getWordState(word) { const s = getSM2(); return s[word] || {interval:0, repetition:0, efactor:2.5, nextDate:'', status:'new'}; }
function setWordState(word, state) { const s = getSM2(); s[word] = state; saveSM2(); }

function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }

const PANELS = ['books','book-detail','all-words','quiz'];
function showPanel(id) {
  PANELS.forEach(p => { var el = document.getElementById('panel-'+p); if(el) el.classList.remove('active'); });
  document.getElementById('panel-'+id).classList.add('active');
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  if(id==='books'||id==='book-detail') document.querySelectorAll('.tab')[0].classList.add('active');
  else if(id==='all-words') { document.querySelectorAll('.tab')[1].classList.add('active'); renderAllWords(); }
  else if(id==='quiz') { document.querySelectorAll('.tab')[2].classList.add('active'); initQuiz(); }
}

function renderBooks(filter) {
  filter = (filter||'').toLowerCase();
  var parts = [];
  DATA.books.forEach(function(b, i) {
    var wds = BW[b.title] || [];
    if(filter && !b.title.toLowerCase().includes(filter) && !(b.cn||'').includes(filter) && !wds.some(function(w){return w.word.toLowerCase().includes(filter)})) return;
    var level = i < 11 ? 'L1-Phonics' : i < 30 ? 'L1-Elephant&Piggie' : i < 42 ? 'L2-First Reading' : 'L1-Little Critter';
    var bc = i >= 42 ? '#6c5ce7' : i >= 30 ? '#e17055' : i >= 11 ? '#00b894' : '#0984e3';
    parts.push('<div class="book-card" onclick="showBookDetail(\\''+esc(b.title).replace(/'/g,"\\\\'")+'\\')"><h3>'+esc(b.title)+'</h3><div class="cn-title">'+esc(b.cn||'')+'</div><span class="word-count">'+wds.length+'词</span><span class="level-badge" style="background:'+bc+'">'+level+'</span></div>');
  });
  document.getElementById('book-grid').innerHTML = parts.join('');
}
function filterBooks(v) { renderBooks(v); }

function showBookDetail(title) {
  var b = BOOKS_MAP[title];
  var wds = BW[title] || [];
  var parts = ['<div class="book-header"><h2>'+esc(b.title)+'</h2><div class="cn">'+esc(b.cn||'')+'</div></div>'];
  wds.forEach(function(w) {
    var st = getWordState(w.word);
    var badge = st.status==='mastered'?'<span class="sm2-badge sm2-mastered">已掌握</span>':st.status==='review'?'<span class="sm2-badge sm2-review">复习</span>':st.status==='learning'?'<span class="sm2-badge sm2-learning">学习中</span>':'<span class="sm2-badge sm2-new">新词</span>';
    parts.push('<div class="word-item"><div><span class="word-en">'+esc(w.word)+'</span><span class="word-pos">'+esc(w.pos)+'</span>'+badge+'</div><div class="word-cn">'+esc(w.meaning)+'</div>'+(w.examples||[]).map(function(e){return '<div class="word-ex">'+esc(e)+'</div>'}).join('')+'</div>');
  });
  document.getElementById('book-detail').innerHTML = parts.join('');
  showPanel('book-detail');
}

// All words - lazy pagination
var _allWordsRendered = 0;
var _allWordsFilter = '';
var PAGE_SIZE = 60;

function renderAllWords() {
  var list = document.getElementById('all-words-list');
  _allWordsRendered = 0;
  _allWordsFilter = '';
  var parts = [];
  var count = Math.min(PAGE_SIZE, DATA.words.length);
  for (var i = 0; i < count; i++) {
    parts.push(buildWordItem(DATA.words[i]));
  }
  _allWordsRendered = count;
  list.innerHTML = parts.join('');
  document.getElementById('load-more-btn').style.display = _allWordsRendered < DATA.words.length ? 'block' : 'none';
}

function buildWordItem(w) {
  var st = getWordState(w.word);
  var badge = st.status==='mastered'?'<span class="sm2-badge sm2-mastered">已掌握</span>':st.status==='review'?'<span class="sm2-badge sm2-review">复习</span>':st.status==='learning'?'<span class="sm2-badge sm2-learning">学习中</span>':'<span class="sm2-badge sm2-new">新词</span>';
  return '<div class="word-item"><div><span class="word-en">'+esc(w.word)+'</span><span class="word-pos">'+esc(w.pos)+'</span>'+badge+'</div><div class="word-cn">'+esc(w.meaning)+'</div>'+(w.examples||[]).slice(0,2).map(function(e){return '<div class="word-ex">'+esc(e)+'</div>'}).join('')+'<div class="word-books">'+(w.books||[]).map(function(b){return '<span class="book-tag">'+esc(b)+'</span>'}).join('')+'</div></div>';
}

function loadMoreWords() {
  var list = document.getElementById('all-words-list');
  var parts = [];
  var end = Math.min(_allWordsRendered + PAGE_SIZE, DATA.words.length);
  for (var i = _allWordsRendered; i < end; i++) {
    if (_allWordsFilter && !DATA.words[i].word.toLowerCase().includes(_allWordsFilter) && !DATA.words[i].meaning.includes(_allWordsFilter)) continue;
    parts.push(buildWordItem(DATA.words[i]));
  }
  _allWordsRendered = end;
  list.insertAdjacentHTML('beforeend', parts.join(''));
  document.getElementById('load-more-btn').style.display = _allWordsRendered < DATA.words.length ? 'block' : 'none';
}

function filterWords(v) {
  _allWordsFilter = v.toLowerCase();
  var list = document.getElementById('all-words-list');
  if (!v) { renderAllWords(); return; }
  var parts = [];
  DATA.words.forEach(function(w) {
    if (!w.word.toLowerCase().includes(_allWordsFilter) && !w.meaning.includes(_allWordsFilter)) return;
    parts.push(buildWordItem(w));
  });
  list.innerHTML = parts.join('');
  document.getElementById('load-more-btn').style.display = 'none';
}

// Quiz
var quizQueue=[], quizIdx=0, quizCorrect=0, quizWrong=[], quizBookFilter='', quizInited=false;
function initQuiz() {
  if (quizInited) return;
  quizInited = true;
  var filterDiv = document.getElementById('quiz-filter');
  var parts = ['<button class="quiz-filter-btn active" onclick="setQuizFilter(this,\\'\\')">全部</button>'];
  DATA.books.forEach(function(b) {
    parts.push('<button class="quiz-filter-btn" onclick="setQuizFilter(this,\\''+esc(b.title).replace(/'/g,"\\\\'")+'\\')">'+esc(b.cn||b.title)+'</button>');
  });
  filterDiv.innerHTML = parts.join('');
  startQuiz();
}
function setQuizFilter(btn, book) {
  document.querySelectorAll('.quiz-filter-btn').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  quizBookFilter = book;
  startQuiz();
}
function startQuiz() {
  var pool = QUIZ;
  if(quizBookFilter) pool = QUIZ.filter(function(q){return (q.books||[]).includes(quizBookFilter)});
  quizQueue = pool.sort(function(){return Math.random()-0.5}).slice(0, 20);
  quizIdx = 0; quizCorrect = 0; quizWrong = [];
  renderQuizQuestion();
}
function renderQuizQuestion() {
  var area = document.getElementById('quiz-area');
  if(quizIdx >= quizQueue.length) { renderQuizResult(); return; }
  var q = quizQueue[quizIdx];
  var pct = Math.round((quizIdx/quizQueue.length)*100);
  var blankHTML = esc(q.blank).replace('______','<span class="blank">______</span>');
  var optsHTML = '';
  q.options.forEach(function(o) {
    optsHTML += '<button class="quiz-opt" onclick="checkAnswer(this,\\''+esc(o).replace(/'/g,"\\\\'")+'\\',\\''+esc(q.answer).replace(/'/g,"\\\\'")+'\\')">'+esc(o)+'</button>';
  });
  area.innerHTML = '<div class="quiz-container"><div class="quiz-progress"><div class="quiz-bar"><div class="quiz-bar-fill" style="width:'+pct+'%"></div></div><div class="quiz-score">'+quizIdx+'/'+quizQueue.length+'</div></div><div class="quiz-question">选择正确的单词填入空白处：</div><div class="quiz-sentence">'+blankHTML+'</div><div class="quiz-options">'+optsHTML+'</div><button class="quiz-next" id="quiz-next" onclick="nextQuestion()">下一题</button></div>';
}
function checkAnswer(btn, chosen, answer) {
  var opts = document.querySelectorAll('.quiz-opt');
  opts.forEach(function(o) { o.classList.add('disabled'); if(o.textContent === answer) o.classList.add('correct'); if(o.textContent === chosen && chosen !== answer) o.classList.add('wrong'); });
  if(chosen === answer) {
    quizCorrect++;
    var st = getWordState(answer);
    st.repetition = (st.repetition||0) + 1;
    st.efactor = Math.max(1.3, (st.efactor||2.5) + 0.1);
    st.interval = st.repetition < 2 ? 1 : Math.round(st.interval * st.efactor);
    st.status = st.repetition >= 5 ? 'mastered' : st.repetition >= 2 ? 'review' : 'learning';
    var d = new Date(); d.setDate(d.getDate()+st.interval);
    st.nextDate = d.toISOString().slice(0,10);
    setWordState(answer, st);
  } else {
    quizWrong.push({word:answer, chosen:chosen});
    var st = getWordState(answer);
    st.repetition = 0; st.interval = 0; st.efactor = Math.max(1.3, (st.efactor||2.5) - 0.2);
    st.status = 'learning';
    setWordState(answer, st);
  }
  document.getElementById('quiz-next').style.display = 'block';
}
function nextQuestion() { quizIdx++; renderQuizQuestion(); }
function renderQuizResult() {
  var area = document.getElementById('quiz-area');
  var pct = quizQueue.length ? Math.round(quizCorrect/quizQueue.length*100) : 0;
  var html = '<div class="quiz-result"><h2>测试完成！</h2><div class="score-big">'+pct+'%</div><p style="margin-top:8px;color:#636e72">答对 '+quizCorrect+'/'+quizQueue.length+' 题</p>';
  if(quizWrong.length) {
    html += '<div class="wrong-list"><h3 style="margin-bottom:10px;color:#d63031">错题回顾</h3>';
    quizWrong.forEach(function(w) { html += '<div class="wrong-item"><strong>'+esc(w.word)+'</strong> - 你选了 "'+esc(w.chosen)+'"</div>'; });
    html += '</div>';
  }
  html += '<button class="quiz-next" style="display:block;margin-top:24px" onclick="startQuiz()">再做一组</button></div>';
  area.innerHTML = html;
}

// Init - only render books on load (lightweight)
renderBooks();
"""
js_code += '</script>'

html.append(js_code)
html.append('</body>')
html.append('</html>')

with open('/workspace/kids_vocab/index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))

print("HTML: " + str(len(books)) + " books, " + str(len(words)) + " words, " + str(len(quiz_data)) + " quiz")
