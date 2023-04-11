#!/usr/bin/env python3
import datetime
import random
import logging
from models.senha import Senha
from models.caixa import Caixa
from models.atendimento import Atendimento

# Carregar duas filas

fila_normal = []
fila_preferencial = []

# Fila de atendimentos
atendimentos = []

# 5 Caixas para atendimento, 3 para normal, 2 para atendimento preferencial

caixas = []
caixa1 = Caixa("NORMAL", "Aberto")
caixa2 = Caixa("NORMAL", "Aberto")
caixa3 = Caixa("NORMAL", "Aberto")
caixa4 = Caixa("PREFERENCIAL", "Aberto")
caixa5 = Caixa("PREFERENCIAL", "Aberto")

caixas.append(caixa1)
caixas.append(caixa2)
caixas.append(caixa3)
caixas.append(caixa4)
caixas.append(caixa5)

logging.basicConfig(filename='log/log_file.txt', level=logging.DEBUG)

tempo_medio = 0
# Funções auxiliares
def calculoDeTempoMedio():
    if len(atendimentos) != 0:
        soma_tempo = 0
        for atendimento in atendimentos:
            soma_tempo += atendimento.tempo_atendimento

        return soma_tempo / len(atendimentos)

    return 0

def chamadaDeSenha():
    for caixa in caixas:
        if caixa.tipo == "NORMAL" and caixa.status == "Aberto":
            if len(fila_normal) != 0:
                tempo_de_atendimento = random.randint(1, 30)
                entrada = datetime.datetime.now()
                saida = entrada + datetime.timedelta(minutes=tempo_de_atendimento)
                atendimento = Atendimento(fila_normal[0], caixa, entrada, saida, tempo_de_atendimento)
                atendimentos.append(atendimento)
                caixa.atendimento = atendimento
                caixa.status = "Fechado"

            elif len(fila_preferencial) != 0:
                tempo_de_atendimento = random.randint(1, 30)
                entrada = datetime.datetime.now()
                saida = entrada + datetime.timedelta(minutes=tempo_de_atendimento)
                atendimento = Atendimento(fila_preferencial[0], caixa, entrada, saida, tempo_de_atendimento)
                atendimentos.append(atendimento)
                caixa.atendimento = atendimento
                caixa.status = "Fechado"

        if caixa.tipo == "PREFERENCIAL" and caixa.status == "Aberto":
            if len(fila_preferencial) != 0:
                tempo_de_atendimento = random.randint(1, 30)
                entrada = datetime.datetime.now()
                saida = entrada + datetime.timedelta(minutes=tempo_de_atendimento)
                atendimento = Atendimento(fila_preferencial[0], caixa, entrada, saida, tempo_de_atendimento)
                atendimentos.append(atendimento)
                caixa.atendimento = atendimento
                caixa.status = "Fechado"

            elif len(fila_normal) != 0:
                tempo_de_atendimento = random.randint(1, 30)
                entrada = datetime.datetime.now()
                saida = entrada + datetime.timedelta(minutes=tempo_de_atendimento)
                atendimento = Atendimento(fila_normal[0], caixa, entrada, saida, tempo_de_atendimento)
                atendimentos.append(atendimento)
                caixa.atendimento = atendimento
                caixa.status = "Fechado"

def checagemTempoDeEspera():
    for pessoa in fila_normal:
        data_abertura = datetime.datetime.strptime(pessoa.data, "%d-%m-%Y %H:%M:%S")
        data_check = datetime.datetime.now()
        tempo_espera = (data_check - data_abertura).total_seconds()
        tempo_espera_minutos = int(tempo_espera / 60)
        if tempo_espera_minutos > 15 and len(caixas) < 7:
            print("ALERTA: Abrir outro caixa!")
            if len(caixas) == 5:
                caixas.append(caixa6 = Caixa("NORMAL", "Aberto"))
            if len(caixas) == 6:
                caixas.append(caixa7 = Caixa("NORMAL", "Aberto"))

    for pessoa in fila_preferencial:
        data_abertura = datetime.datetime.strptime(pessoa.data, "%d-%m-%Y %H:%M:%S")
        data_check = datetime.datetime.now()
        tempo_espera = (data_check - data_abertura).total_seconds()
        tempo_espera_minutos = int(tempo_espera / 60)
        if tempo_espera_minutos > 15 and len(caixas) < 7:
            print("ALERTA: Abrir outro caixa!")
            if len(caixas) == 5:
                caixas.append(caixa6 = Caixa("NORMAL", "Aberto"))
            if len(caixas) == 6:
                caixas.append(caixa7 = Caixa("NORMAL", "Aberto"))

def aberturaDeCaixa():
    for caixa in caixas:
        if caixa.atendimento != None:
            data_fim = datetime.datetime.strptime(caixa.atendimento.fim, "%d-%m-%Y %H:%M:%S")
            if data_fim < datetime.datetime.now():
                caixa.status = "Aberto"
                logging.INFO("Atendimento Finalizado! Horário de Ínicio: ", caixa.atendimento.inicio, " Horário de Finalização: ", caixa.atendimento.fim)

def checarNumero(lista):
    if len(lista) == 0:
        print("Está aqui!")
        return 1

    return lista[-1].id + 1

i = True
while i == True:
    print("Escolha uma opção")
    print("1 - Gerar Senha")
    print("2 - Encerrar serviço")
    x = int(input("Digite sua escolha: "))

    if x == 2:
        i = False

    if x == 1:
        print("=========================================")
        print("Escolha o tipo da senha!")
        print("1 - Normal")
        print("2 - Preferencial")
        tipo = int(input("Digite o tipo da senha: "))

        if tipo == 1:
            print("=========================================")
            print("==============GERANDO SENHA===========================")
            Senha.id = checarNumero(fila_normal)
            Senha.tipo = "NORMAL"
            Senha.data = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            fila_normal.append(Senha)
            print("SENHA GERADA COM SUCESSO: ")
            print("Código: ", Senha.id)
            print("Fila: " + Senha.tipo)
            print("Data de abertura: " + Senha.data)
            print("POR FAVOR AGUARDE NA FILA")
            print("TEM ", len(fila_normal)-1, " PESSOAS NA SUA FRENTE")
            if calculoDeTempoMedio() != 0:
                print("TEMPO MÉDIO PARA ATENDIMENTOS: ", calculoDeTempoMedio(), " Minutos \n")
            else:
                print("SEU ATENDIMENTO SERÁ REALIZADO EM BREVE! \n")
        chamadaDeSenha()
        aberturaDeCaixa()
        checagemTempoDeEspera()

        if tipo == 2:
            print("===================================== f====")
            print("==============GERANDO SENHA===========================")
            Senha.id = checarNumero(fila_preferencial)
            Senha.tipo = "PREFERENCIAL"
            Senha.data = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            fila_preferencial.append(Senha)
            print("SENHA GERADA COM SUCESSO: ")
            print("Código: ", Senha.id)
            print("Fila: " + Senha.tipo)
            print("Data de abertura: " + Senha.data)
            print("POR FAVOR AGUARDE NA FILA")
            print("TEM ", len(fila_preferencial)-1, " PESSOAS NA SUA FRENTE")
            if calculoDeTempoMedio() != 0:
                print("TEMPO MÉDIO PARA ATENDIMENTOS: ", calculoDeTempoMedio(), " Minutos \n")
            else:
                print("SEU ATENDIMENTO SERÁ REALIZADO EM BREVE! \n")
        chamadaDeSenha()
        aberturaDeCaixa()
        checagemTempoDeEspera()
