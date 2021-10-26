cmake_minimum_required(VERSION 3.15)
project(DeliveryProblem)

include_directories(../../sparsehash-c11)

add_executable(dp
    bounds.cpp
    task.cpp
    main.cpp
    )
