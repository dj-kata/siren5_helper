#!/usr/bin/python3
from enum import Enum
import csv

class item_category(Enum):
    kusa     = (1, "草")
    makimono = (2, "巻物")
    udewa    = (3, "腕輪")
    tubo     = (4, "壺")
    tue      = (5, "杖")
    buki     = (6, "武器")
    tate     = (7, "盾")
    okou     = (8, "お香")

    def __init__(self, id, ja):
        self.id = id
        self.ja = ja

class Item:
    def __init__(self, name, category:item_category, buy:str, sell:str, bin:str, tin:str, demerit:bool=False, 
                normal_shop:bool=False, vip_shop:bool=False, memo:str='', default_get:bool=False):
        print(name, )
        self.name = name
        self.category = category
        self.buy = int(buy)
        self.sell = int(sell)
        self.bin = bin
        self.tin=tin

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

class Tue(Item):
    def __init__(self, name, buy:str, sell:str, buy_unit:str, sell_unit:str, capa_min:str, capa_max:str, bin:str, tin:str,
                 demerit:bool=False, normal_shop:bool=False, vip_shop:bool=False, memo:str='', default_get:bool=False):
        super().__init__(name, item_category.tue, buy, sell, bin, tin, demerit, normal_shop, vip_shop, memo, default_get)
        self.buy_unit  = int(buy_unit)
        self.sell_unit = int(sell_unit)
        self.capa_min  = int(capa_min)
        self.capa_max  = int(capa_max)
        self.buy_max   = int(buy)+int(buy_unit)*int(capa_max)
        self.sell_max  = int(sell)+int(sell_unit)*int(capa_max)

    def disp(self):
        str_demerit = ''
        if self.demerit:
            str_demerit = "(デメリット) " 
        print(f"{self.name}[{self.capa_min}-{self.capa_max}] {str_demerit}({self.category.ja}), 買値:{self.buy:,}-{self.buy_max:,}, 売値:{self.sell:,}-{self.sell_max:,}")

class Tubo(Item):
    def __init__(self, name, buy:str, sell:str, buy_unit:str, sell_unit:str, capa_min:str, capa_max:str, bin:str, tin:str,
                 demerit:bool=False, normal_shop:bool=False, vip_shop:bool=False, memo:str='', default_get:bool=False):
        super().__init__(name, item_category.tubo, buy, sell, bin, tin, demerit, normal_shop, vip_shop, memo, default_get)
        self.buy_unit  = int(buy_unit)
        self.sell_unit = int(sell_unit)
        self.capa_min  = int(capa_min)
        self.capa_max  = int(capa_max)
        self.buy_max   = int(buy)+int(buy_unit)*int(capa_max)
        self.sell_max  = int(sell)+int(sell_unit)*int(capa_max)

    def disp(self):
        str_demerit = ''
        if self.demerit:
            str_demerit = "(デメリット) " 
        print(f"{self.name}[{self.capa_min}-{self.capa_max}] {str_demerit}({self.category.ja}), 買値:{self.buy:,}-{self.buy_max:,}, 売値:{self.sell:,}-{self.sell_max:,}")

class ItemList:
    kusa = []
    makimono = []
    udewa=[]
    tue = []
    tubo = []
    okou = []
    buki = []
    tate = []
    header = '6_'
    with open(f'data/{header}kusa.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            kusa.append(Item(t[0], item_category.kusa, t[1], t[2], t[3], t[4], memo=t[5]))
    with open(f'data/{header}makimono.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            makimono.append(Item(t[0], item_category.makimono, t[1], t[2], t[3], t[4], memo=t[5]))
    with open(f'data/{header}udewa.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            udewa.append(Item(t[0], item_category.udewa, t[1], t[2], t[3], t[4], memo=t[5]))
    with open(f'data/{header}buki.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            buki.append(Item(t[0], item_category.udewa, t[1], t[2], t[3], t[4], memo=t[5]))
    with open(f'data/{header}tate.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            tate.append(Item(t[0], item_category.udewa, t[1], t[2], t[3], t[4], memo=t[5]))
    with open(f'data/{header}tue.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            tue.append(Tue(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], memo=t[9]))
    with open(f'data/{header}tubo.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            tubo.append(Tubo(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], memo=t[9]))
    with open(f'data/{header}okou.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for t in [row for row in reader][1:]:
            okou.append(Tubo(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], memo=t[9]))

    def load(self, params):
        """ユーザデータのjsonからチェック済みの状態を読み込む

        Args:
            params (dict): settings.jsonの内容
        """
        print(params)
        for i,tmp in enumerate(self.kusa):
            tmp.get = bool(params['kusa'][i])
        for i,tmp in enumerate(self.makimono):
            tmp.get = bool(params['makimono'][i])
        for i,tmp in enumerate(self.udewa):
            tmp.get = bool(params['udewa'][i])
        for i,tmp in enumerate(self.tubo):
            tmp.get = bool(params['tubo'][i])
        for i,tmp in enumerate(self.okou):
            tmp.get = bool(params['okou'][i])
        for i,tmp in enumerate(self.tue):
            tmp.get = bool(params['tue'][i])
        for i,tmp in enumerate(self.buki):
            tmp.get = bool(params['buki'][i])
        for i,tmp in enumerate(self.tate):
            tmp.get = bool(params['tate'][i])

    def save(self, params):
        """チェック済みかどうかの状態をdictへ出力

        Args:
            params (dict): 出力先となるsettings.jsonの内容
        """
        for i,tmp in enumerate(self.kusa):
            params['kusa'][i] = tmp.get
        for i,tmp in enumerate(self.makimono):
            params['makimono'][i] = tmp.get
        for i,tmp in enumerate(self.udewa):
            params['udewa'][i] = tmp.get
        for i,tmp in enumerate(self.tubo):
            params['tubo'][i] = tmp.get
        for i,tmp in enumerate(self.okou):
            params['okou'][i] = tmp.get
        for i,tmp in enumerate(self.tue):
            params['tue'][i] = tmp.get
        for i,tmp in enumerate(self.buki):
            params['buki'][i] = tmp.get
        for i,tmp in enumerate(self.tate):
            params['tate'][i] = tmp.get

    def reset(self):
        for i in self.kusa:
            i.get = i.default_get
        for i in self.makimono:
            i.get = i.default_get
        for i in self.udewa:
            i.get = i.default_get
        for i in self.tubo:
            i.get = i.default_get
        for i in self.okou:
            i.get = i.default_get
        for i in self.tue:
            i.get = i.default_get
        for i in self.buki:
            i.get = i.default_get
        for i in self.tate:
            i.get = i.default_get

    def get_stat(self):
        cnt = [0,0,0,0,0,0,  0,0,0] # 草、巻物、腕輪、壺、お香、杖、100,300,500草
        total = [0,0,0,0,0,0, 0,0,0] # 分母

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
            if not tmp.default_get:
                total[1] += 1
                if tmp.get:
                    cnt[1] += 1
        for i,tmp in enumerate(self.udewa):
            total[2] += 1
            if tmp.get:
                cnt[2] += 1
        for i,tmp in enumerate(self.tubo):
            if not tmp.default_get:
                total[3] += 1
                if tmp.get:
                    cnt[3] += 1
        for i,tmp in enumerate(self.okou):
            total[4] += 1
            if tmp.get:
                cnt[4] += 1
        for i,tmp in enumerate(self.tue):
            total[5] += 1
            if tmp.get:
                cnt[5] += 1
        return cnt, total

if __name__ == '__main__':
    a = ItemList()
    for i in a.makimono:
        i.disp()
    for i in a.tue:
        i.disp()
    print(a.get_stat())