# すずドリル

2年生 文しょうだいの自動まるつけアプリ（PWA）。
公開URL: https://akipaje181.github.io/suzu-drill/

iPadのSafariで開き「ホーム画面に追加」で使います。ログイン不要・オフライン可。

## 画面
- ホーム → きょうの 5問（8単元・34型の生成器から毎回ちがう問題）／テストの プリント（1-⑤〜1-⑦ 各10まい）／にがてを とく／せんせいの ワンポイント（34講座）／きろく／いんさつ（型から作る・PDF）
- 各問題に手書きエリア：（しき）・こたえ の罫線＋（ひっさん・図）の方眼。ペン／けしゴム／太さ3段階。太さボタンは選択中の道具に効き、ペンとけしゴムで別々に記憶（localStorage: suzu.pen.size / suzu.eraser.size）。Apple Pencil＝書く／指＝スクロール（枠ごとの「指で かく」で指書きに切替）。Pencil使用中は手のひら・2本目の指を無視

## ファイル
- `index.html` アプリ本体（**これが元データ**。問題データ・講座文も中に入っている）
- `sw.js` オフライン用キャッシュ
- `manifest.webmanifest` / `icon-*.png` ホーム画面用
- `pdf/<テスト>/{problems,answers,points,all}.pdf` 印刷用PDF（`../文しょうだい再テスト/` と同じもの）

## 更新のしかた
1. `index.html` を直す（テストの固定問題は `var DATA`、型は `var TYPES`／`var UNITS`、講座は `var LESSONS`、生成器は `GEN.<型>`）
2. **`sw.js` の `VERSION` を上げる**（例: v2 → v3）。上げないと端末側が古いキャッシュを使い続けることがある
3. `git commit` → `git push origin main` で自動公開（数十秒〜数分）

## 記録
各端末の `localStorage`（キー `suzu.bunsho.v1`）にだけ保存。
`_types`（型別の正誤）、`_log`（1回ごとの結果）、テストIDごとの `sheets`（プリント別ベスト）。
「きろく」画面の「きろくを 書き出す」でJSONを取り出せる。

## PDF書き出し（型を選んでプリントを作る）
ヘッドレスChromeで `index.html?gen=<単元id or keys:型,型,...>&n=<まい数>&seed=<数>&ans=1` を `--print-to-pdf` すると、
プリントだけのPDFになる（`ans=1` でこたえページ付き）。単元id: tashihiki / zu / narabi / nagasa / kasa / toki / kakezan / okane。
