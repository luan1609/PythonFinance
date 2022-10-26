import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
from datetime import datetime
from datetime import timedelta
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import mplcyberpunk
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import service
from webdriver_manager.firefox import GeckoDriverManager
import requests
from bcb import currency
from bcb import sgs
from fpdf import FPDF
from matplotlib.dates import date2num
import warnings

warnings.filterwarnings('ignore')
indices = ['^BVSP', '^GSPC']  # Adicionando em uma lista os índices para relatório(IBOV e S&P500)
hoje = datetime.now()  # Adicionando em uma variável a data de hj utilizando datetime
um_ano_atras = hoje - timedelta(days = 366) #armazenando em uma variável os dias de um ano inteiro(de hj até 366dias atrás)
dados_mercado = pdr.get_data_yahoo(indices, start= um_ano_atras, end = hoje).round() # armazenando redimentos dos indices no perído de 1 ano atrás até hj
#print(dados_mercado)
dados_fechamento = dados_mercado['Adj Close']# Armazenando em uma variável somente a coluna Adj close da tabela dados_mercado.
dados_fechamento.columns = ['Ibov','S&P500']# Criando duas colunas (Ibov e sp500 na nova lista)
dados_fechamento = dados_fechamento.dropna()#removendo index vazios da tabela
#print(dados_fechamento)#Exibindo a tabela
dados_anuais = dados_fechamento.resample("Y").last()#Armazenando em uma variável os dados de fechamento redimensionando os dados para exibir os dados de forma anual e n diária
#print(dados_anuais)

dado_mensais = dados_fechamento.resample("M").last()#Armazenando em uma variável os dados de fechamento redimensionando os dados para exibir os dados de forma Mensal e n diária
#print(dado_mensais)
retorno_diario = dados_fechamento.pct_change().dropna()#retorna um DataFrame com a diferença percentual entre os valores de cada linha e, por padrão, a linha anterior
#print(retorno_diario)

retorno_mes_a_mes = dado_mensais.pct_change().dropna()#retorna um DataFrame com a diferença percentual entre os valores de cada linha e, por padrão, a linha anterior
retorno_mes_a_mes = retorno_mes_a_mes.iloc[1: , :]#Seleciona os dados a partir da primeira linha "1:" e todas as colunas ":"
#print(retorno_mes_a_mes)
retorno_anual = dados_anuais.pct_change().dropna()#retorna um DataFrame com a diferença percentual entre os valores de cada linha e, por padrão, a linha anterior
retorno_anual = retorno_anual.iloc[:,:]#Selecionando a tabela(Matriz) inteira
#print(retorno_anual)

fechamento_do_dia = retorno_diario.iloc[-1:,:]#Selecionando toda a matriz a partir da segunda linha(index 1)
#print(fechamento_do_dia * 100)
volatilidade_12m_ibov = round(retorno_diario['Ibov'].std() * np.sqrt(252),3)# calculando volatilidade do indíce ibov
volatilidade_12m_sp = round(retorno_diario['S&P500'].std() * np.sqrt(252),3)# calculando volatilidade do indíce S&P500
#print(volatilidade_12m_ibov)
#print(volatilidade_12m_sp)

'''
fig, ax =plt.subplots()#Criando uma figura e seus eixos.
plt.style.use("cyberpunk")#Utilizando estilo para plotagem.
ax.plot(dados_fechamento.index,dados_fechamento['Ibov'])#Definindo eixos da o gráfico.
ax.grid(False)#Define a existência de grades no gráfico
ax.set_title('Ibov mês a mês')#Adicionando título ao Gráfico
#plt.savefig('ibov.png',dpi = 300)
plt.show()#Exibindo gráfico.
'''

'''
fig, ax = plt.subplots()
plt.style.use('ggplot')
ax.plot(dados_fechamento.index,dados_fechamento['S&P500'])
ax.grid(True)
plt.show()
'''

data_inicial = dados_fechamento[0]
if (datetime.now().hour < 10):
    data_final = dados_fechamento.index[-1]