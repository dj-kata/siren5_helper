# siren5_helperについて
風来のシレン5向けの識別支援ツールです。  
Windows(64bit)で動作します。

# 中身
- siren5_helper.exe: プログラム本体
- icon.ico: アイコン(一応入れている)
- stat.html: OBSへの識別情報表示用HTML
- soubi.html: OBSへの装備印情報表示用HTML

# できること
## 各アイテムの識別(値段識別、識別済みアイテムのメモ)
値段判別時に役に立つ機能を備えています。  
以下のようなリストビューで値段を参考にしつつ、  
識別済みのアイテムを記録していくことでより効率的にアイテムの候補を絞ることができます。
![image](https://user-images.githubusercontent.com/61326119/231684122-80278d92-83e9-482e-bbb2-3b7588b177d5.png)

## トライごとのメモの保存
以下のように、識別情報とは別にメモが必要な場合にテキストを書き込めるようになっています。  
救助パス作成時などにも役に立つかと思います。  
メモ欄は冒険用と全体用の2つを用意しており、前者はリセット(=乙)時に消えるようにしています。
![image](https://user-images.githubusercontent.com/61326119/231685390-6c4e1f03-7bfd-470e-a7c9-57ee5de8a082.png)

## 装備印、識別状況の情報をOBSへリアルタイムに反映
OBSを使った配信の補助用に、現在の装備についた印をチェックするとOBS側に反映してくれる仕組みも搭載しています。  
同梱のstat.html、soubi.htmlをOBSのブラウザソースで取り込むことで使えます。
![image](https://user-images.githubusercontent.com/61326119/231686063-afe06bc4-f502-4e59-b9ce-1cf1357e6287.png)
![image](https://user-images.githubusercontent.com/61326119/231687238-1e016ea8-482c-4497-bd99-928f1f606060.png)

## モンスターテーブルの表示
原始のモンスターテーブルを表示する機能も搭載しています。  
個人的にきついフロアは紫、何らかの草を稼げそうなフロアは緑、にぎり系がいるフロアは青、のような色付けをしています。
![image](https://user-images.githubusercontent.com/61326119/231711025-0346b46a-4446-4b91-80a0-3cf647fb80e1.png)

# 使い方
1. [Releaseページ](https://github.com/dj-kata/siren5_helper/releases)から最新のsiren5_helper.zipをダウンロードし、好きなフォルダに解凍する
2. 解凍したsiren5_helper内にあるsiren5_helper.exeを実行する
3. 乙った場合はリセットを押す

# 作者について
HN: かた
Twitter: @cold_planet_
