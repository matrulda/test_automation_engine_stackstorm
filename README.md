# Test automation engine: Stackstorm

The purpose of this repo is to serve as a template when setting up similar functionality in other automation engines.

See DATAOPS-1144 for details.

## Prerequisites
- pyenv
- docker engine

## Preparation

Make sure the following services are running locally on your machine:
- arteria-runfolder: https://github.com/arteria-project/arteria (port 9991)
- checkqc: https://github.com/Molmed/checkQC (port 9992)

Example on how to achieve this:

In separate terminal windows, run:
```
pyenv install 3.13.10
pyenv virtualenv 3.13.10 checkqc
pyenv activate checkqc
pip install setuptools
pip install checkQC -r checkQC/requirements/prod
checkqc-ws --port 9992 --config checkqc_qc_config.yaml --log_config checkqc_logger.yaml test_data
```

```
pyenv install 3.12.7
pyenv virtualenv 3.12.7 arteria
pyenv activate arteria
pip install arteria
arteria-runfolder --config_file arteria_runfolder.yaml
```

## Start Stackstorm

```
docker/up
```

### Enter st2client to interact with Stackstorm

```
docker/st2client
```

### Investigate sensor log

```
docker logs st2-docker-st2sensorcontainer-1
```
