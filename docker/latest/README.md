# wai.annotations latest (based on code in repos)

## Build

```bash
docker build -t wai.annotations:latest .
```

## Local

### Deploy

* Log into https://aml-repo.cms.waikato.ac.nz with user that has write access

  ```bash
  docker login -u USER public-push.aml-repo.cms.waikato.ac.nz:443
  ```

* Execute commands

  ```bash
  docker tag \
      wai.annotations:latest \
      public-push.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:latest
      
  docker push public-push.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:latest
  ```

### Use

* Log into https://aml-repo.cms.waikato.ac.nz with public/public credentials for read access

  ```bash
  docker login -u public --password public public.aml-repo.cms.waikato.ac.nz:443
  ```

* Use image

  ```bash
  docker run -u $(id -u):$(id -g) \
      -v /local/dir:/workspace \
      -it public.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:latest
  ```

**NB:** Replace `/local/dir` with a local directory that you want to map inside the container. 
For the current directory, simply use `pwd`.


## Docker hub

### Deploy

* Log into docker hub as user `waikatoufdl`:

  ```bash
  docker login -u waikatoufdl --password-stdin
  ```

* Execute command:

  ```bash
  docker tag \
      wai.annotations:latest \
      waikatoufdl/wai.annotations:latest
  
  docker push waikatoufdl/wai.annotations:latest
  ```

### Use

```bash
docker run -u $(id -u):$(id -g) \
    -v /local/dir:/workspace \
    -it waikatoufdl/wai.annotations:latest
```

**NB:** Replace `/local/dir` with a local directory that you want to map inside the container. 
For the current directory, simply use `pwd`.
