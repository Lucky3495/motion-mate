from typing import Callable, Iterator
from dataclasses import dataclass
from serial import Serial

Streamer = Callable[[], Iterator]

@dataclass
class EMGStreamer:

    com: str = "COM12"
    baud_rate: int = 115200

    # def __post_init__(self):
    #     self.open()

    def __enter__(self):
        self.serial = Serial(self.com, self.baud_rate)
        return self
    
    def __call__(self, label: str="nothing", person: str="saher", log=True) -> list:
        
        output = [x for x in self.serial.readline().decode().strip().split()]

        if log:
            record = [str(x) for x in output]
            record = ", ".join(output) + f", {label}, {person}"
            print(record)

        data = [int(x) for x in output]

        return data

    def __exit__(self, *_args):
        self.serial.close()
    
    def open(self):
        self.__enter__()
    
    def close(self):
        self.__exit__()