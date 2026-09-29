import os
import unittest
from unittest.mock import patch
from app import process
class OpenProjectTests(unittest.TestCase):
    def test_comment(self):
        event={"work_package":{"id":12,"subject":"Fix it","description":{"raw":"No acceptance criteria"}}}
        calls=[]
        with patch.dict(os.environ,{"TYPESAFE_API_KEY":"test"}):
            process(event,evaluate=lambda text,policy,key:{"outcome":"incomplete"},comment=lambda *args:calls.append(args))
        self.assertEqual(calls[0][0],12)
        self.assertEqual(calls[0][1]["outcome"],"incomplete")

    def test_comment_request(self):
        from app import add_comment
        import json
        requests=[]
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self): return b'{}'
        result={"outcome":"incomplete","probability":0.95,"policyVersion":"0.1.0","inputSha256":"123456789012"}
        with patch.dict(os.environ,{"OPENPROJECT_URL":"https://op.example","OPENPROJECT_API_TOKEN":"secret"}),patch('app.urlopen',side_effect=lambda request,timeout:requests.append(request) or Response()):
            add_comment(8,result)
        self.assertIn('/api/v3/work_packages/8/activities',requests[0].full_url)
        self.assertIn('Jev review',json.loads(requests[0].data)['comment']['raw'])
        self.assertEqual(requests[0].get_method(),'POST')
        import base64
        self.assertEqual(requests[0].get_header('Authorization'),'Basic '+base64.b64encode(b'apikey:secret').decode())
