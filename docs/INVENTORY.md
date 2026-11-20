# フレージング道場 / Phrasing Dojo — 中身の一覧

書法コア（共通部品）を切り出すかを検討するための一覧。コードを読んで確かめたことだけを書き、推測には「（推測）」と付けた。
行番号は 2026-11-20 時点の `index.html`（コミット 09dbb38）のもの。

---

## 1. 概要

### アプリ名・目的
- 名前：フレージング道場 / Phrasing Dojo（旧名「抑揚ドリル」。localStorage のキー `yokuyo-style` に旧名が残る）
- 目的：旋律の抑揚（強弱・時間・音の長さ・音程の動き）とアーティキュレーションを、聴いて判断する力を鍛える。
- 主な機能
  - 4つのスタイル（タブ）：クラシック `c`、ジャズ `j`、ロック `r`、弦・歌 `s`
  - 形式は2つ。
    - 「山はどこ？」「アクセントはどこ？」：五線上の音を選ぶ。`answerPeak`、`answerAcc`
    - 「聴き比べ」：模範と誤答2つ、計3つの演奏から選ぶ。`answerCmp`
  - 原則（principle）ごとの絞り込み、種類（GROUPS）ごとのまとまり、「全部」で通し練習：`buildStatic`、`refreshList`
  - 答え合わせで強弱曲線、タイミング曲線、正誤の理由文を表示：`drawCurves`、`timingSeries`、`whyJ`、`hintFor`
  - リズム隊（ジャズ、ボサノヴァ、ラテン、ロック）：`playJ` の後半
  - 設定：言語（日英）、テーマ、再生テンポ（70〜120%）、音色、クラシックの旋律（ピアノ・チェロ）
  - 原則ごとの成績をブラウザに保存：`REC`、`rec`
  - キー操作：1・2・3、A・B・C、スペース、Enter、R、← →（`keydown` のハンドラ、2612行付近）
- 課題数：クラシック 20、ジャズ 25、ロック 16、弦・歌 18（計79）。画面の数は 123（`tools/test.py` が数える）

### 言語・フレームワーク・ビルド・公開
- 素の HTML、CSS、JavaScript を1ファイル（`index.html`、約2660行）に書いている。フレームワーク、ライブラリ、npm は使わない。
- ビルドはしない。音源を base64 で埋め込んだ1ファイル版と、Pages 用の分割版を `tools/pages.py` で相互に変換する。
- 公開は GitHub Pages（https://cellish.github.io/phrasing-dojo/）。`.github/` はないので、ブランチ直下からの配信と思われる（推測。Pages の設定は API で確かめられなかった）。
- チェロの物理モデルは Faust の DSP を libfaust-wasm で WebAssembly に変換し、base64 で `index.html` に埋め込んでいる（`tools/faust/README.md`）。変換はリポジトリの外で手作業で行った。

### ファイル構成
| ファイル | 役割 |
|---|---|
| `index.html` | アプリ全体（データ、文言、音、描画、UI） |
| `samples/<楽器>/<キー>.mp3` | 楽器の録音。合計 4.8MB。piano、epiano、cello、vibes、abass、ebass、nylon、odguitar、woodblock、agogo |
| `tools/pages.py` | 1ファイル版と Pages 版の変換（`split`、`embed`） |
| `tools/test.py` | Playwright で全課題を日英で通し、エラー、翻訳漏れ、スマホ幅のはみ出しを調べる |
| `tools/add_cello.py` | 予備のチェロ録音を取り込み、オンセット、ループ位置、音量をそろえて `SAMPLE_DATA` に登録する |
| `tools/faust/cello.dsp`、`README.md` | チェロの物理モデルのソースと変換手順 |
| `LICENSE`、`THIRD_PARTY_NOTICES.md`、`licenses/` | 著作権表示と他者の著作物 |

`index.html` の中の区切り（コメント `/* ===== */`）：
`data`（326行）→ `i18n`（387）→ 課題データ（695〜1214）→ `parsing`（1215）→ `classical dynamics`（1318）→ `jazz articulation`（1428）→ `audio`（1520）→ `recorded samples`（1623）→ `bowed cello`（1701）→ `staff`（2101）→ `state & UI`（2294）

---

## 2. 音楽データの表し方（最重要）

### 音高
- 課題データでは**音名の文字列**で持つ。`'C4'`、`'F#4'`、`'Bb4'`。休符は `'r'`。オクターブは科学的表記（C4 が中央ハ）。
- `parse(name)`（1217行）が次の形に展開する。
  ```js
  {name:'F#4', letter:'F', acc:1, oct:4, midi:66, step:3+7*4}
  // acc: -1/0/+1（♭/なし/♯）。step = 音名の番号(C=0..B=6) + 7*oct（五線上の位置）
  ```
- **異名同音は区別する**。`letter` と `step` が違うので、C♯4 と D♭4 は五線上の位置が違う。
- 重変化（𝄪、𝄫）は扱わない。正規表現は `/^([A-G])([#b]?)(\d)$/`。オクターブは1桁のみ。
- 再生と計算は `midi`（整数）で行う。周波数は `440*2^((midi-69)/12)`（平均律）。
- 弦・歌のチェロは、記譜より1オクターブ下（`n.midi-12`）で鳴らす（`playCRaw`）。表示はト音記号のままで、8va の記号はない。

### 音価・拍・小節
- 音価は**拍数の数値**（4分音符 = 1）。`.5`（8分）、`.25`（16分）、`1/3`（3連符）、`1.5`（付点4分）、`3`（付点2分）、`4`。
- 小節は配列の入れ子で持つ。`bars:[[音, 音, …], [音, …]]`。1音は `[音名, 拍数, フラグ]`。
- 拍子は `ts:[4,4]`（既定は 4/4）、弱起は `pickup`（拍数）、テンポは `bpm`。
- `prep(ph,style)`（1222行）が通しの位置を計算する。
  - `items`（休符を含む）と `notes`（音のみ）を作る。
  - 各音に `on`（曲頭からの拍）、`dur`、`bar`、`pos`（小節内の拍）、`flag`、`idx`、`afterRest` を付ける。
  - `ph.total` は全体の拍数。
- 小節内の拍数が拍子と合うかは**検査していない**。
- タイはフラグで表す。`t` が次の音へつなぐ音、`c` がつながれた後ろの音（同じ高さを書く）。
- 3連符はフラグ `T` と `dur:1/3` で表す。

### フラグ（音ごとの注釈）
音の3番目の要素は文字列で、スタイルによって意味が違う。

| スタイル | 文字 | 意味 |
|---|---|---|
| クラシック（694行のコメント） | `a`、`r`、`p` | 倚音、解決音、弱起 |
| ジャズ、ロック（`jart`、`jcat`、`answerAcc`） | `A` | アクセント |
| | `o` | 軽いアクセント（選んでも誤りにしない） |
| | `g` | ゴースト（ロックではミュート） |
| | `s` | 短く切る |
| | `t`、`c` | タイ |
| | `T` | 3連符 |

組み合わせて `'As'`、`'TA'`、`'At'` のように書く。

### 声部
- **旋律は1声だけ**。複数の旋律を持つ仕組みはない。
- 伴奏は和音データから作る（下記）。ジャズとロックでは、ベースとコンピングをコードネームからその場で組み立てる。

### 和音
スタイルによって持ち方が違う。

| スタイル | 持ち方 |
|---|---|
| クラシック、弦・歌 | `chords:[[開始拍, 拍数, 'ローマ数字', ['C3','G3','C4']], …]`。表示用のローマ数字の文字列と、実際に鳴らす音名の配列を**両方手で書く**。ローマ数字から構成音は計算しない。転回形の表記はなく、`'V⁷'` のように上付き文字で書く。 |
| ジャズ、ロック | `chords:[[開始拍, 拍数, 'Dm7'], …]`。コードネームだけ書き、`chordInfo(sym)`（1968行）で根音と音程の並びに変換する。 |

- `chordInfo` が扱える種類は `QUAL`（1967行）にあるものだけ：`maj7`、`m7`、`7`、`6`、`m7b5`、`''`、`m`、`5`。
- 9th、sus、dim、テンション、分数コードは**なし**。根音の♯・♭は扱える。
- 数字付き低音は**なし**。

### 調・転調
- `key:'C'`、`'Dm'`、`'Em'` などの文字列。使い道は、最初のローマ数字の前に `C: ` と表示することだけ（`drawStaff` の和音ラベル）。
- 調号は**描かない**。臨時記号を小節ごとに付ける（`drawStaff` の `accMem`）。
- 転調、調の判定、音階の計算は**なし**。

### データの例（短く）
```js
// クラシック（695行）
{id:'1-1',pr:1,ts:[4,4],bpm:92,pickup:0,
 bars:[[['C4',1],['D4',1],['E4',1],['F4',1]],[['G4',2],['A4',1],['G4',1]],[['F4',1],['E4',1],['D4',2]],[['C4',4]]],
 peak:5, alt:{4:'…'}, why:'…', dist:[{t:'flat'},{t:'end'}]}
// 倚音と解決、和音つき
 bars:[…,[['C5',2,'a'],['B4',2,'r']],…], chords:[[4,4,'V',['G2','D3','B3']],…]
// ジャズ（812行）：拍子は書かない（4/4 が既定）
{id:'J1-1',pr:1,bpm:132,chords:[[0,4,'Dm7'],[4,4,'G7']],
 bars:[[['F4',.5],['A4',.5,'A'],…],[…,['E4',1,'As'],['r',1]]], dist:[{t:'classical'},{t:'flat'}]}
```

---

## 3. 機能ごとの実装

### 楽譜表示
- ライブラリは使わず、**自前の SVG 描画**。`drawStaff(ph)`（2137行）。
  - 五線、ト音記号、拍子、小節線、終止線、符頭、符幹、旗、連桁、付点、加線、臨時記号、タイ、スラー、休符（8分、4分、2分、全）、和音ラベル、区間の括弧（`sections`、`subs`）を描く。
- **ト音記号のみ**。ヘ音記号、ハ音記号、複数段、大譜表は**なし**。
- 音部記号は Noto Music などのフォントの字形 U+1D11E で、`fitClef` が大きさを合わせる。臨時記号は `drawAcc` が線で描く。
- 横位置は音価に比例する（`24+15*dur`）。連桁のまとまりは `btype` と `gkey` で決める（4/4 は2拍ごと、それ以外は1拍ごと）。
- 五線の位置：`yOf(step)=BOT-(step-30)*GAP/2`（step 30 = E4 = 第1線）。
- 記号は `drawMarks`（アクセント、スタッカート、ゴーストの括弧）、強弱とタイミングの曲線は `drawCurves`。
- 音を選ぶ操作は、各音の `<g class="note" id="n{i}">` にある透明な `rect.hit` で受ける。

### MIDI入力
なし。

### 音の再生
- Web Audio API を直接使う。
  - `buildCtx`（1523行）：master → 中低域を削る EQ → 高域シェルフ → コンプレッサー。合成 IR のリバーブへ送る。
  - `stopAll`（1926行）が止め、`playTok` で読み込み待ちの再生を取り消す。
- 録音サンプル：`SAMPLE_DATA[楽器][キー]={m,o,p,g,a,ls,le,d?}`、`sampler()`（1673行）。
  - 近い高さの録音を `playbackRate` で移調する。ピアノとエレピは強弱2層をクロスフェードする。
  - 読み込みは楽器ごとに必要になったとき（`loadInst`、`instsFor`、`loadFor`、`whenReady`）。
- チェロは Faust violinModel の物理モデル。
  - WebAssembly を AudioWorklet で動かす：`BOW_WORKLET`、`FaustBow`、`initBow`、`ctrlAt`。
  - 楽譜を `{f,s,e,v,sh,bc,c,gl,vib}` の列にして worklet に送る。s と e はサンプル位置。
  - 胴の IR（`celloBodyIR`）と開放弦の共鳴（`openStrings`）を加える。
  - 物理モデルを使えないときは録音（`celloNote`）、それもなければピアノ。
- 合成音（予備）：`piano`、`pluck`（Karplus-Strong）、`guitar`、`vibes`。打楽器はすべて合成：`kick`、`snare`、`cymbal`、`brush`、`conga` ほか。
- 演奏の組み立て
  - クラシックと弦・歌は `playCRaw(ph,dyn,len,tm,env,pitch)`。時間の伸び縮みは `secC`。
  - ジャズとロックは `playJ(ph,art)`。スウィング比と前後のずれは `noteT`、`makeT`。
  - 入口は `play(ph,d)` と `playPlain(ph)`。`d` は誤答の種類 `{t:'flat'}` など。`null` なら模範。

### マイク入力・音高判定
なし。

### 音程・コード・調の計算
- 音名と MIDI の変換：`parse`。
- コードネームの根音と構成音：`chordInfo`、`QUAL`、`inRange`（ある音高以上で最も低い同じ音名）。
- ジャズのウォーキングベース：`playJ` の中で、構成音と次の根音への半音の経過音を作る。
- 音程の名前（3度、6度など）、調の判定、和声分析は**なし**。旋律の「最高音」「同じ高さの連続」を `midi` で比べる程度（`shape`、`jcat`）。

### 規則の判定と採点
- 規則で判定するのではなく、**課題データに正解を書いておき、それと照らし合わせる**。
  - 山：`ph.peak` と別解の `ph.alt`（`answerPeak`）
  - アクセント：音のフラグ（`answerAcc`）
  - 聴き比べ：`S.order` の中の模範（`answerCmp`）
- 誤答の理由文は、規則で選ぶか（`hintFor`、`whyJ`、`jcat`）、課題ごとの文（`why`、`alt`、`dist[].why`、`hints`）を使う。
- 抑揚は規則で作る（演奏の生成で、正誤の判定ではない）。
  - クラシックの強弱は `shape`（頂点へ向かう弧、強拍、同じ音の連続、倚音と解決、弱起）、`archSegs`、`versionC`。
  - 音の中の形は `envC`、時間は `tmC`、`secC`。
  - ジャズとロックの強弱、長さ、スウィング比、ずれは `jart`。
  - 弦・歌の音程の動きは `specS`。
- 得点はセッション内の `S.score` と、保存する `REC`（原則・形式ごとの［正解数, 回答数］）。

### 課題・問題データ
- すべて `index.html` の中の JS リテラル。
  - `CLASSICAL`（695行）、`JAZZ`（812）、`ROCK`（948）、`STRINGS`（1105）
  - 誤答の定義：`DISTS`、`DISTS_EN`
  - 原則の名前と説明：`PRS`、`PRS_EN`
  - 原則の種類：`GROUPS`
  - 英語の課題文：`EN`（`EN[id].why`、`alt`、`dw`、`hints`）
- 課題ごとの主な属性。
  - 共通：`id`、`pr`、`bpm`、`ts`、`pickup`、`key`、`bars`、`chords`、`peak`、`alt`、`why`、`dist`、`hints`、`sub`、`cmpOnly`
  - クラシック：`segs`、`slurs`、`subs`、`timing`
  - ジャズとロック：`feel`（`bossa`、`latin`）、`clave`、`shuffle`、`sixteen`、`dt`、`laid`、`laidAll`、`timeFeel`、`chartRef`、`sec`、`sections`、`kimeFrom`、`brush`、`forceRhythm`、`swing`
  - 弦・歌：`lead`、`slide`、`vib`、`breath`、`badBreath`、`ending`、`pass`、`baroque`、`ballad`、`scoop`
- 外部ファイルからの読み込みは**なし**。

### ファイルの読み込み・書き出し
なし（MusicXML、MIDI ファイルの入出力はない）。

### 言語切替
- `LANG`（`'ja'` か `'en'`）。保存がなければブラウザの言語から決める（2647行付近）。
- 文言は次の対に分かれている。
  - `UI.ja` と `UI.en`
  - `PRS` と `PRS_EN`
  - `TEXT` と `TEXT_EN`
  - `DISTS` と `DISTS_EN`
  - 日本語の課題文は課題データに直接書き、英語は別表の `EN`
- 日本語のときは、文中の音名を「ミ（E4）」の形にする：`jn()`、`SOLF`。
- 切替時は `buildStatic()` と `load()` で画面を作り直す。

### 保存（localStorage）
| キー | 中身 |
|---|---|
| `phrasing-record` | 成績。`{"c:3:peak":[正解,回答], …}` の JSON |
| `yokuyo-style` | 最後に開いたスタイル（旧名のまま） |
| `phrasing-lang` | `ja` / `en` |
| `phrasing-theme` | `auto` / `light` / `dark` |
| `phrasing-timbre` | `genre` / `pianoS` / `epiano`（古い値 `piano` を `pianoS` に読み替える） |
| `phrasing-clead` | クラシックの旋律（`piano` / `cello`） |
| `phrasing-speed` | 再生テンポの倍率 |

### PWA・オフライン対応
なし（manifest も service worker もない）。音源を埋め込んだ1ファイル版（`tools/pages.py embed`）は、ネットにつながなくても動く（書体の読み込みを除く）。

### 著作権表示
- `LICENSE`（All rights reserved、日英）、`THIRD_PARTY_NOTICES.md`、`licenses/`、README の節
- 画面の一番下：楽器音のクレジット（`UI.*.credit`）と `© 2026 jun All rights reserved.`（315行）

---

## 4. 依存関係

### 外部ライブラリ
- JavaScript のライブラリは**なし**。
- 書体は Google Fonts から CDN で読み込む：Shippori Mincho、Zen Kaku Gothic New、Noto Music。Noto Music はト音記号の字形に使う。
- 生成コード：Faust physmodels.lib 1.2.14 を Faust コンパイラ（faustwasm の libfaust-wasm、版は未記録）で変換した WebAssembly。`BOW_WASM` に埋め込み。
- 音源：Salamander Grand Piano、jRhodes3、FluidR3_GM（MIDI.js Soundfonts 経由）、Karoryfer、Freesound flcellogrl。`samples/` に同梱。
- 開発用：Python 3、Playwright、ffmpeg、numpy（`tools/`）。

### 他のアプリからコピーしてきたコード
- コードのコメントや履歴には、他のアプリからコピーしたという記録は**ない**。
- 道場シリーズの共通点（`btn` の作り、テーマの3択、`HOST_THEME`、日英の `UI` 表、localStorage のつつみ方）は、同じ作り手による同じ書き方の可能性がある（推測）。

---

## 5. 共通化の候補

### 他の音楽アプリでも使えそうな部分
- **音名の解析**（`parse`）：音名、変化記号、オクターブから `midi` と `step` を作る。異名同音を区別する形なので、五線表示と再生の両方の土台になる。ただし重変化とヘ音記号は足す必要がある。
- **SVG の五線描画**（`drawStaff`、`drawAcc`、`fitClef`、`yOf`、`el`）
  - 依存がなく軽い。符頭ごとに `id` と当たり判定を持つので、音を選ぶ課題に向く。
  - 一方で、ト音記号1段、1声、調号なしに限られる。和声や対位法のアプリに使うには、音部記号、複数声部、大譜表を足す必要がある。
- **コードネームの解析**（`chordInfo`、`QUAL`、`inRange`）：根音と構成音の配列を返す小さな部品。種類が少ないので拡げる必要がある。
- **録音サンプルの読み込みと再生**（`SAMPLE_DATA` の形式、`loadInst`、`sampler`、`tools/pages.py`）
  - 楽器ごとの遅延読み込み、近い音からの移調、強弱2層、ループ、オンセット補正をまとめて持つ。
  - ピアノの音を使う他のアプリでもそのまま使える形。
- **チェロの物理モデル**（`BOW_WORKLET`、`initBow`、`celloBodyIR`、`openStrings`、`tools/faust/`）：楽譜から弓の速さ、音程、ビブラートを動かす。弦楽器で歌わせたい他のアプリ（ハモリ道場など）にも使える（推測）。
- **再生の土台**：`buildCtx` のマスター系、`stopAll`、`playTok`、`btn` の再生と停止の切り替え。
- **画面まわり**：日英の文言表（`UI`、`U()`）、テーマ切替（`applyTheme`）、localStorage のつつみ方、キー操作の方式。
- **テストの仕組み**（`tools/test.py`）：全画面を日英で通し、翻訳漏れとスマホ幅のはみ出しを調べる。

### 共通化しにくい部分
- **抑揚とアーティキュレーションの生成**（`shape`、`versionC`、`envC`、`specS`、`jart`、`noteT`）：この教材の「模範」と「誤答」を作るための調整値の塊で、スタイルごとの約束に強く結びついている。
- **フラグの文字列**：同じ `'a'`、`'A'`、`'s'` などがスタイルによって別の意味を持つ。他のアプリと形式をそろえるなら、まず意味ごとの属性に分ける必要がある。
- **和音の持ち方が2通り**ある。クラシックは「ローマ数字の文字列＋手書きの構成音」、ジャズは「コードネームのみ」。ローマ数字と数字付き低音の解析がないので、和声のアプリとはそのままでは合わない。
- **リズム隊の生成**（`playJ` の後半）：ジャンルごとのパターンを直接書いており、汎用の伴奏エンジンではない。
- **課題データと解説文**：課題ごとの文、誤答の文、英語の別表が密に結びついている。

---

## 6. 既知の問題

- **1ファイルが大きい**：`index.html` 約2660行に、データ、文言、音、描画、UI、WASM（base64）がすべて入っている。部品を切り出すには、まずファイルを分ける必要がある。
- **楽譜表示の制約**：ト音記号のみ、1段、調号なし。弦・歌のチェロは実音より1オクターブ上に書いているが、その記号（8va のト音記号など）はない。
- **小節の拍数を検査していない**（`prep`）。課題を書き間違えても気づけない。
- **フラグの判定がまちまち**：`flag==='p'` のような完全一致と、`flag.includes('A')` のような部分一致が混在している（`hintFor`、`shape`、`jart`）。
- **`jart` の中で `var secLv`** を `if` の中から関数の外へ漏らして使っている（`typeof secLv` で判定）。
- **localStorage のキー名がそろっていない**：`yokuyo-style` だけ旧名。
- **使われなくなった分岐が残っている**
  - `useS()` の `S.timbre!=='synth'`：合成音の選択肢は削除済み。
  - `melodyNote` などの合成音への分岐：録音がない1ファイル版以外では通らない（推測）。
- **マジックナンバーが多い**：音量、スウィング比、ずれ、IR の共鳴の値が、コードの中に直接書かれている。
- **物理モデルの再現手順が手作業**：WASM の変換はリポジトリの外で行っていて、ビルドスクリプトはない（`tools/faust/README.md` に手順のみ）。
- TODO、FIXME のコメントは**なし**（grep で確認）。

---

## 7. 作者のメモ

### 共通にしたい部分：

### このアプリに残したい部分：
