from server_connection import *
import time

if __name__ == "__main__":
    client = init("12340987")
    time.sleep(5)
    data_publish(client, "12340987", "avsdfpoij")
    config_publish(client, "12340987", "config message")
    time.sleep(1)
    end(client)
