# CLAUDE.md — フレージング道場

旋律の抑揚とアーティキュレーションを聴き分けるブラウザ用ドリル。素の HTML/CSS/JS で、ライブラリもビルドもない。中身の詳しい一覧は `docs/INVENTORY.md`。現状は `STATUS.md`、未完了の作業は `PLAN.md`。

## 決まり
- 利用者への返事と報告は日本語。UI の文言は必ず日本語と英語の両方を書く（`UI.ja`/`UI.en`、`PRS`/`PRS_EN`、`TEXT`/`TEXT_EN`、`DISTS`/`DISTS_EN`、課題の英語は `EN`）。
- **push は利用者が言ったときだけ。** コミットは日本語で書く（1行目に要約、本文に箇条書き）。
- コミットの作者は `cellish <9362763+cellish@users.noreply.github.com>` にする。
- 著作権は「All rights reserved」で、オープンソースのライセンスは付けない。音源などを加えたら `THIRD_PARTY_NOTICES.md`、`licenses/`、画面下のクレジット（`UI.*.credit`）をそろえて更新する。

## 構成
- `index.html`：アプリ全体。データ → i18n → 課題（`CLASSICAL`/`JAZZ`/`ROCK`/`STRINGS`）→ `prep` → 抑揚の生成 → 音 → 五線（自前の SVG）→ UI の順に並んでいる。
- `samples/<楽器>/<キー>.mp3`：楽器の録音。楽器ごとに、必要になったときだけ読み込む（`loadInst`、`instsFor`、`whenReady`）。
- チェロは Faust violinModel の物理モデル（`BOW_WASM`、`BOW_WORKLET`、`initBow`）。ソースと変換手順は `tools/faust/`。録音のチェロは予備。
- スタイルのコードは `c`（クラシック）、`j`（ジャズ）、`r`（ロック）、`s`（弦・歌）。`c` と `s` は `playCRaw`、`j` と `r` は `playJ` で鳴らす。

## 動かし方と確認
- `file://` で開くと音源を読み込めない。`python3 -m http.server` で開く。
- 変更したら `python3 tools/test.py` を通す（Playwright と Chromium を使う）。全課題を日英で通し、エラー、翻訳漏れ、スマホ幅のはみ出しを調べ、「all good」と出れば合格。
- 音量を調べるときは、OfflineAudioContext で書き出して ffmpeg の ebur128 で LUFS を測る。各タブはおよそ −25 LUFS にそろえている。
- 1ファイル版を作る、または戻すときは `python3 tools/pages.py embed OUT.html` / `split SINGLE.html`（リポジトリの直下で実行する）。

## 課題を足すとき
- 音は `[音名, 拍数, フラグ]` の形で書く。音名は `'F#4'` の形、休符は `'r'`、4分音符が1拍。
- フラグの意味はスタイルで違う。クラシックは `a` 倚音、`r` 解決音、`p` 弱起。ジャズとロックは `A` アクセント、`o` 軽いアクセント、`g` ゴースト、`s` 短く、`t`/`c` タイ、`T` 3連符。
- 誤答は `dist:[{t:'flat'},…]` の形で書き、`t` の名前は `versionC`、`jart`、`specS` の分岐に合わせる。原則を足したときは `GROUPS` にも入れる。
- 小節内の拍数が拍子と合っているかはコードで検査していないので、自分で確かめる。

## ドキュメント更新
- 作業の終わりに STATUS.md を上書き更新（50行以内、updated を更新）
- 完了した作業は PLAN.md から削除し、STATUS の「実装済み」に要約
- 外部素材を追加・削除したら THIRD_PARTY_NOTICES.md を更新
- OS・ブラウザ対応が変わったら STATUS の os: と対応状況を更新（未確認を「対応」と書かない）
- 詳細方針は道場シリーズ親フォルダの DOCS-POLICY.md を参照
