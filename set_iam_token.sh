export IAM_TOKEN=$(curl -X POST -d "{\"yandexPassportOauthToken\":\"${YANDEX_TOKEN}\"}" https://iam.api.cloud.yandex.net/iam/v1/tokens | jq -r '.iamToken')