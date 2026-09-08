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

## テストの読み取り（AI）
- ホームの「テストを よみとる」：写真 → 名前を黒塗り → Claude で型・○✗を読み取り → 確認 → その子用の10まいページ。
- ブラウザから直接 Anthropic API を呼ぶ（`@anthropic-ai/sdk@0.124.0` を jsDelivr の ESM で読み込み、`dangerouslyAllowBrowser`）。
  APIキーは端末の `localStorage`（`suzu.apikey`）にだけ保存。サーバは無い。
- モデル `claude-opus-5`、画像は長辺2000pxのJPEG、`output_config.format` の JSONスキーマで構造化出力。
  安全分類器の拒否に備えて `fallbacks: "default"`（beta `server-side-fallback-2026-07-01`）を付け、400なら通常エンドポイントで再試行。
- 読み取り結果は「型・要約・数・正答・本人の答え・○✗・自信」。問題文の原文は保存しない（要約のみ）。
- 作ったページは `recs._pages`（seed付き）。プリント10まいは生成器から seed で再現。○✗は型別の記録に即反映。
- 費用の目安: 1枚 ¥15〜40（利用者のAPIアカウントに課金）。

## やる気の仕組み（ポイント・レベル・スタンプ・メダル・ドリまる）
- ポイント: 答えを入れた問題 +1、正解 +2（にがてモードは +3）、5/5で +5、講座の「ためしてみよう」正解 +2、テスト読み取り +10。
- レベル: 次のレベルに必要なポイントは `20 + 8×(Lv−1)`（Lv2=20、Lv10まで累計468）。
- ドリまる: レベルで たまご(1)→あかちゃん(3)→こども(6)→おとな(10)→マスター(15)。色6色、名前変更、アクセサリー6種（レベルやメダルで解放）。SVGで描画（`charSVG`）。
- スタンプカード: まるつけした日に1こ。30こで1枚。連続日数を表示。
- メダル: 16種（`BADGES`）。型マスター＝その型を5回以上解いて正答率8割。
- 状態は `recs._game`（xp, name, color, wear, stamps, badges, lessonsRead, wasWeak, sound, perfects, sets, weakSets, scans）。初回は過去の `_log` から換算。
- 音（レベルアップ・メダル時の短い和音）は「そだてる」画面でオン/オフ。

## 記録
各端末の `localStorage`（キー `suzu.bunsho.v1`）にだけ保存。
`_types`（型別の正誤）、`_log`（1回ごとの結果）、テストIDごとの `sheets`（プリント別ベスト）。
「きろく」画面の「きろくを 書き出す」でJSONを取り出せる。

## PDF書き出し（型を選んでプリントを作る）
ヘッドレスChromeで `index.html?gen=<単元id or keys:型,型,...>&n=<まい数>&seed=<数>&ans=1` を `--print-to-pdf` すると、
プリントだけのPDFになる（`ans=1` でこたえページ付き）。単元id: tashihiki / zu / narabi / nagasa / kasa / toki / kakezan / okane。
