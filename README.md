# String To LoRA Name

stringで指定したloraファイルを、LoRA Loaderの"lora_name"ソケットに差すノードです

LoRAファイルなどをtomlなどの設定データから読み込むために使用します

※便宜上どんなソケットにも挿さる使用なのでDiffusion Modelsなどリストから名称を選ぶタイプならあらゆるソケットで使用できるかもしれません

# PathCleaner

ダブルクォーテーションで囲まれているパスからそれらを除去したパスを生成します

※Windows標準の「パスをコピー」を使用してスムーズにパスを貼り付けるためのノード

# Sequential Directory Generator

動画を連続して生成しpngなどの連番で保存する場合、どんどん同じフォルダにデータが書き出されてしまいます。

これを避けるために生成毎に自動で新しいフォルダを作成します。

アウトプットは作成されたディレクトリのパスを返すだけです。パスが入力できる保存ノードのピンに接続してご利用下さい。

# Square BBox From Mask

マスクを入力すると、そのマスクを正方形に整形したbboxのデータを出力します

実際にクロップする場合は Crop (mtb) などに接続してください

# update

## 260/1/28

String to LoRA Name追加

## 26/01/08

Square BBox From Mask追加
