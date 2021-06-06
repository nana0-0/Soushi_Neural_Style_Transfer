# soushi_Neural_Style_Transfer
高校の課題研究の授業で作成しました。
既存のNeural Style TransferをWebで動かせるようにしました。

cloneして実行したい場合は、以下のコマンドを実行してください。
```
$ git clone https://github.com/nana0-0/soushi_Neural_Style_Transfer.git
$ cd soushi_Neural_Style_Transfer/
$ git submodule update --init
```

https://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat をダウンロードしてneural_styleフォルダの中に入れてください。
srcフォルダの中にOutputフォルダを作ってから実行してください。


pythonと仮想環境(poetry)
python 3.6.8をinstallして実行してください。
```
$ pip install poetry
$ poerty install
$ poetry shell
```
