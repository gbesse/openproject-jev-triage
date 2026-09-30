import os
import unittest
from unittest.mock import patch
from app import process
class OpenProjectTests(unittest.TestCase):
    def test_comment(self):
        event={"work_package":{"id":12,"subject":"Fix it","description":{"raw":"No acceptance criteria"}}}
        calls=[]
        with patch.dict(os.environ,{"TYPESAFE_API_KEY":"test"}):
            process(event,evaluate=lambda text,policy,key:{"outcome":"incomplete"},comment=lambda *args:calls.append(args),already_reviewed=lambda *args:False)
        self.assertEqual(calls[0][0],12)
        self.assertEqual(calls[0][1]["outcome"],"incomplete")

    def test_replayed_work_package_skips_jev_and_comment(self):
        event={"work_package":{"id":12,"subject":"Fix it","description":{"raw":"No acceptance criteria"}}}
        with patch.dict(os.environ,{},clear=True):
            result=process(event,evaluate=lambda *_: self.fail("Jev must not run"),comment=lambda *_: self.fail("No duplicate comment"),already_reviewed=lambda work_id,digest,version: work_id==12 and len(digest)==64 and version=="0.1.0")
        self.assertEqual(result,{"skipped":"already reviewed"})

    def test_existing_comment_marker_is_detected(self):
        from app import review_exists
        digest="a"*64
        marker=f"jev-review:0.1.0:{digest}"
        requests=[]
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self,*args): return json.dumps({"_embedded":{"elements":[{"comment":{"raw":marker}}]},"count":1,"total":1}).encode()
        import json
        with patch.dict(os.environ,{"OPENPROJECT_URL":"https://op.example","OPENPROJECT_API_TOKEN":"secret"}),patch('app.urlopen',side_effect=lambda request,timeout:requests.append(request) or Response()):
            self.assertTrue(review_exists(8,digest,"0.1.0"))
        self.assertEqual(requests[0].get_method(),"GET")
        self.assertEqual(requests[0].full_url,"https://op.example/api/v3/work_packages/8/activities")

    def test_incomplete_activities_fail_closed(self):
        from app import review_exists
        import json
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self,*args): return json.dumps({"_embedded":{"elements":[]},"count":0,"total":1}).encode()
        with patch.dict(os.environ,{"OPENPROJECT_URL":"https://op.example","OPENPROJECT_API_TOKEN":"secret"}),patch('app.urlopen',return_value=Response()):
            with self.assertRaisesRegex(ValueError,"incomplete activities"):
                review_exists(8,"a"*64,"0.1.0")

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
        self.assertIn('jev-review:0.1.0:123456789012',json.loads(requests[0].data)['comment']['raw'])
        self.assertEqual(requests[0].get_method(),'POST')
        import base64
        self.assertEqual(requests[0].get_header('Authorization'),'Basic '+base64.b64encode(b'apikey:secret').decode())
