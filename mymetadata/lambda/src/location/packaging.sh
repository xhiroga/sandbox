rm ../../target/location/lambda.zip

zip -j ../../target/location/lambda.zip spent_time_importer.py
zip -j ../../target/location/lambda.zip ../common/postgres.py

mkdir ../../tmp
mkdir ../../tmp/location
cd ../../tmp/location
cp -r ../../wrk/psycopg2 .
cp -r ../../wrk/pandas/* .
pyenv exec pip install pytz -t .
pyenv exec pip install requests -t .
# 本当はpyenvの参照元から直接取りたいのだが、-jと-rのオプションの併用がよくわからない

zip -r ../../target/location/lambda.zip *
