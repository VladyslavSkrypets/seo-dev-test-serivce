# seo-dev-test-service


## How to start locally

1. Make sure, that you have a docker on your PC !
2. Create an `.env` file with the following content:

```dotenv
ENVIRONMENT=PROD
DATABASE_NAME=seo.dev.test.database
```

3. Run the following command:

```shell
some-dir$ docker compose --env-file .env -f docker-compose.yml up
```

4. Visit the url http://0.0.0.0/ to check if app was started (if `ENVIRONMENT=PROD`) otherwise check the http://127.0.0.1:5555/


