import json
import requests as req


class GrapheneRPC:
    def __init__(self, url):
        self.url = url

    def call(self, method, params=[], id_=1):
        data = {"jsoncall": "2.0", "method": method, "id": id_, "params": params}
        return req.post(self.url, data=json.dumps(data))

    def get_account_count(self):
        res = self.call("get_account_count")
        return res.json()["result"]

    def get_all_account_names(self):
        n_accounts = self.get_account_count()

        account_names = set()
        start_char = "0"
        while n_accounts != len(account_names):
            res = self.call("lookup_accounts", params=[start_char, 1000])
            res = res.json()["result"]
            account_names.update(res)

            # first two chars of last found object
            start_char = res[-1][:2]

        return list(account_names)
