#include "control_thread.hpp"

ServerControler::~ServerControler()
{
    if (_thread.joinable()) {
        _thread.join();
    }
}

void ServerControler::start()
{
    std::lock_guard<std::mutex> lock(_mutex);
    _thread = std::thread(&ServerControler::controller, this);
}

void ServerControler::controller()
{
    // controll
}