# Copyright 2015 Kyriakos Toumbas
#
# Licensed under the MIT License, (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import requests
from .models import Entity, Generator, Test

API_BASE_URL = 'https://backend.cec.com.cy/{api}'
DEFAULT_TIMEOUT = 10


__all__ = ['Error', 'Response', 'BaseAPI', 'Entities', 'Generators','Tests', 'CEC']

class Error(Exception):
    pass


class Response(object):
    def __init__(self, body, status_code):
        self.raw = body
        self.body = json.loads(body)

        if status_code == requests.codes.ok or status_code==requests.codes.created:
            self.successful = True
        else:
            self.successful = False
        self.error = ''
        if isinstance(self.raw,dict):
            self.error = self.raw.get('detail','')

class BaseAPI(object):
    def __init__(self, username=None, password=None, timeout=DEFAULT_TIMEOUT, api_base_url=API_BASE_URL):
        self.username = username
        self.password = password
        self.timeout = timeout
        self.api_base_url = api_base_url

    def _request(self, method, api, **kwargs):
        if self.username:
            kwargs['auth'] = (self.username, self.password)

        response = method(self.api_base_url.format(api=api),
                          timeout=self.timeout,
                          **kwargs)

        response.raise_for_status()

        response = Response(response.text, response.status_code)
        if not response.successful:
            raise Error(response.error)

        return response

    def get(self, api, **kwargs):
        return self._request(requests.get, api, **kwargs)

    def post(self, api, data, **kwargs):
        kwargs.update(json=data)
        return self._request(requests.post, api, **kwargs)

    def put(self, api, data, **kwargs):
        kwargs.update(json=data)
        return self._request(requests.put, api, **kwargs)

    def delete(self, api, **kwargs):
        return self._request(requests.delete, api, **kwargs)

class API(BaseAPI):
    def test(self, error=None, **kwargs):
        if error:
            kwargs['error'] = error

        return self.get('test/', params=kwargs)


class Auth(BaseAPI):
    def test(self):
        return self.get('authtest/')


class Entities(BaseAPI):
    def list(self):
        response = self.get('entities/')
        result = list()
        for record in response.body:
            result.append(Entity(**record))
        return result
    def info(self, entity_id):
        return Entity(**self.get('entities/%s' % entity_id).body)
    def update(self, entity_id, name, extra=None):
        data = dict()
        data['cid'] = entity_id
        if extra:
            data['extra'] = extra
        data['name'] = name
        return self.put('entities/%s/' % entity_id, data)
    def update_cid(self, entity_id,new_entity_id):
        return self.put('entities/%s/' % entity_id, {'cid':new_entity_id})

class Generators(BaseAPI):
    def list(self):
        response = self.get('generators/')
        result = list()
        for record in response.body:
            result.append(Generator(**record))
        return result
    def info(self, generator_id):
        return Generator(**self.get('generators/%s' % generator_id).body)
class Tests(BaseAPI):
    def list(self):
        response = self.get('tests/')
        result = list()
        for record in response.body:
            result.append(Test(**record))
        return result
    def list_for_entity(self, entity_id):
        response = self.get('tests/', params={'entity__cid': entity_id})
        for record in response.body:
            result.append(Test(**record))
        return result
    def info(self, test_id):
        return Test(**self.get('tests/%s' % test_id).body)
    def generate(self,entity_id, generator_id, title=""):
        data = dict()
        data['entity'] = entity_id
        data['generator'] = generator_id
        data['title'] = title
        return  Test(**self.post('tests/', data).body)
    def update(self, test_id, was_finalized, answerws_given,marked_questions, notes, state):
        pass

    def update(self, channel, ts, text):
        self.post('chat.update',
                  data={'channel': channel, 'ts': ts, 'text': text})

    def delete(self, channel, ts):
        self.post('chat.delete', data={'channel': channel, 'ts': ts})

class CEC(object):

    def __init__(self, username,password,
                 timeout=DEFAULT_TIMEOUT, api_base_url=API_BASE_URL):
        if api_base_url:
            if api_base_url[-1] != "/":
                    api_base_url += "/"
            api_base_url = api_base_url + "{api}"
        self.entities = Entities(username=username, password=password, timeout=timeout, api_base_url=api_base_url)
        self.generators = Generators(username=username, password=password, timeout=timeout, api_base_url=api_base_url)
        self.tests = Tests(username=username, password=password, timeout=timeout, api_base_url=api_base_url)
