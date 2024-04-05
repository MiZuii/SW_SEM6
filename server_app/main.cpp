#include <iostream>
#include <mqtt/client.h>
#include <string>
#include <thread>
#include <chrono>

static constexpr char ADDRESS[24] = "tcp://192.168.0.66:1883";

int main()
{
    std::cout << "Start" << std::endl;

    mqtt::async_client    cli(ADDRESS, "test_cli_id");
    mqtt::topic           topic(cli, "test");
    mqtt::connect_options connOpts;
    
	connOpts.set_automatic_reconnect(true);

    try
    {
        cli.connect(connOpts)->wait();
        std::cout << "Connected" << std::endl;
        std::chrono::milliseconds sleep_time(500); // or whatever

        while(true)
        {
            std::string payload = "c:";
            topic.publish(std::move(payload));
            std::this_thread::sleep_for(sleep_time);
        }
    }
    catch (const mqtt::exception& exc) {
		std::cerr << exc.what() << std::endl;
		return 1;
	}

    return 0;
}