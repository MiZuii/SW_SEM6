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
        cli.start_consuming();

        auto tok = cli.connect(connOpts);
        auto rsp = tok->get_connect_response();
        std::cout << "Connected to " << rsp.get_server_uri() << std::endl;

        cli.subscribe(REGISTRATION_TOPIC, 2)->wait();

        std::cout << "Listening" << std::endl;

        while(true)
        {
            auto msg = cli.consume_message();
            auto msg_str = msg->to_string();

            if( ids.find(msg_str) != ids.end() )
            {
                if( msg_str.substr(0, 6) == "quit: ")
                {
                    // deregister client
                    auto cli_id = msg_str.substr(7);
                    if( ids.find(cli_id) != ids.end() )
                    {
                        ids.erase(cli_id);
                        continue;
                    }

                    std::cerr << "Incorrent quit ID\n";
                    continue;
                }
                
                std::cerr << "ID already exists\n";
                continue;
            }

            // run new python thread and registered id
            ids.insert(msg_str);
            std::stringstream cmd;
            cmd << python_interpreter << " " << python_session_script << " " << msg_str;

            std::thread t{[](std::string cmd) { std::system(cmd.c_str()); }, cmd.str()};
            t.detach();

            std::cerr << "Registered " + msg_str + "\n";
        }
    }
    catch (const mqtt::exception& exc) {
		std::cerr << exc.what() << std::endl;
		return 1;
	}

    return 0;
}