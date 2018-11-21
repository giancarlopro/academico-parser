# Academico Parser
Webcrawler for [QAcadêmico](https://academico.iff.edu.br).

## Dependency

- `chromedriver`
- `Google Chrome`
- `requirements.txt`

## Heroku Buildpacks

- `heroku/python`
- [`chromedriver`](https://github.com/heroku/heroku-buildpack-chromedriver)
- [`Google Chrome`](https://github.com/heroku/heroku-buildpack-google-chrome)

## Build
```
pip install -r requirements.txt
heroku git:remote -a academico-parser
git push heroku master
```

## Steps - Parser
- [x] parses `Diario` data
- [x] stores users credentials
- [ ] parses `Boletim` data
- [ ] retrieve user data e.g.: (profile photo, name, email, personal data, etc...)

## Steps - Android App
- [ ] Create a login screen
- [ ] Encrypt user credentials using fingerprint
