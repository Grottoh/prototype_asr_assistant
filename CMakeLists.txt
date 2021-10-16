# I build it with <cd ~/ASR/voice_assistant/build && rm -r * && cmake .. -DCMAKE_BUILD_TYPE=Release -Dflashlight_DIR=/usr/local/flashlight -DCUDNN_LIBRARY=/usr/local/cuda-11.1/lib64/ && make -j$(nproc)>
cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(InferenceCTC InferenceCTC.cpp)

find_package(flashlight CONFIG REQUIRED)
target_link_libraries(InferenceCTC PRIVATE flashlight::flashlight PRIVATE flashlight::flashlight-app-asr)
