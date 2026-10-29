#!/usr/bin/env python3
"""合成被测目标：草稿系统。命令驱动，观察输出即断言依据。

三个独立观察通道用于证据三角：
  get     —— 业务读取（重新读回）
  query   —— 直接查存储层的原始记录
  logs    —— 应用操作日志
"""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(BASE, "store.json")
LOG = os.path.join(BASE, "app.log")


def load():
    if not os.path.exists(STORE):
        json.dump({
            "build": "2026-10-29-a",
            "defect": {"rename_persist": False},
            "drafts": [
                {"id": "d-1", "owner": "member-1", "name": "OldDraft", "status": "draft"},
                {"id": "d-2", "owner": "member-1", "name": "KeepName", "status": "submitted"},
                {"id": "d-3", "owner": "member-2", "name": "OtherDraft", "status": "submitted"},
            ],
        }, open(STORE, "w"))
    return json.load(open(STORE))


def save(s):
    json.dump(s, open(STORE, "w"))


def logline(msg):
    with open(LOG, "a") as f:
        f.write(msg + "\n")


def session(path):
    return json.load(open(path))


def find(st, did):
    for d in st["drafts"]:
        if d["id"] == did:
            return d
    return None


def main():
    if len(sys.argv) < 2:
        print("commands: drafts|get|rename|export|query|logs|build"); sys.exit(2)
    cmd = sys.argv[1]
    args = {a.lstrip("-"): v for a, v in (x.split("=", 1) for x in sys.argv[2:] if "=" in x)}
    st = load()
    s = session(args["session"])

    if cmd == "build":
        print(st["build"])

    elif cmd == "drafts":
        for d in st["drafts"]:
            print(f"{d['id']} owner={d['owner']} name={d['name']} status={d['status']}")

    elif cmd == "get":
        d = find(st, args["id"])
        if not d:
            print("not found"); sys.exit(1)
        print(f"{d['id']} owner={d['owner']} name={d['name']} status={d['status']}")

    elif cmd == "query":
        d = find(st, args["id"])
        if not d:
            print("not found"); sys.exit(1)
        print("row=" + json.dumps(d, ensure_ascii=False, sort_keys=True))

    elif cmd == "logs":
        if os.path.exists(LOG):
            for line in open(LOG):
                if args.get("id", "") in line:
                    print(line.rstrip())

    elif cmd == "rename":
        d = find(st, args["id"])
        if not d:
            print("not found"); sys.exit(1)
        if d["owner"] != s["user"]:
            print("permission denied: not the owner", file=sys.stderr); sys.exit(3)
        if d["status"] == "archived":
            print("permission denied: draft is archived", file=sys.stderr); sys.exit(5)
        logline(f"rename {d['id']} by {s['user']} -> {args['name']} status={d['status']} result=ok")
        if d["status"] != "draft" and not st.get("defect", {}).get("rename_persist", True):
            # 已注入的缺陷：已提交/已归档之外的改名请求被受理，但值未变更
            print(f"renamed {d['id']} -> {args['name']}")
            sys.exit(0)
        d["name"] = args["name"]
        save(st)
        print(f"renamed {d['id']} -> {args['name']}")

    elif cmd == "export":
        if s.get("role") != "admin":
            print("permission denied: admin role required", file=sys.stderr); sys.exit(4)
        for d in st["drafts"]:
            print(f"exported {d['id']} {d['name']}")
    else:
        print("unknown command"); sys.exit(2)


main()
