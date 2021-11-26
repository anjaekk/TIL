## Login
```
sudo docker login https://<DOMAIN NAME>:<PORT>
```
- Harbor 아이디와 비밀번호 입력 후 로그인

## Image Push

### Tag 지정
Harbor 레지스트리의 프로젝트로 푸시할 이미지에 사용하려는 네임스페이스와 동일한 이름으로 태그 지정
push를 원하는 프로젝트에 들어가서 `PUSH COMMAND`의 `Tag an image for this project:`를 사용해 지정하면 된다.
![](https://images.velog.io/images/anjaekk/post/70a416a5-2346-481e-b4af-a3bda5cf46a4/image.png)

```
docker tag SOURCE_IMAGE<:TAG> <DOMAIN NAME>:<PORT>/<PROJECT NAME>/REPOSITORY<:TAG>
```

### Push
```
docker push <DOMAIN NAME>:<PROT>/<PROJECT NAME>/REPOSITORY<:TAG>
```


## Image Pull
```
sudo docker pull [DOMAIN NAME]:[PORT]/[PROJECT NAME]/REPOSITORY[:TAG]
```
