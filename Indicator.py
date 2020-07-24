import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from pandas.util.testing import assert_frame_equal
from matplotlib.dates import date2num
import math

# Name of top 50 stocks of NSE
nifty_50 = ['ADANIPORTS.NS','ASIANPAINT.NS','AXISBANK.NS','BAJAJ-AUTO.NS','BAJAJFINSV.NS','BAJFINANCE.NS','BHARTIARTL.NS','BPCL.NS','BRITANNIA.NS','CIPLA.NS','COALINDIA.NS','DRREDDY.NS','EICHERMOT.NS','GAIL.NS','GRASIM.NS','HCLTECH.NS','HDFC.NS','HDFCBANK.NS','HEROMOTOCO.NS','HINDALCO.NS','HINDUNILVR.NS','ICICIBANK.NS','INDUSINDBK.NS','INFRATEL.NS','INFY.NS','IOC.NS','ITC.NS','JSWSTEEL.NS','KOTAKBANK.NS','LT.NS','M&M.NS','MARUTI.NS','NESTLEIND.NS','NTPC.NS','ONGC.NS','POWERGRID.NS','RELIANCE.NS','SBIN.NS','SUNPHARMA.NS','TATAMOTORS.NS','TATASTEEL.NS','TCS.NS','TECHM.NS','TITAN.NS','ULTRACEMCO.NS','UPL.NS','VEDL.NS','WIPRO.NS','YESBANK.NS','ZEEL.NS']

# Name of top 500 stocks of NSE
nifty_500 = ['3MINDIA.NS','ACC.NS','AIAENG.NS','APLAPOLLO.NS','AUBANK.NS','AARTIIND.NS','AAVAS.NS','ABBOTINDIA.NS','ADANIGAS.NS','ADANIGREEN.NS','ADANIPORTS.NS','ADANIPOWER.NS','ADANITRANS.NS','ABCAPITAL.NS','ABFRL.NS','ADVENZYMES.NS','AEGISCHEM.NS','AFFLE.NS','AJANTPHARM.NS','AKZOINDIA.NS','APLLTD.NS','ALKEM.NS','ALLCARGO.NS','AMARAJABAT.NS','AMBER.NS','AMBUJACEM.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','ARVINDFASN.NS','ASAHIINDIA.NS','ASHOKLEY.NS','ASHOKA.NS','ASIANPAINT.NS','ASTERDM.NS','ASTRAZEN.NS','ASTRAL.NS','ATUL.NS','AUROPHARMA.NS','AVANTIFEED.NS','DMART.NS','AXISBANK.NS','BASF.NS','BEML.NS','BSE.NS','BAJAJ-AUTO.NS','BAJAJCON.NS','BAJAJELEC.NS','BAJFINANCE.NS','BAJAJFINSV.NS','BAJAJHLDNG.NS','BALKRISIND.NS','BALMLAWRIE.NS','BALRAMCHIN.NS','BANDHANBNK.NS','BANKBARODA.NS','BANKINDIA.NS','MAHABANK.NS','BATAINDIA.NS','BAYERCROP.NS','BERGEPAINT.NS','BDL.NS','BEL.NS','BHARATFORG.NS','BHEL.NS','BPCL.NS','BHARTIARTL.NS','INFRATEL.NS','BIOCON.NS','BIRLACORPN.NS','BSOFT.NS','BLISSGVS.NS','BLUEDART.NS','BLUESTARCO.NS','BBTC.NS','BOMDYEING.NS','BOSCHLTD.NS','BRIGADE.NS','BRITANNIA.NS','CARERATING.NS','CCL.NS','CESC.NS','CRISIL.NS','CADILAHC.NS','CANFINHOME.NS','CANBK.NS','CAPLIPOINT.NS','CGCL.NS','CARBORUNIV.NS','CASTROLIND.NS','CEATLTD.NS','CENTRALBK.NS','CDSL.NS','CENTURYPLY.NS','CERA.NS','CHALET.NS','CHAMBLFERT.NS','CHENNPETRO.NS','CHOLAHLDNG.NS','CHOLAFIN.NS','CIPLA.NS','CUB.NS','COALINDIA.NS','COCHINSHIP.NS','COLPAL.NS','CONCOR.NS','COROMANDEL.NS','CREDITACC.NS','CROMPTON.NS','CUMMINSIND.NS','CYIENT.NS','DBCORP.NS','DCBBANK.NS','DCMSHRIRAM.NS','DLF.NS','DABUR.NS','DALBHARAT.NS','DEEPAKNTR.NS','DELTACORP.NS','DHFL.NS','DBL.NS','DISHTV.NS','DCAL.NS','DIVISLAB.NS','DIXON.NS','LALPATHLAB.NS','DRREDDY.NS','EIDPARRY.NS','EIHOTEL.NS','EDELWEISS.NS','EICHERMOT.NS','ELGIEQUIP.NS','EMAMILTD.NS','ENDURANCE.NS','ENGINERSIN.NS','EQUITAS.NS','ERIS.NS','ESCORTS.NS','ESSELPACK.NS','EXIDEIND.NS','FDC.NS','FEDERALBNK.NS','FMGOETZE.NS','FINEORG.NS','FINCABLES.NS','FINPIPE.NS','FSL.NS','FORTIS.NS','FCONSUMER.NS','FLFL.NS','FRETAIL.NS','GAIL.NS','GEPIL.NS','GET&D.NS','GHCL.NS','GMRINFRA.NS','GALAXYSURF.NS','GARFIBRES.NS','GAYAPROJ.NS','GICRE.NS','GILLETTE.NS','GLAXO.NS','GLENMARK.NS','GODFRYPHLP.NS','GODREJAGRO.NS','GODREJCP.NS','GODREJIND.NS','GODREJPROP.NS','GRANULES.NS','GRAPHITE.NS','GRASIM.NS','GESHIP.NS','GREAVESCOT.NS','GRINDWELL.NS','GUJALKALI.NS','GUJGASLTD.NS','GMDCLTD.NS','GNFC.NS','GPPL.NS','GSFC.NS','GSPL.NS','GULFOILLUB.NS','HEG.NS','HCLTECH.NS','HDFCAMC.NS','HDFCBANK.NS','HDFCLIFE.NS','HFCL.NS','HATSUN.NS','HAVELLS.NS','HEIDELBERG.NS','HERITGFOOD.NS','HEROMOTOCO.NS','HEXAWARE.NS','HSCL.NS','HIMATSEIDE.NS','HINDALCO.NS','HAL.NS','HINDCOPPER.NS','HINDPETRO.NS','HINDUNILVR.NS','HINDZINC.NS','HONAUT.NS','HUDCO.NS','HDFC.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','ISEC.NS','ICRA.NS','IDBI.NS','IDFCFIRSTB.NS','IDFC.NS','IFBIND.NS','IFCI.NS','IIFL.NS','IRB.NS','IRCON.NS','ITC.NS','ITDCEM.NS','ITI.NS','INDIACEM.NS','ITDC.NS','IBULHSGFIN.NS','IBULISL.NS','IBREALEST.NS','IBVENTURES.NS','INDIAMART.NS','INDIANB.NS','IEX.NS','INDHOTEL.NS','IOC.NS','IOB.NS','INDOSTAR.NS','IGL.NS','INDUSINDBK.NS','INFIBEAM.NS','NAUKRI.NS','INFY.NS','INOXLEISUR.NS','INTELLECT.NS','INDIGO.NS','IPCALAB.NS','JBCHEPHARM.NS','JKCEMENT.NS','JKLAKSHMI.NS','JKPAPER.NS','JKTYRE.NS','JMFINANCIL.NS','JSWENERGY.NS','JSWSTEEL.NS','JAGRAN.NS','JAICORPLTD.NS','JISLJALEQS.NS','J&KBANK.NS','JAMNAAUTO.NS','JINDALSAW.NS','JSLHISAR.NS','JSL.NS','JINDALSTEL.NS','JCHAC.NS','JUBLFOOD.NS','JUBILANT.NS','JUSTDIAL.NS','JYOTHYLAB.NS','KPRMILL.NS','KEI.NS','KNRCON.NS','KPITTECH.NS','KRBL.NS','KAJARIACER.NS','KALPATPOWR.NS','KANSAINER.NS','KTKBANK.NS','KARURVYSYA.NS','KSCL.NS','KEC.NS','KENNAMET.NS','KIRLOSENG.NS','KOLTEPATIL.NS','KOTAKBANK.NS','L&TFH.NS','LTTS.NS','LICHSGFIN.NS','LAXMIMACH.NS','LAKSHVILAS.NS','LTI.NS','LT.NS','LAURUSLABS.NS','LEMONTREE.NS','LINDEINDIA.NS','LUPIN.NS','LUXIND.NS','MASFIN.NS','MMTC.NS','MOIL.NS','MRF.NS','MAGMA.NS','MGL.NS','MAHSCOOTER.NS','MAHSEAMLES.NS','M&MFIN.NS','M&M.NS','MAHINDCIE.NS','MHRIL.NS','MAHLOG.NS','MANAPPURAM.NS','MRPL.NS','MARICO.NS','MARUTI.NS','MFSL.NS','METROPOLIS.NS','MINDTREE.NS','MINDACORP.NS','MINDAIND.NS','MIDHANI.NS','MOTHERSUMI.NS','MOTILALOFS.NS','MPHASIS.NS','MCX.NS','MUTHOOTFIN.NS','NATCOPHARM.NS','NBCC.NS','NCC.NS','NESCO.NS','NHPC.NS','NIITTECH.NS','NLCINDIA.NS','NMDC.NS','NTPC.NS','NH.NS','NATIONALUM.NS','NFL.NS','NBVENTURES.NS','NAVINFLUOR.NS','NESTLEIND.NS','NETWORK18.NS','NILKAMAL.NS','NAM-INDIA.NS','OBEROIRLTY.NS','ONGC.NS','OIL.NS','OMAXE.NS','OFSS.NS','ORIENTCEM.NS','ORIENTELEC.NS','ORIENTREF.NS','PCJEWELLER.NS','PIIND.NS','PNBHOUSING.NS','PNCINFRA.NS','PTC.NS','PVR.NS','PAGEIND.NS','PARAGMILK.NS','PERSISTENT.NS','PETRONET.NS','PFIZER.NS','PHILIPCARB.NS','PHOENIXLTD.NS','PIDILITIND.NS','PEL.NS','POLYCAB.NS','PFC.NS','POWERGRID.NS','PRAJIND.NS','PRESTIGE.NS','PRSMJOHNSN.NS','PGHL.NS','PGHH.NS','PNB.NS','QUESS.NS','RBLBANK.NS','RECLTD.NS','RITES.NS','RADICO.NS','RVNL.NS','RAIN.NS','RAJESHEXPO.NS','RALLIS.NS','RCF.NS','RATNAMANI.NS','RAYMOND.NS','REDINGTON.NS','RELAXO.NS','RELCAPITAL.NS','RELIANCE.NS','RELINFRA.NS','RPOWER.NS','REPCOHOME.NS','RESPONIND.NS','SHK.NS','SBILIFE.NS','SJVN.NS','SKFINDIA.NS','SRF.NS','SADBHAV.NS','SANOFI.NS','SCHAEFFLER.NS','SIS.NS','SFL.NS','SHILPAMED.NS','SHOPERSTOP.NS','SHREECEM.NS','RENUKA.NS','SHRIRAMCIT.NS','SRTRANSFIN.NS','SIEMENS.NS','SOBHA.NS','SOLARINDS.NS','SONATSOFTW.NS','SOUTHBANK.NS','SPANDANA.NS','SPICEJET.NS','STARCEMENT.NS','SBIN.NS','SAIL.NS','STRTECH.NS','STAR.NS','SUDARSCHEM.NS','SPARC.NS','SUNPHARMA.NS','SUNTV.NS','SUNCLAYLTD.NS','SUNDARMFIN.NS','SUNDRMFAST.NS','SUNTECK.NS','SUPRAJIT.NS','SUPREMEIND.NS','SUZLON.NS','SWANENERGY.NS','SYMPHONY.NS','SYNGENE.NS','TCIEXP.NS','TCNSBRANDS.NS','TTKPRESTIG.NS','TVTODAY.NS','TV18BRDCST.NS','TVSMOTOR.NS','TAKE.NS','TASTYBITE.NS','TCS.NS','TATAELXSI.NS','TATAGLOBAL.NS','TATAINVEST.NS','TATAMTRDVR.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTLBSL.NS','TATASTEEL.NS','TEAMLEASE.NS','TECHM.NS','TECHNOE.NS','NIACL.NS','RAMCOCEM.NS','THERMAX.NS','THYROCARE.NS','TIMETECHNO.NS','TIMKEN.NS','TITAN.NS','TORNTPHARM.NS','TORNTPOWER.NS','TRENT.NS','TRIDENT.NS','TRITURBINE.NS','TIINDIA.NS','UCOBANK.NS','UFLEX.NS','UPL.NS','UJJIVAN.NS','ULTRACEMCO.NS','UNIONBANK.NS','UBL.NS','MCDOWELL-N.NS','VGUARD.NS','VMART.NS','VIPIND.NS','VRLLOG.NS','VSTIND.NS','WABAG.NS','VAIBHAVGBL.NS','VAKRANGEE.NS','VTL.NS','VARROC.NS','VBL.NS','VEDL.NS','VENKEYS.NS','VINATIORGA.NS','IDEA.NS','VOLTAS.NS','WABCOINDIA.NS','WELCORP.NS','WELSPUNIND.NS','WESTLIFE.NS','WHIRLPOOL.NS','WIPRO.NS','WOCKPHARMA.NS','YESBANK.NS','ZEEL.NS','ZENSARTECH.NS','ZYDUSWELL.NS','ECLERX.NS']

# datetime is a pandas function to access data of that particular date
# datetime(year , month , day)
start = datetime(2019,8,6)
end = datetime(2020,7,16)

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
volume = data_reset['Volume'].to_list()
def RSI(close, t):
    n = len(close)
    rsi = []
    Ups = 0.0
    Downs = 0.0
    for j in range(t-1):
        rsi.append(-1)
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
#SMA starts here

def SMA(close, t):
    mas = []
    for i in range(t - 1):
        mas.append(0)
    for i in range(len(close) - t + 1):
        sum = 0
        for j in range(i, t + i):
            sum = sum + close[j]
        meann = sum / t
        mas.append(meann)
    return mas

    #SMA Ends here
def EMA(close, t):
    sma= 0.0
    n = len(close)
    for i in range(t):
        sma += close[i]
    sma = sma/(t)
    ema = []
    for j in range(t-1):
        ema.append(0)
    ema.append(sma)
    m = 2/(t+1)
    for i in range(t,n):
        e = close[i]*m + ema[i-t]*(1-m)
        ema.append(e)
    return ema
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
            support_3_pr.append(support_1_pr[i] - final_high[i] + final_low[i])
            resistance_3_pr.append(resistance_1_pr[i] + final_high[i] - final_low[i])
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
    return pivot_point,support_1,support_2,support_3,resistance_1,resistance_2,resistance_3

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
    return macd_line,signal_line,macd_histogram
#MACD Ends Here

#Bollinger Band Starts Here
def bollinger_band(close,n,r):
    up = []
    lo = []
    ma = []
    for i in range(n-1):
        up.append(0)
        lo.append(0)
        ma.append(0)
    for i in range(len(close)-n+1):
        sum = 0
        sqr = 0
        for j in range(i, n+i):
            sum = sum + close[j]
        meann = sum/n
        ma.append(sum / n)
        for z in range(i, n+i):
            sq = close[z]-meann
            sqr = sqr + (sq*sq)
        varr = sqr/n
        std = math.sqrt(varr)
        up.append(meann + (r*std))
        lo.append(meann - (r*std))
    return up,lo,ma

#Bollinger Band Ends here

#Fibonacci Retracement start here
def fib_retracement(p1, p2):
    list =[0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]
    dict = {}
    dist = p2 - p1
    for val in list:
        dict[str(val) ] =  (p2 - dist*val)
    return dict
#Fibonacci Retracement ends here

#Money Flow Index starts here
def MFI(t):
    mfi = []        #money flow index
    typ = []        #typical price
    raw_money = []  #raw money flow
    mfr = []        #money flow ratio
    for i in range(t):
        mfi.append(0)
        mfr.append(0)
    ind = 1
    typ.append( (high[0] + low[0] + close[0]) / 3)
    raw_money.append(typ[0]*volume[0])  #first time assume it is positive

    for i in range(1,len(close)):
        typ.append( (high[i] + low[i] + close[i])/3 )
        if(typ[ind] > typ[ind-1]):
            raw_money.append( typ[i]*volume[i]  )
        else:
            raw_money.append( -typ[i]*volume[i]  )
        ind = ind + 1
    for i in range(t, len(close)):
        positive_flows = 0.0
        negative_flows = 0.0
        for j in range(t):
            if(raw_money[i-j] > 0):
                positive_flows += raw_money[i-j]
            else:
                negative_flows += -raw_money[i-j]
        if(negative_flows != 0):        ratio = positive_flows/negative_flows
        else:                           ratio = positive_flows
        mfr.append( ratio )
        mfi.append( (100- (100/(1+ratio)) ) )
    return mfi
#Money Flow Index ends here



# Stochastic Rsi Starts ahi thi


def Rsi_high(high, t):

   rsi_H = []
   for i in range(0,t-1):
        rsi_H.append(-1)


   i = 0
   for j in range(t, len(high)+1):
        HIGH = high[i:t]
        rsi_H.append(max(HIGH))
        t += 1
        i += 1

   return rsi_H



def Rsi_low(low, t):

   rsi_L = []
   for i in range(0,t-1):
        rsi_L.append(-1)

   i = 0

   for j in range(t, len(low) + 1):
        if low!=-1:
            LOW = low[i:t]
            rsi_L.append(min(LOW))
            t += 1
            i += 1

   return rsi_L

def stoch(source, high, low, t,rt):
    rsi_high = []
    rsi_low = []

    rsi_low = Rsi_low(high, t)
    rsi_high = Rsi_high(low, t)

    count=0
    for x in rsi_low:
        if(x==-1):
            count+=1

    Stochastic=[]
    for i in range(0,count):
        Stochastic.append(-1)

    cnt=0
    rsi=RSI(close,rt)
    for i in range(count,(len(source))):
        y=(rsi[i]-rsi_low[i])
        z=(rsi_high[i]-rsi_low[i])
        w=y/z
        Stochastic.append(w*100)
        cnt+=1


    return Stochastic,count

def sma(rsi,t,count):
    x=[]
    cnt=0
    for i in range(0,count):
        x.append(-1)
        cnt+=1
    for i in range(t-1):
        x.append(-1)
        cnt += 1

    cnt+=1
    cnt1=cnt

    for i in range(cnt,len(rsi)+1):
        temp=rsi[cnt1-t:cnt1]
        sum=0.0000
        for j in temp:
            sum=sum+j

        sum=sum/t
        cnt1+=1
        del temp
        x.append(sum)


    return x


def S_RSI(Close, t, K, D, rt):
    # rt=rsi peroid
    # t=Stochastic Rsi Period
    # K=main line
    # D= moving average of K

    rsi =RSI(Close, rt)
    Stochstic,count=stoch(rsi, rsi, rsi,t,rt)
    k = sma(Stochstic,K,count)
    d = sma(k,D,count)

    return k,d

    #k= blue line on trading view
    #d= orange line on trading view

# Stochastic Rsi Ends Here


