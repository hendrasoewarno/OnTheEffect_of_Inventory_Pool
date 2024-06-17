#on the effect of inventory pool
#https://ddu.ext.unb.ca/4690/Lecture_notes/Lec3.pdf
#https://www.scribd.com/doc/266473289/Crack-the-Code-Safety-Stock
import math
import numpy as np
import statistics

np.random.seed(500)

#paramter
num_samples=10000
num_of_location=2

#time increment for calculating standard deviasi of demand 
T1= 1 #month

#performance cycle, another term of (periodic review+leadtime)
review_period = 1 #month
lead_time = 0.5 #2 week
PC=review_period+lead_time

mean=10 #per-month
cov=1.5
std_dev_demand=mean*cov

service_level = 0.95
z_score = statistics.NormalDist().inv_cdf(service_level)

#Demand during leadtime
mean_DDLT = PC/T1*mean
std_dev_DDLT = math.sqrt(PC/T1)*std_dev_demand

#decentralized
safety_stock = np.round(z_score * math.sqrt(PC/T1) * std_dev_demand)
reorder_point = mean*PC/T1 + safety_stock

#centralized
pool_safety_stock = np.round(z_score * math.sqrt(PC/T1) * math.sqrt((std_dev_demand**2)*num_of_location))
pool_reorder_point = mean*PC/T1*num_of_location + pool_safety_stock

#generate DDLT for each location
loc_DDLT=[]
for i in range(num_of_location):
    DDLT = np.round(np.random.normal(mean_DDLT, std_dev_DDLT, num_samples))
    loc_DDLT.append(DDLT)

#centralized performance
pool_fill_rate = []
stockout = 0
for i in range(num_samples):
    #sum DDLT from each location
    total_DDLT = sum([(0 if DDLT[i]<0 else DDLT[i]) for DDLT in loc_DDLT])
    
    if pool_reorder_point > total_DDLT:
        pool_fill_rate.append(1)
    else:
        pool_fill_rate.append(pool_reorder_point/total_DDLT)
        stockout +=1
        
print("Centralized Performance")       
print("Total Safety Stock", pool_safety_stock)
print("Fill Rate", statistics.mean(pool_fill_rate))
print("Service Level", 1-stockout/num_samples)        

#decentralized performance
loc_fill_rate = []
loc_stockout = []
for loc in range(num_of_location):
    fill_rate = []
    stockout = 0
    for i in range(num_samples):    
        DDLT = 0 if loc_DDLT[loc][i]<0 else loc_DDLT[loc][i]
        
        if reorder_point > DDLT:
            fill_rate.append(1)
        else:
            fill_rate.append(reorder_point/DDLT)
            stockout +=1
            
    loc_fill_rate.append(fill_rate)
    loc_stockout.append(stockout)

print("Decentralized Performance")
print("Total Safety Stock", safety_stock*num_of_location) 
for loc in range(num_of_location):
    print("Location", loc+1)
    print("Fill Rate", statistics.mean(loc_fill_rate[loc]))
    print("Service Level", 1-loc_stockout[loc]/num_samples)