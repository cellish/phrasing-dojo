# チェロの物理モデル / Cello physical model

`cello.dsp` は、Faust の physmodels.lib（violinModel の部品）をチェロの音域で鳴らすための Faust ソースです。`index.html` の `BOW_WASM` は、これを Faust コンパイラ（[faustwasm](https://github.com/grame-cncm/faustwasm) の libfaust-wasm）で WebAssembly に変換し、base64 にしたものです。

- 変換：`createDSPFactory('cello', code, '-ftz 2', true)` で得た `.wasm` を base64 に、JSON から `size` と各パラメータの `index` を `BOW_META` に写します。
- パラメータ：`freq`（Hz）、`pressure`、`velocity`、`position`、`noise`（弓の速さの揺らぎ）。
- 出力：0 番が胴の響きなしの弦、1 番が `pm.violinBody` つき。アプリは 0 番を使い、ブラウザ側で合成した胴のインパルス応答と開放弦の共鳴を加えています。

physmodels.lib は LGPL 2.1 以降ですが、Faust コンパイラが生成したコードは例外として自由なライセンスで配れます（`licenses/Faust-physmodels-LICENSE.txt`）。

`cello.dsp` drives Faust's physmodels.lib (the violinModel parts) in the cello range. `BOW_WASM` in `index.html` is this file compiled to WebAssembly with libfaust-wasm from faustwasm and encoded as base64. The app uses output 0 (string without body) and adds its own synthesized body impulse response and open-string resonance.
