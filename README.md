# Test automation engine: Stackstorm

The purpose of this repo is to serve as a test case template when testing new automation engines.

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

Trigger the test workflow manually by running:

```
st2 run test_packs.run_checkqc_workflow runfolder_name=200624_A00834_0183_BHMTFYTINY runfolder_path=<full path to>/test_automation_engine_stackstorm/test_data/200624_A00834_0183_BHMTFYTINY --async
```

If you make changes to test_packs, run:

```
st2ctl reload
```

### The Runfolder Sensor
Run the following to inspect the sensor log:
```
docker logs st2-docker-st2sensorcontainer-1
```

Remove `test_data/200624_A00834_0183_BHMTFYTINY/.arteria` to trigger the sensor to start a workflow.

### Troubleshooting
If you encounter issues when running docker/up. Try:

1. "Rebooting" your docker env (Note: this will remove all your pulled images):
```
docker rm -vf $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
docker volume rm $(docker volume ls -q)
```

2. Uncommenting line 130 in st2-docker/docker-compose.yml