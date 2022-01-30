from ctypes import *
import serial
import math

c_float_p = POINTER(c_float)

class LaserScan(Structure):
    _fields_ = [
        ("time_sec", c_long),
        ("time_nsec", c_long),
        ("angle_min", c_float),
        ("angle_max", c_float),
        ("angle_increment", c_float),
        ("time_increment", c_float),
        ("scan_time", c_float),
        ("range_min", c_float),
        ("range_max", c_float),
        ("beam_size", c_size_t),       # not present for ROS
        ("ranges_p", c_float_p),
        ("intensities_p", c_float_p),
    ]

    def ranges(self):
        #return cast(self.ranges_p, POINTER(c_float * self.beam_size)).contents
        return self.ranges_p[0:self.beam_size]
    def intensities(self):
        #return cast(self.intensities_p, POINTER(c_float * self.beam_size)).contents
        return self.intensities_p[0:self.beam_size]

    def __str__(self):
        return "LaserScan(time=%d.%09s, angle=%f to %f step %f, scan_time=%f step %f, range %f to %f, %s, %s)" % (
            self.time_sec, self.time_nsec, self.angle_min, self.angle_max, self.angle_increment, self.scan_time, self.time_increment, self.range_min, self.range_max,
            self.ranges, self.intensities
        )

class PointData(Structure):
    _fields_ = [
        ("angle", c_float),
        ("distance", c_float),
        ("confidence", c_uint8),
        ("x", c_double),
        ("y", c_double)]

    def __repr__(self):
        return "PointData(angle=%f, distance=%f, confidence=%d, addr=0x%08x)" % (self.angle, self.distance, self.confidence, addressof(self))

lib = cdll.LoadLibrary("./libld06.so")

lib.GetSpeed.argtypes = []
lib.GetSpeed.restype = c_double
lib.GetTimestamp.argtypes = []
lib.GetTimestamp.restype = c_uint16

lib.IsPkgReady.argtypes = []
lib.IsPkgReady.restype = c_bool
lib.IsFrameReady.argtypes = []
lib.IsFrameReady.restype = c_bool
lib.ResetFrameReady.argtypes = []
lib.ResetFrameReady.restype = None
lib.GetErrorTimes.argtypes = []
lib.GetErrorTimes.restype = c_long
lib.GetPkgData.argtypes = []
lib.GetPkgData.restype = POINTER(PointData * 12)  # POINT_PER_PACK is 12
lib.Parse.argtypes = [c_char_p, c_long]
lib.Parse.restype = c_bool
lib.AssemblePacket.argtypes = []
lib.AssemblePacket.restype = c_bool
lib.GetLaserScan.argtypes = []
lib.GetLaserScan.restype = POINTER(LaserScan)
#lib.SetLidarFrame.argtypes = [std::string]
#lib.SetLidarFrame.restype = None

def run_cli():
    global pkg
    pkg = None
    with serial.Serial('/dev/ttyUSB0', 230400, timeout=10, ) as ser:
        while True:
            xs = ser.read(1024)
            print(len(xs))
            if lib.Parse(xs, len(xs)):
                lib.AssemblePacket()
            if lib.IsPkgReady():
                pkg = lib.GetPkgData()
                print(list(pkg.contents))
                break
            if lib.IsFrameReady() and False:
                pkg = lib.GetLaserScan().contents
                print(str(pkg))
                lib.ResetFrameReady()
                #break

def run_gui():
    global pkg
    pkg = None

    size = 1000
    import tkinter
    top = tkinter.Tk()
    canvas = tkinter.Canvas(top, bg="black", width=size, height=size)
    coord = 10, 50, 240, 210
    canvas.pack()

    with serial.Serial('/dev/ttyUSB0', 230400, timeout=0) as ser:
        lines = []
        def try_read():
            xs = ser.read(1024)
            print(len(xs))
            if lib.Parse(xs, len(xs)):
                lib.AssemblePacket()
            if lib.IsPkgReady():
                pkg = lib.GetPkgData()
                print(list(pkg.contents))
                #top.quit()
                x0, y0 = size/2, size/2
                for p in pkg.contents:
                    angle = -p.angle / 360 * 2*math.pi
                    dist = p.distance*size/2/5
                    color = "#%02x%02x%02x" % (255-p.confidence, p.confidence, 0)
                    lines.append(canvas.create_line(x0, y0, x0+math.sin(angle)*dist, y0+math.cos(angle)*dist, fill=color))
                    if len(lines) > 500:
                        canvas.delete(lines[0])
                        del lines[0]
            if lib.IsFrameReady() and False:
                pkg = lib.GetLaserScan().contents
                print(str(pkg))
                lib.ResetFrameReady()
                #top.quit()
            top.after(10, try_read)
        top.after(10, try_read)
        top.mainloop()

run_gui()
