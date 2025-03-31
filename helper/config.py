from woocommerce import API
from decouple import config

wcapi = API(
    url="https://nepalfloraandfauna.com.np",
    consumer_key=config("WC_CONSUMER_KEY"),
    consumer_secret=config("WC_CONSUMER_SECRET"),
    wp_api=True,
    version="wc/v3"
)
