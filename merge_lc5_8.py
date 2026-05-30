#!/usr/bin/env python3
"""Merge LC-5~8 into vocabulary.json"""
import json

with open('/workspace/kids_vocab/vocabulary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
books = data['books']

word_map = {}
for w in words:
    word_map[w['word'].lower()] = w

def add_word(word, pos, meaning, examples, book_title):
    key = word.lower()
    if key in word_map:
        existing = word_map[key]
        if book_title not in existing.get('books', []):
            existing['books'].append(book_title)
        for ex in examples:
            if ex not in existing.get('examples', []):
                existing['examples'].append(ex)
        print(f"  MERGED: {word} + {book_title}")
    else:
        new_w = {"word": word, "pos": pos, "meaning": meaning, "examples": examples, "books": [book_title]}
        words.append(new_w)
        word_map[key] = new_w
        print(f"  NEW: {word}")

# ===== Book 46: Just Saving My Money (Little Critter 5) =====
b46 = "Just Saving My Money"
books.append({"title": b46, "cn": "只是攒钱"})

add_word("skateboard", "n", "滑板", ["My skateboard is old."], b46)
add_word("old", "adj", "陈旧的", ["My skateboard is old."], b46)
add_word("money", "n", "钱，钞票", ["You need money."], b46)
add_word("any", "adj", "一些", ["Do you have any?"], b46)
add_word("money jar", "n", "储蓄罐", ["I get my money jar."], b46)
add_word("How about", "phrase", "你认为……怎样", ["How about this?"], b46)
add_word("save", "v", "储蓄，节省", ["You need to save more money for a skateboard."], b46)
add_word("chore", "n", "家庭杂务", ["I will do chores and earn lots of money."], b46)
add_word("earn", "v", "赚得，挣钱", ["I will do chores and earn lots of money."], b46)
add_word("lots of", "phrase", "许多；大量", ["I will do chores and earn lots of money."], b46)
add_word("a list of chores", "phrase", "家务清单", ["I make a list of chores that will make me money."], b46)
add_word("first", "adv", "首先", ["First, I feed the dog."], b46)
add_word("feed", "v", "饲养，喂养", ["First, I feed the dog."], b46)
add_word("empty", "v", "清空", ["I empty the dishwasher."], b46)
add_word("dishwasher", "n", "洗碗工；洗碟机", ["I empty the dishwasher."], b46)
add_word("heavy", "adj", "重的，沉的", ["The dishes are too heavy."], b46)
add_word("clean", "v", "清洁，清理", ["I clean my room."], b46)
add_word("pay", "v", "支付，付", ["Mom pays me some money."], b46)
add_word("sell", "v", "出售，售卖", ["I sell lemonade."], b46)
add_word("lemonade", "n", "柠檬汁", ["I sell lemonade."], b46)
add_word("savings account", "n", "储蓄账户", ["You need a savings account."], b46)
add_word("bank", "n", "银行", ["Dad takes me to the bank."], b46)
add_word("manager", "n", "经理，管理人", ["We see the manager."], b46)
add_word("write on", "phrase", "在……上写", ["Dad writes on some bank papers."], b46)
add_word("upset", "adj", "不高兴的", ["I am upset."], b46)
add_word("pour", "v", "倾倒，倒出", ["They pour my money into a machine."], b46)
add_word("machine", "n", "机器", ["They pour my money into a machine."], b46)
add_word("count", "v", "数数；计数", ["It counts my money."], b46)
add_word("how much", "phrase", "多少，多少钱", ["It tells me how much money I have."], b46)
add_word("not yet", "phrase", "还没有", ["Not yet. You must save more money."], b46)
add_word("finally", "adv", "终于，最后", ["Finally, I save enough money for a new skateboard."], b46)
add_word("enough", "adj", "充足的，足够的", ["Finally, I save enough money for a new skateboard."], b46)
add_word("anymore", "adv", "（不）再，再也（不）", ["But I don't want that anymore."], b46)
add_word("Robot Dinosaur", "n", "机器恐龙", ["Now I want a Robot Dinosaur."], b46)

# ===== Book 47: This is My Town (Little Critter 6) =====
b47 = "This is My Town"
books.append({"title": b47, "cn": "这是我的小镇"})

add_word("live", "v", "生活在；居住", ["This is where I live."], b47)
add_word("post office", "n", "邮局", ["This is our post office."], b47)
add_word("mail", "n", "邮件，信件", ["The mail comes in here."], b47)
add_word("letters", "n", "信", ["I come here to mail letters."], b47)
add_word("come here", "phrase", "来这里", ["I come here to mail letters."], b47)
add_word("fire station", "n", "消防站", ["This is our fire station."], b47)
add_word("firetruck", "n", "救火车", ["The firetruck lives here."], b47)
add_word("put out", "phrase", "熄灭", ["They put the fire out."], b47)
add_word("police station", "n", "派出所；警察局", ["This is our police station."], b47)
add_word("police officer", "n", "警官", ["Police officers work here."], b47)
add_word("keep safe", "phrase", "保证……安全", ["They keep our town safe."], b47)
add_word("diner", "n", "小餐馆，小饭店", ["This is our diner."], b47)
add_word("sometimes", "adv", "有时，间或", ["Sometimes we come here for lunch."], b47)
add_word("town hall", "n", "市政厅", ["This is our town hall."], b47)
add_word("mayor", "n", "镇长，市长", ["Our mayor works here."], b47)
add_word("parade", "n", "游行", ["Sometimes we have parades in our town."], b47)
add_word("library", "n", "图书馆", ["This is our library."], b47)
add_word("during", "prep", "在……期间", ["During story hours, the librarian reads to us."], b47)
add_word("story", "n", "故事", ["During story hours, the librarian reads to us."], b47)
add_word("librarian", "n", "图书馆管理员", ["The librarian reads to us."], b47)
add_word("over", "adv", "结束", ["When story hour is over we have to be quiet."], b47)
add_word("quiet", "adj", "安静的", ["We have to be quiet."], b47)
add_word("movie theater", "n", "电影院", ["This is our movie theater."], b47)
add_word("ticket", "n", "票，入场券", ["I can buy my own ticket."], b47)
add_word("popcorn", "n", "爆米花", ["I like to get popcorn."], b47)
add_word("extra", "adv", "特别，格外", ["I am always extra careful."], b47)
add_word("careful", "adj", "仔细的，小心的", ["I am always extra careful."], b47)
add_word("walk", "v", "走，行走", ["Sometimes Mom and Dad let me walk here by myself."], b47)
add_word("myself", "pron", "我自己；我亲自", ["Sometimes Mom and Dad let me walk here by myself."], b47)
add_word("school", "n", "学校", ["This is our school."], b47)
add_word("park", "n", "公园", ["This is our park."], b47)
add_word("play football", "phrase", "踢足球", ["We play football here."], b47)
add_word("bakery", "n", "面包店", ["This is our bakery."], b47)
add_word("best", "adj", "最好的", ["It has the best cupcakes."], b47)
add_word("cupcake", "n", "纸托蛋糕；杯形蛋糕", ["It has the best cupcakes."], b47)
add_word("office", "n", "办公室", ["This is the office of our town newspaper."], b47)
add_word("newspaper", "n", "报纸", ["It is a busy place."], b47)
add_word("busy", "adj", "繁忙的，忙碌的", ["It is a busy place."], b47)
add_word("last week", "phrase", "上周，上星期", ["Last week my picture was in the newspaper."], b47)
add_word("nicest", "adj", "最美好的", ["It is the nicest place in the whole world."], b47)
add_word("in the whole world", "phrase", "在全世界中", ["It is the nicest place in the whole world."], b47)

# ===== Book 48: The Fall Festival (Little Critter 7) =====
b48 = "The Fall Festival"
books.append({"title": b48, "cn": "秋季狂欢节"})

add_word("fall", "n", "秋天，秋季", ["It is fall."], b48)
add_word("change", "v", "改变，变化", ["The leaves change colors."], b48)
add_word("turn", "v", "转变", ["They turn yellow and red."], b48)
add_word("wagon", "n", "四轮运货车", ["We bring a wagon to hold the things we buy."], b48)
add_word("hold", "v", "容纳，存放，盛放", ["We bring a wagon to hold the things we buy."], b48)
add_word("so many", "phrase", "那么多的", ["I see so many apples."], b48)
add_word("try", "v", "品尝", ["I try one."], b48)
add_word("cider", "n", "苹果酒；苹果汁", ["Little Sister has apple cider."], b48)
add_word("spill", "v", "洒出", ["She spills it."], b48)
add_word("sticky", "adj", "黏的", ["It is sticky."], b48)
add_word("hayride", "n", "乘坐装有干草的大车出游", ["We go on a hayride."], b48)
add_word("hay", "n", "干草", ["There is not much hay."], b48)
add_word("through", "prep", "穿过", ["We ride through a field full of pumpkins."], b48)
add_word("field", "n", "田地，田野", ["We ride through a field full of pumpkins."], b48)
add_word("full of", "phrase", "装满", ["We ride through a field full of pumpkins."], b48)
add_word("pumpkin", "n", "南瓜", ["We ride through a field full of pumpkins."], b48)
add_word("shoot", "v", "发射", ["I watch a critter shoot pumpkins into the air."], b48)
add_word("pick", "v", "采，摘（花、果）", ["I get to pick apples, too."], b48)
add_word("get to", "phrase", "开始……", ["I get to pick apples, too."], b48)
add_word("apple pie", "n", "苹果派", ["Mom will make many apple pies."], b48)
add_word("no more", "phrase", "不再", ["Mom says, No more apples."], b48)
add_word("Halloween pumpkin", "n", "万圣节南瓜", ["Next we look for a Halloween pumpkin."], b48)
add_word("funny looking", "adj", "好玩（奇怪）的样子", ["Some pumpkins are too funny looking."], b48)
add_word("perfect", "adj", "无瑕的，完好的", ["I find the perfect pumpkin."], b48)
add_word("horseshoe game", "n", "掷马蹄铁游戏", ["We play the horseshoe game."], b48)
add_word("throw", "n", "投掷", ["We each get three throws."], b48)
add_word("prize", "n", "奖品；奖项", ["We can win prizes."], b48)
add_word("go first", "phrase", "先走，先来", ["I go first."], b48)
add_word("aim", "v", "瞄准，对准", ["I aim."], b48)
add_word("let go", "phrase", "放开", ["I forgot to let go."], b48)
add_word("every time", "phrase", "每一次", ["He wins every time."], b48)
add_word("pull", "v", "拉，拽", ["Little Sister pulls the wagon."], b48)
add_word("carry", "v", "提，扛，背", ["Dad carries the pumpkin."], b48)
add_word("pick up", "phrase", "捡起；获得", ["Mom picks up the apples that we drop."], b48)
add_word("drop", "v", "掉落", ["Mom picks up the apples that we drop."], b48)
add_word("eat", "v", "吃", ["I ate too many apples."], b48)
add_word("too many", "phrase", "太多", ["I ate too many apples."], b48)

# ===== Book 49: Going to The Sea Park (Little Critter 8) =====
b49 = "Going to The Sea Park"
books.append({"title": b49, "cn": "去海洋公园"})

add_word("today", "adv", "今天，今日", ["Today my class goes to the Sea Park."], b49)
add_word("sea park", "n", "海洋公园", ["Today my class goes to the Sea Park."], b49)
add_word("pretty", "adj", "漂亮的，标致的", ["Some fish are pretty."], b49)
add_word("really", "adv", "很，十分", ["Some fish are really ugly."], b49)
add_word("ugly", "adj", "丑陋的，难看的", ["Some fish are really ugly."], b49)
add_word("petting tank", "n", "养鱼的玻璃缸", ["We all go to the petting tank."], b49)
add_word("horseshoe crab", "n", "马蹄蟹", ["I pet a horseshoe crab."], b49)
add_word("weird", "adj", "奇怪的，不寻常的", ["That is weird!"], b49)
add_word("fall into", "phrase", "落入", ["Timothy falls into the tank."], b49)
add_word("octopus", "n", "章鱼", ["He meets an octopus."], b49)
add_word("lunchroom", "n", "餐厅", ["Our teacher takes us to the lunchroom."], b49)
add_word("swordfish", "n", "剑鱼", ["They sell a swordfish burger on the menu."], b49)
add_word("burger", "n", "汉堡包", ["They sell a swordfish burger on the menu."], b49)
add_word("menu", "n", "菜单", ["They sell a swordfish burger on the menu."], b49)
add_word("pretend", "adj", "假装的", ["We go on a pretend pirate ship."], b49)
add_word("pirate ship", "n", "海盗船", ["We go on a pretend pirate ship."], b49)
add_word("steer", "v", "驾驶", ["I steer the ship."], b49)
add_word("scared", "adj", "惊恐的", ["Bun Bun is scared."], b49)
add_word("shark tank", "n", "鲨鱼玻璃缸", ["We see the shark tank."], b49)
add_word("would not like to", "phrase", "不愿意做某事", ["I would not like to have lunch with a shark."], b49)
add_word("whale", "n", "鲸", ["We see baby whales eating fish."], b49)
add_word("manatee", "n", "海牛", ["We see manatees eating plants."], b49)
add_word("plant", "n", "植物", ["We see manatees eating plants."], b49)
add_word("seal show", "n", "海豹表演", ["Next we go to the seal show."], b49)
add_word("no one else", "phrase", "没有其他人", ["No one else wants to."], b49)
add_word("orca", "n", "虎鲸", ["We see Bazoo the orca."], b49)
add_word("in the front row", "phrase", "最前面的一排", ["We sit in the front row."], b49)
add_word("splash", "v", "（被水）溅到", ["We get splashed with water."], b49)
add_word("gift", "n", "礼物", ["Everyone brings money from home to buy a gift."], b49)
add_word("fuzzy", "adj", "毛茸茸的", ["I buy a fuzzy orca."], b49)
add_word("the best part", "phrase", "最精彩的部分", ["Do you know what the best part was?"], b49)

# Update total
data['total'] = len(words)
data['books'] = books
data['words'] = words

with open('/workspace/kids_vocab/vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone! Total: {len(words)} words, {len(books)} books")
