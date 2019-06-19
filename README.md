# lakeman
put data for S3

# create pipline
```
aws cloudformation deploy --template-file ./ci.yml --stack-name lakeman-ci \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides GitHubOAuthToken=${GitHubOAuthToken}  GitHubSecret=${GitHubSecret} \
    --region ${REGION} --profile ${PROFILE}
```


# local test
```
python -m unittest discover -t src -s tests

pipenv lock -r | pip install -r /dev/stdin -t src/vendor/
sam local invoke GetStatusUpdate -e events/status_update.json --env-vars events/env.json -t template.yml --profile ${PROFILE} --region ${REGION}
```