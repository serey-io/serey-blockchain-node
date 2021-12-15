import json
import requests as req
from pprint import pprint
from pathlib import Path

from graphene_rpc import GrapheneRPC


def dump(path, j):
    basepath = Path("serey_dump")
    with open(basepath / f"{path}.json", "w") as f:
        json.dump(j, f, indent=2)


def main():
    url = "http://localhost:8090/rpc"
    rpc = GrapheneRPC(url)

    ####################################################################################
    # ACCOUNTS
    ####################################################################################
    account_names = rpc.get_all_account_names()
    res = rpc.call("get_accounts", params=[account_names])
    account_objs = res.json()["result"]
    dump("accounts", account_objs)

    ####################################################################################
    # REWARD_FUND
    ####################################################################################
    res = rpc.call("get_reward_fund", params=["post"])
    reward_fund = res.json()["result"]
    dump("reward_fund", reward_fund)

    ####################################################################################
    # REWARD_FUND
    ####################################################################################
    params = {"tag": "", "limit": 1000000000000000000, "truncate_body": 1}

    res = rpc.call("get_discussions_by_payout", params=[params])
    discussion_objs = res.json()["result"]
    dump("discussion_by_payout", discussion_objs)

    res = rpc.call("get_post_discussions_by_payout", params=[params])
    post_discussion_objs = res.json()["result"]
    dump("post_discussion_by_payout", post_discussion_objs)

    res = rpc.call("get_comment_discussions_by_payout", params=[params])
    comment_discussion_objs = res.json()["result"]
    dump("comment_discussion_by_payout", comment_discussion_objs)

    discussion_obj_ids = [d["id"] for d in discussion_objs]
    post_discussion_obj_ids = [d["id"] for d in post_discussion_objs]
    comment_discussion_obj_ids = [d["id"] for d in comment_discussion_objs]

    # fuse
    fused = {}
    fused.update({o["id"]: o for o in discussion_objs})
    fused.update({o["id"]: o for o in post_discussion_objs})
    fused.update({o["id"]: o for o in comment_discussion_objs})
    dump("all_discussions", [v for v in fused.values()])


if __name__ == "__main__":
    main()
