# TradeAPI

### Docker run
```bash
# build
USER_ID=$UID docker-compose up -d

# trade_api
docker exec -it trade_api bash

# mysql
docker exec -it mysql bash
```
#
### MySQL setting
```bash
# mysql login
mysql -u root -p
> root

# create database
> create database test1 default character set utf8mb4;

# create table
> create table users
(
    id              int                                   auto_increment            primary key,
    status          enum ('active', 'deleted', 'blocked') default 'active'          not null,
    email           varchar(255)                                                    null,
    api_key         varchar(2000)                                                   null,
    secret_key      varchar(2000)                                                   null,
    updated_at      datetime                              default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    created_at      datetime                              default CURRENT_TIMESTAMP not null
)engine=InnoDB default charset=utf8mb4;

# check database
> show databases;

# check table
> show tables;

# check schema
> desc users;

> exit;
```  
#
### Configuration (trade_api)
Enter your Binance API Key in `app/common/consts.py`
```bash
WEBHOOK_PASSPHRASE = "boraisfantastic"
JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/auth)"
API_KEY = "lpJnCbctrhqVaboaFD4fXmnu****************************************"
SECRET_KEY = "dkIEsoRbRzeLlvugfumuD*******************************************"
```
#
### trade module install
```bash
docker exec -it trade_api bash
python -m pip install -e .
```   
#
### Run API server
```bash
cd app/
sudo python server.py
```
#
### Connect API-docs
[http://0.0.0.0:80/docs](http://0.0.0.0:80/docs)
