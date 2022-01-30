// https://docs.ros.org/en/diamondback/api/sensor_msgs/html/LaserScan_8h_source.html
// http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/LaserScan.html
#include <time.h>
namespace sensor_msgs {
    struct LaserScan {
        struct { struct timespec stamp; } header;
        float angle_min;
        float angle_max;
        float angle_increment;
        float time_increment;
        float scan_time;
        float range_min;
        float range_max;
        size_t beam_size;
        float* ranges;
        float* intensities;
    };
}