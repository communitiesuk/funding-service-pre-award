from gevent import monkey

monkey.patch_all()

from fsd_utils.gunicorn.config.devtest import *  # noqa

# bind = "127.0.0.1:5000"
