from server_connection import *
import time

if __name__ == "__main__":
    client = init("12340987")
    time.sleep(1)
    publish(client, "12340987", "the test message")
    time.sleep(5)
    end(client)
