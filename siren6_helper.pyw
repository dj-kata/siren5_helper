import PySimpleGUI as sg
from item import ItemList
from enum import Enum
from inlist import bukiin,tatein
from monster import MonsterList
import os, json, codecs
# TODO self.modeを廃止する

SWNAME = 'siren6_helper'
SWVER  = 'v1.0.0'

class gui_mode(Enum):
    main=1

class UserSettings:
    def __init__(self, savefile='settings.json'):
        self.savefile = savefile
        self.params   = self.load_settings()
    def get_default_settings(self):
        tmp = ItemList()
        ret = {
        'lx':0,'ly':0,'lw':970,'lh':930,'memo':'', 'memo_const':'',
        }
        ret['kusa']     = [0]*len(tmp.kusa)
        ret['makimono'] = [0]*len(tmp.makimono)
        ret['udewa']    = [0]*len(tmp.udewa)
        ret['tubo']     = [0]*len(tmp.tubo)
        ret['okou']     = [0]*len(tmp.okou)
        ret['tue']      = [0]*len(tmp.tue)
        ret['buki']     = [0]*len(tmp.buki)
        ret['tate']     = [0]*len(tmp.tate)
        return ret
    def load_settings(self):
        default_val = self.get_default_settings()
        ret = {}
        try:
            with open(self.savefile) as f:
                ret = json.load(f)
                print(f"設定をロードしました。\n")
        except Exception:
            print(f"有効な設定ファイルなし。デフォルト値を使います。")

        ### 後から追加した値がない場合にもここでケア
        for k in default_val.keys():
            if not k in ret.keys():
                print(f"{k}が設定ファイル内に存在しません。デフォルト値({default_val[k]}を登録します。)")
                ret[k] = default_val[k]

        return ret

    def save_settings(self):
        with open(self.savefile, 'w') as f:
            json.dump(self.params, f, indent=2)

class GUI:
    def __init__(self):
        self.savefile = 'settings.json'
        self.settings = UserSettings(self.savefile)
        #print(self.settings.params)
        sg.theme('SystemDefault')
        self.FONT = ('Meiryo',16)
        self.mode = 'kusa'
        self.window = False
        self.itemlist = ItemList()
        self.itemlist.load(self.settings.params)
        self.conv_tabname = {'草':'kusa', '巻物':'makimono','腕輪':'udewa','壺':'tubo','お香':'okou', '杖':'tue'}

    # icon用
    def ico_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def gui_main(self): #メインウィンドウ
        if self.window:
            self.window.close()
        header=['名前','容量','買値','売値','武器印', '盾印', 'メモ']
        menuitems = [['ファイル',['設定',]],['ヘルプ',[f'{SWNAME}について']]]
        right_click_menu = ['&Right', ['貼り付け']]
        layout_det_table = []
        for i,k in enumerate(['kusa', 'makimono', 'udewa', 'tubo', 'okou', 'tue', 'buki', 'tate']):
            wmod = 7 if i in (3, 4) else 0
            layout_det_table.append(sg.Table([], key=f'table_{k}', headings=header,font=self.FONT
                    ,vertical_scroll_only=False
                    ,auto_size_columns=False
                    ,col_widths=[15,5,6+wmod,6+wmod,10,10,100]
                    ,justification='left'
                    ,size=(1,10)
                    ,background_color='#ffffff'
                    ,alternating_row_color='#dddddd'
                    )
            )
        layout_det = [
            [sg.TabGroup([
                [
                    sg.Tab('草', [[layout_det_table[0]]]),
                    sg.Tab('巻物', [[layout_det_table[1]]]),
                    sg.Tab('腕輪', [[layout_det_table[2]]]),
                    sg.Tab('壺', [[layout_det_table[3]]]),
                    sg.Tab('お香', [[layout_det_table[4]]]),
                    sg.Tab('杖', [[layout_det_table[5]]]),
                    sg.Tab('武器(Lv1)', [[layout_det_table[6]]]),
                    sg.Tab('盾(Lv1)', [[layout_det_table[7]]]),
                ]
            ],key='tg_det',font=self.FONT)],
            [sg.Button('識別済にする', key='btn_get', font=self.FONT), sg.Button('未識別に戻す', key='btn_lost', font=self.FONT), ],
            [
                sg.Text('草:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_kusa'),
                sg.Text('巻物:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_makimono'),
                sg.Text('腕輪:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_udewa'),
                sg.Text('壺:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_tubo'),
                sg.Text('お香:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_okou'),
                sg.Text('杖:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_tue'),
            ],
            #[
            #    sg.Text('100G草:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_100kusa'),
            #    sg.Text('300G草:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_300kusa'),
            #    sg.Text('500G草:', font=self.FONT), sg.Text('0/0', font=self.FONT, key='cnt_500kusa'),
            #],
        ]
        layout_monster =[
            [sg.Text('この階層以降を表示:', font=self.FONT), sg.Combo([f"{i}" for i in range(1,100)], default_value='1', readonly=True, font=self.FONT, enable_events=True, key='floor')],
            [sg.Table([['']*10 for i in range(99)], headings=['階層','1','2','3','4','5','6','7','8','9'], key='table_monster', font=self.FONT
                    ,vertical_scroll_only=False
                    ,auto_size_columns=False
                    ,col_widths=[4,13,13,13,13,13,13,13,13,13]
                    ,justification='left'
                    ,size=(1,10)
                    ,background_color='#ffffff'
                    ,alternating_row_color='#dddddd'
                    )
            ],
        ]
        layout_memo = [
            [sg.Text('メモ(冒険用)',font=self.FONT)],
            [sg.Multiline('', key='memo',font=self.FONT)],
            [sg.Text('メモ(リセット時に削除されない)',font=self.FONT)],
            [sg.Multiline('', key='memo_const',font=self.FONT)],
        ]
        layout = [
            #[sg.TabGroup([[sg.Tab('識別', layout_det, key='tab_det'), sg.Tab('装備品', layout_soubi, key='tab_soubi'), sg.Tab('モンスター', layout_monster, key='tab_monster'), sg.Tab('メモ', layout_memo, key='tab_memo')]],key='tg_top',font=self.FONT)],
            [sg.TabGroup([[sg.Tab('識別', layout_det, key='tab_det'), sg.Tab('メモ', layout_memo, key='tab_memo')]],key='tg_top',font=self.FONT)],
            [sg.Button('リセット', key='btn_reset', font=self.FONT)],
            [sg.Text('', key='txt_info', font=('Meiryo',10))],
        ]
        ico=self.ico_path('icon.ico')
        #self.window = sg.Window(SWNAME, layout, grab_anywhere=True,return_keyboard_events=True,resizable=True,finalize=True,enable_close_attempted_event=True,icon=ico,location=(self.settings.params['lx'], self.settings.params['ly']), size=(self.settings.params['lw'],self.settings.params['lh']))
        self.window = sg.Window(SWNAME, layout, grab_anywhere=True,return_keyboard_events=True,resizable=True,finalize=True,enable_close_attempted_event=True,icon=ico,location=(self.settings.params['lx'], self.settings.params['ly']), size=(990, 930))
        # 設定値の反映
        self.window['tg_top'].expand(expand_x=True, expand_y=True)
        self.window['tg_det'].expand(expand_x=True, expand_y=True)
        self.window['table_kusa'].expand(expand_x=True, expand_y=True)
        self.window['table_makimono'].expand(expand_x=True, expand_y=True)
        self.window['table_udewa'].expand(expand_x=True, expand_y=True)
        self.window['table_tubo'].expand(expand_x=True, expand_y=True)
        self.window['table_okou'].expand(expand_x=True, expand_y=True)
        self.window['table_tue'].expand(expand_x=True, expand_y=True)
        self.window['table_buki'].expand(expand_x=True, expand_y=True)
        self.window['table_tate'].expand(expand_x=True, expand_y=True)
        #self.window['table_monster'].expand(expand_x=True, expand_y=True)
        self.window['memo'].expand(expand_x=True, expand_y=True)
        self.window['memo'].update(self.settings.params['memo'])
        self.window['memo_const'].expand(expand_x=True, expand_y=True)
        self.window['memo_const'].update(self.settings.params['memo_const'])
        self.update_table()
        self.mode = 'kusa'
        #self.update_monster(1)
        ### 印の反映
        #for k in self.settings.params.keys():
        #    if ('bin_' in k) or ('tin_' in k):
        #        self.window[k].update(self.settings.params[k])

    def mod_target(self, category, idx:int, val:bool):
        target = []
        if category == 'kusa':
            self.itemlist.kusa[idx].get = val
        elif category == 'makimono':
            self.itemlist.makimono[idx].get = val
        elif category == 'udewa':
            self.itemlist.udewa[idx].get = val
        elif category == 'tue':
            self.itemlist.tue[idx].get = val
        elif category == 'tubo':
            self.itemlist.tubo[idx].get = val
        elif category == 'okou':
            self.itemlist.okou[idx].get = val
        #elif category == 'buki':
        #    self.itemlist.buki[idx].get = val
        #elif category == 'tate':
        #    self.itemlist.tate[idx].get = val

    def get_target(self, category):
        target = []
        if category == 'kusa':
            target = self.itemlist.kusa
        elif category == 'makimono':
            target = self.itemlist.makimono
        elif category == 'udewa':
            target = self.itemlist.udewa
        elif category == 'tue':
            target = self.itemlist.tue
        elif category == 'tubo':
            target = self.itemlist.tubo
        elif category == 'okou':
            target = self.itemlist.okou
        elif category == 'buki':
            target = self.itemlist.buki
        elif category == 'tate':
            target = self.itemlist.tate
        return target

    def update_table(self):
        #for k in ['kusa', 'makimono', 'udewa', 'tubo', 'tue', 'buki', 'tate']:
        for k in ['kusa', 'makimono', 'udewa', 'tubo', 'okou', 'tue', 'buki', 'tate']:
            data=[]
            target = self.get_target(k)
            row_colors = []
            pre_buy = target[0].buy
            is_odd = False
            for i,item in enumerate(target):
                capacity = ''
                fontcolor = 'black'
                buy = f"{item.buy:,}"
                sell = f"{item.sell:,}"
                if k in ['tue','tubo','okou']:
                    if item.capa_min == item.capa_max:
                        capacity = item.capa_max
                    else:
                        capacity = f"{item.capa_min}-{item.capa_max}"
                    buy = f"{item.buy:,} - {item.buy_max:,}"
                    sell = f"{item.sell:,} - {item.sell_max:,}"
                data.append([item.name, capacity, buy, sell, item.bin, item.tin, item.memo])
                if item.buy != pre_buy:
                    pre_buy = item.buy
                    is_odd = not is_odd
                if is_odd:
                    bgcolor = '#ffffb0'
                else:
                    bgcolor = '#b0ffff'
                if item.get:
                    bgcolor = '#666666'
                if item.default_get:
                    bgcolor = '#666666'
                if item.demerit: # 完全なデメリットアイテムは文字を灰色に
                    fontcolor='#888888'
                row_colors.append((i, fontcolor, bgcolor))
            self.window[f'table_{k}'].update(data)
            self.window[f'table_{k}'].update(row_colors=row_colors)

        # 統計情報の取得
        self.write_stat_xml()
        cnt,total = self.itemlist.get_stat()
        #for i,name in enumerate(['kusa', 'makimono', 'udewa', 'tubo', 'tue', '100kusa','300kusa', '500kusa']):
        for i,name in enumerate(['kusa', 'makimono', 'udewa', 'tubo', 'tue']):
            self.window[f'cnt_{name}'].update(f"{cnt[i]}/{total[i]}")

    def update_info(self, msg):
        self.window['txt_info'].update(msg)

    # モンスター表を更新する。st:この階層以降を表示
    def update_monster(self, st):
        a = MonsterList()
        dat = []
        row_colors = []
        for i,monsters in enumerate(a.dat):
            if i+1 >= st:
                line = [f"{i+1}F"]
                for j in range(9):
                    if j < len(monsters):
                        line.append(monsters[j])
                    else:
                        line.append('')
                dat.append(line)
                if i+1 in (29,30,47,48,49,56,57,58,66,67,68,77,78,93,94,95,96,97,98,99): # ドラゴン、戦車、ラビ
                    row_colors.append([i-st+1, '#000000', '#ff88ff'])
                elif i+1 in (3,4,5,36,37,38,61,62,72,73): # 草稼ぎ、復活稼ぎ
                    row_colors.append([i-st+1, '#000000', '#aaffaa'])
                elif i+1 in (6,7,22,23,44,45,85,86,87,88): # にぎり
                    row_colors.append([i-st+1, '#000000', '#aaaaff'])
                elif i+1 in (10,25,50,75): # 店
                    row_colors.append([i-st+1, '#000000', '#ffffaa'])
                elif i+1 in (8,9,31,32,33,50,51,70,71): # マゼルン
                    row_colors.append([i-st+1, '#000000', '#aaffff'])
                elif i+1 in (14,): # デビル稼ぎ
                    row_colors.append([i-st+1, '#000000', '#ffaaff'])
                else:
                    if i % 2 == 0:
                        row_colors.append([i-st+1, '#000000', '#FFFFFF'])
                    else:
                        row_colors.append([i-st+1, '#000000', '#bbbbbb'])

        self.window['table_monster'].update(dat, row_colors=row_colors)

    def write_stat_xml(self):
        cnt,total = self.itemlist.get_stat()

        with codecs.open('stat.xml', 'w', 'utf-8') as w:
            w.write('<?xml version="1.0" encoding="utf-8"?>\n')
            w.write('<Items>\n')
            #for i,name in enumerate(['kusa', 'makimono', 'udewa', 'tubo', 'tue', 'kusa1','kusa3', 'kusa5']):
            for i,name in enumerate(['kusa', 'makimono', 'udewa', 'tubo', 'okou', 'tue']):
                out = f"{cnt[i]}/{total[i]}"
                w.write(f"<{name}>{out}</{name}>\n")
            w.write('</Items>\n')

    def write_yin_xml(self, val):
        out_bukiin = ''
        out_tatein = ''
        out_bukiin_short = ''
        out_tatein_short = ''
        for k in bukiin.keys():
            if val[f'bin_{k}']:
                out_bukiin += f"{bukiin[k]}, "
                out_bukiin_short += f"{bukiin[k][:2]},"
        for k in tatein.keys():
            if val[f'tin_{k}']:
                out_tatein += f"{tatein[k]}, "
                out_tatein_short += f"{tatein[k][:2]},"

        with codecs.open('soubi.xml', 'w', 'utf-8') as w:
            w.write('<?xml version="1.0" encoding="utf-8"?>\n')
            w.write('<Items>\n')
            w.write(f'<bukiin>{out_bukiin}</bukiin>\n')
            w.write(f'<tatein>{out_tatein}</tatein>\n')
            w.write(f'<bukiin_short>{out_bukiin_short}</bukiin_short>\n')
            w.write(f'<tatein_short>{out_tatein_short}</tatein_short>\n')
            w.write('</Items>\n')

    def main(self):
        self.gui_main()
        while 1:
            ev, val = self.window.read()
            for v in val.keys():
                if 'tg_' in v:
                    print(f"val[{v}]:{val[v]}")
            print(f"ev={ev}")
            # アプリ終了時に実行
            if ev in (sg.WIN_CLOSED, '-WINDOW CLOSE ATTEMPTED-', 'btn_close', 'Escape:27'): # 終了処理
                self.settings.params['lx'] = self.window.current_location()[0]
                self.settings.params['ly'] = self.window.current_location()[1]
                self.settings.params['lw'] = self.window.current_size_accurate()[0]
                self.settings.params['lh'] = self.window.current_size_accurate()[1]
                self.window.close()
                self.itemlist.save(self.settings.params)
                self.settings.params['memo'] = val['memo']
                self.settings.params['memo_const'] = val['memo_const']
                ### 印の反映
                #for k in self.settings.params.keys():
                #    if ('bin_' in k) or ('tin_' in k):
                #        self.settings.params[k] = val[k]
                # ファイルに保存
                self.settings.save_settings()
                break
            elif ev == 'btn_get':
                if (not '武器' in val['tg_det']) and (not '盾' in val['tg_det']): 
                    mode = self.conv_tabname[val['tg_det']]
                    for i in val[f'table_{mode}']:
                        self.mode = mode
                        self.mod_target(self.mode, i, True)
                    self.update_table()
                    self.update_info('')
            elif ev == 'btn_lost':
                if (not '武器' in val['tg_det']) and (not '盾' in val['tg_det']): 
                    mode = self.conv_tabname[val['tg_det']]
                    for i in val[f'table_{mode}']:
                        self.mode = mode
                        self.mod_target(self.mode, i, False)
                    self.update_table()
                    self.update_info('')
            #elif (ev.startswith('bin_')) or (ev.startswith('tin_')):
            #    self.write_yin_xml(val)
            elif ev == 'floor':
                self.update_monster(int(val['floor']))
            elif ev == 'btn_reset':
                self.itemlist.reset()
                self.window['memo'].update('')
                pre_mode = self.mode
                self.update_table()
                self.mode = pre_mode
                for k in val.keys():
                    if ('bin_' in k) or ('tin_' in k):
                        self.window[k].update(False)
                val_false = val
                for k in val.keys():
                    val_false[k] = False
                #self.write_yin_xml(val_false)
                self.update_info('リセットしました。')

if __name__ == '__main__':
    a = GUI()
    a.main()