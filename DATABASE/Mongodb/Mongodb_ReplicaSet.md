# Mongodb Replica Set

Mongodb에서 이벤트 스트림을 사용하기 위해서는 Replica set으로 구성해야만 한다.

## Mongo Replica Set

### 1. security.keFile 생성

key file 관련 몽고디비 문서: [https://www.mongodb.com/docs/manual/tutorial/enforce-keyfile-access-control-in-existing-replica-set/](https://www.mongodb.com/docs/manual/tutorial/enforce-keyfile-access-control-in-existing-replica-set/)

미생성시 다음과 같은 오류가 발생한다. 

![image](https://github.com/anjaekk/TIL/assets/74139727/53b0245f-93d3-4ef2-9414-6eebdd0ad45a)

생성을 위해 터미널에서 아래와 같이 입력한다. 

```python
touch mongodb.key
```

난수 생성

```python
openssl rand -base64 756 > <path-to-keyfile>
# openssl rand -base64 756 > mongodb.key
```

소유자에게만 읽기권한을 주기위해 권한 변경

```python
chmod 400 <path-to-keyfile>
# chmod 400 mongodb.key
```

### 2. docker-compose 파일 구성 후 컨테이너 올리기

docker-compose.yaml

```
mongodb-1:
		&mongodb
    image: mongo
    container_name: mongodb-1
    restart: unless-stopped
    ports:
      - 27017:27017
    volumes:
      - mongo-db1:/data/db
      - ./mongodb.key:/etc/mongodb.key 
    environment:
      - MONGO_INITDB_ROOT_USERNAME=root
      - MONGO_INITDB_ROOT_PASSWORD=1234 
      - MONGO_INITDB_DATABASE=dbname
    command: mongod --replSet replication --keyFile /etc/mongodb.key --port 27017
    networks:
      - mongo-net

  mongodb-2:
		<<: *mongodb
    container_name: mongodb-2
    ports:
      - 27018:27017
    volumes:
      - mongo-db2:/data/db
      - ./mongodb.key:/etc/mongodb.key 


  mongodb-3:
		<<: *mongodb
    container_name: mongodb-3
    ports:
      - 27019:27017
    volumes:
      - mongo-db3:/data/db
      - ./mongodb.key:/etc/mongodb.key 


volumes:
  mongo-db1:
    driver: local
  mongo-db2:
    driver: local
  mongo-db3:
    driver: local
```

### 3. mongodb replica set 초기화

- mongodb 인스턴스 접속

```python
docker exec -it mongodb-1 bash
```

- mongosh 접속(mongo version 6.0 이상 부터는 mongosh로 접속)

```python
mongosh -u root -p 1234
```

- replica set 초기화

```python
rs.initiate({
	 _id: "replication",
	 members: [
	   {_id: 0, host: "mongodb-1"},
	   {_id: 1, host: "mongodb-2"},
	   {_id: 2, host: "mongodb-3"}
	 ]
});
```

아래와 같이 나오면 성공

![image](https://github.com/anjaekk/TIL/assets/74139727/a5f2fd8f-f5cf-4d43-9df6-0ae3ca2310c9)

### 4. db connection string

db connection string은 아래와 같이 된다.
```
mongodb://root:1234@mongodb-1:27017,mongodb-2:27017,mongodb-3:27017/?replicaSet=replication
```
