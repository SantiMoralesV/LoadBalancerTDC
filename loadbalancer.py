import math
import random

import random as r
import matplotlib.pyplot as plt
import math as m

input = 50
maxPowerConsumption = 575
maxSpeed = 3.1 # In Ghz
perturbationChance = 0.1
maxPerturbation = 550
perturbationTTL = 3
CPUAmount = 5
iterationAmount = 500
minCPUAmount = 1
maxCPUAmount = 8
maxRPS = 3100 # In Mips
t=0
error = 0
transitionaryState = True
usage = []
requests = []
time = []

class CPU:
    # We used an INTEL Xeon 6960P as reference
    # 72 Cores -> 144 Threats
    # At a maximum 3.1 GHz speed
    # Assuming a IPC=1.0 (Average for Intel Server CPUs) => maxIPS = 3.1GIPS = 3,100 MIPS
    def __init__(self,usage,activeRequests,powerConsumption):
        self.usage = usage
        self.activeRequests = activeRequests #IPS in M (10^6)
        self.speed = 0 #In GHz (10^9 cicles per second)
        self.powerConsumption = powerConsumption
        self.perturbationAmount = 0
        self.perturbationTTL = 0

CPUs = [CPU(0,0,0)]*CPUAmount

# Controllers (Sacamos el derivativo?)
kd = 0.3
kp = 0.75

def totalRequests():
    return sum(C.activeRequests for C in CPUs) # Perturbations stay constant on the CPUs that are handling them

def requestForCPU(requestAmount):
    return m.ceil(requestAmount/len(CPUs))

def GenerateRequests():
    requestAmount = round(r.random()*maxRPS)
    return requestForCPU(requestAmount)

def CalculateUsage(cpu:CPU):
    cpu.usage = (cpu.activeRequests+cpu.perturbationAmount)/maxRPS
    cpu.powerConsumption = maxPowerConsumption * cpu.usage
    cpu.speed = maxSpeed * cpu.usage

def refreshCPUs(requests,perturbations):
    for C in CPUs:  # Assign the requests and refresh the usage
        C.activeRequests = requests
        C.perturbationAmount += perturbations
        if perturbations != 0:
            C.perturbationTTL = round(r.random()*perturbationTTL)
        else:
            C.perturbationTTL = max(C.perturbationTTL-1,0)
        CalculateUsage(C)

def loadbalancer(error): #If a Heavy query is executed it will stay on the CPU that's managing it
    print("entered with error: " + str(error))
    global transitionaryState
    if abs(error) >= 25:
        if not transitionaryState:
            print("The system reached failure state! Aborting")
            return 1
    if 15 <= abs(error) <= 25:# Need to add or delete a CPU
        print("Entered the second")
        transitionaryState = False
        totalError = error * len(CPUs) # Total excess
        CPUdifference = m.ceil(totalError/input) # The amount of CPUs to add or delete
        ActiveRequests = totalRequests() # The total amount of active requests
        if CPUdifference<0: # Need to delete a CPU
            for x in range(abs(CPUdifference)):
                if len(CPUs) > 1:
                    CPUs.pop()
                else: print("Minimum CPU amount of  ("+ str(minCPUAmount) +") reached! no more CPUs will be deactivated"); break;
        else:
            for x in range(abs(CPUdifference)):
                if len(CPUs) < maxCPUAmount:
                    newCPU = CPU(0,0,0)
                    CPUs.append(newCPU)
                else: print("Maximum CPU amount of  ("+ str(maxCPUAmount) +") reached! no more CPUs will be activated"); break;
        CPURequest = requestForCPU(ActiveRequests) # Divide the request between the new amount of CPUs
        refreshCPUs(CPURequest,0)
    return 0

while t<iterationAmount:

    # 30% of the time a random amount of requests is deleted
    if r.random()< 0.3:
        deletedRequest = CPUs[0].activeRequests*0.6*r.random()# Delete a random amount of requests up to 60% of the active requests
        for C in CPUs:
            C = max(C.activeRequests - deletedRequest, 0)

    # Clean perturbations
    if CPUs[0].perturbationTTL == 0:
        for C in CPUs:
            C.perturbationAmount = 0

    # Perturbations that occur because of a spike in the need of CPU usage by  are randomly generated
    perturbation = 0
    if r.random() < perturbationChance:
        perturbation = r.random()*maxPerturbation

    # Generate the incoming requests in this t
    requestPerCPU = GenerateRequests()
    #Refresh the CPUs
    refreshCPUs(requestPerCPU,perturbation)



    # Error signal
    previousError = error
    error = (input/100) - (CPUs[0].usage*100) # All CPUs Have the same usage, this represents the excess of usage in each CPU
    proportionalError = kp*error

    derivativeError = kd*(error-previousError)
    calculatedError = proportionalError+derivativeError

    #Balance the charge
    balanceResult = loadbalancer(calculatedError)
    usage.append(CPUs[0].usage)
    time.append(t)
    if (not transitionaryState) & balanceResult == 1 :
        print("breaks here")
        break



    print(t)
    t += 1

plt.figure(figsize=(10, 6))
plt.plot(time, usage, label="CPU Usage (%)", color="blue", marker="o")
plt.title("CPU Usage Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("CPU Usage (%)")
plt.grid(True)
plt.legend()
plt.show()

