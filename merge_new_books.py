#!/usr/bin/env python3
"""Merge new books into vocabulary.json"""
import json

with open('/workspace/kids_vocab/vocabulary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
books = data['books']

# Build lookup
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

# ===== Book 41: The Dragon and The Phoenix (L2) =====
b41 = "The Dragon and The Phoenix"
books.append({"title": b41, "cn": "龙与凤凰"})

add_word("dragon", "n", "（传说中的）龙", ["This is the story of Dragon Mountain."], b41)
add_word("phoenix", "n", "凤凰，不死鸟", ["Phoenix Mountain and a shining lake."], b41)
add_word("thousand", "n", "千", ["It begins thousands of years ago, in China."], b41)
add_word("China", "n", "中国", ["It begins thousands of years ago, in China."], b41)
add_word("beside", "prep", "在……旁边", ["Long, long ago, a dragon lived beside a magic river."], b41)
add_word("dark", "adj", "黑暗的，昏暗的", ["A dark forest grew on the other side of the river."], b41)
add_word("the other", "phrase", "另一个", ["A dark forest grew on the other side of the river."], b41)
add_word("swim", "v", "游泳", ["Every day, the dragon swam in the river."], b41)
add_word("fly", "v", "飞，飞翔", ["Every day, the phoenix flew in the sky above."], b41)
add_word("above", "adv", "在（或向）上面", ["Every day, the phoenix flew in the sky above."], b41)
add_word("meet", "v", "偶遇，结识", ["One day, they met on an island in the river."], b41)
add_word("island", "n", "岛，岛屿", ["One day, they met on an island in the river."], b41)
add_word("pebble", "n", "鹅卵石", ["A shiny pebble lay on the sand."], b41)
add_word("lay", "v", "安放，放置", ["A shiny pebble lay on the sand."], b41)
add_word("wash", "v", "清洗，洗涤", ["The dragon washed it in the river."], b41)
add_word("polish", "v", "擦亮，磨光", ["The phoenix polished it with a feather."], b41)
add_word("feather", "n", "羽毛", ["The phoenix polished it with a feather."], b41)
add_word("pearl", "n", "珍珠", ["And the pebble became a pearl."], b41)
add_word("stay on", "phrase", "继续停留", ["The dragon and the phoenix stayed on the island."], b41)
add_word("watch", "v", "看，注视", ["Watching the pearl."], b41)
add_word("shine", "v", "发光，照耀", ["The pearl shone brighter than stars."], b41)
add_word("bright", "adj", "明亮的", ["The pearl shone brighter than stars."], b41)
add_word("than", "conj", "比", ["The pearl shone brighter than stars."], b41)
add_word("send", "v", "派遣", ["That night, she sent a guard to steal it."], b41)
add_word("guard", "n", "看守", ["That night, she sent a guard to steal it."], b41)
add_word("steal", "v", "偷窃，盗窃", ["That night, she sent a guard to steal it."], b41)
add_word("fly up", "phrase", "向上飞", ["They flew up to Heaven and saw the Queen."], b41)
add_word("lake", "n", "湖，湖泊", ["It landed on the ground and became a shining lake."], b41)
add_word("still", "adv", "还，依旧", ["They are still there today."], b41)

# ===== Book 42: Snowball Soup (Little Critter 1) =====
b42 = "Snowball Soup"
books.append({"title": b42, "cn": "雪球汤"})

add_word("little", "adj", "小的，比较小的", ["I am Little Critter."], b42)
add_word("critter", "n", "生物，动物", ["I am Little Critter."], b42)
add_word("look at", "phrase", "看", ["Look at all the snow!"], b42)
add_word("like", "v", "喜欢，喜爱", ["Dog likes snow."], b42)
add_word("too", "adv", "也", ["I like snow, too."], b42)
add_word("dig", "v", "挖，掘", ["I dig in the snow."], b42)
add_word("roll", "v", "翻滚，滚动", ["Little Sister rolls in the snow."], b42)
add_word("throw", "v", "投，掷，抛，扔", ["We throw snowballs."], b42)
add_word("oops", "int", "哎哟，啊呀", ["Oops! Sorry, Little Sister."], b42)
add_word("sorry", "adj", "抱歉的", ["Oops! Sorry, Little Sister."], b42)
add_word("some", "det", "一些", ["We roll some big snowballs."], b42)
add_word("on the bottom", "phrase", "在底部", ["One snowball on the bottom."], b42)
add_word("on top", "phrase", "在上面", ["The next one goes on top."], b42)
add_word("ta-da", "int", "塔哒，哇呀（表示惊喜）", ["Ta-da!"], b42)
add_word("put on", "phrase", "穿上，戴上", ["Little Sister puts on the hat."], b42)
add_word("then", "adv", "接下来", ["Then we put on the eyes."], b42)
add_word("lunch", "n", "午餐，午饭", ["Time for lunch, Snowman!"], b42)
add_word("soup", "n", "汤，羹", ["Snowball soup!"], b42)
add_word("spoon", "n", "匙，勺子", ["We give the snowman a spoon."], b42)
add_word("silly", "adj", "愚蠢的，傻的", ["Silly dog!"], b42)
add_word("go inside", "phrase", "进（屋里）去", ["We go inside."], b42)
add_word("yum", "int", "呀呣（表示好吃）", ["Yum! Yum!"], b42)
add_word("go outside", "phrase", "外出；往外走", ["We go outside."], b42)
add_word("don't worry", "phrase", "不要紧；不用担心", ["Don't worry, Snowman!"], b42)

# ===== Book 43: Just Helping My Dad (Little Critter 2) =====
b43 = "Just Helping My Dad"
books.append({"title": b43, "cn": "只是帮爸爸"})

add_word("wake up", "phrase", "起床", ["Wake up, Dad."], b43)
add_word("sleepy", "adj", "困的，打瞌睡的", ["Dad is sleepy."], b43)
add_word("breakfast", "n", "早餐", ["I make breakfast for him all by myself."], b43)
add_word("all by myself", "phrase", "全靠自己", ["I make breakfast for him all by myself."], b43)
add_word("cut", "v", "割，砍，剪", ["I cut the grass."], b43)
add_word("grass", "n", "草地，草坪", ["I cut the grass."], b43)
add_word("mower", "n", "割草机", ["The mower got away!"], b43)
add_word("get away", "phrase", "离开；逃脱", ["The mower got away!"], b43)
add_word("leave", "v", "让……处于（某种状态）", ["Who left the windows open?"], b43)
add_word("window", "n", "窗，窗玻璃", ["Who left the windows open?"], b43)
add_word("open", "v", "打开", ["Who left the windows open?"], b43)
add_word("paint", "v", "（给……）上油漆", ["I can paint."], b43)
add_word("finish", "v", "完成，做好", ["But Dad has to finish."], b43)
add_word("nest", "n", "窝，巢，穴", ["I see a bees' nest."], b43)
add_word("fix", "v", "处理，解决；修理", ["I will fix it, Dad."], b43)
add_word("yell", "v", "叫喊，大喊", ["Dad is yelling something."], b43)
add_word("fast", "adj", "快的，迅速的", ["I run fast."], b43)
add_word("town", "n", "城镇，市镇", ["We go to town, just Dad and me."], b43)
add_word("pump gas", "phrase", "加油", ["I can pump gas."], b43)
add_word("store", "n", "商店", ["We go to the store."], b43)
add_word("hammer", "n", "锤子，榔头", ["Dad needs a new hammer."], b43)
add_word("nail", "n", "钉子", ["Sorry about the nails."], b43)
add_word("parking ticket", "n", "违规停车罚单", ["We get a parking ticket."], b43)
add_word("mad", "adj", "生气的，气愤的", ["I am not mad, just not happy."], b43)
add_word("that's fair", "phrase", "这很公平", ["That's fair, Dad."], b43)
add_word("toilet", "n", "抽水马桶，坐便器", ["The toilet is broken."], b43)
add_word("forget", "v", "忘记，遗忘", ["I forgot to turn off the hose."], b43)
add_word("turn off", "phrase", "关掉，关闭", ["I forgot to turn off the hose."], b43)
add_word("hose", "n", "软管，水龙带", ["I forgot to turn off the hose."], b43)
add_word("watch a movie", "phrase", "看电影", ["Dad and I watch a movie."], b43)
add_word("tire", "v", "感到累", ["Dad is tired."], b43)
add_word("tuck me in", "phrase", "帮我盖被子", ["Dad tucks me in."], b43)

# ===== Book 44: Going to The Firehouse (Little Critter 3) =====
b44 = "Going to The Firehouse"
books.append({"title": b44, "cn": "去消防站"})

add_word("class", "n", "班级", ["Today my class is going to the firehouse!"], b44)
add_word("firehouse", "n", "消防站；消防队", ["Today my class is going to the firehouse!"], b44)
add_word("fireman", "n", "消防员", ["I dress like a fireman."], b44)
add_word("fight a fire", "phrase", "救火", ["Time to fight a fire!"], b44)
add_word("boots", "n", "靴子", ["Fireman Joe has boots."], b44)
add_word("jacket", "n", "夹克衫，短上衣", ["He has a jacket."], b44)
add_word("helmet", "n", "头盔，安全帽", ["He has a helmet."], b44)
add_word("slide down", "phrase", "滑下，往下滑", ["Joe slides down the pole."], b44)
add_word("pole", "n", "杆，柱", ["Joe slides down the pole."], b44)
add_word("howl", "v", "（狗、狼等）嗥叫，长嚎", ["Sparky howls."], b44)
add_word("fire truck", "n", "消防车", ["We see a fire truck."], b44)
add_word("ladder", "n", "梯子", ["It has hoses and a ladder."], b44)
add_word("check", "v", "检查", ["Joe checks the hoses."], b44)
add_word("work fine", "phrase", "运作正常", ["This hose is working fine."], b44)
add_word("up and up", "phrase", "越来越高", ["He goes up and up."], b44)
add_word("siren", "n", "汽笛，警报器", ["Joe checks the siren."], b44)
add_word("loud", "adj", "大声的，响亮的", ["The siren is very loud."], b44)
add_word("cover my ears", "phrase", "捂住我耳朵", ["I cover my ears."], b44)
add_word("smoke", "n", "烟，烟雾", ["He tells us smoke goes up."], b44)
add_word("go down to the floor", "phrase", "趴在地板上", ["We must go down to the floor."], b44)
add_word("has a surprise", "phrase", "有一个惊喜", ["He has a surprise."], b44)
add_word("reach into", "phrase", "伸手去……拿", ["He reaches into his truck."], b44)
add_word("one day", "phrase", "有一天", ["I will be a good fireman one day."], b44)
add_word("fire alarm", "n", "火警警报器", ["Ding! Ding! goes the fire alarm."], b44)
add_word("wave", "v", "挥手；挥手示意", ["I wave good bye to Fireman Joe."], b44)
add_word("ready to go", "phrase", "准备好出发", ["Fireman Joe is ready to go!"], b44)

# ===== Book 45: Just Critters Who Care (Little Critter 4) =====
b45 = "Just Critters Who Care"
books.append({"title": b45, "cn": "关心别人的小毛怪"})

add_word("hit", "v", "击（球）", ["I hit the ball very hard."], b45)
add_word("hard", "adv", "用力地，猛烈地", ["I hit the ball very hard."], b45)
add_word("next door", "phrase", "隔壁邻居，隔壁的房间", ["The ball flies next door."], b45)
add_word("spooky", "adj", "幽灵般的，令人毛骨悚然的", ["The ball is in the spooky yard."], b45)
add_word("yard", "n", "后院，院子", ["The ball is in the spooky yard."], b45)
add_word("maybe", "adv", "大概，或许", ["Maybe a monster lives there."], b45)
add_word("monster", "n", "怪兽，怪物", ["Maybe a monster lives there."], b45)
add_word("brave", "adj", "勇敢的", ["I am brave."], b45)
add_word("trip and fall", "phrase", "摔跟头，摔跤", ["I trip and fall."], b45)
add_word("bunny", "n", "（儿童用语）兔子", ["A little old bunny hands me our ball."], b45)
add_word("hand", "v", "交，递", ["A little old bunny hands me our ball."], b45)
add_word("why", "adv", "为什么", ["I ask my dad why it looks so spooky."], b45)
add_word("no one", "phrase", "没有人", ["She has no one to help her."], b45)
add_word("What a great idea", "phrase", "真是个好主意", ["What a great idea."], b45)
add_word("meet", "v", "碰头；集合", ["We meet at my house."], b45)
add_word("wear", "v", "穿（衣服）", ["Everyone wears a T-shirt."], b45)
add_word("parents", "n", "父母；双亲", ["Parents come, too."], b45)
add_word("knock on", "phrase", "敲击（门、窗）", ["I knock on the door."], b45)
add_word("clip", "v", "修剪；剪下", ["We clip the bushes."], b45)
add_word("bush", "n", "灌木，灌木丛", ["We clip the bushes."], b45)
add_word("pull up", "phrase", "拔起", ["We pull up weeds."], b45)
add_word("weed", "n", "野草，杂草", ["We pull up weeds."], b45)
add_word("trim", "v", "修剪，修整", ["We trim the trees."], b45)
add_word("porch", "n", "门廊；走廊", ["Dad fixes the porch step."], b45)
add_word("step", "n", "梯级，台阶", ["Dad fixes the porch step."], b45)
add_word("shutter", "n", "百叶窗，活动护窗", ["Tiger's dad fixes the shutter."], b45)
add_word("blow away", "phrase", "吹走", ["I blow away old leaves."], b45)
add_word("leaf", "n", "树叶", ["I blow away old leaves."], b45)
add_word("cookie", "n", "曲奇饼，小甜饼", ["Mrs. Bunny brings cookies and juice for all."], b45)
add_word("juice", "n", "（水果和蔬菜的）汁", ["Mrs. Bunny brings cookies and juice for all."], b45)
add_word("good idea", "phrase", "好主意，好想法", ["Everyone says, Good idea!"], b45)

# Update total
data['total'] = len(words)
data['books'] = books
data['words'] = words

with open('/workspace/kids_vocab/vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone! Total: {len(words)} words, {len(books)} books")
