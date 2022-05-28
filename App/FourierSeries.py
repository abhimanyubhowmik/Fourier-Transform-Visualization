import numpy as np
from matplotlib.pyplot import *
import scipy.integrate as integrate
import plotly.graph_objects as go
import time
import Logging
import streamlit as st

log = Logging.app_logging()




class fourier:

    def __init__(self,li,lf,n,wave,waveName,step_size):

        self.li = li
        self.lf = lf
        self.n = n
        self.wave = wave
        self.waveName = waveName
        self.step_size = step_size
 
 
 
# Function that will convert any given function 'f' defined in a given range '[li,lf]' to a periodic function of period 'lf-li' 
    def periodicf(self,x):
        try :
            if x>=self.li and x<=self.lf :
                return self.waveName(x)
            elif x>self.lf:
                x_new=x-(self.lf-self.li)
                return self.periodicf(x_new)
            elif x<(self.li):
                x_new=x+(self.lf-self.li)
                return self.periodicf(x_new)
            log.info('Perodic Function generated')

        except Exception as e:
            log.error(e)
 
 



    def fourierCoeffs(self,n):
        try:
            l = (self.lf-self.li)/2
            # Constant term
            a0=1/l*integrate.quad(lambda x: self.waveName(x), self.li, self.lf)[0]
            # Cosine coefficents
            A = np.zeros((n))
            # Sine coefficents
            B = np.zeros((n))
            
            for i in range(1,n+1):
                A[i-1]=1/l*integrate.quad(lambda x: self.waveName(x)*np.cos(i*np.pi*x/l), self.li, self.lf)[0]
                B[i-1]=1/l*integrate.quad(lambda x: self.waveName(x)*np.sin(i*np.pi*x/l), self.li, self.lf)[0]

            log.info("Fourier coefficients generated")

        except Exception as e:
            log.error(e)
    
        return [a0/2.0, A, B]
 
# This functions returns the value of the Fourier series for a given value of x given the already calculated Fourier coefficients
    def fourierSeries(self,coeffs,x,l,n):
        value = coeffs[0]
        for i in range(1,n+1):
            value = value + coeffs[1][i-1]*np.cos(i*np.pi*x/l) +  coeffs[2][i-1]*np.sin(i*np.pi*x/l)
        return value


    def plotFourier(self):

        try:

            placeholder = st.empty()

            color = {
                'Sawtooth Wave' : ['darkkhaki','forestgreen'],
                'Square Wave' : ['tomato','maroon'],
                'Triangular Wave' : ['orange','darkgoldenrod'],
                'Cycloid' : ['slateblue', 'teal']
            }

            # Limits for the functions
            li = self.li
            lf = self.lf
            l = (lf-li)/2.0

            # Number of harmonic terms

            n = self.n

            #plt.title('Fourier Series Approximation\n{wave}\n n = '+str(n).format(wave=self.wave))

            coeffs = self.fourierCoeffs(n)


            # Limits for plotting
            x_l = li*2
            x_u = lf*2

            # Sample values of x for plotting
            x = np.arange(x_l,x_u,self.step_size)

            y = [self.periodicf(xi) for xi in x]
            y_fourier = [self.fourierSeries(coeffs,xi,l,n) for xi in x]

            x_plot =[]
            # Square
            y_plot2 = []
            y_plot2_fourier = []


            for i in range(x.size):
            
                x_plot.append(x[i])
                # Actual function values
                y_plot2.append(y[i])
                # Values from fourier series
                y_plot2_fourier.append(y_fourier[i])

                #Plot
                trace1 = go.Scatter(x = x_plot, y = y_plot2, name=self.wave,mode = 'lines',line = dict(color = color[self.wave][0]))
                trace2 = go.Scatter(x = x_plot, y = y_plot2_fourier,name='Fourier Approximation', mode = 'lines',line = dict(color = color[self.wave][1]))

                layout= go.Layout(
                    autosize= True,
                    title= 'Fourier Series Approximation\n {wave} \n n = '.format(wave= self.wave)+str(n),
                    hovermode= 'closest',
                    showlegend= True
                )

                

                data = [trace2, trace1]
                fig = go.Figure(data=data,layout= layout)   

                fig.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
                ))

                log.info('Model figures generated successfully.')

                time.sleep(0.001)

                placeholder.write(fig)

        except Exception as e:
            log.error(e)
