# auction-workshop


## Start for back, while docker is not ready:

### before start:
```
pip install -r requirements.txt
```

### then:
```
redis-server
python -m celery -A back worker -l info
python -m manage.py
```

### Otherwise
```
docker compose up
```

## For front, soon:
