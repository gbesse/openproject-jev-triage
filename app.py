"""OpenProject work-package completeness review from signed webhooks."""
import base64
import json
import os
from pathlib import Path
from urllib.request import Request,urlopen
from jev_core import decide
from webhook import make_app,serve
POLICY=json.loads(Path(__file__).with_name("policy.json").read_text())

def process(event, *, evaluate=decide, comment=None):
    work=event.get("work_package") or event.get("workPackage") or {}
    if not isinstance(work.get("id"),int): return {"skipped":"not a work package"}
    description=work.get("description") or {}
    raw=description.get("raw","") if isinstance(description,dict) else str(description)
    text=(work.get("subject") or "")+"\n"+raw
    result=evaluate(text,POLICY,os.environ["TYPESAFE_API_KEY"])
    (comment or add_comment)(work["id"],result)
    return result

def add_comment(work_id,result):
    base=os.environ["OPENPROJECT_URL"].rstrip("/")
    token=os.environ["OPENPROJECT_API_TOKEN"]
    if not base.startswith("https://"): raise ValueError("HTTPS required")
    raw=f"Jev review: {result['outcome']} (p={result['probability']:.3f}; policy={result['policyVersion']}; input={result['inputSha256'][:12]}). Human review required before changing status."
    body={"comment":{"raw":raw}}
    auth=base64.b64encode(f"apikey:{token}".encode()).decode()
    req=Request(f"{base}/api/v3/work_packages/{work_id}/activities?notify=false",data=json.dumps(body).encode(),headers={"Authorization":"Basic "+auth,"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=15) as response: response.read()

if __name__=="__main__":
    serve(make_app(process,secret=os.environ["OPENPROJECT_WEBHOOK_SECRET"],header="HTTP_X_OP_SIGNATURE",scheme="sha1"))
