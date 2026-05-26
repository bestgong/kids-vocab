#!/usr/bin/env python3
"""
解析斯伯恩自然拼读分级读物PDF，提取词汇+例句（优化版）
"""
import fitz
import json
import re
from collections import OrderedDict

BOOKS = [
    {"file": "books/01_Big_pig_on_a_dig.pdf", "title": "Big Pig on a Dig", "cn": "大胖猪挖宝"},
    {"file": "books/02_Ted_in_a_red_bed.pdf", "title": "Ted in a Red Bed", "cn": "小熊Ted的红床"},
    {"file": "books/03_Sam_Sheep_cant_sleep.pdf", "title": "Sam Sheep can't Sleep", "cn": "小绵羊睡不着"},
    {"file": "books/04_Teds_Shed.pdf", "title": "Ted's Shed", "cn": "小熊Ted的小屋"},
    {"file": "books/05_Fox_on_a_box.pdf", "title": "Fox on a Box", "cn": "箱子上的狐狸"},
    {"file": "books/06_Shark_in_the_park.pdf", "title": "Shark in the Park", "cn": "公园里的鲨鱼"},
    {"file": "books/07_Goose_on_the_loose.pdf", "title": "Goose on the Loose", "cn": "横冲直撞的白鹅"},
    {"file": "books/08_Fat_cat_on_a_mat.pdf", "title": "Fat Cat on a Mat", "cn": "垫子上的胖猫"},
    {"file": "books/09_Mouse_moves_house.pdf", "title": "Mouse Moves House", "cn": "小老鼠搬家"},
    {"file": "books/10_Hens_pens.pdf", "title": "Hen's Pens", "cn": "母鸡的画笔"},
    {"file": "books/11_Frog_on_a_log.pdf", "title": "Frog on a Log", "cn": "青蛙和圆木"},
    {"file": "books/12_I_love_my_new_toy.pdf", "title": "I Love My New Toy", "cn": "我爱我的新玩具"},
    {"file": "books/13_I_am_going.pdf", "title": "I Am Going", "cn": "我要走了"},
    {"file": "books/14_Are_you_ready.pdf", "title": "Are You Ready to Play Outside", "cn": "准备好出去玩了吗"},
    {"file": "books/15_Can_I_play_too.pdf", "title": "Can I Play Too", "cn": "我也能一起玩吗"},
    {"file": "books/16_Pigs_Make_Me_Sneeze.pdf", "title": "Pigs Make Me Sneeze", "cn": "小猪让我打喷嚏"},
    {"file": "books/17_Happy_Pig_Day.pdf", "title": "Happy Pig Day", "cn": "快乐小猪节"},
    {"file": "books/18_I_Am_Invited_to_a_Party.pdf", "title": "I Am Invited to a Party", "cn": "我受邀参加派对"},
    {"file": "books/19_My_Friend_is_Sad.pdf", "title": "My Friend is Sad", "cn": "我的朋友不开心"},
    {"file": "books/20_Listen_to_My_Trumpet.pdf", "title": "Listen to My Trumpet", "cn": "听我吹小号"},
    {"file": "books/21_I_Really_Like_Slop.pdf", "title": "I Really Like Slop", "cn": "我超爱泔水"},
    {"file": "books/22_There_Is_a_Bird_on_Your_Head.pdf", "title": "There Is a Bird on Your Head", "cn": "你头上有只鸟"},
    {"file": "books/23_Watch_Me_Throw_the_Ball.pdf", "title": "Watch Me Throw the Ball", "cn": "看我扔球"},
    {"file": "books/24_Lets_Go_For_a_Drive.pdf", "title": "Let's Go For a Drive", "cn": "我们去兜风吧"},
    {"file": "books/25_My_New_Friend_Is_So_Fun.pdf", "title": "My New Friend Is So Fun", "cn": "我的新朋友真好玩"},
    {"file": "books/26_Im_a_Frog.pdf", "title": "I'm a Frog", "cn": "我是一只青蛙"},
    {"file": "books/27_Should_I_Share_My_Ice_Cream.pdf", "title": "Should I Share My Ice Cream", "cn": "我该分享冰淇淋吗"},
    {"file": "books/28_I_Will_Take_a_Nap.pdf", "title": "I Will Take a Nap", "cn": "我要睡个午觉"},
    {"file": "books/29_I_Broke_My_Trunk.pdf", "title": "I Broke My Trunk", "cn": "我弄断了鼻子"},
    {"file": "books/30_The_Thank_You_Book.pdf", "title": "The Thank You Book", "cn": "感谢书"},
]

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    pages = [page.get_text() for page in doc]
    doc.close()
    return pages

def parse_glossary(glossary_text):
    """解析词汇表页面，返回 [{word, pos, meaning}]
    
    核心策略：优先匹配「单词 + 词性 + 释义」模式，
    否则用中英文边界自动切分（找到第一个中文字符的位置）。
    """
    entries = []
    lines = glossary_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or '《' in line or '分级阅读译文' in line or '斯伯恩' in line or 'Usborne' in line:
            continue
        
        # ────── 模式1: word n./v./adj./adv./prep./pron. + meaning ──────
        # 先尝试用词性标签来定位切分点（最可靠）
        match = re.match(
            r'^([a-zA-Z][a-zA-Z\s\-\']*?)\s+(n\.?|v\.?|adj\.?|adv\.?|prep\.?|pron\.?|conj\.?|int\.?|aux\.?|det\.?)\s+(.+?)$',
            line
        )
        if match:
            word = match.group(1).strip()
            pos = match.group(2).strip().rstrip('.')
            meaning = match.group(3).strip()
            # 清理括号注释
            meaning = re.sub(r'\s*[（(]\s*第三人称单数[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]\s*现在分词[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]\s*过去时态[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]\s*drew[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]\s*尤指[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]mouse[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]let us[^）)]*[）)]', '', meaning)
            meaning = re.sub(r'\s*[（(]\s*文中[^）)]*[）)]', '', meaning)
            meaning = meaning.strip(' ,，')
            if meaning:
                entries.append({
                    "word": word.lower().strip(),
                    "pos": pos,
                    "meaning": meaning,
                })
            continue
        
        # ────── 模式2: 中英文边界切分（核心修复） ──────
        # 找到行中第一个中文字符的位置，在此之前为英文词条，之后为中文释义
        # 这样 "look for 寻找" → word="look for", meaning="寻找"
        #      "pop on  瞬间出现" → word="pop on", meaning="瞬间出现"
        cjk_match = re.search(r'[\u4e00-\u9fff]', line)
        if cjk_match:
            cjk_start = cjk_match.start()
            
            # 从 CJK 位置向前找英文部分的结束位置
            # 去掉尾部的空白和标点
            en_part = line[:cjk_start].strip().rstrip(' .,， ')
            cn_part = line[cjk_start:].strip()
            
            # 英文部分可能还残留词性标签（和中文粘在一起的情况）
            # 比如 "jiggle 、wiggle v. 都是扭动，摆动得意思"
            # 这时需要在英文部分里识别出词性标签
            pos = ""
            
            # 检查是否英文部分末尾有 (v.) (n.) 等标签
            pos_match = re.search(r'\s+(n\.?|v\.?|adj\.?|adv\.?|prep\.?|pron\.?|conj\.?|int\.?|aux\.?|det\.?)$', en_part)
            if pos_match:
                pos = pos_match.group(1).rstrip('.')
                en_part = en_part[:pos_match.start()].strip()
            
            if en_part and cn_part and len(en_part) >= 1:
                # 过滤掉纯数字或过短的英文
                en_word = en_part.lower().strip()
                # 跳过仅为词性标签的残留行（如 "v." → 跳过）
                if en_word in ('n', 'v', 'adj', 'adv', 'prep', 'pron', 'conj', 'int', 'aux', 'det', 'n.', 'v.', 'adj.', 'adv.', 'prep.', 'pron.', 'conj.', 'int.', 'aux.', 'det.'):
                    continue
                if en_word.replace(' ', '').replace('-', '').replace("'", '').isascii() and len(en_word) >= 1:
                    if len(en_word.split()) >= 2:
                        pos = pos or "phrase"
                    entries.append({
                        "word": en_word,
                        "pos": pos,
                        "meaning": cn_part,
                    })
            continue
        
        # ────── 模式3: 无中文的纯英文行，跳过 ──────
        # 这部分通常是格式噪音
    
    # ────── 后处理：去重 + 合并 ──────
    # 移除完全重复的条目
    seen = set()
    unique = []
    for entry in entries:
        key = (entry["word"], entry.get("pos", ""))
        if key not in seen:
            seen.add(key)
            unique.append(entry)
        else:
            # 已存在：保留释义更完整的
            for u in unique:
                if (u["word"], u.get("pos", "")) == key:
                    if len(entry.get("meaning", "")) > len(u.get("meaning", "")):
                        u["meaning"] = entry["meaning"]
                    break
    
    return unique

def clean_english_sentence(s):
    """清理英文句子：去掉中文、特殊字符、词汇注释、引号"""
    # 去掉书名号
    s = re.sub(r'[《》「」『』]', '', s)
    # 先去掉全角括号及其中内容（如"醒来（第三人称单数形式wakes)" → "醒来")
    s = re.sub(r'（[^）]*）', '', s)
    s = re.sub(r'\([^)]*[\u4e00-\u9fff][^)]*\)', '', s)  # 英文括号含中文内容的也去掉
    # 去掉中文字符（但保留英文标点）
    s = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+', '', s)
    # 去掉中文标点和各种引号
    s = s.strip(' ，。！？；：""''\"\'（）【】、…\u201c\u201d\u2018\u2019')
    # 去掉开头/结尾残留引号
    for q in ['\u201c', '\u201d', '\u2018', '\u2019', '"', "'"]:
        if s.startswith(q):
            s = s[len(q):]
        if s.endswith(q):
            s = s[:-len(q)]
    # 清理多余空格
    s = re.sub(r'\s+', ' ', s).strip()
    # 去掉纯粹的词汇注释行（含词性标签的）
    if re.match(r'^[a-zA-Z\-\']+\s+(n\.|v\.|adj\.|adv\.|prep\.|pron\.|conj\.|int\.|aux\.|det\.)', s):
        return ""
    # 过滤残留碎片：全是短单词组合且不像句子（无标点、无冠词、无be动词等句子标志）
    if len(s) < 15:
        # 短文本额外检查：看起来像词汇标注残片而非完整句子
        sentence_markers = r'[.,!?;:]|(\b(the|a|an|is|are|was|were|can|will|has|have|I|he|she|it|they|we|you|this|that)\b)'
        if not re.search(sentence_markers, s, re.IGNORECASE):
            return ""
    if len(s) < 8:
        return ""
    return s

def extract_story_sentences(pages):
    """从故事页面提取纯英文句子"""
    sentences = []
    for page_text in pages[2:-1]:  # skip cover/intro + last glossary
        lines = page_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line or len(line) < 8:
                continue
            # 跳过元数据行
            if any(skip in line for skip in ['分级阅读译文', '斯伯恩', 'Usborne', '内页展示', '语调']):
                continue
            # 必须是包含英文的行
            if not re.search(r'[a-zA-Z]{2,}', line):
                continue
            # 预过滤：明显是词汇注释的行（短英文 + 中文释义）
            # 如 "wake up  醒来（第三人称单数形式wakes)" → 跳过
            if re.match(r'^[a-zA-Z][a-zA-Z\s\-\']{1,25}\s{2,}[\u4e00-\u9fff]', line):
                continue
            
            # 清理
            clean = clean_english_sentence(line)
            if clean:
                sentences.append(clean)
    
    # 去重保持顺序
    seen = set()
    unique = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return unique

def build_word_form_pattern(word):
    """为一个单词生成匹配其各种词形变化的正则模式。
    包括常规后缀 + 去e规则 + 双写尾字母 + 常见不规则变化。
    """
    forms = [re.escape(word)]
    
    # 常规后缀: -s, -es, -ed, -ing, -er, -est, 's
    for suffix in ['s', 'es', 'ed', 'ing', 'er', 'est', "'s"]:
        forms.append(re.escape(word + suffix))
    
    # 以 e 结尾的词 → 去 e 加 ing/ed: slice → slicing
    if word.endswith('e') and len(word) > 2:
        stem = word[:-1]
        for suffix in ['ing', 'ed', 'es', 'er']:
            forms.append(re.escape(stem + suffix))
    
    # 辅-元-辅结尾 → 双写尾字母: dig→digging
    if len(word) >= 3:
        a, b, c = word[-3], word[-2], word[-1]
        if (a.lower() not in 'aeiou' and b.lower() in 'aeiou' and c.lower() not in 'aeiou'):
            double = word + word[-1]
            for suffix in ['ing', 'ed', 'er']:
                forms.append(re.escape(double + suffix))
    
    # 常见不规则动词变化
    IRREGULARS = {
        'draw': ['drew', 'drawn'],
        'sleep': ['slept'],
        'wake': ['woke', 'woken'],
        'fly': ['flew', 'flown'],
        'sit': ['sat'],
        'dig': ['dug'],
        'get': ['got', 'gotten'],
        'give': ['gave', 'given'],
        'feel': ['felt'],
        'fall': ['fell', 'fallen'],
        'mean': ['meant'],
        'put': ['put'],
    }
    for base, irregulars in IRREGULARS.items():
        if word == base:
            for irr in irregulars:
                forms.append(re.escape(irr))
    
    # 去重，按长度降序（长匹配优先，避免 show 匹配到 show 而非 shows）
    forms = sorted(set(forms), key=len, reverse=True)
    return re.compile(r'\b(' + '|'.join(forms) + r')\b', re.IGNORECASE)


def build_phrase_pattern(phrase):
    """为多词短语生成匹配模式，每个单词支持词形变化。"""
    words = phrase.split()
    word_patterns = []
    for w in words:
        # 跳过纯标点/非字母的词
        if not any(c.isalpha() for c in w):
            continue
        forms = build_word_forms(w)
        # 清理 forms 中的特殊字符
        safe_forms = []
        for f in forms:
            try:
                re.compile(re.escape(f))
                safe_forms.append(f)
            except re.error:
                safe_forms.append(re.sub(r'[^\w\s]', '', f))
        if len(safe_forms) > 1:
            word_patterns.append('(' + '|'.join(re.escape(f) for f in safe_forms) + ')')
        elif safe_forms:
            word_patterns.append(re.escape(safe_forms[0]))
    
    if not word_patterns:
        # 如果所有词都被过滤了，用原始短语的转义
        return re.compile(re.escape(phrase), re.IGNORECASE)
    
    full_pattern = r'\b' + r'\s+'.join(word_patterns) + r'\b'
    return re.compile(full_pattern, re.IGNORECASE)


def build_word_forms(word):
    """返回一个单词的所有可能词形（不含正则转义），用于短语内部匹配"""
    forms = [word]
    for suffix in ['s', 'es', 'ed', 'ing', 'er', 'est', "'s"]:
        forms.append(word + suffix)
    if word.endswith('e') and len(word) > 2:
        stem = word[:-1]
        for suffix in ['ing', 'ed', 'es', 'er']:
            forms.append(stem + suffix)
    if len(word) >= 3:
        a, b, c = word[-3], word[-2], word[-1]
        if (a.lower() not in 'aeiou' and b.lower() in 'aeiou' and c.lower() not in 'aeiou'):
            double = word + word[-1]
            for suffix in ['ing', 'ed', 'er']:
                forms.append(double + suffix)
    # 不规则
    IRREGULARS = {
        'wake': ['woke', 'woken'], 'draw': ['drew', 'drawn'], 'sleep': ['slept'],
        'fly': ['flew', 'flown'], 'sit': ['sat'], 'dig': ['dug'],
        'get': ['got', 'gotten'], 'give': ['gave', 'given'], 'feel': ['felt'],
        'fall': ['fell', 'fallen'], 'mean': ['meant'], 'put': ['put'],
    }
    if word in IRREGULARS:
        forms.extend(IRREGULARS[word])
    return sorted(set(forms), key=len, reverse=True)


def match_sentences(all_words, all_sentences):
    """为每个单词匹配合适的例句，兼容词形变化"""
    for word_entry in all_words:
        w = word_entry["word"]
        if ' ' in w:
            pattern = build_phrase_pattern(w)
        else:
            pattern = build_word_form_pattern(w)
        
        matched = []
        for s in all_sentences:
            if pattern.search(s) and len(s) > 10:
                # 去掉开头引号
                clean_s = re.sub(r'^[""」「]\s*', '', s).strip()
                clean_s = re.sub(r'\s*[""」「]$', '', clean_s).strip()
                if clean_s not in matched and clean_s.lower() != w.lower():
                    matched.append(clean_s)
        
        word_entry["examples"] = matched[:3]
    
    return all_words

# PDF 字体编码常见错误映射
PDF_ENCODING_FIX = {
    '丌': '不',
}

def fix_encoding_errors(entries):
    """修正 PDF 提取中的字体编码错误"""
    for entry in entries:
        for bad, good in PDF_ENCODING_FIX.items():
            if bad in entry.get('meaning', ''):
                entry['meaning'] = entry['meaning'].replace(bad, good)
            for i, ex in enumerate(entry.get('examples', [])):
                if bad in ex:
                    entry['examples'][i] = ex.replace(bad, good)
    return entries


def get_glossary_text(pages):
    """智能识别词汇表页面（支持跨多页），返回合并后的词汇表文本。
    从最后一页向前扫描，收集所有含词汇条目的页面。
    """
    glossary_texts = []
    for i in range(len(pages) - 1, max(len(pages) - 5, -1), -1):
        text = pages[i]
        lines = text.strip().split('\n')
        vocab_lines = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r'^[a-zA-Z][a-zA-Z\s\-\'\.…]*\s+(n\.|v\.|adj\.|adv\.|prep\.|pron\.|conj\.|int\.|aux\.|det\.)', line):
                vocab_lines += 1
            elif re.match(r'^[a-zA-Z][a-zA-Z\s\-\'\.…]+\s{2,}[\u4e00-\u9fff]', line):
                vocab_lines += 1
        if vocab_lines >= 3:
            glossary_texts.insert(0, text)
        elif glossary_texts:
            break  # 已收集到词汇表且当前页不满足条件，停止
    
    if not glossary_texts:
        glossary_texts = [pages[-1]]
    
    return '\n'.join(glossary_texts)


def main():
    base_dir = "/workspace/kids_vocab"
    all_words = OrderedDict()
    
    for book in BOOKS:
        filepath = f"{base_dir}/{book['file']}"
        pages = extract_text_from_pdf(filepath)
        
        # 解析词汇表（支持多页）
        glossary_text = get_glossary_text(pages)
        entries = parse_glossary(glossary_text)
        entries = fix_encoding_errors(entries)
        
        # 提取故事例句
        story_sentences = extract_story_sentences(pages)
        
        # 匹配例句
        entries = match_sentences(entries, story_sentences)
        
        for entry in entries:
            word = entry["word"]
            entry["book"] = book["title"]
            entry["book_cn"] = book["cn"]
            
            if word in all_words:
                existing = all_words[word]
                # 合并例句
                for e in entry["examples"]:
                    if e not in existing["examples"]:
                        existing["examples"].append(e)
                existing["examples"] = existing["examples"][:3]
                # 更新释义
                if not existing.get("meaning") and entry.get("meaning"):
                    existing["meaning"] = entry["meaning"]
                if not existing.get("pos") and entry.get("pos"):
                    existing["pos"] = entry["pos"]
                if book["title"] not in existing.get("books", []):
                    if "books" not in existing:
                        existing["books"] = [existing.get("book", "")]
                    existing["books"].append(book["title"])
            else:
                entry["books"] = [book["title"]]
                all_words[word] = entry
        
        print(f"📖 {book['title']}: {len(entries)} 词条")
    
    # 清理最终数据
    cleaned = []
    skip_words = set()
    
    for w, entry in all_words.items():
        # 跳过无释义的
        if not entry.get("meaning"):
            continue
        # 清理
        entry.pop("book", None)
        entry.pop("book_cn", None)
        entry["examples"] = [e for e in entry["examples"] if len(e) > 8][:3]
        cleaned.append(entry)
    
    print(f"\n✅ 总计: {len(cleaned)} 个不重复词汇")
    
    # 统计有例句/无例句
    with_ex = sum(1 for e in cleaned if e["examples"])
    print(f"   📝 有例句: {with_ex}")
    print(f"   ❓ 暂无例句: {len(cleaned) - with_ex}")
    
    output = {
        "total": len(cleaned),
        "books": [{"title": b["title"], "cn": b["cn"]} for b in BOOKS],
        "words": cleaned,
    }
    
    output_path = f"{base_dir}/vocabulary.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 已保存到 {output_path}")

if __name__ == "__main__":
    main()
