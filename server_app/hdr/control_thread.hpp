#pragma once

#include <iostream>
#include <thread>
#include <mutex>

class ServerControler {
private:
    ServerControler() {}
    ~ServerControler();

    std::mutex _mutex;
    std::thread _thread;

    ServerControler(const ServerControler&) = delete;
    ServerControler& operator=(const ServerControler&) = delete;

    void controller();

public:
    void start();
};
