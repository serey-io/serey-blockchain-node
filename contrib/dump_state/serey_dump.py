import json
import requests as req
from pprint import pprint
from pathlib import Path
import datetime as dt
import click

from graphene_rpc import GrapheneRPC


def dump(path, j):
    basepath = Path("serey_dump")
    basepath.mkdir(parents=True, exist_ok=True)
    with open(basepath / f"{path}.json", "w") as f:
        # Nicefy:
        #json.dump(j, f, indent=2)
        json.dump(j, f)


def parse_time(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")


def extract_amount(s: str):
    amount, symbol = s.split(" ")
    if symbol == "VESTS":
        precision = 6
    elif symbol in ["SRY", "SEREY"]:
        precision = 3
    return int(float(amount) * 10**precision)


# fmt: off
@click.command()
@click.option(
    "--min_cashout_time", type=str, required=True,
    help="Format: YYYY-MM-DDTHH:MM:SS")
@click.option(
    "--rpc_url", type=str,
    help="Format: http(s)://api.serey.io",
    default="http://localhost:8090/rpc")
# fmt: on
def main(min_cashout_time, rpc_url):
    min_cashout_time = parse_time(min_cashout_time)

    rpc = GrapheneRPC(rpc_url)

    ####################################################################################
    # ACCOUNTS
    ####################################################################################
    account_names = rpc.get_all_account_names()
    res = rpc.call("get_accounts", params=[account_names])
    account_objs = res.json()["result"]
    for i in account_objs:
        for k in [
            "vesting_balance",
            "balance",
            "savings_balance",
            "reward_steem_balance",
            "reward_vesting_balance",
            "reward_vesting_steem",
            "vesting_shares",
            "delegated_vesting_shares",
            "received_vesting_shares",
            "vesting_withdraw_rate",
        ]:
            i[k] = extract_amount(i[k])
    dump("accounts", account_objs)

    ####################################################################################
    # REWARD_FUND
    ####################################################################################
    res = rpc.call("get_reward_fund", params=["post"])
    reward_fund = res.json()["result"]
    reward_fund["reward_balance"] = extract_amount(reward_fund["reward_balance"])
    dump("reward_fund", reward_fund)

    ####################################################################################
    # Dynamic Properties
    ####################################################################################
    res = rpc.call("get_dynamic_global_properties", params=["post"])
    dynamic_global_properties = res.json()["result"]
    for k in [
        "current_supply",
        "confidential_supply",
        "total_vesting_fund_steem",
        "total_reward_fund_steem",
        "pending_rewarded_vesting_steem",
        "pending_rewarded_vesting_shares",
        "total_vesting_shares",
    ]:
        dynamic_global_properties[k] = extract_amount(dynamic_global_properties[k])
    dump("dynamic_global_properties", dynamic_global_properties)

    ####################################################################################
    # PENDING_CASHOUTS
    ####################################################################################
    discussion_objs = []
    discussions = []
    while True:
        params = {"tag": "", "limit": 100, "truncate_body": 1}
        if discussions:
            params["start_author"] = discussions[-1]["author"]
            params["start_permlink"] = discussions[-1]["permlink"]
        res = rpc.call("get_discussions_by_payout", params=[params])
        discussions = res.json()["result"]
        discussion_objs.extend(discussions)
        if len(discussions) < 100:
            break

    res = rpc.call("get_post_discussions_by_payout", params=[params])
    post_discussion_objs = res.json()["result"]

    res = rpc.call("get_comment_discussions_by_payout", params=[params])
    comment_discussion_objs = res.json()["result"]

    discussion_obj_ids = [d["id"] for d in discussion_objs]
    post_discussion_obj_ids = [d["id"] for d in post_discussion_objs]
    comment_discussion_obj_ids = [d["id"] for d in comment_discussion_objs]

    # fuse
    fused = {}
    fused.update({o["id"]: o for o in discussion_objs})
    fused.update({o["id"]: o for o in post_discussion_objs})
    fused.update({o["id"]: o for o in comment_discussion_objs})

    has_pending_cashout = lambda o: (parse_time(o["cashout_time"]) > min_cashout_time)
    dump("discussions", [o for o in fused.values() if has_pending_cashout(o)])


if __name__ == "__main__":
    main()
