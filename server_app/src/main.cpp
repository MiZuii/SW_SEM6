#include <iostream>
#include <mqtt/client.h>
#include <string>
#include <thread>
#include <chrono>
#include <unordered_set>
#include <sstream>

#include "main.hpp"


int main(int argc, char *argv[])
{
    if( argc != 3 )
    {
        std::cerr << "Invalid number of arguments\n";
        std::cerr << "Arg1: python interpreter path\n";
        std::cerr << "Arg2: python session script path\n";
        exit(1);
    }

    std::unordered_set<std::string> ids;
    std::string python_interpreter(argv[1]);
    std::string python_session_script(argv[2]);

    mqtt::async_client    cli(ADDRESS, SERVER_ID);
    mqtt::topic           topic(cli, REGISTRATION_TOPIC);
    mqtt::connect_options connOpts;
    
	connOpts = mqtt::connect_options_builder()
        .clean_session(false)
        .finalize();

    try
    {
        auto tok = cli.connect(connOpts);
        auto rsp = tok->get_connect_response();

        std::cout << "Connected to " << rsp.get_server_uri() << std::endl;

        cli.subscribe(REGISTRATION_TOPIC, 2)->wait();
        cli.start_consuming();

        std::cout << "Listening" << std::endl;

        while(true)
        {
            auto msg = cli.consume_message();
            
            if( ids.find(msg->to_string()) == ids.end() )
            {
                std::cerr << "ID already exists";
            }
            else
            {
                // run new python thread and registered id
                ids.insert(msg->to_string());
                std::stringstream cmd;
                cmd << python_interpreter << " " << python_session_script << " " << msg->to_string();

                std::thread t{[](std::string cmd) { std::system(cmd.c_str()); }, cmd.str()};
                t.detach();

                std::cerr << "Registered " + msg->to_string() + "\n";
            }
        }
    }
    catch (const mqtt::exception& exc) {
		std::cerr << exc.what() << std::endl;
		return 1;
	}

    return 0;
}