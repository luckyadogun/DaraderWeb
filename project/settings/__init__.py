import os

import environ
from split_settings.tools import include, optional

env = environ.Env()

environment = os.environ.get("ENVIRONMENT")

include("components/*.py", "environments/{0}.py".format(env("ENVIRONMENT")))