#include <iostream>
#include <mqtt/client.h>
#include <string>
#include <thread>
#include <chrono>
#include <unordered_set>
#include <sstream>

#include "main.hpp"


class ServerCB : public virtual mqtt::callback
{
private:
    std::unordered_set<std::string> _ids;
    std::string _pip;
    std::string _ssp;

public:
    ServerCB(std::string python_interpreter_path, std::string session_script_path) :
        _pip(python_interpreter_path), _ssp(session_script_path)
    { }

    void message_arrived(mqtt::const_message_ptr msg) override
    {
        if( _ids.find(msg->get_payload()) == _ids.end() )
        {
            std::cerr << "ID already exists";
            return;
        }
        else
        {
            // run new python thread and registered id
            _ids.insert(msg->get_payload());
            std::stringstream cmd;
            cmd << _pip << " " << _ssp << " " << msg->get_payload();

            std::thread t{[](std::string cmd) { std::system(cmd.c_str()); }, cmd.str()};
            t.detach();

            std::cerr << "Registered " + msg->get_payload() + "\n";
        }
    }
};


int main(int argc, char *argv[])
{
    if( argc != 3 )
    {
        std::cerr << "Invalid number of arguments\n";
        std::cerr << "Arg1: python interpreter path\n";
        std::cerr << "Arg2: python session script path\n";
        exit(1);
    }

    std::string python_interpreter(argv[1]);
    std::string python_session_script(argv[2]);

    mqtt::async_client    cli(ADDRESS, SERVER_ID);
    mqtt::topic           topic(cli, REGISTRATION_TOPIC);
    mqtt::connect_options connOpts;

    auto cb = ServerCB(python_interpreter, python_session_script);
    cli.set_callback(cb);
    
	connOpts = mqtt::connect_options_builder()
        .clean_session(false)
        .finalize();

    try
    {
        auto tok = cli.connect(connOpts);
        auto rsp = tok->get_connect_response();

        std::cout << "Connected to " << rsp.get_server_uri() << std::endl;

        cli.start_consuming();
        cli.subscribe(REGISTRATION_TOPIC, 2);

        while(true)
        {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
    catch (const mqtt::exception& exc) {
		std::cerr << exc.what() << std::endl;
		return 1;
	}

    return 0;
}