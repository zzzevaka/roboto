# Roboto - a sandbox for ML research in finance

- running IPython notebooks in Django environment
- tools for collecting data from finam and oanda
- saving trained ML and DL models to database

## Starting:

touch app.env

app.env example:
```bash
ROBOTO_GLOBAL_DEBUG=1

ROBOTO_ROLLBAR_KEY=<rollbar key>
ROBOTO_ROLLBAR_ENV=development

ROBOTO_OANDA_TOKEN=<oanda token>
```

docker-compose up -d

