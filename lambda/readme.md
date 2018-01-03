# lambdaでの外部ライブラリの利用方法

基本的にはルートディレクトリにライブラリをおけば問題ない。
ただし、psycopg2に限ってはAWS側がLambda実行環境にlibpqを共有ライブラリとして提供してくれていないため、手元でソースをコンパイルする。

参考:
https://dev.classmethod.jp/cloud/aws/build-psycopg2-for-aws-lambda-python/
# 手順
1. AWS Lambdaと同じAMIでEC2インスタンスを作成,起動
2. PostgreSQLをインストール
3. Python3を導入
4. pscycopg2のソースを取得しビルド
	この時、Python3でsetup.pyを実行すること
5. 動作確認

# 3.Python3の導入について
$ sudo yum install python36
$ sudo yum install python36-devel
$ LD_LIBRARY_PATH=$PG_DIR/lib:$LD_LIBRARY_PATH python36 setup.py build


# 5. 動作確認
ビルドしたオブジェクトはこちら
build/lib.linux-x86_64-3.6/psycopg2/
フォルダ名の"3.6"はPythonのバージョンによって異なるようです。

