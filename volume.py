from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# 获取自己的音频设备及其参数
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#由于vol_range与0-100这个不是对应的关系，不方便设置实际的声音，故需要进行装换，但是无法得知其转换关系，只能通过字典的形式查询：
def vol_tansfer(x):
    # volume 0 ~ 100 对应的分贝值
    dbs = [ -63.5,  -56.99, -51.67, -47.74, -44.62, -42.03, -39.82, -37.89, -36.17, -34.63,  -33.04,
            -31.96, -30.78, -29.68, -28.66, -27.7,  -26.8,  -25.95, -25.15, -24.38, -23.55,
            -22.96, -22.3,  -21.66, -21.05, -20.46, -19.9,  -19.35, -18.82, -18.32, -17.82,
            -17.35, -16.88, -16.44, -16.0,  -15.58, -15.16, -14.76, -14.37, -13.99, -13.62,
            -13.26, -12.9,  -12.56, -12.22, -11.89, -11.56, -11.24, -10.93, -10.63, -10.33,
            -10.04, -9.75,  -9.47,  -9.19,  -8.92,  -8.65,  -8.39,  -8.13,  -7.88,  -7.63,
            -7.38,  -7.14,  -6.9,   -6.67,  -6.44,  -6.21,  -5.99,  -5.76,  -5.55,  -5.33,
            -5.12,  -4.91,  -4.71,  -4.5,   -4.3,   -4.11,  -3.91,  -3.72,  -3.53,  -3.34,
            -3.15,  -2.97,  -2.79,  -2.61,  -2.43,  -2.26,  -2.09,  -1.91,  -1.75,  -1.58,
            -1.41,  -1.25,  -1.09,  -0.93,  -0.77,  -0.61,  -0.46,  -0.3,   -0.15,  0.0]
    return dbs[x]

#设置声音大小, 0-100
def set_vol(vol):
    global volume
    db = vol_tansfer(vol)
    print("db: ", db)   
    volume.SetMasterVolumeLevel(db, None)
