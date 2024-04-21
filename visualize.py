import itertools
import math
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from serial import Serial
import time
from typing import Optional, Tuple, Any
from dataclasses import dataclass
from matplotlib.animation import FuncAnimation, FFMpegWriter
from typing import Callable, Iterator
from collections import deque
from utils import EMGStreamer, Streamer


@dataclass
class Plot:
    fig: Figure
    lines: np.ndarray
    tick: np.ndarray
    streamer: Streamer
    history: list[deque]

    @classmethod
    def seperate(cls, nrows: int=7, ncols: int=2, streamer: Optional[Streamer]=None, max_history: int = 100) -> 'Plot':

        fig, axs = plt.subplots(nrows, ncols, figsize=(8, 6), sharex=True)
        lines = [ax.plot([], [])[0] for ax in axs.flatten()] # what we need to update
        history = [deque(np.zeros(max_history), maxlen=max_history) for _ in axs.flatten()]
        
        plt.xlabel('Ticks')
        plt.tight_layout()

        for i, ax in enumerate(axs.flatten()):
            ax.set_xlim(0, max_history)
            ax.set_title(f'Channel {i+1}') 

        # gyro plots
        for line, ax in zip(lines[:6], axs.flatten()[:6]) :
            line.set_color('orange')
            # for whatever reason gryo data has a different range
            ax.set_ylim(-500, 1000)

        for _, ax in zip(lines[6:], axs.flatten()[6:]) :
            ax.set_ylim(1500, 3000)

        tick = np.linspace(0, max_history-1, max_history)

        if streamer is None:
            streamer = random_data

        self = cls(fig, lines, tick, streamer, history)

        return self
    
    @classmethod
    def single(cls, n: int=14, streamer: Optional[Streamer]=None, max_history: int=100) -> 'Plot':
        fig, ax = plt.subplots(figsize=(8, 6))
        lines = [ax.plot([], [])[0] for _ in range(n)]
        history = [deque(np.zeros(max_history), maxlen=max_history) for _ in range(n)]

        plt.xlabel('Ticks')
        plt.tight_layout()

        ax.set_xlim(0, max_history)
        ax.set_ylim(1500, 3000)

        tick = np.linspace(0, max_history-1, max_history)

        # too intrusive
        # legends = [f"Channel {i}" for i in range(1,n+1)]
        # ax.legend(lines, legends, loc='lower left')

        return cls(fig, lines, tick, streamer, history)
    
    @classmethod
    def double(cls, streamer: Optional[Streamer]=None, max_history: int=100, left: int=8, right:int=6):
        fig, (ax_emg, ax_gyro) = plt.subplots(nrows=1, ncols=2, figsize=(8,6))
        lines_emg = [ax_emg.plot([], [])[0] for _ in range(left)]
        lines_gyro = [ax_gyro.plot([], [])[0] for _ in range(right)]
        lines = lines_gyro + lines_emg
        
        history = [deque(np.zeros(max_history), maxlen=max_history) for _ in range(left+right)]

        ax_emg.set_title("EMG channels")
        ax_gyro.set_title("Gyro channels")

        ax_emg.set_xlim(0, max_history)
        ax_gyro.set_xlim(0, max_history)

        ax_emg.set_ylim(1500, 3000)
        ax_gyro.set_ylim(-500, 1000)

        tick = np.linspace(0, max_history-1, max_history)

        plt.xlabel('Ticks')
        plt.tight_layout()

        return cls(fig, lines, tick, streamer, history)

    def update(self, _frame_idx:int):

        data = self.streamer()
        # if _frame_idx == 60*10:
        #     plt.close()
        #     return None
            
        for i, datum in enumerate(data):
            self.history[i].append(datum)

        for i, line in enumerate(self.lines):
            line.set_xdata(self.tick)
            line.set_ydata(self.history[i])
        
        return self.lines

    def animate(self):
        # dont delete this var
        # according to the docs we dont want it to be garbage collected
        self.ani = FuncAnimation(self.fig, self.update, cache_frame_data=False, frames=60*10, blit=True, repeat=True, interval=0.1)
        # writer = FFMpegWriter(fps=60)
        # writer = FFMpegWriter(fps=60)
        # self.ani.save('lets-go.mp4', writer)
        plt.show()


def get_data(ser: Serial) -> list:
        response = [int(x) for x in ser.readline().decode().strip().split()]

        return response

def random_data():
    return np.random.rand(14)

class SinStreamer:

    def __init__(self) -> None:
        self.t = 0
        self.repeat = 14

    def __call__(self) -> float:
        res = math.sin(self.t)
        self.t += 1

        return [res] * self.repeat

def main():
    # plt.style.use('dark_background')
    # kos-windows
    plt.rcParams['animation.ffmpeg_path'] = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg"

    with EMGStreamer() as s:
        # while True:
        #     s()
        plot = Plot.seperate(streamer=s)
        # plot = Plot.double(streamer=s)
        # plot = Plot.seperate(streamer=s)
        plot.animate()
        return

if __name__ == "__main__":
    main()