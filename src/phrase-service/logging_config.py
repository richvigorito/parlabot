# logging_config.py

import logging
import sys
## from asgi_correlation_id import correlation_id_filter, CorrelationIdMiddleware
import asgi_correlation_id

logger = logging.getLogger(__name__)

def setup_logging():
    # cid_filter = correlation_id_filter(uuid_length=32)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.addFilter(asgi_correlation_id.CorrelationIdFilter())
    logging.basicConfig(
        handlers=[console_handler],
        level=logging.INFO,
        # format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        format="%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s",
    )

