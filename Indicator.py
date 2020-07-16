import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from pandas.util.testing import assert_frame_equal
from matplotlib.dates import date2num

# Name of top 50 stocks of NSE
nifty_50 = ['ADANIPORTS.NS','ASIANPAINT.NS','AXISBANK.NS','BAJAJ-AUTO.NS','BAJAJFINSV.NS','BAJFINANCE.NS','BHARTIARTL.NS','BPCL.NS','BRITANNIA.NS','CIPLA.NS','COALINDIA.NS','DRREDDY.NS','EICHERMOT.NS','GAIL.NS','GRASIM.NS','HCLTECH.NS','HDFC.NS','HDFCBANK.NS','HEROMOTOCO.NS','HINDALCO.NS','HINDUNILVR.NS','ICICIBANK.NS','INDUSINDBK.NS','INFRATEL.NS','INFY.NS','IOC.NS','ITC.NS','JSWSTEEL.NS','KOTAKBANK.NS','LT.NS','M&M.NS','MARUTI.NS','NESTLEIND.NS','NTPC.NS','ONGC.NS','POWERGRID.NS','RELIANCE.NS','SBIN.NS','SUNPHARMA.NS','TATAMOTORS.NS','TATASTEEL.NS','TCS.NS','TECHM.NS','TITAN.NS','ULTRACEMCO.NS','UPL.NS','VEDL.NS','WIPRO.NS','YESBANK.NS','ZEEL.NS']

# Name of top 500 stocks of NSE
nifty_500 = ['3MINDIA.NS','ACC.NS','AIAENG.NS','APLAPOLLO.NS','AUBANK.NS','AARTIIND.NS','AAVAS.NS','ABBOTINDIA.NS','ADANIGAS.NS','ADANIGREEN.NS','ADANIPORTS.NS','ADANIPOWER.NS','ADANITRANS.NS','ABCAPITAL.NS','ABFRL.NS','ADVENZYMES.NS','AEGISCHEM.NS','AFFLE.NS','AJANTPHARM.NS','AKZOINDIA.NS','APLLTD.NS','ALKEM.NS','ALLCARGO.NS','AMARAJABAT.NS','AMBER.NS','AMBUJACEM.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','ARVINDFASN.NS','ASAHIINDIA.NS','ASHOKLEY.NS','ASHOKA.NS','ASIANPAINT.NS','ASTERDM.NS','ASTRAZEN.NS','ASTRAL.NS','ATUL.NS','AUROPHARMA.NS','AVANTIFEED.NS','DMART.NS','AXISBANK.NS','BASF.NS','BEML.NS','BSE.NS','BAJAJ-AUTO.NS','BAJAJCON.NS','BAJAJELEC.NS','BAJFINANCE.NS','BAJAJFINSV.NS','BAJAJHLDNG.NS','BALKRISIND.NS','BALMLAWRIE.NS','BALRAMCHIN.NS','BANDHANBNK.NS','BANKBARODA.NS','BANKINDIA.NS','MAHABANK.NS','BATAINDIA.NS','BAYERCROP.NS','BERGEPAINT.NS','BDL.NS','BEL.NS','BHARATFORG.NS','BHEL.NS','BPCL.NS','BHARTIARTL.NS','INFRATEL.NS','BIOCON.NS','BIRLACORPN.NS','BSOFT.NS','BLISSGVS.NS','BLUEDART.NS','BLUESTARCO.NS','BBTC.NS','BOMDYEING.NS','BOSCHLTD.NS','BRIGADE.NS','BRITANNIA.NS','CARERATING.NS','CCL.NS','CESC.NS','CRISIL.NS','CADILAHC.NS','CANFINHOME.NS','CANBK.NS','CAPLIPOINT.NS','CGCL.NS','CARBORUNIV.NS','CASTROLIND.NS','CEATLTD.NS','CENTRALBK.NS','CDSL.NS','CENTURYPLY.NS','CERA.NS','CHALET.NS','CHAMBLFERT.NS','CHENNPETRO.NS','CHOLAHLDNG.NS','CHOLAFIN.NS','CIPLA.NS','CUB.NS','COALINDIA.NS','COCHINSHIP.NS','COLPAL.NS','CONCOR.NS','COROMANDEL.NS','CREDITACC.NS','CROMPTON.NS','CUMMINSIND.NS','CYIENT.NS','DBCORP.NS','DCBBANK.NS','DCMSHRIRAM.NS','DLF.NS','DABUR.NS','DALBHARAT.NS','DEEPAKNTR.NS','DELTACORP.NS','DHFL.NS','DBL.NS','DISHTV.NS','DCAL.NS','DIVISLAB.NS','DIXON.NS','LALPATHLAB.NS','DRREDDY.NS','EIDPARRY.NS','EIHOTEL.NS','EDELWEISS.NS','EICHERMOT.NS','ELGIEQUIP.NS','EMAMILTD.NS','ENDURANCE.NS','ENGINERSIN.NS','EQUITAS.NS','ERIS.NS','ESCORTS.NS','ESSELPACK.NS','EXIDEIND.NS','FDC.NS','FEDERALBNK.NS','FMGOETZE.NS','FINEORG.NS','FINCABLES.NS','FINPIPE.NS','FSL.NS','FORTIS.NS','FCONSUMER.NS','FLFL.NS','FRETAIL.NS','GAIL.NS','GEPIL.NS','GET&D.NS','GHCL.NS','GMRINFRA.NS','GALAXYSURF.NS','GARFIBRES.NS','GAYAPROJ.NS','GICRE.NS','GILLETTE.NS','GLAXO.NS','GLENMARK.NS','GODFRYPHLP.NS','GODREJAGRO.NS','GODREJCP.NS','GODREJIND.NS','GODREJPROP.NS','GRANULES.NS','GRAPHITE.NS','GRASIM.NS','GESHIP.NS','GREAVESCOT.NS','GRINDWELL.NS','GUJALKALI.NS','GUJGASLTD.NS','GMDCLTD.NS','GNFC.NS','GPPL.NS','GSFC.NS','GSPL.NS','GULFOILLUB.NS','HEG.NS','HCLTECH.NS','HDFCAMC.NS','HDFCBANK.NS','HDFCLIFE.NS','HFCL.NS','HATSUN.NS','HAVELLS.NS','HEIDELBERG.NS','HERITGFOOD.NS','HEROMOTOCO.NS','HEXAWARE.NS','HSCL.NS','HIMATSEIDE.NS','HINDALCO.NS','HAL.NS','HINDCOPPER.NS','HINDPETRO.NS','HINDUNILVR.NS','HINDZINC.NS','HONAUT.NS','HUDCO.NS','HDFC.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','ISEC.NS','ICRA.NS','IDBI.NS','IDFCFIRSTB.NS','IDFC.NS','IFBIND.NS','IFCI.NS','IIFL.NS','IRB.NS','IRCON.NS','ITC.NS','ITDCEM.NS','ITI.NS','INDIACEM.NS','ITDC.NS','IBULHSGFIN.NS','IBULISL.NS','IBREALEST.NS','IBVENTURES.NS','INDIAMART.NS','INDIANB.NS','IEX.NS','INDHOTEL.NS','IOC.NS','IOB.NS','INDOSTAR.NS','IGL.NS','INDUSINDBK.NS','INFIBEAM.NS','NAUKRI.NS','INFY.NS','INOXLEISUR.NS','INTELLECT.NS','INDIGO.NS','IPCALAB.NS','JBCHEPHARM.NS','JKCEMENT.NS','JKLAKSHMI.NS','JKPAPER.NS','JKTYRE.NS','JMFINANCIL.NS','JSWENERGY.NS','JSWSTEEL.NS','JAGRAN.NS','JAICORPLTD.NS','JISLJALEQS.NS','J&KBANK.NS','JAMNAAUTO.NS','JINDALSAW.NS','JSLHISAR.NS','JSL.NS','JINDALSTEL.NS','JCHAC.NS','JUBLFOOD.NS','JUBILANT.NS','JUSTDIAL.NS','JYOTHYLAB.NS','KPRMILL.NS','KEI.NS','KNRCON.NS','KPITTECH.NS','KRBL.NS','KAJARIACER.NS','KALPATPOWR.NS','KANSAINER.NS','KTKBANK.NS','KARURVYSYA.NS','KSCL.NS','KEC.NS','KENNAMET.NS','KIRLOSENG.NS','KOLTEPATIL.NS','KOTAKBANK.NS','L&TFH.NS','LTTS.NS','LICHSGFIN.NS','LAXMIMACH.NS','LAKSHVILAS.NS','LTI.NS','LT.NS','LAURUSLABS.NS','LEMONTREE.NS','LINDEINDIA.NS','LUPIN.NS','LUXIND.NS','MASFIN.NS','MMTC.NS','MOIL.NS','MRF.NS','MAGMA.NS','MGL.NS','MAHSCOOTER.NS','MAHSEAMLES.NS','M&MFIN.NS','M&M.NS','MAHINDCIE.NS','MHRIL.NS','MAHLOG.NS','MANAPPURAM.NS','MRPL.NS','MARICO.NS','MARUTI.NS','MFSL.NS','METROPOLIS.NS','MINDTREE.NS','MINDACORP.NS','MINDAIND.NS','MIDHANI.NS','MOTHERSUMI.NS','MOTILALOFS.NS','MPHASIS.NS','MCX.NS','MUTHOOTFIN.NS','NATCOPHARM.NS','NBCC.NS','NCC.NS','NESCO.NS','NHPC.NS','NIITTECH.NS','NLCINDIA.NS','NMDC.NS','NTPC.NS','NH.NS','NATIONALUM.NS','NFL.NS','NBVENTURES.NS','NAVINFLUOR.NS','NESTLEIND.NS','NETWORK18.NS','NILKAMAL.NS','NAM-INDIA.NS','OBEROIRLTY.NS','ONGC.NS','OIL.NS','OMAXE.NS','OFSS.NS','ORIENTCEM.NS','ORIENTELEC.NS','ORIENTREF.NS','PCJEWELLER.NS','PIIND.NS','PNBHOUSING.NS','PNCINFRA.NS','PTC.NS','PVR.NS','PAGEIND.NS','PARAGMILK.NS','PERSISTENT.NS','PETRONET.NS','PFIZER.NS','PHILIPCARB.NS','PHOENIXLTD.NS','PIDILITIND.NS','PEL.NS','POLYCAB.NS','PFC.NS','POWERGRID.NS','PRAJIND.NS','PRESTIGE.NS','PRSMJOHNSN.NS','PGHL.NS','PGHH.NS','PNB.NS','QUESS.NS','RBLBANK.NS','RECLTD.NS','RITES.NS','RADICO.NS','RVNL.NS','RAIN.NS','RAJESHEXPO.NS','RALLIS.NS','RCF.NS','RATNAMANI.NS','RAYMOND.NS','REDINGTON.NS','RELAXO.NS','RELCAPITAL.NS','RELIANCE.NS','RELINFRA.NS','RPOWER.NS','REPCOHOME.NS','RESPONIND.NS','SHK.NS','SBILIFE.NS','SJVN.NS','SKFINDIA.NS','SRF.NS','SADBHAV.NS','SANOFI.NS','SCHAEFFLER.NS','SIS.NS','SFL.NS','SHILPAMED.NS','SHOPERSTOP.NS','SHREECEM.NS','RENUKA.NS','SHRIRAMCIT.NS','SRTRANSFIN.NS','SIEMENS.NS','SOBHA.NS','SOLARINDS.NS','SONATSOFTW.NS','SOUTHBANK.NS','SPANDANA.NS','SPICEJET.NS','STARCEMENT.NS','SBIN.NS','SAIL.NS','STRTECH.NS','STAR.NS','SUDARSCHEM.NS','SPARC.NS','SUNPHARMA.NS','SUNTV.NS','SUNCLAYLTD.NS','SUNDARMFIN.NS','SUNDRMFAST.NS','SUNTECK.NS','SUPRAJIT.NS','SUPREMEIND.NS','SUZLON.NS','SWANENERGY.NS','SYMPHONY.NS','SYNGENE.NS','TCIEXP.NS','TCNSBRANDS.NS','TTKPRESTIG.NS','TVTODAY.NS','TV18BRDCST.NS','TVSMOTOR.NS','TAKE.NS','TASTYBITE.NS','TCS.NS','TATAELXSI.NS','TATAGLOBAL.NS','TATAINVEST.NS','TATAMTRDVR.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTLBSL.NS','TATASTEEL.NS','TEAMLEASE.NS','TECHM.NS','TECHNOE.NS','NIACL.NS','RAMCOCEM.NS','THERMAX.NS','THYROCARE.NS','TIMETECHNO.NS','TIMKEN.NS','TITAN.NS','TORNTPHARM.NS','TORNTPOWER.NS','TRENT.NS','TRIDENT.NS','TRITURBINE.NS','TIINDIA.NS','UCOBANK.NS','UFLEX.NS','UPL.NS','UJJIVAN.NS','ULTRACEMCO.NS','UNIONBANK.NS','UBL.NS','MCDOWELL-N.NS','VGUARD.NS','VMART.NS','VIPIND.NS','VRLLOG.NS','VSTIND.NS','WABAG.NS','VAIBHAVGBL.NS','VAKRANGEE.NS','VTL.NS','VARROC.NS','VBL.NS','VEDL.NS','VENKEYS.NS','VINATIORGA.NS','IDEA.NS','VOLTAS.NS','WABCOINDIA.NS','WELCORP.NS','WELSPUNIND.NS','WESTLIFE.NS','WHIRLPOOL.NS','WIPRO.NS','WOCKPHARMA.NS','YESBANK.NS','ZEEL.NS','ZENSARTECH.NS','ZYDUSWELL.NS','ECLERX.NS']

# datetime is a pandas function to access data of that particular date
# datetime(year , month , day)
start = datetime(2019,6,7)
end = datetime(2020,10,7)

# web.DataReader helps to access data of a particular stock from the site you want from starting date to ending date
# data = web.DataReader('Stock Name', 'Website', starting date, ending date)
# to see how values are stored in data please print to verify
data = web.DataReader('ACC.NS', 'yahoo', start, end)

# data.reset_index() will shift the Date from Header column to normal column you can print to check
data_reset = data.reset_index()
# This line is compulsory to make Date  column readable to python programme
data_reset['date_ax'] = data_reset['Date'].apply(lambda date: date2num(date))

# putting every column in an individual list
close = data_reset['Close'].to_list()
high = data_reset['High'].to_list()
low = data_reset['Low'].to_list()
openn = data_reset['Open'].to_list()
date = data_reset['Date'].to_list()
dt = data_reset['date_ax'].to_list()


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
#RSI Ends Here

def EMA(close, t):
    sma= 0.0
    n = len(close)
    for i in range(t):
        sma += close[i]
    sma = sma/(t)
    ema = []
    ema.append(sma)
    m = 2/(t+1)
    for i in range(t,n):
        e = close[i]*m + ema[i-t]*(1-m)
        ema.append(e)
    return ema

val = EMA(close, 9)
print(val)
#EMA ends here


# From Here Pivot Points
final_high = []
final_low = []
final_close = []
final_counts = []

def assigning(countt,high_maxx,low_minn,closee):
    final_counts.append(countt)
    final_high.append(high_maxx)
    final_low.append(low_minn)
    final_close.append(closee)

def pivot_points():
    flag = 0
    count = 0
    high_max = 0
    low_min = 320000
    for i in range(len(close)):
        date_st = str(date[i])
        if date_st[5] == "0" and date_st[6] == "1":
            if flag == 12:
                assigning(count,high_max,low_min,close[i-1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min :
                    low_min = low[i]
                flag = 1
                count += 1
        elif date_st[5] == "0" and date_st[6] == "2":
            if flag == 1:
                assigning(count,high_max,low_min,close[i-1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 2
                count += 1
        elif date_st[5] == "0" and date_st[6] == "3":
            if flag == 2:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 3
                count += 1
        elif date_st[5] == "0" and date_st[6] == "4":
            if flag == 3:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 4
                count += 1
        elif date_st[5] == "0" and date_st[6] == "5":
            if flag == 4:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 5
                count += 1
        elif date_st[5] == "0" and date_st[6] == "6":
            if flag == 5:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 6
                count += 1
        elif date_st[5] == "0" and date_st[6] == "7":
            if flag == 6:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 7
                count += 1
        elif date_st[5] == "0" and date_st[6] == "8":
            if flag == 7:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 8
                count += 1
        elif date_st[5] == "0" and date_st[6] == "9":
            if flag == 8:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 9
                count += 1
        elif date_st[5] == "1" and date_st[6] == "0":
            if flag == 9:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 10
                count += 1
        elif date_st[5] == "1" and date_st[6] == "1":
            if flag == 10:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 11
                count += 1
        elif date_st[5] == "1" and date_st[6] == "2":
            if flag == 11:
                assigning(count, high_max, low_min, close[i - 1])
                flag = 0
                count = 0
                high_max = 0
                low_min = 320000
            else:
                if high[i] > high_max:
                    high_max = high[i]
                if low[i] < low_min:
                    low_min = low[i]
                flag = 12
                count += 1

    pivot_point = []
    resistance_1 = []
    resistance_2 = []
    resistance_3 = []
    support_1 = []
    support_2 = []
    support_3 = []
    pivot_point_pr = []
    resistance_1_pr = []
    resistance_2_pr = []
    resistance_3_pr = []
    support_1_pr = []
    support_2_pr = []
    support_3_pr = []

    for i in range(len(final_counts)):
            pivot_point_pr.append((final_high[i]+final_low[i]+final_close[i])/3)
            support_1_pr.append((2*pivot_point_pr[i])-final_high[i])
            resistance_1_pr.append((2*pivot_point_pr[i])-final_low[i])
            support_2_pr.append(pivot_point_pr[i] - final_high[i] + final_low[i])
            resistance_2_pr.append(pivot_point_pr[i] + final_high[i] - final_low[i])
            support_3_pr.append(pivot_point_pr[i] - 2*final_high[i] + 2*final_low[i])
            resistance_3_pr.append(pivot_point_pr[i] + 2*final_high[i] - 2*final_low[i])

    for i in range(final_counts[0]):
        pivot_point.append(0)
        resistance_1.append(0)
        resistance_2.append(0)
        resistance_3.append(0)
        support_1.append(0)
        support_2.append(0)
        support_3.append(0)

    for i in range(1, len(final_counts)):
        for j in range(final_counts[i]):
            pivot_point.append(pivot_point_pr[i])
            resistance_1.append(resistance_1_pr[i])
            resistance_2.append(resistance_2_pr[i])
            resistance_3.append(resistance_3_pr[i])
            support_1.append(support_1_pr[i])
            support_2.append(support_2_pr[i])
            support_3.append(support_3_pr[i])

    print(pivot_point)
    print(support_1)
    print(support_2)
    print(support_3)
    print(resistance_1)
    print(resistance_2)
    print(resistance_3)

pivot_points()
#Pivot Points Ends Here

#MACD Starts From Here
def EMA_MACD(t, macd):
    sma= 0.0
    n = len(macd)
    for i in range(t):
        sma += macd[i]
    sma = sma/(t)
    ema = []
    ema.append(sma)
    m = 2/(t+1)
    for i in range(t,n):
        e = macd[i]*m + ema[i-t]*(1-m)
        ema.append(e)
    return ema

def MACD(x,y,z):
    val_pr = EMA(close, x)
    val2_pr = EMA(close, y)
    val = []
    val2 = []
    for i in range(x):
        val.append(0)
    for i in range(y):
        val2.append(0)

    for i in range(len(val_pr)):
        val.append(val_pr[i])
    for i in range(len(val2_pr)):
        val2.append(val2_pr[i])

    macd_line = []
    macd_histogram = []
    signal_line = []



    for i in range(len(val)):
        macd_line.append(val[i]-val2[i])

    for i in range(z-1):
        signal_line.append(0)

    signal_line_pr = EMA_MACD(z,macd_line)

    for i in range(len(signal_line_pr)):
        signal_line.append(signal_line_pr[i])

    for i in range(len(val)):
        macd_histogram.append(macd_line[i] - signal_line[i])

    print(macd_line)
    print(signal_line)
    print(macd_histogram)

MACD(12,26,9)
#MACD Ends Here