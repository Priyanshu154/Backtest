import data_of_stocks

#generally we take the closing prices to calculate rsi but we will soon make it flexible
close = data_of_stocks.close

"""
Maine iss link se sikha tha formula:  https://www.macroption.com/rsi-calculation/
Example of the formula:               https://www.macroption.com/rsi-calculator/
RSI = 100 - (100/(1+rs))
where 
    rs = (avg Ups)/(avg Downs)
    avgUPs matlab averagly stock kitna up move kiya (close[i] > close[i-1])
    avgDowns "      "       "     "    downn " "    (close[i] < close[i-1])
Now 
   To calculate avgUps/avgDowns, three methods are there:
        1. Simple Moving average
        2. Exponential Moving average
        3. Wilder Smoothing method
   popular sites like tradingview uses the third one so we will also opt for third one
   
   To calculate rsi using the third method:
        for i in range(t, n):
            diff = close[i]- close[i-1] 
            if(diff > 0):
               avgUps = (1/t)*diff + ( (t-1)/(t) )*prev_avgUps
               avgDowns =( (t-1)/(t) )*prev_avgUps
            else:
               avgUps =( (t-1)/(t) )*prev_avgUps
               avgDowns = (1/t)*(-diff) + ( (t-1)/(t) )*prev_avgUps            
            rs = avgUps/avgDowns
            rsi = ( 100 - (100/(1+rs)) ) 
            //Yaha tak ek din ka rsi mila isme loop chalaya hai to rsi array bana dene ki 
        where
            t is the time period (generally 14)
            prev_avgUps uske piche wala avgUp
            diff = difference of the values of current and previous price            
        ab puchoge first time loop me prev_avgUps ki value kya hogi?:
            first time prev_avgUps ki value simply pichle t days ka simple average
        Aiye code dekhte hai aur isme dekhenge konsi line kis step ko belong karti hai
"""
def RSI(t):
    n = len(close)
    rsi = []
    avgU = []
    avgD = []
    Ups = 0.0
    Downs = 0.0
    #Ye sabse pehla avgU/avgD find karne ke liye simple average vala step
    for i in range(1,t):
        diff = close[i] - close[i-1]
        if(diff > 0):
            Ups += diff
        else:
            Downs += (-diff)

    preU = Ups/t
    preD = Downs/t
    #simple average mil gaya to hamara pehla rsi bi mil gaya
    rs = preU/preD
    rsi.append( (100 - (100/(1+rs))) )

    #yaha se prev_avgUp vala loop
    Ups = 0.0
    Downs = 0.0
    for i in range(t,n):
        diff = close[i] - close[i-1]
        if(diff > 0):
            Ups = diff
            Downs = 0.0
        else:
            Downs = (-diff)
            Ups = 0.0
        u = (1/t)*Ups + ((t-1)/t)*preU
        d = (1/t)*Downs + ((t-1)/t)*preD
        preU = u    #Update previous-Up and previous-Down
        preD = d
        rs = u/d
        rsi.append( (100 - (100/(1+rs))) )   #RSI for a particular date
    return rsi


val = RSI(14)
print(val)