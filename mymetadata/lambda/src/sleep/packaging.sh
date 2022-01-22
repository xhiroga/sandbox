rm ../../target/sleep/lambda.zip

mkdir ../../target/sleep
zip -j ../../target/sleep/lambda.zip sleep_time_importer.py
zip -j ../../target/sleep/lambda.zip ../common/postgres.py

mkdir ../../tmp
mkdir ../../tmp/sleep
cd ../../tmp/sleep
cp -r ../../wrk/psycopg2 .
pyenv exec pip install pytz -t .
pyenv exec pip install requests -t .
# 本当はpyenvの参照元から直接取りたいのだが、-jと-rのオプションの併用がよくわからない

zip -r ../../target/sleep/lambda.zip *
