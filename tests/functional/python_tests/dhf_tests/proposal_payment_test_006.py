#!/usr/bin/python3

import sys
sys.path.append("../../")
import hive_utils

from uuid import uuid4
from time import sleep
import logging
import test_utils
import os
import datetime

return_code = 0

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)-15s - %(name)s - %(levelname)s - %(message)s"
MAIN_LOG_PATH = "hdf_proposal_payment_006.log"
log_dir = os.environ.get("TEST_LOG_DIR", None)
if log_dir is not None:
    MAIN_LOG_PATH = log_dir + "/" + MAIN_LOG_PATH
else:
    MAIN_LOG_PATH = "./" + MAIN_LOG_PATH


MODULE_NAME = "DHF-Tests"
logger = logging.getLogger(MODULE_NAME)
logger.setLevel(LOG_LEVEL)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(LOG_LEVEL)
ch.setFormatter(logging.Formatter(LOG_FORMAT))

fh = logging.FileHandler(MAIN_LOG_PATH)
fh.setLevel(LOG_LEVEL)
fh.setFormatter(logging.Formatter(LOG_FORMAT))

if not logger.hasHandlers():
  logger.addHandler(ch)
  logger.addHandler(fh)

try:
    from beem import Hive
except Exception as ex:
    logger.error("beem library is not installed.")
    sys.exit(1)

# Greedy baby scenario
# 0. In this scenario we have one proposal with huge daily pay and couple with low daily pay
#    all proposals have the same number of votes, greedy proposal is last
# 1. create few proposals - in this scenario proposals have different starting and ending dates
# 2. vote on them to show differences in asset distribution (depending on collected votes)
# 3. wait for proposal payment phase
# 4. verify (using account history and by checking regular account balance) that given accounts have been correctly paid.

# Expected result: all got paid.


if __name__ == '__main__':
    logger.info("Performing SPS tests")
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("creator", help = "Account to create test accounts with")
    parser.add_argument("treasury", help = "Treasury account")
    parser.add_argument("wif", help="Private key for creator account")
    parser.add_argument("--node-url", dest="node_url", default="http://127.0.0.1:8090", help="Url of working hive node")
    parser.add_argument("--run-hived", dest="hived_path", help = "Path to hived executable. Warning: using this option will erase contents of selected hived working directory.")
    parser.add_argument("--working-dir", dest="hived_working_dir", default="/tmp/hived-data/", help = "Path to hived working directory")
    parser.add_argument("--config-path", dest="hived_config_path", default="../../hive_utils/resources/config.ini.in",help = "Path to source config.ini file")
    parser.add_argument("--no-erase-proposal", action='store_false', dest = "no_erase_proposal", help = "Do not erase proposal created with this test")


    args = parser.parse_args()

    node = None

    if args.hived_path:
        logger.info("Running hived via {} in {} with config {}".format(args.hived_path, 
            args.hived_working_dir, 
            args.hived_config_path)
        )
        
        node = hive_utils.hive_node.HiveNodeInScreen(
            args.hived_path, 
            args.hived_working_dir, 
            args.hived_config_path
        )
    
    node_url = args.node_url
    wif = args.wif

    if len(wif) == 0:
        logger.error("Private-key is not set in config.ini")
        sys.exit(1)

    logger.info("Using node at: {}".format(node_url))
    logger.info("Using private-key: {}".format(wif))

    accounts = [
        # place accounts here in the format: {'name' : name, 'private_key' : private-key, 'public_key' : public-key}
        {"name" : "tester001", "private_key" : "5KQeu7SdzxT1DiUzv7jaqwkwv1V8Fi7N8NBZtHugWYXqVFH1AFa", "public_key" : "TST8VfiahQsfS1TLcnBfp4NNfdw67uWweYbbUXymbNiDXVDrzUs7J"},
        {"name" : "tester002", "private_key" : "5KgfcV9bgEen3v9mxkoGw6Rhuf2giDRZTHZjzwisjkrpF4FUh3N", "public_key" : "TST5gQPYm5bs9dRPHpqBy6dU32M8FcoKYFdF4YWEChUarc9FdYHzn"},
        {"name" : "tester003", "private_key" : "5Jz3fcrrgKMbL8ncpzTdQmdRVHdxMhi8qScoxSR3TnAFUcdyD5N", "public_key" : "TST57wy5bXyJ4Z337Bo6RbinR6NyTRJxzond5dmGsP4gZ51yN6Zom"},
        {"name" : "tester004", "private_key" : "5KcmobLVMSAVzETrZxfEGG73Zvi5SKTgJuZXtNgU3az2VK3Krye", "public_key" : "TST8dPte853xAuLMDV7PTVmiNMRwP6itMyvSmaht7J5tVczkDLa5K"},
    ]
    account_names = [ v['name'] for v in accounts ]

    if not accounts:
        logger.error("Accounts array is empty, please add accounts in a form {\"name\" : name, \"private_key\" : private_key, \"public_key\" : public_key}")
        sys.exit(1)

    keys = [wif]
    for account in accounts:
        keys.append(account["private_key"])
    
    if node is not None:
        node.run_hive_node(["--enable-stale-production"])
    try:
        if node is None or node.is_running():
            node_client = Hive(node = [node_url], no_broadcast = False, 
                keys = keys
            )

            # create accounts
            test_utils.create_accounts(node_client, args.creator, accounts)
            # tranfer to vesting
            test_utils.transfer_to_vesting(node_client, args.creator, accounts, "300.000", 
                "TESTS"
            )
            logger.info("Wait 30 days for full voting power")
            hive_utils.debug_quick_block_skip(node_client, wif, (30 * 24 * 3600 / 3))
            hive_utils.debug_generate_blocks(node_client.rpc.url, wif, 10)
            # transfer assets to accounts
            test_utils.transfer_assets_to_accounts(node_client, args.creator, accounts, 
                "400.000", "TESTS", wif
            )

            test_utils.transfer_assets_to_accounts(node_client, args.creator, accounts, 
                "400.000", "TBD", wif
            )

            logger.info("Balances for accounts after initial transfer")
            test_utils.print_balance(node_client, accounts)
            # transfer assets to treasury
            test_utils.transfer_assets_to_treasury(node_client, args.creator, args.treasury, 
                "1000000.000", "TBD", wif
            )
            test_utils.print_balance(node_client, [{'name' : args.treasury}])

            # create post for valid permlinks
            test_utils.create_posts(node_client, accounts, wif)

            now = node_client.get_dynamic_global_properties(False).get('time', None)
            if now is None:
                raise ValueError("Head time is None")
            now = test_utils.date_from_iso(now)

            proposal_data = [
                ['tester001', 1 + 0, 1, 24.000], # starts 1 day from now and lasts 1 day
                ['tester002', 1 + 1, 1, 24.000], # starts 2 days from now and lasts 1 day
                ['tester003', 1 + 2, 1, 24.000],  # starts 3 days from now and lasts 1 day
                ['tester004', 1 + 0, 3, 240000.000], # starts one day from now and lasts 3 days
            ]
            proposals_daily_pay = [ (prop[0], prop[3]) for prop in proposal_data ]
            proposals_datetime_ranges = {}

            proposals = [
                # pace proposals here in the format: {'creator' : creator, 'receiver' : receiver, 'start_date' : start-date, 'end_date' : end_date}
                
            ]

            start = None
            for pd in proposal_data:
                start_date, end_date = test_utils.get_start_and_end_date(now, pd[1], pd[2])
                if start is None:
                    start =  test_utils.date_from_iso(start_date)
                proposal = {'creator' : pd[0], 'receiver' : pd[0], 'start_date' : start_date, 'end_date' : end_date, 'daily_pay' : f'{pd[3] :.3f} TBD'}
                proposals.append(proposal)
                proposals_datetime_ranges[pd[0]] = { "start": test_utils.date_from_iso(start_date), "end": test_utils.date_from_iso(end_date) }

            test_utils.create_proposals(node_client, proposals, wif)

            # each account is voting on proposal
            test_utils.vote_proposals(node_client, accounts, wif)

            propos = node_client.get_dynamic_global_properties(False)
            period = test_utils.date_from_iso(propos["next_maintenance_time"])

            while period + datetime.timedelta(hours = 1) < start:
                period = period + datetime.timedelta(hours = 1)

            pre_test_start_date = period
            test_start_date = pre_test_start_date
            pre_test_start_date = test_start_date - datetime.timedelta( seconds = 2 )
            test_start_date_iso = test_utils.date_to_iso(test_start_date)
            pre_test_start_date_iso = test_utils.date_to_iso(pre_test_start_date)

            test_end_date = test_start_date + datetime.timedelta(days = 3)
            test_end_date_iso = test_utils.date_to_iso(test_end_date)

            # list proposals with inactive status, it shoud be list of pairs id:total_votes
            votes = test_utils.list_proposals(node_client, test_start_date_iso, "inactive")
            for vote in votes:
                #should be 0 for all
                assert vote == 0, "All votes should be equal to 0"

            logger.info("Balances for accounts after creating proposals")
            balances = test_utils.print_balance(node_client, accounts)
            for balance in balances:
                #should be 390.000 TBD for all
                assert balance == '390000', "All balances should be equal to 390.000 TBD"
            test_utils.print_balance(node_client, [{'name' : args.treasury}])

            # move forward in time to see if proposals are paid
            # moving is made in 1h increments at a time, after each 
            # increment balance is printed and checked
            logger.info("Moving to date: {}".format(test_start_date_iso))
            hive_utils.common.debug_generate_blocks_until(node_client.rpc.url, wif, pre_test_start_date_iso, False)
            previous_balances = dict(zip( account_names, test_utils.print_balance(node_client, accounts)))
            hive_utils.common.debug_generate_blocks_until(node_client.rpc.url, wif, test_start_date_iso, False)
            current_date = test_start_date

            while current_date < test_end_date:
                current_date = current_date + datetime.timedelta(hours = 1)
                current_date_iso = test_utils.date_to_iso(current_date)

                logger.info("Moving to date: {}".format(current_date_iso))
                budget = test_utils.calculate_propsal_budget( node_client, args.treasury, wif )
                hive_utils.common.debug_generate_blocks_until(node_client.rpc.url, wif, current_date_iso, False)

                logger.info("Balances for accounts at time: {}".format(current_date_iso))
                accnts = dict(zip( account_names, test_utils.print_balance(node_client, accounts)))
                expected_results = dict()
                for acc, payout in proposals_daily_pay:
                    date_ranges = proposals_datetime_ranges[acc]
                    if current_date >= date_ranges["start"] and current_date < date_ranges["end"]:
                        expected_results[acc] = payout
                expected_results = test_utils.calculate_expected_hourly_payout( expected_results, budget )

                for acc, ret in accnts.items():
                    if acc in expected_results.keys():
                        # because of rounding mechanism
                        assert abs((int(previous_balances[acc]) + expected_results[acc])- int(ret)) < 2, f"too big missmatch, prev: {previous_balances[acc]}, budget: {budget}, now: {ret}, expected: {expected_results[acc]}, account: {acc}"

                previous_balances = accnts

            # move additional hour to ensure that all proposals ended
            logger.info("Moving to date: {}".format(test_end_date_iso))
            hive_utils.common.debug_generate_blocks_until(node_client.rpc.url, wif, current_date_iso, False)
            logger.info("Balances for accounts at time: {}".format(test_end_date_iso))
            balances = test_utils.print_balance(node_client, accounts)
        else:
            raise Exception("no node detected")
    except Exception as ex:
        logger.error("Exception: {}".format(ex))
        return_code = 1
    finally:
        if node is not None:
            # input()
            node.stop_hive_node()
        sys.exit( return_code )
