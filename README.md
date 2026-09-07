# すずドリル

2年生 文しょうだいの自動まるつけアプリ（PWA）。
公開URL: https://akipaje181.github.io/suzu-drill/

iPadのSafariで開き「ホーム画面に追加」で使います。ログイン不要・オフライン可。

## ファイル
- `index.html` アプリ本体（1-⑤〜1-⑦の問題データ込み）
- `sw.js` オフライン用キャッシュ
- `manifest.webmanifest` / `icon-*.png` ホーム画面用

## 更新のしかた
1. もとの `../文しょうだいアプリ.html`（claude.aiアーティファクト版）を直し、`index.html` に組み替える
   （`<head>` の追加、`<h1>` を「すずドリル」に、末尾にSW登録と「きろくを 書き出す」）
2. **`sw.js` の `VERSION` を上げる**（例: v1 → v2）。上げないと端末側が古いキャッシュを使い続けることがある
3. `git commit` → `git push origin main` で自動公開（数十秒〜数分）

記録は各端末の `localStorage`（キー `suzu.bunsho.v1`）にだけ保存されます。
