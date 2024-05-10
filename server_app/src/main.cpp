#include <iostream>
#include <mqtt/client.h>
#include <string>
#include <thread>
#include <chrono>

#include "main.hpp"
#include "control_thread.hpp"

/*
1. Befor actions a thread for server management is started. (functionalities: list clients, restart client processes, change arguments of processes)
2. Main cpp -> creates server mqtt topic and registers for new topic info
3. When a new topic is registered through the main topic a python script is run with name as argument
*/

int main()
{
    std::unique_ptr<ServerControler> controler = std::make_unique<ServerControler>();
    controler->start();

    mqtt::async_client    cli(ADDRESS, SERVER_ID);
    mqtt::topic           topic(cli, SERVER_TOPIC);
    mqtt::connect_options connOpts;
    
	connOpts = mqtt::connect_options_builder()
        .clean_session(false)
        .finalize();

    try
    {
        cli.start_consuming();
        auto tok = cli.connect(connOpts);
        std::cout << "Connecting" << std::endl;
        auto rsp = tok->get_connect_response();

        std::cout << "Connected to " << rsp.get_server_uri() << std::endl;
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