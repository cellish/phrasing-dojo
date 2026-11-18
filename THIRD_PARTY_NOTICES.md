# 他者の著作物の一覧 / Third-party notices

このアプリに同梱している、または読み込んでいる他者の著作物です。ライセンス文の原文は `licenses/` にあります。

## 同梱しているもの（`samples/` の楽器の録音）

録音は、元の音源から音を選んで切り出し、MP3 に変換して音量をそろえたものです（改変を含みます）。

| 名前 | 用途 | 権利者 | ライセンス | ライセンス文 |
|---|---|---|---|---|
| [Salamander Grand Piano](https://github.com/sfzinstruments/SalamanderGrandPiano) | ピアノ（`samples/piano/`） | Alexander Holm | CC BY 3.0 | `licenses/SalamanderGrandPiano-LICENSE.txt` |
| [jRhodes3](https://github.com/sfzinstruments/jlearman.jRhodes3d) | エレクトリックピアノ（`samples/epiano/`） | Jeff Learman | **CC BY-NC 4.0**（非営利のみ。営利での利用は作者の許可が必要） | `licenses/jRhodes3-LICENSE.txt` |
| [Real Cello Notes](https://freesound.org/people/flcellogrl/packs/12408/)（Freesound） | チェロ（`samples/cello/`） | flcellogrl | CC BY 3.0 | `licenses/Freesound-flcellogrl-cello-pack.txt` |
| [Karoryfer Samples](https://shop.karoryfer.com/pages/free-samples)：Sneakybass | ウッドベース（`samples/abass/`） | Karoryfer Samples | CC0 1.0 | `licenses/Karoryfer-Sneakybass-LICENSE.txt` |
| Karoryfer Samples のエレキベース（[tonejs-instruments](https://github.com/nbrosowsky/tonejs-instruments) 経由） | エレキベース（`samples/ebass/`） | Karoryfer Samples | CC0 1.0 | `licenses/Karoryfer-Sneakybass-LICENSE.txt`（同じ CC0 の文）、出典は `licenses/tonejs-instruments-sample-source-info.txt` |
| FluidR3_GM サウンドフォント（[MIDI.js Soundfonts](https://github.com/gleitz/midi-js-soundfonts) で変換したもの） | ヴィブラフォン、歪みギター、ナイロン弦ギター、ウッドブロック、アゴゴ（`samples/vibes/` ほか） | Frank Wen（音源）、Benjamin Gleitzman（変換） | 音源は CC BY 3.0、変換ツールは MIT | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)、`licenses/midi-js-soundfonts-LICENSE.txt` |

出典の表示は、ページの一番下と README にも載せています。

## 外部から読み込んでいるもの

| 名前 | 用途 | 権利者 | ライセンス |
|---|---|---|---|
| Shippori Mincho（Google Fonts） | 見出しの書体 | FONTDASU | SIL Open Font License 1.1 |
| Zen Kaku Gothic New（Google Fonts） | 本文の書体 | Yoshimichi Ohira | SIL Open Font License 1.1 |
| Noto Music（Google Fonts） | 楽譜記号の書体 | Google | SIL Open Font License 1.1 |

これらは Google Fonts から読み込んでいるだけで、アプリには同梱していません。アプリとして書体を同梱して配るときは、SIL Open Font License の文の同梱が必要です。

打楽器（ドラム、シェイカーなど）と予備の合成音は、ブラウザの中で計算して作っており、他者の素材は使っていません。ライブラリやフレームワークは使っていません。

## English

Bundled instrument recordings in `samples/` were cut from the sources above, converted to MP3 and level-matched. Piano: Salamander Grand Piano by Alexander Holm (CC BY 3.0). Electric piano: jRhodes3 by Jeff Learman (CC BY-NC 4.0, noncommercial use only; commercial use needs the author's permission). Cello: "Real Cello Notes" by flcellogrl on Freesound (CC BY 3.0). Upright and electric bass: Karoryfer Samples (CC0 1.0). Other instruments: the FluidR3_GM soundfont by Frank Wen (CC BY 3.0), converted by MIDI.js Soundfonts by Benjamin Gleitzman (MIT). Fonts (Shippori Mincho, Zen Kaku Gothic New, Noto Music) are loaded from Google Fonts under the SIL Open Font License 1.1 and are not bundled. Percussion and the fallback synthesized sounds are generated in the browser. License texts are in `licenses/`.
