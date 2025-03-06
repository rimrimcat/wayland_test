import evdev
from multiprocessing import Process, Event
from multiprocessing.synchronize import Event as _Event
from evdev.device import InputDevice


# Use a multiprocessing Event for synchronization
stop_event = Event()

def monitor_device(device: InputDevice, stop_event: _Event):
    # print("Monitoring:", device.path, device.name, device.phys)

    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            print("Got event:", evdev.categorize(event))

            print("Detected device:")
            print("  path:", device.path)
            print("  name:", device.name)
            print("  phys:", device.phys)
            stop_event.set()
            return

if __name__ == "__main__":
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    processes = []
    
    for dev in devices:
        proc = Process(target=monitor_device, args=(dev, stop_event))
        proc.start()
        processes.append(proc)

    print(f"Monitoring {len(devices)} devices, waiting for input.")
    stop_event.wait()

    for proc in processes:
        proc.terminate()

    for proc in processes:
        proc.join()
