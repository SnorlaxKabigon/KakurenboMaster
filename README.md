# かくれんぼマスター

画像の中から指定された数字を探し出すアプリです。

## 機能

- 画像のアップロード (PNG, JPG, JPEG)
- 探したい数字の入力 (3桁)
- 画像内の数字の検出と赤丸での強調表示

## セットアップ

このアプリを実行するには Python が必要です。

1. **Python のインストール**:
   Python がインストールされていない場合は、[python.org](https://www.python.org/) からインストールしてください。インストール時に "Add Python to PATH" にチェックを入れることを忘れないでください。

2. **依存関係のインストール**:
   ターミナルで以下のコマンドを実行して、必要なライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
   ※ `pip` コマンドが認識されない場合は `python -m pip install -r requirements.txt` を試してください。

3. **アプリの実行**:
   以下のコマンドでアプリを起動します。
   ```bash
   streamlit run app.py
   ```
   または、VS Code のタスク "Run Kakurenbo Master" を実行してください。

## 技術スタック

- Python
- Streamlit (Webフレームワーク)
- OpenCV (画像処理)
- EasyOCR (文字認識)
