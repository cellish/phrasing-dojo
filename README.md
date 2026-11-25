# フレージング道場 / Phrasing Dojo

旋律の抑揚（フレージング）とアーティキュレーションを解釈する力を鍛えるブラウザ用ドリルです。クラシック・ジャズ・ロック・弦と歌の4つのタブを切り替えて使えます。

- **クラシック編**：フレーズの頂点を選ぶ「山はどこ？」と、3通りの抑揚を聴き比べる「聴き比べ」。10の原則を4つの種類に分けています。
  - フレーズの形：弓なり形と終止、跳躍と最高音、反復とゼクエンツ、フレーズの入れ子
  - 和声：倚音と解決、和声の緊張
  - 拍とリズム：弱起、反復音
  - 時間と音のつなぎ方：時間の取り方、スラーのまとまり
- **ジャズ編**：アクセントやゴーストノートを置く音を選ぶ「アクセントはどこ？」と「聴き比べ」。12の原則を3つの種類に分けています。
  - アクセント：裏拍のアクセント、線の頂点、先取り、ゴーストノート、短い終わり
  - リズムの種類：3連符、3つずつのフレーズ、ボサノヴァ、ラテン（クラーベ）、ダブルタイム
  - タイム感：ビートとの位置（レイドバック、オントップ、休符のあとの入り）、ハネの深さ
- **ロック編**：アクセントとミュートを置く音を選ぶ「アクセントはどこ？」と「聴き比べ」。8の原則を3つの種類に分けています。
  - アクセント：先取り（食い）、3＋3＋2、リフの刻み、16分のグルーヴ
  - タイミング：キメ、ノリの位置、シャッフル
  - 構成：セクションの盛り上がり

- **弦・歌**：チェロの物理モデルで、伸ばしている音の中の抑揚や音程の動かし方を聴き比べます（すべて「聴き比べ」）。9の原則を3つの種類に分けています。
  - 音の形と流れ：長い音の歌わせ方、音の終わり方、次の音への受け渡し、息継ぎと弓の返し
  - 音程の表現：表現的な音程（導音）、ポルタメント、ビブラートの配分
  - 様式による違い：バロックの長い音（メッサ・ディ・ヴォーチェ）、ジャズのバラード

「全部」を選ぶと、そのスタイルの課題を両方の形式で通して練習できます。

音は楽器の録音（サンプル）を使い（チェロだけは物理モデルでブラウザ内で計算）、ジャズ編・ロック編ではリズム隊を重ねられます。右上の「設定」から、言語（日本語・英語）、テーマ（自動・ライト・ダーク）、再生テンポ（70〜120%）、音色（ジャンル別・ピアノ・エレピ）、クラシックの旋律（ピアノ・チェロ）を切り替えられます。成績は原則ごとにブラウザに保存され、原則一覧に表示されます。パソコンではキー操作（1・2・3で聴く、A・B・Cで選ぶ、← → で前後へ など）も使えます。

## 著作権・ライセンス

ライセンスは [`LICENSE`](LICENSE)、同梱している他者の著作物(楽器の録音・物理モデル・書体)は [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) を参照してください。

## ファイル構成

- `index.html`：ページ本体
- `LICENSE`：著作権とこのアプリの利用条件
- `THIRD_PARTY_NOTICES.md`、`licenses/`：同梱している他者の著作物の一覧とライセンス文
- `samples/`：楽器の録音（楽器ごとのフォルダ）。選んだスタイルで使う楽器だけを読み込みます。
- `tools/pages.py`：音源を埋め込んだ1ファイル版と、この構成とを相互に変換するスクリプト
- `tools/test.py`：全課題を日英両方で通して動かし、エラーや翻訳漏れ、スマホ幅のはみ出しを調べるテスト
- `tools/add_cello.py`：予備のチェロの録音を取り込み、ループ位置と音量をそろえて登録するスクリプト
- `tools/faust/`：チェロの物理モデルの Faust ソース（`cello.dsp`）と、WebAssembly への変換手順

## English

A browser drill for interpreting melodic phrasing and articulation in four tabs. The classical edition (10 principles) asks you to find the peak of a phrase and compare three shaped versions. The jazz edition (12 principles) asks you to mark accents and ghost notes and compare articulations, triplets, bossa nova, Latin clave, double time and time feel. The rock edition (8 principles) covers anticipations, 3+3+2 groupings, riffs, 16th-note grooves, kicks, time feel, shuffle and section dynamics. The strings & voice tab (9 principles) uses a physically modeled cello to compare shaping inside held notes, note endings, breaths and bow changes, expressive intonation, portamento, vibrato, Baroque messa di voce and jazz-ballad phrasing.

Sounds are recorded instrument samples (the cello is a physical model computed in the browser); percussion is synthesized in the browser. Credits and licenses are in `THIRD_PARTY_NOTICES.md`.

The interface switches between Japanese and English and follows the browser language by default.

See `LICENSE` for the license and `THIRD_PARTY_NOTICES.md` for third-party works.
