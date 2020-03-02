# Card Generator (CLI)
Automatic generation of JSON codes for Microsoft Adaptive Cards
Adaptive Cards自動作成ツールのCLI版です。

Dependencies: Python 3, pandas, math, json

使い方:
1. input.csvにアンケートのデータを入力
2. コマンドプロンプト上で本ツールのディレクトリ上に移動し"python CardGeneratorCLI.py <title> <description>"を実行
title: アンケートのタイトル
description: アンケートの説明
3. 同ディレクトリ上にoutput.jsonが出力されていることを確認し、ファイル内の文字列をCognigyのノード内にコピー
4. Webchat ConfigurationでAdaptive Cardsのプラグインが追加されていることを確認したうえでWebchatを実行し、Adaptive Cardが適切に表示されているか確認

