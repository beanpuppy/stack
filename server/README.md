# Server

## Requirements

* Python >= v3.7
* PostgreSQL >= v13.x
* Redis >= v6.x

## Setup/Development

Install requirements:

```bash
pip install -r requirements_dev.txt
```

Add an `.env` file for API keys or database connection settings.

```
# See `config.py` for all variables

# Secret for JWTs. You must make your own one !!!
# For example, by using: `openssl rand -base64 32`
# This is DIFFERENT to the VITE_SECRET_KEY in /client
JWT_SECRET_KEY=<secret>

# Database variables
DB_USER=<user>
DB_PASSWORD=<password>
```

Run migrations:

```bash
rider migrate
```

Start the server:

```
python3 main.py
```

## Important Libraries

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
* [Estoult](https://estoult.readthedocs.io/en/latest/)
