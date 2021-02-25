import threading
import time
import uuid
import datetime
import queue
import requests
import json
from enum import Enum, unique

exit_flag = 0


@unique
class RequestType(Enum):
    PROFILE = "PROFILE"     # Get a specific profile by profile uuid
    PROFILES = "PROFILES"   # Get all profiles from a player by playername
    GETUUID = "GETUUID"     # Get players UUID from name
    TESTKEY = "TESTKEY"     # Get api key information
    NOOP = "NOOP"           # Do not call any api, but increment api_calls

    @classmethod
    def has_value(cls, value):
        return str(value) in cls._value2member_map_

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return f'{self.value}'


class SBAPIRequest():

    def __init__(self, type, params, uid=None):
        if uid is None:
            self.id = uuid.uuid4()
        else:
            self.id = uid
        self.type = type
        self.params = params
        if not self.check_type():
            raise ValueError()

    def check_type(self):
        return RequestType.has_value(self.type)

    def __str__(self):
        return f"SBAPIRequest<{self.id}, {self.type}, {self.params}>"


class APICall(threading.Thread):
    def __init__(self, id, output, urlcall):
        threading.Thread.__init__(self)
        self.output = output
        self.urlcall = urlcall
        self.id = id

    def run(self):
        print("API: Fetching " + self.urlcall)
        response = requests.get(self.urlcall)
        if response.status_code == 200:
            self.output[str(self.id)] = json.loads(response.text)
        else:
            self.output[str(self.id)] = {'dd_error': True, 'dd_no_200': True}


class SkyblockAPI(threading.Thread):
    def __init__(self, hypixel_api_key):
        threading.Thread.__init__(self)
        self.hypixel_api_key = hypixel_api_key
        self.input = queue.Queue()
        self.output = {}
        self.api_calls = 0
        self.api_reset_times = []
        self.shall_stop = False

    async def request(self, sb_api_request, timeout=5):
        start_time = time.time()
        self.input.put(sb_api_request)
        while True:
            if time.time() - start_time >= timeout:
                return {'dd_error': True, 'dd_timeout': True}
            if str(sb_api_request.id) in self.output:
                return self.output.pop(str(sb_api_request.id))

    def stop(self):
        self.shall_stop = True

    def _consume_item(self, item):
        if not isinstance(item, SBAPIRequest):
            raise ValueError("Consumed item is not of type API Request")
        if item.type == RequestType.GETUUID:
            callthread = APICall(
                item.id,
                self.output,
                "https://api.mojang.com/users/profiles/"
                + f"minecraft/{item.params[0]}")
            callthread.start()

        elif item.type == RequestType.NOOP:
            self.api_calls += 1
            self.api_reset_times.append(time.time() + 123)
            print(f"{datetime.datetime.now().isoformat()} - "
                  + "NOOP Call {item.id}")

        elif item.type == RequestType.PROFILES:
            self.api_calls += 1
            self.api_reset_times.append(time.time() + 123)
            callthread = APICall(
                item.id,
                self.output,
                "https://api.hypixel.net/skyblock/profiles?key="
                + f"{self.hypixel_api_key}&uuid={item.params[0]}"
            )
            callthread.start()

        elif item.type == RequestType.TESTKEY:
            self.api_calls += 1
            self.api_reset_times.append(time.time() + 123)
            callthread = APICall(
                item.id,
                self.output,
                f"https://api.hypixel.net/key?key={self.hypixel_api_key}"
            )
            callthread.start()

        elif item.type == RequestType.PROFILE:
            self.api_calls += 1
            self.api_reset_times.append(time.time() + 123)
            callthread = APICall(
                item.id,
                self.output,
                "https://api.hypixel.net/skyblock/profile?key="
                + f"{self.hypixel_api_key}&profile={item.params[0]}"
            )
            callthread.start()

    def run(self):
        while(True):
            if self.shall_stop and self.input.empty():
                break

            self.api_calls -= self.api_reset_times.count(time.time())

            while ((not self.input.empty()) and (self.api_calls < 120)):
                item = self.input.get()
                self._consume_item(item)

            pass

        time.sleep(3)  # Sleep to give time to clean up after this thread
