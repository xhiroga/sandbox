rm -rf src/__pycache__
# zipで-rコマンドと-xコマンドの併用のしかたがよくわからない為の措置

zip -j ../../target/step/lambda.zip lambda_function.py
zip -j ../../target/step/lambda.zip add_step_count.py
zip -j ../../target/step/lambda.zip ../common/postgres.py

mkdir ../../tmp
mkdir ../../tmp/step
cd ../../tmp/step
cp -r ../../wrk/psycopg2 .
pyenv exec pip install pytz -t .
pyenv exec pip install requests -t .
# 本当はpyenvの参照元から直接取りたいのだが、-jと-rのオプションの併用がよくわからない

zip -r ../../target/step/lambda.zip *
