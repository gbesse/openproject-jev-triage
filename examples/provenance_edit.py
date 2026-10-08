"""Show that a changed work-package text receives a different provenance hash offline."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jev_core import decide

policy = json.loads((Path(__file__).resolve().parents[1] / 'policy.json').read_text())

class Response:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, *args):
        answer = {'choice': 'ready', 'probabilities': {'ready': 0.96}}
        return json.dumps({'model': policy['model'], 'answers': {policy['question']: answer}}).encode()

def offline_open(request, timeout):
    assert request.full_url == 'https://api.typesafe.ai/v1/systemone'
    return Response()

first = decide('Add an export button with an owner.', policy, 'offline-fixture', opener=offline_open)
edited = decide('Add an export button with an owner and acceptance criteria.', policy, 'offline-fixture', opener=offline_open)
assert first['inputSha256'] != edited['inputSha256']
print(json.dumps({'synthetic': True, 'firstOutcome': first['outcome'], 'editedOutcome': edited['outcome'], 'sameInputHash': False}))
