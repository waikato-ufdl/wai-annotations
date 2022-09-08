# wai.annotations 0.7.8

## Build

```bash
docker build -t wai.annotations:0.7.8 .
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
      wai.annotations:0.7.8 \
      public-push.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:0.7.8
      
  docker push public-push.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:0.7.8
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
      -it public.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:0.7.8
  ```

**NB:** Replace `/local/dir` with a local directory that you want to map inside the container. 
For the current directory, simply use `pwd`.


## Docker hub

### Deploy

* Log into docker hub as user `waikatoufdl`:

  ```bash
  docker login -u waikatoufdl
  ```

* Execute command:

  ```bash
  docker tag \
      wai.annotations:0.7.8 \
      waikatoufdl/wai.annotations:0.7.8
  
  docker push waikatoufdl/wai.annotations:0.7.8
  ```

### Use

```bash
docker run -u $(id -u):$(id -g) \
    -v /local/dir:/workspace \
    -it waikatoufdl/wai.annotations:0.7.8
```

**NB:** Replace `/local/dir` with a local directory that you want to map inside the container. 
For the current directory, simply use `pwd`.
