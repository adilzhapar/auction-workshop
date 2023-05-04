# auction-workshop
 - **DRF** 
 - **DRF-spectacular**
 -  **ViewSet** 
 - **Validation**
 -  **Celery**
 -  **Redis**
 - **JWT token**
 - **Docker-compose (redis, django, celery)**

## Basic set-up:

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

## Otherwise (simple way)
```
docker compose up --build
```
and go to http://localhost:1337


## Business logic of API:

1. The bulletin board in this case is a list of all ads, which is displayed on the main page of the service 
2. There is an authorized zone - personal account

    a. Registration is available (email and password must be specified)
    
    b. Authentication (login) to the personal account using the email and password specified during registration
    
    c. The email specified during registration is used to communicate with the user during transactions (have to make it async)
4. In the personal account, the user can create an ad and place it on the bulletin board in the general list
5. When creating an ad, you need to specify the name, description, minimum price and add images 
6. Ads have 2 statuses - ACTIVE, ON_SALE, SOLD
7. The user can select an ad in the general list and express the intention to buy the product by raising the price (placing a bid). The user who made the previous bet receives a notification that his bet was outbid. In the general list, both the minimum and the current price are indicated in the ad 
8. After the first customer has appeared, the countdown begins. After this time, the user who made the last bid becomes a buyer: the seller and the buyer receive notifications, and the ad is removed from publication, part of the money goes to charity. The time is set as a parameter


