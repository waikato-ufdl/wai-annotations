# wai.annotations 0.7.5

## Build

```bash
docker build -t wai.annotations:0.7.5 .
```

## Local

### Deploy

* Log into https://aml-repo.cms.waikato.ac.nz

  ```bash
  docker login -u waikatoufdl --password-stdin public-push.aml-repo.cms.waikato.ac.nz:443
  ```

* Execute commands

  ```bash
  docker tag \
      wai.annotations:0.7.5 \
      public-push.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:0.7.5
      
  docker public-push.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:0.7.5
  ```

### Use

```bash
docker run -u $(id -u):$(id -g) \
    -v /local/dir:/workspace
    -it public.aml-repo.cms.waikato.ac.nz:443/waikatoufdl/wai.annotations:0.7.5
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
      wai.annotations:0.7.5 \
      waikatoufdl/wai.annotations:0.7.5
  
  docker push waikatoufdl/wai.annotations:0.7.5
  ```

### Use

```bash
docker run -u $(id -u):$(id -g) \
    -v /local/dir:/workspace
    -it waikatoufdl/wai.annotations:0.7.5
```

**NB:** Replace `/local/dir` with a local directory that you want to map inside the container. 
For the current directory, simply use `pwd`.