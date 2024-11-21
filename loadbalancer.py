import random

import random as r
#import matplotlib.pyplot as plt
import math as m

input = 2.5
perturbationChance = 0.1
CPUAmount = 5
iterationAmount = 500
minCPUAmount = 1
maxCPUAmount = 10
t=0
maxRequestPerCPU = 1500
maxRPS = 500

class CPU:
    def __init__(self,usage,ActiveRequests):
        self.usage = usage
        self.ActiveRequests = ActiveRequests
        self.maxRequests = maxRequestPerCPU
        self.perturbationPercentage = 0
        self.perturbationTTL = 0

CPUs = [CPU(0,0)]*CPUAmount


#Range = (input-15%,input+15%)
acceptableRange = 0.15
#Range = (input-25%,input-15%)U(input+15%,input+25%)
errorRange = 0.25
# The rest is considered failure

# Controllers
kd = 0.3
kp = 0.75

def CPUUsageToVolts(usage):
    return usage*5.0

def VoltsToCPUUsage(volts):
    return volts/5.0

def GenerateRequests():
    requestAmount = round(r.random()*maxRPS)
    return round(requestAmount / CPUAmount)

def loadbalancer(requestAmountPerCPU):
    return 0
while (t<iterationAmount):
    #30% of the time a random amount of requests is deleted
    if (r.random()< 0.3):
        deletedRequest = GenerateRequests()
        for CPU in CPUs:
            CPU = max(CPU.ActiveRequests - deletedRequest, 0)

    #Un random determina si hay una perturbacion disparando en cierto porcentaje el uso del CPU
    #Cada iteracion decremento el TTL hasta que llega a 0 borrando la perturbacion

    print("hola")
    requestAmountPerCPU = GenerateRequests()
    loadbalancer(requestAmountPerCPU)