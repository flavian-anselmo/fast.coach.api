# Fast.Coach.API 📌
FastCoach is an attempt to build a  bus ticketing platform 

Old repo is [here](https://github.com/flavian-anselmo/fast-coach-api)



## Tools and Technology 👩‍💻
1. Backend 
    - FastApi
    - Python
    - PostgreSQL: storage 
    - Celery: used to create workers for the background tasks 
    - Flower: For monitoring background tasks 
    - RabbitMQ: A backend for the background tasks 

## Endpoints
### Users
![users](assets/users.png)
### auth
![auth](assets/auth.png)
### admin (Drivers, Buses & Routes)
![admin](assets/admin.png)
### Book a ticket 
![tickets](assets/ticket.png)
### payments (AfricasTalking API)
![pay](assets/pay.png)


# How to install and Run 🏃‍♂️

## install dependancies 
```bash 
pip install -r requirements.txt

```
## start the app
```bash
uvicorn app.main:app --reload 
 
```
## start the celery workers

```bash 
celery -A celery_worker.celery worker --loglevel=DEBUG 
```

# How to run it with Docker🏃‍♂️

```bash

``` 
# Read the Docs 
## locally 
- [localhost:8000/docs](https://localhost:8000/dcos)
## deployed
- [somelink]()