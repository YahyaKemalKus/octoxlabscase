## Instructions

For the fast start (It might take a while)
```sh
docker-compose --env-file .env.docker up -d --build
```
Then head to <a href="http://localhost:8001">here</a> for the swagger docs.<br>
OctoXLabs admin and OctoXLabs user accounts has already been created. See [here](./docker/docker-entrypoint.sh)


Use `/auth` endpoint to get OctoXLabs's special token with the data given in [here](./.env.docker):
```json
{
  "username": "<OCTOXLABS_SUPERUSER_NAME>",
  "password": "<OCTOXLABS_SUPERUSER_PASSWORD>"
}
```

Use `/auth` endpoint to get a jwt token with the following data:
```json
{
  "username": "<OCTOXLABS_USER_NAME>",
  "password": "<OCTOXLABS_USER_PASSWORD>"
}
```

Then pass the token you received(special one or jwt) to Swagger's Authorize panel. Now, you can safely use `/search` endpoint. <br><br>
Two hosts data has already been created in ElasticSearch. See [here](./docker/docker-entrypoint.sh) and [here](./docker/seedelastic.py)<br>
Use `/search` endpoint to query in ElasticSearch
- Example request body:
  ```json
  {
    "query": "Hostname = octoxlabs*"
  }
  ```

### Kibana
head to <a href="https://localhost:5601/app/home#/">here</a>, then pass the credentials given in [here](./.env.docker):
 - username: <ELASTIC_USERNAME>
 - password: <ELASTIC_PASSWORD>

### Management Commands
- Creating a OctoXLabs admin account:
  - `python manage.py createoctoxadmin -u <USERNAME> -p <PASSWORD> -e <EMAIL>`
- Creating a OctoXLabs user account:
  - `python manage.py createoctoxuser -u <USERNAME> -p <PASSWORD> -e <EMAIL>`
- Sending request to `/search` endpoint:
  - `python manage.py searchhosts -q <QUERY> -u <USERNAME> -p <PASSWORD>`
  - Examples:<br>
    The command below needs a locally running backend
    - ```sh
      python manage.py searchhosts -q "Hostname = octo*" -u octoAdmin -p 123456
      ```
    If you want to send a request to dockerized backend:
    - ```sh
      python manage.py searchhosts -q "Hostname = octo*" -u octoAdmin -p 123456 --port 8001
      ```

### Tests
- build and run
  ```shell
  docker compose --env-file .env.test -f "docker-compose-test.yml" up -d --build
  ```
- check lint errors
  ```shell
  docker-compose --env-file .env.test -f "docker-compose-test.yml" exec web ruff check .
  ```
- run tests
  ```shell
  docker-compose --env-file .env.test -f "docker-compose-test.yml" exec web python manage.py test
  ```
- shut down and remove containers
  ```shell
  docker-compose -f "docker-compose-test.yml" down
  ```