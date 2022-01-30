#include "lipkg.h"

LiPkg inst;

extern "C" double GetSpeed(void) {
    return inst.GetSpeed();
}
extern "C" uint16_t GetTimestamp(void) {
    return inst.GetTimestamp();
}
extern "C" bool IsPkgReady(void) {
    return inst.IsPkgReady();
}
extern "C" bool IsFrameReady(void) {
    return inst.IsFrameReady();
}
extern "C" void ResetFrameReady(void) {
    return inst.ResetFrameReady();
}
extern "C" long GetErrorTimes(void) {
    return inst.GetErrorTimes();
}
extern "C" const PointData* GetPkgData(void) {
    return inst.GetPkgData().data();
}
extern "C" bool Parse(const uint8_t* data , long len) {
    return inst.Parse(data, len);
}
extern "C" bool AssemblePacket() {
    return inst.AssemblePacket();
}
extern "C" const sensor_msgs::LaserScan* GetLaserScan() {
    return &inst.GetLaserScan();
}
extern "C" void SetLidarFrame(const std::string lidar_frame) {
    return inst.SetLidarFrame(lidar_frame);
}
