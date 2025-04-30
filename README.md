#  Titanic Data with Flask + MySQL + Docker

Development in Python 

Build different container for different function
-  `MySQL`：save Titanic info
-  `db_init`：init database and import titanic csv
-  `Flask`：provide info in the web

---

## Project Structure

```
Docker_titanic/
├── flask_app/              # Flask web API
│   ├── flask_app.py
│   ├── view_data.py
│   ├── Dockerfile
│   └── requirements.txt

├── db_mysql/               # create database
│   ├── connect_database.py
│   ├── set_database.py
│   ├── import_data.py
│   ├── Dockerfile
│   └── requirements.txt
├── titanic_file/           # CSV file from kaggle
│   ├── train.csv
│   ├── test.csv
│   └── gender_submission.csv
├── docker-compose.yml
├── .env
├── .env.example
└── README.md
```

---

## Quick Start 

### 1️. Buind `.env` 

```
MYSQL_HOST=mysql_titanic
MYSQL_USER=root
MYSQL_PASSWORD=P@ssw0rd
MYSQL_DB=titanic
```

### 2. Build Docker container

```bash
docker-compose up --build
```
Auto start database and import CSV and sopen the web `http://localhost:10108`

---

## Web

website:
```
http://localhost:10108
```
you can see the top 20 in the site

---

## Development Description

| Service | Class| container |
|------|------|----------|
| MySQL database | connect_database | `container_mysql_titanic` |
| create table + import csv| set_database <br> import_data | `container_db_init` |
| Flask Web_API |flask_app| `container_flask` |

---

## System Reques

- Docker 20+
- docker-compose 1.27+
- Python 3.11




