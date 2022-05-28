
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import Logging
import streamlit as st
from numpy import arange
from scipy.fftpack import fft

log = Logging.app_logging()

class FFT():
    
    def __init__(self, t, Signal, wave):
        
        self.t = t
        self.f = Signal
        self.N = len(t)
        self.wave = wave
        
    def Freq(self):

        try:
        
            freqs = arange(1, self.N, 1)[:int(self.N/2) - 1]
            Ampts = (2/self.N)* abs( fft(self.f)[:int(self.N/2)] )[1:]
            log.info('Freq and Ampts generated')
        
        except Exception as e:
            log.error(e)
        
        return freqs, Ampts

    def PlotFFT(self):

        try:
        
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Signal", "FFT"))
            
            # signal plot

            freqs, Ampts = self.Freq()

            trace1 = go.Scatter(x = self.t, y = self.f, mode = 'lines',line = dict(color = 'blue'))

            trace2 = go.Scatter(x = freqs, y = Ampts, mode = 'lines',line = dict(color = 'red'))

            
            fig.add_trace(trace1,row=1, col=1)
            fig.add_trace(trace2,row=1, col=2)

            fig.update_xaxes(title_text="time (s)", row=1, col=1)
            fig.update_xaxes(title_text="frequency (Hz)", row=1, col=2)

            fig.update_yaxes(title_text="Voltage", row=1, col=1)

            fig.update_layout(title_text="Fast Fourier Transform of {wave}".format(wave=self.wave), showlegend=False)

            st.plotly_chart(fig)

            log.info('Model figures generated successfully.')

        except Exception as e:

            log.error(e)