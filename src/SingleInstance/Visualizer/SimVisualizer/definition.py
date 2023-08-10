import pandas as pd
import plotly.graph_objects as go
from numpy import arange, pi
from plotly.subplots import make_subplots
import os
import numpy as np

from src.Utils.DataParser.definition import DataParser
class SimVisualizer:
    """
    This class aims to save plots associated with a single simulation. You pass in a DataParser instance which links to
    a data directory. This is then reformatted and plotted for visualization purposes.
    """

    def __init__(self, data_parser: DataParser, args):
        self.data_parser = data_parser
        self.transient_time, self.transient_index = data_parser.get_transient_time()
        self.args = args
        self.output = self.data_parser.get_output_k_amps()
        self.ss_mode = np.absolute(self.data_parser.get_k_amps())[-1]
        self.freqs = np.fft.fftfreq(len(self.ss_mode), d=self.args['dz']) * 2 * np.pi
        self.tag = 'base'
        if self.args['custom_start']:
            self.tag = 'dynamic'

    def plot_binary(self) -> None:
        times = self.data_parser.get_times()
        binary = self.data_parser.get_bin_vals()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=binary, mode='lines', name='Amplitude'))
        fig.update_layout(title={'text': 'Binary Inputs', 'x': 0.5},
                          xaxis_title={'text': 'Time (s)', 'standoff': 25},
                          yaxis_title={'text': 'Amplitude', 'standoff': 5},
                          width=900, height=600)
        fig.write_image(os.path.join(self.args['sim_dir'], f'binary_plot_{self.tag}.png'))

    def plot_x(self) -> None:
        times = self.data_parser.get_times()[:self.transient_index]
        x_amps_output = self.data_parser.get_output_x_amps()[:self.transient_index]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=x_amps_output, mode='lines', name='Amplitude'))
        fig.add_hline(y=max(x_amps_output), line_width=3, line_dash="dash", line_color="green",
                      annotation_text=rf"Max Amplitude: {max(x_amps_output):.3e}",
                      annotation_position="top left",
                      annotation_font=dict(size=15, color="green"),
                      )

        fig.update_layout(title={'text': 'Amplitude at Output', 'x': 0.5},
                          xaxis_title={'text': 'Time (s)', 'standoff': 25},
                          yaxis_title={'text': 'Amplitude', 'standoff': 5},
                          width=900, height=600)
        fig.write_image(os.path.join(self.args['sim_dir'], f'amplitude_plot_{self.tag}.png'))

    def plot_k_90(self) -> None:
        k_90 = self.data_parser.get_k_amps_at_x_percent()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.freqs, y=k_90, mode='markers', name='Amplitude'))
        fig.update_layout(title={'text': 'Spatial Frequency Amplitude at 90% of SSV', 'x': 0.5},
                          xaxis_title={'text': r'Mode (1/m)', 'standoff': 25},
                          yaxis_title={'text': 'Amplitude', 'standoff': 5},
                          width=900, height=600,yaxis_type="log")
        fig.write_image(os.path.join(self.args['sim_dir'], f'k_90_plot_{self.tag}.png'))

    def plot_max_modes(self):
        k_amps = np.absolute(self.data_parser.get_k_amps())
        k_max_ind = np.argmax(self.ss_mode)

        total_points = int(0.05 * len(self.ss_mode))
        lower_ind = k_max_ind
        upper_ind = k_max_ind
        points_count = 1

        while points_count < total_points:
            lower_ind = (lower_ind - 1) % len(self.ss_mode)
            points_count += 1
            if points_count < total_points:
                upper_ind = (upper_ind + 1) % len(self.ss_mode)
                points_count += 1

        if lower_ind < upper_ind:
            freq_indices = range(lower_ind, upper_ind)
        else:
            freq_indices = list(range(lower_ind, len(self.ss_mode))) + list(range(0, upper_ind))

        m_dynamics = np.zeros((len(freq_indices), len(k_amps)))
        for i in range(len(k_amps)):
            for j, freq_index in enumerate(freq_indices):
                m_dynamics[j][i] = np.absolute(k_amps[i][freq_index])

        data = {f'k={ (self.freqs[freq_indices[idx]]):.2f}': m_dynamics[idx] for idx in
                range(0, len(freq_indices) - 1, 5)}

        df = pd.DataFrame(data)
        df.insert(0, 'Time (s)', self.data_parser.get_times())

        fig = make_subplots(rows=1, cols=1)
        for name in df.columns[1:]:
            fig.add_trace(go.Scatter(x=df['Time (s)'], y=df[name], mode='lines', name=name), row=1, col=1)
        fig.update_layout(title={'text': 'Max Spatial Frequency Amplitudes Over Time', 'x': 0.5},
                          xaxis_title={'text': 'Time (s)', 'standoff': 25},
                          yaxis_title={'text': 'Max K Amplitudes', 'standoff': 5},
                          width=900, height=600)
        fig.write_image(os.path.join(self.args['sim_dir'], f'k_max_modes_plot_{self.tag}.png'))

    def plot_phase(self):
        times = self.data_parser.get_times()[:self.transient_index]
        phase = self.data_parser.get_phase_x()[:self.transient_index]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=phase, mode='lines', name='Phase (degrees)'))
        fig.update_layout(title={'text': 'Phase at Signal Output', 'x': 0.5},
                          xaxis_title={'text': 'Time (s)', 'standoff': 25},
                          yaxis_title={'text': 'Phase (degrees)', 'standoff': 5},
                          width=900, height=600)
        fig.write_image(os.path.join(self.args['sim_dir'], f'phase_plot_{self.tag}.png'))