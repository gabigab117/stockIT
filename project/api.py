from ninja import NinjaAPI

from account.api import account_api


api = NinjaAPI(docs_url="documentation", urls_namespace="api")
api.add_router("account", account_api)
