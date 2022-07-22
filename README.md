# TradeAPI

### 1. Docker run
```bash
# build
USER_ID=$UID docker-compose up -d

# trade_api
docker exec -it trade_api bash
```
  
#
### 2. Configuration (trade_api)
Enter your Binance API Key in `app/common/consts.py`  
해당 파일이 포함되어 있지 않습니다. 개인정보이기 때문에 포함시키지 않았습니다.  
저 경로에 파일을 생성해서 아래 내용을 채워주세요.  
- WEBHOOK_PASSPHRASE : 트레이딩뷰 설정값
- JWT_SECRET : 임의의 설정값(맘대로)
- API_KEY : 발급받은 바이낸스 API KEY
- SECRET_KEY : 발급받은 바이낸스 API KEY의 SECRET KEY
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
### 3. trade module install
```bash
docker exec -it trade_api bash
python -m pip install -e .
```   
#
### 4. Run API server
```bash
cd app/
sudo python main.py
```
#
### 5. Connect API-docs
따로 테스트 해보고 싶다면 아래 주소로 접속해서 직접 쿼리!  
그게 아니라면 트레이딩 뷰 웹훅 응답에 의해서 자동매매 됩니다.  
[http://0.0.0.0:80/docs](http://0.0.0.0:80/docs)
#
### MySQL guide
database와 table은 서버 실행시 자동으로 만들어지게 해놔서 아래 명령어는 참고만..
```bash
# mysql
docker exec -it mysql bash
```

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
