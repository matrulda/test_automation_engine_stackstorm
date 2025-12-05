from st2reactor.sensor.base import PollingSensor
from datetime import datetime
import os
import requests


class RunfolderSensor(PollingSensor):

    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(RunfolderSensor, self).__init__(sensor_service=sensor_service,
                                              config=config,
                                              poll_interval=poll_interval)
        self._logger = self._sensor_service.get_logger(__name__)
        self._client = None
        self._hostconfigs = {}

    def setup(self):
        self._infolog("setup")

    def poll(self):
        self._infolog("poll")
        self._infolog("Checking for available runfolders")
        result = self.next_ready()
        self._infolog("Result from client: {0}".format(result))
        if result:
            self._handle_result(result)

    def next_ready(self):
        """
        Pulls the next runfolder that's ready.
        """
        host = "host.docker.internal"
        self._logger.info("Querying {0}".format(host))
        url = f"http://{host}:9991/api/1.0/runfolders/next"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                self._logger.error(
                    "RunfolderClient: Got status_code={0} from "
                    "endpoint {1}".format(resp.status_code, url)
                )
            else:
                json_resp = resp.json()
                self._logger.info(
                    "RunfolderClient: Successful call to {0}. {1}.".format(
                        url, json_resp
                    )
                )
                result = dict()
                result["response"] = json_resp
                result["requesturl"] = url
                return result
        except requests.exceptions.ConnectionError:
            self._logger.error(
                "RunfolderClient: Not able to connect to host {0}".format(host)
            )
        return None

    def cleanup(self):
        self._infolog("cleanup")

    def add_trigger(self, trigger):
        self._infolog("add_trigger")

    def update_trigger(self, trigger):
        self._infolog("update_trigger")

    def remove_trigger(self, trigger):
        self._infolog("remove_trigger")

    def _handle_result(self, result):
        self._infolog("_handle_result")
        runfolder_path = result['response']['path']
        runfolder_name = os.path.split(runfolder_path)[1]
        trigger = "test_packs.runfolder_ready"
        payload = {
            'host': result['response']['host'],
            'runfolder': runfolder_path,
            'runfolder_name': runfolder_name,
            'link': result['response']['link'],
            'timestamp': datetime.utcnow().isoformat(),
            'destination': ""
        }
        self._infolog(str(payload))
        self._sensor_service.dispatch(trigger=trigger, payload=payload, trace_tag=runfolder_name)

    def _infolog(self, msg):
        self._logger.info("[snpseq_packs." + self.__class__.__name__ + "] " + msg)
