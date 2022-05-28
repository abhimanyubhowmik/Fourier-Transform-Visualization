import streamlit as st
import Logging
import FourierSeries as fs
import numpy as np
from numpy import pi, sin, append, linspace, array, arange
from numpy.random import rand
import FastFourierTransform as fft
from PIL import Image

log = Logging.app_logging()

im = Image.open("App/favicon.png")
st.set_page_config(
page_title="Fourier Series Vizualizer",
page_icon=im,
layout="wide",
initial_sidebar_state="expanded",
menu_items={
        "Get Help": "https://github.com/abhimanyubhowmik/Fourier-Transform-Visualization",
        "Report a bug": "https://github.com/abhimanyubhowmik/Fourier-Transform-Visualization/issues",
        "About": "### An application for Visualization of Fourier and Fast Fourier Transform \n :copyright: Abhimayu Bhowmik \n\n Github: https://github.com/abhimanyubhowmik \n\n Linkedin: https://linkedin.com/in/bhowmikabhimanyu ",
    }
)

# Non-periodic sawtooth function defined for a range [-l,l]
def sawtooth(x):
    return x
 
# Non-periodic square wave function defined for a range [-l,l]
def square(x):
    if x>0:
        return np.pi
    else:
        return -np.pi
# Non-periodic triangle wave function defined for a range [-l,l]
def triangle(x):
    if x>0:
        return x
    else:
        return -x
# Non-periodic cycloid wave function defined for a range [-l,l]
def cycloid(x):
    return np.sqrt(np.pi**2-x**2)


st.title('Fourier Series Vizualizer')
viz_name = st.sidebar.selectbox('Select Visualization', ('Fourier transform', 'Fast fourier transform'))

def get_viz(viz_name):
    try:
        if viz_name == 'Fourier transform':
            time = 0
            n = st.sidebar.slider('No. of Harmonics',min_value= 1,max_value= 20,step= 1)
            li = st.sidebar.slider('Initial Limit',min_value= -np.pi,max_value=-0.009)
            lf = st.sidebar.slider('Final Limit',min_value= -0.001,max_value=np.pi)
            step = st.sidebar.slider('Step Size',min_value = 0.01, max_value= 1.0)
            wave = st.sidebar.selectbox('Select Wave',('Sawtooth Wave','Square Wave','Triangular Wave','Cycloid'))
            return n,wave,li,lf,step,time
        else:
            n = 0
            li = 0
            lf = 0
            wave = st.sidebar.selectbox('Select Signal',('Sinusoidal Signal', 'Square wave','Sinusoidal Signal with Noise'))
            time = st.sidebar.slider('Time',min_value= 1,max_value= 10)
            step = st.sidebar.slider('No. of steps',min_value = 10, max_value= 500)
            log.info('Input values successfully updated')
            return n,wave,li,lf,step,time

    except Exception as e:
        log.error(e)



def visualization(viz_name,n,wave,li,lf,step_size,time):

    try:
        if viz_name == 'Fourier transform':

            if wave == 'Sawtooth Wave':
                fourier = fs.fourier(li,lf,n,wave,sawtooth,step_size)

            elif wave == 'Square Wave':
                fourier = fs.fourier(li,lf,n,wave,square,step_size)

            elif wave == 'Triangular Wave':
                fourier = fs.fourier(li,lf,n,wave,triangle,step_size)
            
            else:
                fourier = fs.fourier(li,lf,n,wave,cycloid,step_size)

            fourier.plotFourier()

        elif viz_name == 'Fast fourier transform':

            t = linspace(0, time, step_size)

            if wave == 'Sinusoidal Signal':
                f = sin(2* pi* 5* t) + 0.5* sin(2* pi* 10* t)
                log.info('Sinusoidal Signal generated')

                SignalFFT = fft.FFT(t, f,wave)
                SignalFFT.PlotFFT()

            elif wave == 'Square wave':
                f = array([])
                for i in t:
                    if i <= 0.5:
                        f = append(f, 1)
                    else:
                        f = append(f, -1)
                    
                    log.info('Square Signal generated')

                SignalFFT = fft.FFT(t, f, wave)
                SignalFFT.PlotFFT()

            else:
                f = sin(2* pi* 5* t) + 0.5* sin(2* pi* 10* t) + rand( len(t) )
                log.info('Sinusoidal Signal with Noise is generated')
                SignalFFT = fft.FFT(t, f, wave)
                SignalFFT.PlotFFT()

        else:
            log.error('Wrong Selection of Visualization')
    
    except Exception as e:
        log.error(e)



if __name__ == '__main__':
    n, wave, li, lf, step,time = get_viz(viz_name)
    visualization(viz_name, n, wave,li,lf, step, time)