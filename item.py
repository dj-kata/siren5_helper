#!/usr/bin/python3
from enum import Enum
import math

class item_category(Enum):
    kusa     = (1, "草")
    makimono = (2, "巻物")
    udewa    = (3, "腕輪")
    tubo     = (4, "壺")
    tue      = (5, "杖")
    buki     = (6, "武器")
    tate     = (7, "盾")

    def __init__(self, id, ja):
        self.id = id
        self.ja = ja

class Item:
    def __init__(self, name, category:item_category, buy:int, demerit:bool=False, 
                normal_shop:bool=False, vip_shop:bool=False, memo:str='', default_get:bool=False):
        self.name = name
        self.category = category
        self.buy = buy
        self.sell = int(buy*0.35)
        self.demerit = demerit # 完全なるデメリットアイテムのみ
        self.default_get = default_get
        self.get = default_get
        self.normal_shop = normal_shop
        self.vip_shop    = vip_shop
        self.memo = memo

    def disp(self):
        str_demerit = ''
        if self.demerit:
            str_demerit = "(デメリット) " 
        print(f"{self.name} {str_demerit}({self.category.ja}), 買値:{self.buy:,}, 売値:{self.sell:,}")

class Tubo(Item):
    def __init__(self, name, buy:int, capa_min:int, capa_max:int, demerit:bool=False, 
                normal_shop:bool=False, vip_shop:bool=False, memo:str='', default_get:bool=False):
        super().__init__(name, item_category.tubo, buy, demerit, normal_shop, vip_shop, memo, default_get)
        self.capa_min = capa_min
        self.capa_max = capa_max
        self.buy_max = int(self.buy*1.25)
        self.sell_max = int(self.sell*1.25)

    def disp(self):
        str_demerit = ''
        if self.demerit:
            str_demerit = "(デメリット) " 
        print(f"{self.name}[{self.capa_min}-{self.capa_max}] {str_demerit}({self.category.ja}), 買値:{self.buy:,}-{self.buy_max:,}, 売値:{self.sell:,}-{self.sell_max:,}")

class Tue(Item):
    def __init__(self, name, buy:int, capa_min:int, capa_max:int, demerit:bool=False, 
                normal_shop:bool=False, vip_shop:bool=False, memo:str='', default_get:bool=False):
        super().__init__(name, item_category.tubo, buy, demerit, normal_shop, vip_shop, memo, default_get)
        self.capa_min = capa_min
        self.capa_max = capa_max
        self.buy_max = int(self.buy*1.35)
        self.sell_max = int(self.sell*1.35)

    def disp(self):
        str_demerit = ''
        if self.demerit:
            str_demerit = "(デメリット) " 
        print(f"{self.name}[{self.capa_min}-{self.capa_max}] {str_demerit}({self.category.ja}), 買値:{self.buy:,}-{self.buy_max:,}, 売値:{self.sell:,}-{self.sell_max:,}")

class ItemList:
    kusa = []
    kusa.append(Item('雑草', item_category.kusa, 10, memo='植物特攻'))
    kusa.append(Item('薬草', item_category.kusa, 50, memo='HP+5'))
    kusa.append(Item('楽草', item_category.kusa, 50))

    kusa.append(Item('弟切草', item_category.kusa, 100, memo='HP+10'))
    kusa.append(Item('毒消し草', item_category.kusa, 100, memo='ドレイン特攻'))
    kusa.append(Item('毒草', item_category.kusa, 100))
    kusa.append(Item('高飛び草', item_category.kusa, 100, memo='浮遊特攻'))

    kusa.append(Item('いやし草', item_category.kusa, 200, memo='HP+15'))

    kusa.append(Item('パワーアップ草', item_category.kusa, 300))
    kusa.append(Item('成長の種', item_category.kusa, 300))
    kusa.append(Item('めぐすり草', item_category.kusa, 300, memo='1ツ目特攻印, 避けアップ印(2つ)'))
    kusa.append(Item('ぬぐすり草', item_category.kusa, 300))
    kusa.append(Item('すばやさ草', item_category.kusa, 300, memo='連続攻撃'))
    kusa.append(Item('胃拡張の種', item_category.kusa, 300))
    kusa.append(Item('胃縮小の種', item_category.kusa, 300, True))
    kusa.append(Item('混乱草', item_category.kusa, 300, memo='混乱'))
    kusa.append(Item('目つぶし草', item_category.kusa, 300, memo='目つぶし'))
    
    kusa.append(Item('命の草', item_category.kusa, 500, memo='HP+20'))
    kusa.append(Item('ちからの草', item_category.kusa, 500))
    kusa.append(Item('ドラゴン草', item_category.kusa, 500, memo='ドラゴン特攻, 炎減少'))
    kusa.append(Item('睡眠草', item_category.kusa, 500, memo='睡眠'))
    kusa.append(Item('狂戦士の草', item_category.kusa, 500))
    kusa.append(Item('ドラコン草', item_category.kusa, 500, True))
    
    kusa.append(Item('復活の草', item_category.kusa, 1000))
    kusa.append(Item('腹活の草', item_category.kusa, 1000, True))
    
    kusa.append(Item('やりなおし草', item_category.kusa, 1500))
    kusa.append(Item('やりなおせ草', item_category.kusa, 1500, True))
    
    kusa.append(Item('無敵草', item_category.kusa, 2000))
    kusa.append(Item('しあわせ草', item_category.kusa, 2000, memo='基本値+3'))
    kusa.append(Item('不幸の草', item_category.kusa, 2000, memo='LVダウン'))
    kusa.append(Item('忌火起草', item_category.kusa, 2000, True))
    kusa.append(Item('物忘れの草', item_category.kusa, 2000, True))

    kusa.append(Item('天使の種', item_category.kusa, 5000, memo='基本値+8'))
    kusa.append(Item('超不幸の種', item_category.kusa, 5000, memo='HP1'))

    makimono = []
    makimono.append(Item('あかりの巻物', item_category.makimono, 100))
    makimono.append(Item('オイルの巻物', item_category.makimono, 100))
    makimono.append(Item('紹介状', item_category.makimono, 100, default_get=True))
    makimono.append(Item('召介状', item_category.makimono, 100, True, default_get=True))
    makimono.append(Item('光の巻物', item_category.makimono, 100, default_get=True, memo='原始には出ない'))

    makimono.append(Item('識別の巻物', item_category.makimono, 200))

    makimono.append(Item('集合の巻物', item_category.makimono, 300))
    makimono.append(Item('道具寄せの巻物', item_category.makimono, 300))
    makimono.append(Item('いかすしの巻物', item_category.makimono, 300))

    makimono.append(Item('おはらいの巻物', item_category.makimono, 500))
    makimono.append(Item('天の恵みの巻物', item_category.makimono, 500))
    makimono.append(Item('地の恵みの巻物', item_category.makimono, 500))
    makimono.append(Item('メッキの巻物', item_category.makimono, 500))
    makimono.append(Item('換金の巻物', item_category.makimono, 500))
    makimono.append(Item('おにぎりの巻物', item_category.makimono, 500))
    makimono.append(Item('壺増大の巻物', item_category.makimono, 500))
    makimono.append(Item('壺増犬の巻物', item_category.makimono, 500, True))
    makimono.append(Item('吸い出しの巻物', item_category.makimono, 500))
    makimono.append(Item('祝福の巻物', item_category.makimono, 500))
    makimono.append(Item('たたりの巻物', item_category.makimono, 500, True))
    makimono.append(Item('夫の恵みの巻物', item_category.makimono, 500))
    makimono.append(Item('他の恵みの巻物', item_category.makimono, 500))
    makimono.append(Item('タダの巻物', item_category.makimono, 500, default_get=True))
    makimono.append(Item('タグの巻物', item_category.makimono, 500, default_get=True, memo='原始には出ない'))

    makimono.append(Item('ゾワゾワの巻物', item_category.makimono, 800))
    makimono.append(Item('ワナ消しの巻物', item_category.makimono, 800))
    makimono.append(Item('水がれの巻物', item_category.makimono, 800, memo='水棲特攻'))
    makimono.append(Item('ワナの巻物', item_category.makimono, 800, True))
    makimono.append(Item('くちなしの巻物', item_category.makimono, 800, True))
    makimono.append(Item('拾えずの巻物', item_category.makimono, 800, True))
    makimono.append(Item('ひきよせの巻物', item_category.makimono, 800, True))

    makimono.append(Item('混乱の巻物', item_category.makimono, 1000))
    makimono.append(Item('バクスイの巻物', item_category.makimono, 1000))
    makimono.append(Item('真空斬りの巻物', item_category.makimono, 1000))
    makimono.append(Item('オーラ消しの巻物', item_category.makimono, 1000))
    makimono.append(Item('敵加速の巻物', item_category.makimono, 1000, True))
    makimono.append(Item('魔物部屋の巻物', item_category.makimono, 1000))
    makimono.append(Item('予防の巻物', item_category.makimono, 1000, memo='爆発無効'))
    makimono.append(Item('困った時の巻物', item_category.makimono, 1000))
    makimono.append(Item('国った時の巻物', item_category.makimono, 1000))
    makimono.append(Item('バクチの巻物', item_category.makimono, 1000, default_get=True))
    makimono.append(Item('昼夜の巻物', item_category.makimono, 1000, default_get=True, memo='原始には出ない'))
    makimono.append(Item('技回復の巻物', item_category.makimono, 1000, default_get=True, memo='原始には出ない'))
    makimono.append(Item('枝回復の巻物', item_category.makimono, 1000, default_get=True, memo='原始には出ない'))

    makimono.append(Item('迷子の巻物', item_category.makimono, 3000, memo='無気力'))
    makimono.append(Item('聖域の巻物', item_category.makimono, 3000))
    makimono.append(Item('金滅の巻物', item_category.makimono, 3000, True))
    makimono.append(Item('全滅の巻物', item_category.makimono, 3000, default_get=True, memo='原始には出ない'))

    makimono.append(Item('白紙の巻物', item_category.makimono, 5000, default_get=True))
    makimono.append(Item('ねだやしの巻物', item_category.makimono, 10000))

    tubo = []
    tubo.append(Tubo('保存の壺', 600,3,5))
    tubo.append(Tubo('ただの壺', 600,3,5))
    tubo.append(Tubo('識別の壺', 600,3,5))
    tubo.append(Tubo('やりすごしの壺', 600,3,5))
    tubo.append(Tubo('四二鉢', 600,3,5, True))

    tubo.append(Tubo('換金の壺', 1000,3,5))
    tubo.append(Tubo('変化の壺', 1000,3,5))
    tubo.append(Tubo('変花の壺', 1000,3,5, True))
    tubo.append(Tubo('手封じの壺', 1000,3,5, True))
    tubo.append(Tubo('割れない壺', 1000,3,5))
    tubo.append(Tubo('底抜けの壺', 1000,2,4))
    tubo.append(Tubo('フィーバーの壺', 1000,3,3))

    tubo.append(Tubo('おはらいの壺', 1600,2,4))
    tubo.append(Tubo('祝福の壺', 1600,2,4))
    tubo.append(Tubo('たたりの壺', 1600,2,4, True, memo='矢、札運びには使える'))

    tubo.append(Tubo('水がめ', 2000,3,5,default_get=True))
    tubo.append(Tubo('天上の器', 2000,3,3))

    tubo.append(Tubo('冷えびえ香の壺', 2500,2,4))
    tubo.append(Tubo('身かわし香の壺', 2500,2,4))
    tubo.append(Tubo('目配り香の壺', 2500,2,4))
    tubo.append(Tubo('山彦香の壺', 2500,2,4))

    tubo.append(Tubo('背中の壺', 3500,3,5,memo='回復'))
    tubo.append(Tubo('トドの壺', 3500,3,5))
    tubo.append(Tubo('魔物の壺', 3500,3,5,True))
    tubo.append(Tubo('クラインの壺', 3500,3,5))
    tubo.append(Tubo('笑いの壺', 3500,2,4))
    tubo.append(Tubo('乙女の祈りの壺', 3500,3,3))

    tubo.append(Tubo('合成の壺', 6000,5,5))
    tubo.append(Tubo('合城の壺', 6000,3,5))

    tubo.append(Tubo('強化の壺', 10000,2,3))
    tubo.append(Tubo('弱化の壺', 10000,2,3, True))

    tubo.append(Tubo('強イヒの壺', 10000,3,5, True))
    tubo.append(Tubo('福寄せの壺', 10000,3,5))
    tubo.append(Tubo('厄寄せの壺', 10000,3,5, True))

    udewa=[]
    udewa.append(Item('ちからの腕輪', item_category.udewa, 2000))
    udewa.append(Item('遠投の腕輪',item_category.udewa, 2000))
    udewa.append(Item('ヘタ投げの腕輪',item_category.udewa, 2000))
    udewa.append(Item('武器束ねの腕輪',item_category.udewa, 2000))

    udewa.append(Item('毒消しの腕輪',item_category.udewa, 3000))
    udewa.append(Item('混乱よけの腕輪',item_category.udewa, 3000))
    udewa.append(Item('睡眠よけの腕輪',item_category.udewa, 3000))
    udewa.append(Item('呪いよけの腕輪',item_category.udewa, 3000))
    udewa.append(Item('保持の腕輪',item_category.udewa, 3000))
    udewa.append(Item('痛恨の腕輪',item_category.udewa, 3000, True))
    udewa.append(Item('呪い師の腕輪',item_category.udewa, 3000))
    udewa.append(Item('魔物呼びの腕輪',item_category.udewa, 3000, True))
    udewa.append(Item('透ネ見の腕輪',item_category.udewa, 3000, True))
    udewa.append(Item('ワナの腕輪',item_category.udewa, 3000, True))

    udewa.append(Item('気配察知の腕輪',item_category.udewa, 5000))
    udewa.append(Item('気配察血の腕輪',item_category.udewa, 5000))
    udewa.append(Item('道具感知の腕輪',item_category.udewa, 5000))
    udewa.append(Item('道具感血の腕輪',item_category.udewa, 5000))
    udewa.append(Item('水グモの腕輪',item_category.udewa, 5000))
    udewa.append(Item('壁抜けの腕輪',item_category.udewa, 5000))
    udewa.append(Item('回復の腕輪',item_category.udewa, 5000, memo='回復'))
    udewa.append(Item('裏道の腕輪',item_category.udewa, 5000))
    udewa.append(Item('高飛びの腕輪',item_category.udewa, 5000))
    udewa.append(Item('爆発の腕輪',item_category.udewa, 5000, memo='爆発無効'))
    udewa.append(Item('ノナリーの腕輪',item_category.udewa, 5000, True))

    udewa.append(Item('しあわせの腕輪',item_category.udewa, 10000))
    udewa.append(Item('弾きよけの腕輪',item_category.udewa, 10000))

    udewa.append(Item('鑑定師の腕輪',item_category.udewa, 30000))

    udewa.append(Item('VIPの腕輪',item_category.udewa, 50000))

    tue=[]
    tue.append(Tue('場所がえの杖', 600, 5, 7))
    tue.append(Tue('吹き飛ばしの杖', 600, 5, 7))
    tue.append(Tue('飛びつきの杖', 600, 5, 7))
    tue.append(Tue('魔道の杖', 600, 5, 7))
    tue.append(Tue('鈍足の杖', 600, 4,6))
    tue.append(Tue('加速の杖', 600, 4,6, memo='連続攻撃'))

    tue.append(Tue('一時しのぎの杖', 900,4,6))
    tue.append(Tue('かなしばりの杖', 900,4,6, memo='かなしばり'))
    tue.append(Tue('かなしばいの杖', 900,4,6, memo='投げつけると目つぶし'))
    tue.append(Tue('転ばぬ先の杖', 900,4,6))
    tue.append(Tue('転ばぬ先生の杖', 900,5,7))
    tue.append(Tue('痛み分けの杖', 900,5,7))
    tue.append(Tue('ただの杖', 900,5,7, memo='魔法特攻'))
    tue.append(Tue('ワナ消しの杖', 900,5,7, '2ダメージ'))

    tue.append(Tue('感電の杖', 1200,4,6))
    tue.append(Tue('盛電の杖', 1200,4,6, True))

    tue.append(Tue('封印の杖', 1500,4,6, memo='封印'))
    tue.append(Tue('身代わりの杖', 1500,4,6))
    tue.append(Tue('身伐わりの杖', 1500,4,6, True))

    tue.append(Tue('しあわせの杖', 1800,4,6))
    tue.append(Tue('しわよせの杖', 1800,4,6, True, memo='余勢'))
    tue.append(Tue('トンネルの杖', 1800,4,6, memo='10ダメージ'))
    tue.append(Tue('土塊の杖', 1800,4,6, memo='爆発無効'))
    tue.append(Tue('不幸の杖', 1800,4,6))

    buki=[]
    buki.append(Item('ただの棒',item_category.buki,300))
    buki.append(Item('超ボロボロの剣',item_category.buki,300))
    buki.append(Item('銅の刃',item_category.buki,700))
    buki[-1].sell = 245
    buki.append(Item('くすんだ金の剣',item_category.buki,1000))
    buki.append(Item('ボロいつるはし',item_category.buki,1000))
    buki.append(Item('カタナ',item_category.buki,1100))
    buki.append(Item('獣の牙',item_category.buki,1600))
    buki.append(Item('キョクタンソード',item_category.buki,2000))
    buki.append(Item('ボロい木づち',item_category.buki,2000))
    buki.append(Item('どうたぬき',item_category.buki,2200))
    buki.append(Item('血引きの刃',item_category.buki,2500))
    buki.append(Item('魔法斬りの剣',item_category.buki,2500))
    buki.append(Item('三日月刀',item_category.buki,2500))
    buki.append(Item('隕石の刃',item_category.buki,3000))
    buki.append(Item('光の刃',item_category.buki,3000))
    buki.append(Item('金食い虫こん棒',item_category.buki,3000))
    buki.append(Item('使い捨て刀',item_category.buki,3000))
    buki.append(Item('封印棒',item_category.buki,3300))
    buki.append(Item('トカゲ斬りの刃',item_category.buki,3500))
    buki.append(Item('かねきりの刃',item_category.buki,3500))
    buki.append(Item('しびれ刀',item_category.buki,4000))
    buki.append(Item('朱剛石の刃',item_category.buki,4200))
    buki.append(Item('ドレイン斬り',item_category.buki,4500))
    buki.append(Item('戦神の斧',item_category.buki,5000))
    buki.append(Item('ガラスの剣',item_category.buki,5000))
    buki.append(Item('草かりのカマ',item_category.buki,5500))
    buki[-1].sell = 1925
    buki.append(Item('一ツ目殺し',item_category.buki,5500))
    buki[-1].sell = 1925
    buki.append(Item('真っ暗棒',item_category.buki,6000))
    buki.append(Item('水斬りの剣',item_category.buki,6500))
    buki.append(Item('おねむガラガラ',item_category.buki,7000))
    buki.append(Item('カブラの刀',item_category.buki,7400))
    buki.append(Item('空の刃',item_category.buki,7500))
    buki.append(Item('かまいたち',item_category.buki,8000))
    buki.append(Item('風魔鉄の剣',item_category.buki,10000))
    buki.append(Item('火の刃',item_category.buki,10000))
    buki.append(Item('サトリピック',item_category.buki,10000))
    buki.append(Item('壊れないハンマー',item_category.buki,15000))
    buki.append(Item('カブラギ',item_category.buki,15000))
    buki.append(Item('必中小刀',item_category.buki,20000))

    tate=[]
    tate.append(Item('ただの木の盾',item_category.buki,360))
    tate[-1].sell = 126
    tate.append(Item('超ボロボロの盾',item_category.buki,360))
    tate[-1].sell = 126
    tate.append(Item('銅の盾',item_category.buki,740))
    tate.append(Item('鉄の盾',item_category.buki,1300))
    tate[-1].sell = 455
    tate.append(Item('くすんだ金の盾',item_category.buki,1500))
    tate.append(Item('灯火の盾',item_category.buki,1500))
    tate.append(Item('おにおおかみ',item_category.buki,1800))
    tate.append(Item('金庫の盾',item_category.buki,1800))
    tate.append(Item('混乱の手斧',item_category.buki,2000))
    tate.append(Item('錠前の盾',item_category.buki,2000))
    tate.append(Item('獣の盾',item_category.buki,2400))
    tate.append(Item('金食い虫の盾',item_category.buki,2500))
    tate.append(Item('イチかゼロの盾',item_category.buki,2500))
    tate.append(Item('反撃の盾',item_category.buki,3000))
    tate.append(Item('動かずの盾',item_category.buki,3000))
    tate.append(Item('攻撃の盾',item_category.buki,3000))
    tate.append(Item('隕石の盾',item_category.buki,3200))
    tate.append(Item('使い捨ての板',item_category.buki,4000))
    tate.append(Item('ややギャドンな盾',item_category.buki,4000))
    tate.append(Item('夜の盾',item_category.buki,4200))
    tate.append(Item('昼の盾',item_category.buki,4200))
    tate.append(Item('朱剛石の盾',item_category.buki,4800))
    tate.append(Item('ハラモチの盾',item_category.buki,5000))
    tate.append(Item('重い盾',item_category.buki,6000))
    tate.append(Item('爆発隠の盾',item_category.buki,6000))
    tate.append(Item('変換の盾',item_category.buki,6000))
    tate.append(Item('ガラスの盾',item_category.buki,6000))
    tate.append(Item('見切りの盾',item_category.buki,8000))
    tate.append(Item('福果の盾',item_category.buki,8000))
    tate.append(Item('風魔鉄の盾',item_category.buki,8500))
    tate.append(Item('受け流しの盾',item_category.buki,9000))
    tate.append(Item('トカゲの盾',item_category.buki,10000))
    tate.append(Item('ややゲイズな盾',item_category.buki,10000))
    tate.append(Item('どんぶりの盾',item_category.buki,10000))
    tate.append(Item('螺旋風魔の盾',item_category.buki,12000))
    tate.append(Item('にぎりよけの盾',item_category.buki,12000))
    tate.append(Item('サトリの盾',item_category.buki,14000))

    def load(self, params):
        for i,tmp in enumerate(self.kusa):
            tmp.get = bool(params['kusa'][i])
        for i,tmp in enumerate(self.makimono):
            tmp.get = bool(params['makimono'][i])
        for i,tmp in enumerate(self.udewa):
            tmp.get = bool(params['udewa'][i])
        for i,tmp in enumerate(self.tubo):
            tmp.get = bool(params['tubo'][i])
        for i,tmp in enumerate(self.tue):
            tmp.get = bool(params['tue'][i])

    def save(self, params):
        for i,tmp in enumerate(self.kusa):
            params['kusa'][i] = tmp.get
        for i,tmp in enumerate(self.makimono):
            params['makimono'][i] = tmp.get
        for i,tmp in enumerate(self.udewa):
            params['udewa'][i] = tmp.get
        for i,tmp in enumerate(self.tubo):
            params['tubo'][i] = tmp.get
        for i,tmp in enumerate(self.tue):
            params['tue'][i] = tmp.get

    def reset(self):
        for i in self.kusa:
            i.get = i.default_get
        for i in self.makimono:
            i.get = i.default_get
        for i in self.udewa:
            i.get = i.default_get
        for i in self.tubo:
            i.get = i.default_get
        for i in self.tue:
            i.get = i.default_get

    def get_stat(self):
        cnt = [0,0,0,0,0,  0,0,0] # 草、巻物、腕輪、壺、杖、100,300,500草
        total = [0,0,0,0,0, 0,0,0] # 分母

        for i,tmp in enumerate(self.kusa):
            total[0] += 1
            if tmp.get:
                cnt[0] += 1
            if tmp.buy == 100:
                total[5] += 1
                if tmp.get:
                    cnt[5] += 1
            if tmp.buy == 300:
                total[6] += 1
                if tmp.get:
                    cnt[6] += 1
            if tmp.buy == 500:
                total[7] += 1
                if tmp.get:
                    cnt[7] += 1
        for i,tmp in enumerate(self.makimono):
            total[1] += 1
            if tmp.get:
                cnt[1] += 1
        for i,tmp in enumerate(self.udewa):
            total[2] += 1
            if tmp.get:
                cnt[2] += 1
        for i,tmp in enumerate(self.tubo):
            total[3] += 1
            if tmp.get:
                cnt[3] += 1
        for i,tmp in enumerate(self.tue):
            total[4] += 1
            if tmp.get:
                cnt[4] += 1
        return cnt, total

if __name__ == '__main__':
    a = ItemList()
    for i in a.makimono:
        i.disp()
    for i in a.tue:
        i.disp()
    print(a.get_stat())