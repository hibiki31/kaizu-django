# kaizu-django-vue

### How to start

```
docker-compose build
docker-compose up -d 
docker-compose run kaizu-app python3 manage.py migrate
docker-compose run kaizu-app python3 manage.py collectstatic
```

### Tools

Create superuser

```
docker-compose exec kaizu-app bash
python3 manage.py createsuperuser
```

Migration database

```
docker-compose run kaizu-app python3 manage.py migrate
```


Backup database

```
docker-compose run kaizu-app python3 manage.py dumpdata > kaizu_`date --iso-8601=seconds`.backup.json
```

Develop command

```
docker-compose down && docker-compose build && docker-compose up -d
```