"""OpenProject work-package completeness review from signed webhooks."""
import base64
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request,urlopen
from jev_core import decide
from webhook import make_app,serve
POLICY=json.loads(Path(__file__).with_name("policy.json").read_text())

def process(event, *, evaluate=decide, comment=None, already_reviewed=None):
    work=event.get("work_package") or event.get("workPackage") or {}
    if not isinstance(work.get("id"),int): return {"skipped":"not a work package"}
    description=work.get("description") or {}
    raw=description.get("raw","") if isinstance(description,dict) else str(description)
    text=(work.get("subject") or "")+"\n"+raw
    digest=hashlib.sha256(text.encode()).hexdigest()
    if (already_reviewed or review_exists)(work["id"],digest,POLICY["version"]):
        return {"skipped":"already reviewed"}
    result=evaluate(text,POLICY,os.environ["TYPESAFE_API_KEY"])
    (comment or add_comment)(work["id"],result)
    return result

def api_settings():
    base=os.environ["OPENPROJECT_URL"].rstrip("/")
    if not base.startswith("https://"): raise ValueError("HTTPS required")
    token=os.environ["OPENPROJECT_API_TOKEN"]
    auth=base64.b64encode(f"apikey:{token}".encode()).decode()
    return base,"Basic "+auth

def review_exists(work_id,digest,policy_version):
    base,auth=api_settings()
    req=Request(f"{base}/api/v3/work_packages/{work_id}/activities",headers={"Authorization":auth,"Accept":"application/hal+json"})
    with urlopen(req,timeout=15) as response:
        data=json.load(response)
    if not isinstance(data,dict): raise ValueError("invalid activities response")
    elements=data.get("_embedded",{}).get("elements")
    count=data.get("count")
    total=data.get("total")
    if not isinstance(elements,list) or not isinstance(count,int) or not isinstance(total,int) or count != len(elements) or total != count:
        raise ValueError("incomplete activities response")
    marker=f"jev-review:{policy_version}:{digest}"
    return any(marker in (item.get("comment") or {}).get("raw","") for item in elements if isinstance(item,dict))

def add_comment(work_id,result):
    base,auth=api_settings()
    marker=f"jev-review:{result['policyVersion']}:{result['inputSha256']}"
    raw=f"Jev review: {result['outcome']} (p={result['probability']:.3f}; policy={result['policyVersion']}; input={result['inputSha256'][:12]}). Human review required before changing status. [{marker}]"
    body={"comment":{"raw":raw}}
    req=Request(f"{base}/api/v3/work_packages/{work_id}/activities?notify=false",data=json.dumps(body).encode(),headers={"Authorization":auth,"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=15) as response: response.read()

if __name__=="__main__":
    serve(make_app(process,secret=os.environ["OPENPROJECT_WEBHOOK_SECRET"],header="HTTP_X_OP_SIGNATURE",scheme="sha1"))
