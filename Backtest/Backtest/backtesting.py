import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from matplotlib.dates import date2num
from . import Indicator
import statistics

# Name of top 500 stocks of NSE
nifty_500 = ['3MINDIA.NS', 'ACC.NS', 'AIAENG.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'AARTIIND.NS', 'AAVAS.NS',
             'ABBOTINDIA.NS', 'ADANIGAS.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ADANITRANS.NS',
             'ABCAPITAL.NS', 'ABFRL.NS', 'ADVENZYMES.NS', 'AEGISCHEM.NS', 'AFFLE.NS', 'AJANTPHARM.NS', 'AKZOINDIA.NS',
             'APLLTD.NS', 'ALKEM.NS', 'ALLCARGO.NS', 'AMARAJABAT.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS',
             'APOLLOTYRE.NS', 'ARVINDFASN.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASHOKA.NS', 'ASIANPAINT.NS',
             'ASTERDM.NS', 'ASTRAZEN.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUROPHARMA.NS', 'AVANTIFEED.NS', 'DMART.NS',
             'AXISBANK.NS', 'BASF.NS', 'BEML.NS', 'BSE.NS', 'BAJAJ-AUTO.NS', 'BAJAJCON.NS', 'BAJAJELEC.NS',
             'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BALKRISIND.NS', 'BALMLAWRIE.NS', 'BALRAMCHIN.NS',
             'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'MAHABANK.NS', 'BATAINDIA.NS', 'BAYERCROP.NS',
             'BERGEPAINT.NS', 'BDL.NS', 'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'INFRATEL.NS',
             'BIOCON.NS', 'BIRLACORPN.NS', 'BSOFT.NS', 'BLISSGVS.NS', 'BLUEDART.NS', 'BLUESTARCO.NS', 'BBTC.NS',
             'BOMDYEING.NS', 'BOSCHLTD.NS', 'BRIGADE.NS', 'BRITANNIA.NS', 'CARERATING.NS', 'CCL.NS', 'CESC.NS',
             'CRISIL.NS', 'CADILAHC.NS', 'CANFINHOME.NS', 'CANBK.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CARBORUNIV.NS',
             'CASTROLIND.NS', 'CEATLTD.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CENTURYPLY.NS', 'CERA.NS', 'CHALET.NS',
             'CHAMBLFERT.NS', 'CHENNPETRO.NS', 'CHOLAHLDNG.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'CUB.NS', 'COALINDIA.NS',
             'COCHINSHIP.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CUMMINSIND.NS',
             'CYIENT.NS', 'DBCORP.NS', 'DCBBANK.NS', 'DCMSHRIRAM.NS', 'DLF.NS', 'DABUR.NS', 'DALBHARAT.NS',
             'DEEPAKNTR.NS', 'DELTACORP.NS', 'DHFL.NS', 'DBL.NS', 'DISHTV.NS', 'DCAL.NS', 'DIVISLAB.NS', 'DIXON.NS',
             'LALPATHLAB.NS', 'DRREDDY.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EDELWEISS.NS', 'EICHERMOT.NS', 'ELGIEQUIP.NS',
             'EMAMILTD.NS', 'ENDURANCE.NS', 'ENGINERSIN.NS', 'EQUITAS.NS', 'ERIS.NS', 'ESCORTS.NS', 'ESSELPACK.NS',
             'EXIDEIND.NS', 'FDC.NS', 'FEDERALBNK.NS', 'FMGOETZE.NS', 'FINEORG.NS', 'FINCABLES.NS', 'FINPIPE.NS',
             'FSL.NS', 'FORTIS.NS', 'FCONSUMER.NS', 'FLFL.NS', 'FRETAIL.NS', 'GAIL.NS', 'GEPIL.NS', 'GET&D.NS',
             'GHCL.NS', 'GMRINFRA.NS', 'GALAXYSURF.NS', 'GARFIBRES.NS', 'GAYAPROJ.NS', 'GICRE.NS', 'GILLETTE.NS',
             'GLAXO.NS', 'GLENMARK.NS', 'GODFRYPHLP.NS', 'GODREJAGRO.NS', 'GODREJCP.NS', 'GODREJIND.NS',
             'GODREJPROP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GRASIM.NS', 'GESHIP.NS', 'GREAVESCOT.NS', 'GRINDWELL.NS',
             'GUJALKALI.NS', 'GUJGASLTD.NS', 'GMDCLTD.NS', 'GNFC.NS', 'GPPL.NS', 'GSFC.NS', 'GSPL.NS', 'GULFOILLUB.NS',
             'HEG.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HFCL.NS', 'HATSUN.NS', 'HAVELLS.NS',
             'HEIDELBERG.NS', 'HERITGFOOD.NS', 'HEROMOTOCO.NS', 'HEXAWARE.NS', 'HSCL.NS', 'HIMATSEIDE.NS',
             'HINDALCO.NS', 'HAL.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'HONAUT.NS',
             'HUDCO.NS', 'HDFC.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'ISEC.NS', 'ICRA.NS', 'IDBI.NS',
             'IDFCFIRSTB.NS', 'IDFC.NS', 'IFBIND.NS', 'IFCI.NS', 'IIFL.NS', 'IRB.NS', 'IRCON.NS', 'ITC.NS', 'ITDCEM.NS',
             'ITI.NS', 'INDIACEM.NS', 'ITDC.NS', 'IBULHSGFIN.NS', 'IBULISL.NS', 'IBREALEST.NS', 'IBVENTURES.NS',
             'INDIAMART.NS', 'INDIANB.NS', 'IEX.NS', 'INDHOTEL.NS', 'IOC.NS', 'IOB.NS', 'INDOSTAR.NS', 'IGL.NS',
             'INDUSINDBK.NS', 'INFIBEAM.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXLEISUR.NS', 'INTELLECT.NS', 'INDIGO.NS',
             'IPCALAB.NS', 'JBCHEPHARM.NS', 'JKCEMENT.NS', 'JKLAKSHMI.NS', 'JKPAPER.NS', 'JKTYRE.NS', 'JMFINANCIL.NS',
             'JSWENERGY.NS', 'JSWSTEEL.NS', 'JAGRAN.NS', 'JAICORPLTD.NS', 'JISLJALEQS.NS', 'J&KBANK.NS', 'JAMNAAUTO.NS',
             'JINDALSAW.NS', 'JSLHISAR.NS', 'JSL.NS', 'JINDALSTEL.NS', 'JCHAC.NS', 'JUBLFOOD.NS', 'JUBILANT.NS',
             'JUSTDIAL.NS', 'JYOTHYLAB.NS', 'KPRMILL.NS', 'KEI.NS', 'KNRCON.NS', 'KPITTECH.NS', 'KRBL.NS',
             'KAJARIACER.NS', 'KALPATPOWR.NS', 'KANSAINER.NS', 'KTKBANK.NS', 'KARURVYSYA.NS', 'KSCL.NS', 'KEC.NS',
             'KENNAMET.NS', 'KIRLOSENG.NS', 'KOLTEPATIL.NS', 'KOTAKBANK.NS', 'L&TFH.NS', 'LTTS.NS', 'LICHSGFIN.NS',
             'LAXMIMACH.NS', 'LAKSHVILAS.NS', 'LTI.NS', 'LT.NS', 'LAURUSLABS.NS', 'LEMONTREE.NS', 'LINDEINDIA.NS',
             'LUPIN.NS', 'LUXIND.NS', 'MASFIN.NS', 'MMTC.NS', 'MOIL.NS', 'MRF.NS', 'MAGMA.NS', 'MGL.NS',
             'MAHSCOOTER.NS', 'MAHSEAMLES.NS', 'M&MFIN.NS', 'M&M.NS', 'MAHINDCIE.NS', 'MHRIL.NS', 'MAHLOG.NS',
             'MANAPPURAM.NS', 'MRPL.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'METROPOLIS.NS', 'MINDTREE.NS',
             'MINDACORP.NS', 'MINDAIND.NS', 'MIDHANI.NS', 'MOTHERSUMI.NS', 'MOTILALOFS.NS', 'MPHASIS.NS', 'MCX.NS',
             'MUTHOOTFIN.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NESCO.NS', 'NHPC.NS', 'NIITTECH.NS', 'NLCINDIA.NS',
             'NMDC.NS', 'NTPC.NS', 'NH.NS', 'NATIONALUM.NS', 'NFL.NS', 'NBVENTURES.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS',
             'NETWORK18.NS', 'NILKAMAL.NS', 'NAM-INDIA.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'OIL.NS', 'OMAXE.NS', 'OFSS.NS',
             'ORIENTCEM.NS', 'ORIENTELEC.NS', 'ORIENTREF.NS', 'PCJEWELLER.NS', 'PIIND.NS', 'PNBHOUSING.NS',
             'PNCINFRA.NS', 'PTC.NS', 'PVR.NS', 'PAGEIND.NS', 'PARAGMILK.NS', 'PERSISTENT.NS', 'PETRONET.NS',
             'PFIZER.NS', 'PHILIPCARB.NS', 'PHOENIXLTD.NS', 'PIDILITIND.NS', 'PEL.NS', 'POLYCAB.NS', 'PFC.NS',
             'POWERGRID.NS', 'PRAJIND.NS', 'PRESTIGE.NS', 'PRSMJOHNSN.NS', 'PGHL.NS', 'PGHH.NS', 'PNB.NS', 'QUESS.NS',
             'RBLBANK.NS', 'RECLTD.NS', 'RITES.NS', 'RADICO.NS', 'RVNL.NS', 'RAIN.NS', 'RAJESHEXPO.NS', 'RALLIS.NS',
             'RCF.NS', 'RATNAMANI.NS', 'RAYMOND.NS', 'REDINGTON.NS', 'RELAXO.NS', 'RELCAPITAL.NS', 'RELIANCE.NS',
             'RELINFRA.NS', 'RPOWER.NS', 'REPCOHOME.NS', 'RESPONIND.NS', 'SHK.NS', 'SBILIFE.NS', 'SJVN.NS',
             'SKFINDIA.NS', 'SRF.NS', 'SADBHAV.NS', 'SANOFI.NS', 'SCHAEFFLER.NS', 'SIS.NS', 'SFL.NS', 'SHILPAMED.NS',
             'SHOPERSTOP.NS', 'SHREECEM.NS', 'RENUKA.NS', 'SHRIRAMCIT.NS', 'SRTRANSFIN.NS', 'SIEMENS.NS', 'SOBHA.NS',
             'SOLARINDS.NS', 'SONATSOFTW.NS', 'SOUTHBANK.NS', 'SPANDANA.NS', 'SPICEJET.NS', 'STARCEMENT.NS', 'SBIN.NS',
             'SAIL.NS', 'STRTECH.NS', 'STAR.NS', 'SUDARSCHEM.NS', 'SPARC.NS', 'SUNPHARMA.NS', 'SUNTV.NS',
             'SUNCLAYLTD.NS', 'SUNDARMFIN.NS', 'SUNDRMFAST.NS', 'SUNTECK.NS', 'SUPRAJIT.NS', 'SUPREMEIND.NS',
             'SUZLON.NS', 'SWANENERGY.NS', 'SYMPHONY.NS', 'SYNGENE.NS', 'TCIEXP.NS', 'TCNSBRANDS.NS', 'TTKPRESTIG.NS',
             'TVTODAY.NS', 'TV18BRDCST.NS', 'TVSMOTOR.NS', 'TAKE.NS', 'TASTYBITE.NS', 'TCS.NS', 'TATAELXSI.NS',
             'TATAGLOBAL.NS', 'TATAINVEST.NS', 'TATAMTRDVR.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTLBSL.NS',
             'TATASTEEL.NS', 'TEAMLEASE.NS', 'TECHM.NS', 'TECHNOE.NS', 'NIACL.NS', 'RAMCOCEM.NS', 'THERMAX.NS',
             'THYROCARE.NS', 'TIMETECHNO.NS', 'TIMKEN.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TRENT.NS',
             'TRIDENT.NS', 'TRITURBINE.NS', 'TIINDIA.NS', 'UCOBANK.NS', 'UFLEX.NS', 'UPL.NS', 'UJJIVAN.NS',
             'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UBL.NS', 'MCDOWELL-N.NS', 'VGUARD.NS', 'VMART.NS', 'VIPIND.NS',
             'VRLLOG.NS', 'VSTIND.NS', 'WABAG.NS', 'VAIBHAVGBL.NS', 'VAKRANGEE.NS', 'VTL.NS', 'VARROC.NS', 'VBL.NS',
             'VEDL.NS', 'VENKEYS.NS', 'VINATIORGA.NS', 'IDEA.NS', 'VOLTAS.NS', 'WABCOINDIA.NS', 'WELCORP.NS',
             'WELSPUNIND.NS', 'WESTLIFE.NS', 'WHIRLPOOL.NS', 'WIPRO.NS', 'WOCKPHARMA.NS', 'YESBANK.NS', 'ZEEL.NS',
             'ZENSARTECH.NS', 'ZYDUSWELL.NS', 'ECLERX.NS']

#stock_name = input("Enter Name of Stock : ")

# datetime is a pandas function to access data of that particular date
# datetime(year , month , day)

# j = 2
# count_entry = 0
# print("Entry conditions")
# while j != '0':
#     indicator_entry.append(input("Enter the Name of Indicator: "))
#     count_entry += 1
#     if indicator_entry[len(indicator_entry) - 1] == "rsi":
#         parameter_entry.append(input(" Crossover , Crosses_under , Above , Below: "))
#         value_entry.append(int(input("enter value between 0 to 100 : ")))
#     elif indicator_entry[len(indicator_entry) - 1] == "bollinger_band":
#         parameter_entry.append(input(" Crossover , Crosses_under  , Above , Below: : "))
#         value_entry.append(input("enter value upper_band , lower_band , middle_band : "))
#     else:
#         indicator_entry.pop()
#     j = input("To add other indicator enter 1 , to go to exit rule enter 0 : ")
#
# j = 2
# count_exit = 0
# print("Exit conditions")
# while j != '0':
#     indicator_exit.append(input("Enter the Name of Indicator: "))
#     count_exit += 1
#     if indicator_exit[len(indicator_exit) - 1] == "rsi":
#         parameter_exit.append(input(" Crossover , Crosses_under , Above , Below : "))
#         value_exit.append(int(input("enter value between 0 to 100 : ")))
#     elif indicator_exit[len(indicator_exit) - 1] == "bollinger_band":
#         parameter_exit.append(input(" Crossover , Crosses_under , Above , Below : "))
#         value_exit.append(input("enter value upper_band , lower_band , middle_band : "))
#     else:
#         indicator_exit.pop()
#     j = input("To add other indicator enter 1 , to see backtesting result enter 0 : ")

def home(stock_name, indicator_entry, parameter_entry, value_entry, indicator_exit, parameter_exit, value_exit):
    col = 'a'
    i = 2
    # indicator_entry = []
    # parameter_entry = []
    # value_entry = []
    # indicator_exit = []
    # parameter_exit = []
    # value_exit = []

    date_entry_pr = []
    close_entry_pr = []
    date_exit_pr = []
    close_exit_pr = []
    rsi_arr = []
    bb_arr = []
    macd_arr = []
    mfi_arr = []
    roc_arr = []
    srsi_arr = []
    wil_arr = []
    sma_arr = []
    ema_arr = []
    pp_arr = []
    ic_arr = []

    start = datetime(2019, 8, 6)
    end = datetime(2020, 7, 16)

    # web.DataReader helps to access data of a particular stock from the site you want from starting date to ending date
    # data = web.DataReader('Stock Name', 'Website', starting date, ending date)
    # to see how values are stored in data please print to verify
    data = web.DataReader(f'{stock_name}.NS', 'yahoo', start, end)

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
    count_entry = len(indicator_entry)
    count_exit = len(indicator_exit)
    for i in range(len(indicator_entry)):
        rsi_arr = []
        bb_arr = []
        macd_arr = []
        mfi_arr = []
        roc_arr = []
        srsi_arr = []
        wil_arr = []
        sma_arr = []
        ema_arr = []
        pp_arr = []
        ic_arr = []
        if indicator_entry[i] == "rsi":
            val = Indicator.RSI(close, 14)  # aiyan t
            if parameter_entry[i] == "crossover":
                for c in range(14):
                    rsi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_entry[i]) < val[j] != 0 and val[j - 1] != 0:
                        rsi_arr.append("Yes")
                    else:
                        rsi_arr.append("No")
                data_reset[col] = rsi_arr
                col += 'a'

            elif parameter_entry[i] == "crossunder":
                for c in range(14):
                    rsi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_entry[i]) > val[j] != 0 and val[j - 1] != 0:
                        rsi_arr.append("Yes")
                    else:
                        rsi_arr.append("No")
                data_reset[col] = rsi_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(14):
                    rsi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_entry[i]):
                        rsi_arr.append("Yes")
                    else:
                        rsi_arr.append("No")
                data_reset[col] = rsi_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(14):
                    rsi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_entry[i]):
                        rsi_arr.append("Yes")
                    else:
                        rsi_arr.append("No")
                data_reset[col] = rsi_arr
                col += 'a'

        elif indicator_entry[i] == "clo" and (value_entry[i] == "lb" or value_entry[i] == "mb" or value_entry[i] == "up"):
            upper, lower, middle = Indicator.bollinger_band(close, 20, 2)
            if parameter_entry[i] == "crossover":
                for c in range(20):
                    bb_arr.append("No")
                for j in range(20, len(close)):
                    if value_entry[i] == "lb":
                        if close[j - 1] <= lower[j] < close[j] and lower[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "up":
                        if close[j - 1] <= upper[j] < close[j] and upper[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "mb":
                        if close[j - 1] <= middle[j] < close[j] and middle[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                data_reset[col] = bb_arr
                col += 'a'
            elif parameter_entry[i] == "crossunder":
                for c in range(20):
                    bb_arr.append("No")
                for j in range(20, len(close)):
                    if value_entry[i] == "lb":
                        if close[j - 1] >= lower[j] > close[j] and lower[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "up":
                        if close[j - 1] >= upper[j] > close[j] and upper[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "mb":
                        if close[j - 1] >= middle[j] > close[j] and middle[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                data_reset[col] = bb_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(20):
                    bb_arr.append("No")
                for j in range(20, len(close)):
                    if value_entry[i] == "lb":
                        if close[j] > lower[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "up":
                        if close[j] > upper[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "mb":
                        if close[j] > middle[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                data_reset[col] = bb_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(20):
                    bb_arr.append("No")
                for j in range(20, len(close)):
                    if value_entry[i] == "lb":
                        if close[j] < lower[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "up":
                        if close[j] < upper[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                    elif value_entry[i] == "mb":
                        if close[j] < middle[j] != 0:
                            bb_arr.append("Yes")
                        else:
                            bb_arr.append("No")
                data_reset[col] = bb_arr
                col += 'a'

        elif indicator_entry[i] == "macd":
            macd_line, signal_line, macd_histogram = Indicator.MACD(close, 12, 26, 9)
            if parameter_entry[i] == "crossover":
                for c in range(26):
                    macd_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_entry[i] == "sig":
                        if macd_line[j - 1] <= signal_line[j] < macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                    elif value_entry[i] == "zero":
                        if macd_line[j - 1] <= 0 < macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                data_reset[col] = macd_arr
                col += 'a'
            elif parameter_entry[i] == "crossunder":
                for c in range(26):
                    macd_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_entry[i] == "sig":
                        if macd_line[j - 1] >= signal_line[j] > macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                    elif value_entry[i] == "zero":
                        if macd_line[j - 1] >= 0 > macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                data_reset[col] = macd_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(26):
                    macd_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_entry[i] == "sig":
                        if signal_line[j] < macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                    elif value_entry[i] == "zero":
                        if 0 < macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                data_reset[col] = macd_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(26):
                    macd_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_entry[i] == "sig":
                        if signal_line[j] > macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                    elif value_entry[i] == "zero":
                        if 0 > macd_line[j]:
                            macd_arr.append("Yes")
                        else:
                            macd_arr.append("No")
                data_reset[col] = macd_arr
                col += 'a'

        elif indicator_entry[i] == "mfi":
            val = Indicator.MFI(high, low, close, volume, 14)  # aiyan t
            if parameter_entry[i] == "crossover":
                for c in range(14):
                    mfi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_entry[i]) < val[j] != 0 and val[j - 1] != 0:
                        mfi_arr.append("Yes")
                    else:
                        mfi_arr.append("No")
                data_reset[col] = mfi_arr
                col += 'a'

            elif parameter_entry[i] == "crossunder":
                for c in range(14):
                    mfi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_entry[i]) > val[j] != 0 and val[j - 1] != 0:
                        mfi_arr.append("Yes")
                    else:
                        mfi_arr.append("No")
                data_reset[col] = mfi_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(14):
                    mfi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_entry[i]):
                        mfi_arr.append("Yes")
                    else:
                        mfi_arr.append("No")
                data_reset[col] = mfi_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(14):
                    mfi_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_entry[i]):
                        mfi_arr.append("Yes")
                    else:
                        mfi_arr.append("No")
                data_reset[col] = mfi_arr
                col += 'a'

        elif indicator_entry[i] == "roc":
            val = Indicator.ROC(close, 9)  # aiyan t
            if parameter_entry[i] == "crossover":
                for c in range(14):
                    roc_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_entry[i]) < val[j] != 0 and val[j - 1] != 0:
                        roc_arr.append("Yes")
                    else:
                        roc_arr.append("No")
                data_reset[col] = roc_arr
                col += 'a'

            elif parameter_entry[i] == "crossunder":
                for c in range(14):
                    roc_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_entry[i]) > val[j] != 0 and val[j - 1] != 0:
                        roc_arr.append("Yes")
                    else:
                        roc_arr.append("No")
                data_reset[col] = roc_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(14):
                    roc_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_entry[i]):
                        roc_arr.append("Yes")
                    else:
                        roc_arr.append("No")
                data_reset[col] = roc_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(14):
                    roc_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_entry[i]):
                        roc_arr.append("Yes")
                    else:
                        roc_arr.append("No")
                data_reset[col] = roc_arr
                col += 'a'

        elif indicator_entry[i] == "srsi":
            k_line, d_line = Indicator.S_RSI(close, 14, 3, 3, 14)
            if parameter_entry[i] == "crossover":
                for c in range(14):
                    srsi_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_entry[i] == "slow":
                        if k_line[j - 1] <= d_line[j] < k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                    else:
                        if k_line[j - 1] <= int(value_entry[i]) < k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                data_reset[col] = srsi_arr
                col += 'a'
            elif parameter_entry[i] == "crossunder":
                for c in range(14):
                    srsi_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_entry[i] == "slow":
                        if k_line[j - 1] >= d_line[j] > k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                    else:
                        if k_line[j - 1] >= int(value_entry[i]) > k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                data_reset[col] = srsi_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(14):
                    srsi_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_entry[i] == "slow":
                        if d_line[j] < k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                    else:
                        if int(value_entry[i]) < k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                data_reset[col] = srsi_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(14):
                    srsi_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_entry[i] == "sig":
                        if d_line[j] > k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                    else:
                        if int(value_entry[i]) > k_line[j]:
                            srsi_arr.append("Yes")
                        else:
                            srsi_arr.append("No")
                data_reset[col] = srsi_arr
                col += 'a'

        elif indicator_entry[i] == "wil":
            val = Indicator.WILLIAM_R(close, 14, high, low)  # aiyan t
            if parameter_entry[i] == "crossover":
                for c in range(14):
                    wil_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_entry[i]) < val[j] != 0 and val[j - 1] != 0:
                        wil_arr.append("Yes")
                    else:
                        wil_arr.append("No")
                data_reset[col] = wil_arr
                col += 'a'

            elif parameter_entry[i] == "crossunder":
                for c in range(14):
                    wil_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_entry[i]) > val[j] != 0 and val[j - 1] != 0:
                        wil_arr.append("Yes")
                    else:
                        wil_arr.append("No")
                data_reset[col] = wil_arr
                col += 'a'

            elif parameter_entry[i] == "above":
                for c in range(14):
                    wil_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_entry[i]):
                        wil_arr.append("Yes")
                    else:
                        wil_arr.append("No")
                data_reset[col] = wil_arr
                col += 'a'

            elif parameter_entry[i] == "below":
                for c in range(14):
                    wil_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_entry[i]):
                        wil_arr.append("Yes")
                    else:
                        wil_arr.append("No")
                data_reset[col] = wil_arr
                col += 'a'

        elif indicator_entry[i] == "sma10" or indicator_entry[i] == "sma20" or indicator_entry[i] == "sma50" or \
                indicator_entry[i] == "sma100" or indicator_entry[i] == "sma200" or (indicator_entry[i] == "clo" and (
                value_entry[i] == "sma10" or value_entry[i] == "sma20" or value_entry[i] == "sma50" or value_entry[
            i] == "sma100" or value_entry[i] == "sma200")):
            val2 = []
            val = []
            if value_entry[i] == "sma20":
                val2 = Indicator.SMA(close, 20)
            elif value_entry[i] == "sma50":
                val2 = Indicator.SMA(close, 50)
            elif value_entry[i] == "sma100":
                val2 = Indicator.SMA(close, 100)
            elif value_entry[i] == "sma200":
                val2 = Indicator.SMA(close, 200)
            elif value_entry[i] == "sma10":
                val2 = Indicator.SMA(close, 10)

            if indicator_entry[i] == "sma20":
                val = Indicator.SMA(close, 20)
            elif indicator_entry[i] == "sma50":
                val = Indicator.SMA(close, 50)
            elif indicator_entry[i] == "sma100":
                val = Indicator.SMA(close, 100)
            elif indicator_entry[i] == "sma200":
                val = Indicator.SMA(close, 200)
            elif indicator_entry[i] == "sma10":
                val = Indicator.SMA(close, 10)
            elif indicator_entry[i] == "clo":
                val = close

            ty = int(value_entry[i].split("a")[1])

            if parameter_entry[i] == "crossover":
                for c in range(ty):
                    sma_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] < val2[j] < val[j]:
                        sma_arr.append("Yes")
                    else:
                        sma_arr.append("No")
                data_reset[col] = sma_arr
                col += 'a'
            elif parameter_entry[i] == "crossunder":
                for c in range(ty):
                    sma_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] > val2[j] > val[j]:
                        sma_arr.append("Yes")
                    else:
                        sma_arr.append("No")
                data_reset[col] = sma_arr
                col += 'a'
            elif parameter_entry[i] == "above":
                for c in range(ty):
                    sma_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] < val[j]:
                        sma_arr.append("Yes")
                    else:
                        sma_arr.append("No")
                data_reset[col] = sma_arr
                col += 'a'
            elif parameter_entry[i] == "below":
                for c in range(ty):
                    sma_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] > val[j]:
                        sma_arr.append("Yes")
                    else:
                        sma_arr.append("No")
                data_reset[col] = sma_arr
                col += 'a'

        elif indicator_entry[i] == "ema10" or indicator_entry[i] == "ema20" or indicator_entry[i] == "ema50" or \
                indicator_entry[i] == "ema100" or indicator_entry[i] == "ema200" or (indicator_entry[i] == "clo" and (
                value_entry[i] == "ema10" or value_entry[i] == "ema20" or value_entry[i] == "ema50" or value_entry[
            i] == "ema100" or value_entry[i] == "ema200")):
            val2 = []
            val = []
            if value_entry[i] == "ema20":
                val2 = Indicator.EMA(close, 20)
            elif value_entry[i] == "ema50":
                val2 = Indicator.EMA(close, 50)
            elif value_entry[i] == "ema100":
                val2 = Indicator.EMA(close, 100)
            elif value_entry[i] == "ema200":
                val2 = Indicator.EMA(close, 200)
            elif value_entry[i] == "ema10":
                val2 = Indicator.EMA(close, 10)

            if indicator_entry[i] == "ema20":
                val = Indicator.EMA(close, 20)
            elif indicator_entry[i] == "ema50":
                val = Indicator.EMA(close, 50)
            elif indicator_entry[i] == "ema100":
                val = Indicator.EMA(close, 100)
            elif indicator_entry[i] == "ema200":
                val = Indicator.EMA(close, 200)
            elif indicator_entry[i] == "ema10":
                val = Indicator.EMA(close, 10)
            elif indicator_entry[i] == "clo":
                val = close

            ty = int(value_entry[i].split("a")[1])

            if parameter_entry[i] == "crossover":
                for c in range(ty):
                    ema_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] < val2[j] < val[j]:
                        ema_arr.append("Yes")
                    else:
                        ema_arr.append("No")
                data_reset[col] = ema_arr
                col += 'a'
            elif parameter_entry[i] == "crossunder":
                for c in range(ty):
                    ema_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] > val2[j] > val[j]:
                        ema_arr.append("Yes")
                    else:
                        ema_arr.append("No")
                data_reset[col] = ema_arr
                col += 'a'
            elif parameter_entry[i] == "above":
                for c in range(ty):
                    ema_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] < val[j]:
                        ema_arr.append("Yes")
                    else:
                        ema_arr.append("No")
                data_reset[col] = ema_arr
                col += 'a'
            elif parameter_entry[i] == "below":
                for c in range(ty):
                    ema_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] > val[j]:
                        ema_arr.append("Yes")
                    else:
                        ema_arr.append("No")
                data_reset[col] = ema_arr
                col += 'a'

        elif indicator_entry[i] == "clo" and (
                value_entry[i] == "pp" or value_entry[i] == "s1" or value_entry[i] == "s2" or value_entry[i] == "s3" or
                value_entry[i] == "r1" or value_entry[i] == "r2" or value_entry[i] == "r3"):
            pp, s1, s2, s3, r1, r2, r3 = Indicator.pivot_points(close, high, low, date)
            val = close
            print("entry")
            print(len(pp))
            print(len(r1))
            for jj in range(abs(len(close) - len(pp))):
                pp.insert(0, 0)
                s1.insert(0, 0)
                s2.insert(0, 0)
                s3.insert(0, 0)
                r1.insert(0, 0)
                r2.insert(0, 0)
                r3.insert(0, 0)
            print(len(pp))
            print(len(r1))
            pp_arr.append("No")
            if parameter_entry[i] == "crossover":
                if value_entry[i] == "pp":
                    for j in range(1, len(pp)):
                        if val[j - 1] < pp[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s1":
                    for j in range(1, len(pp)):
                        if val[j - 1] < s1[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s2":
                    for j in range(1, len(pp)):
                        if val[j - 1] < s2[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s3":
                    for j in range(1, len(pp)):
                        if val[j - 1] < s3[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r1":
                    for j in range(1, len(pp)):
                        if val[j - 1] < r1[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r2":
                    for j in range(1, len(pp)):
                        if val[j - 1] < r1[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r3":
                    for j in range(1, len(pp)):
                        if val[j - 1] < r3[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'

            elif parameter_entry[i] == "crossunder":
                if value_entry[i] == "pp":
                    for j in range(1, len(pp)):
                        if val[j - 1] > pp[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s1":
                    for j in range(1, len(pp)):
                        if val[j - 1] > s1[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s2":
                    for j in range(1, len(pp)):
                        if val[j - 1] > s2[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s3":
                    for j in range(1, len(pp)):
                        if val[j - 1] > s3[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r1":
                    for j in range(1, len(pp)):
                        if val[j - 1] > r1[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r2":
                    for j in range(1, len(pp)):
                        if val[j - 1] > r2[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r3":
                    for j in range(1, len(pp)):
                        if val[j - 1] > r3[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'

            elif parameter_entry[i] == "above":
                if value_entry[i] == "pp":
                    for j in range(1, len(pp)):
                        if pp[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s1":
                    for j in range(1, len(pp)):
                        if s1[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s2":
                    for j in range(1, len(pp)):
                        if s2[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s3":
                    for j in range(1, len(pp)):
                        if s3[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r1":
                    for j in range(1, len(pp)):
                        if r1[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r2":
                    for j in range(1, len(pp)):
                        if r2[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r3":
                    for j in range(1, len(pp)):
                        if r3[j] < val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'

            elif parameter_entry[i] == "below":
                if value_entry[i] == "pp":
                    for j in range(1, len(pp)):
                        if pp[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s1":
                    for j in range(1, len(pp)):
                        if s1[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s2":
                    for j in range(1, len(pp)):
                        if s2[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "s3":
                    for j in range(1, len(pp)):
                        if s3[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r1":
                    for j in range(1, len(pp)):
                        if r1[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r2":
                    for j in range(1, len(pp)):
                        if r2[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'
                elif value_entry[i] == "r3":
                    for j in range(1, len(pp)):
                        if r3[j] > val[j]:
                            pp_arr.append("Yes")
                        else:
                            pp_arr.append("No")
                    data_reset[col] = pp_arr
                    col += 'a'

        elif indicator_entry[i] == "cl" or indicator_entry[i] == "ls" or (indicator_entry[i] == "clo" and (
                value_entry[i] == "cl" or value_entry[i] == "bl" or value_entry[i] == "ls" or value_entry[i] == "gc" or
                value_entry[i] == "rc")):
            val2 = []
            val = []
            cl, bl, sa, sb, ls = Indicator.Icloud(high, low, close, 9, 26, 52, 26)
            if value_entry[i] == "cl":
                val2 = cl
            elif value_entry[i] == "bl":
                val2 = bl
            elif value_entry[i] == "ls":
                val2 = ls
            elif value_entry[i] == "gc":
                for jk in range(len(sa)):
                    val2.append(sa[jk] - sb[jk])
            elif value_entry[i] == "rc":
                for jk in range(len(sa)):
                    val2.append(sb[jk] - sa[jk])

            if indicator_entry[i] == "cl":
                val = cl
            elif indicator_entry[i] == "ls":
                val = ls
            elif indicator_entry[i] == "clo":
                val = close
            ic_arr.append("No")
            if parameter_entry[i] == "crossover":
                for j in range(1, len(val)):
                    if val[j - 1] < val2[j] < val[j]:
                        ic_arr.append("Yes")
                    else:
                        ic_arr.append("No")
                data_reset[col] = ic_arr
                col += 'a'
            elif parameter_entry[i] == "crossunder":
                for j in range(1, len(val)):
                    if val[j - 1] > val2[j] > val[j]:
                        ic_arr.append("Yes")
                    else:
                        ic_arr.append("No")
                data_reset[col] = ic_arr
                col += 'a'
            elif parameter_entry[i] == "above":
                for j in range(1, len(val2)):
                    if val2[j] < val[j] and val2[j] != -1 and val2[j] != 0:
                        ic_arr.append("Yes")
                    else:
                        ic_arr.append("No")
                data_reset[col] = ic_arr
                col += 'a'
            elif parameter_entry[i] == "below":
                for j in range(1, len(val2)):
                    if val2[j] > val[j]:
                        ic_arr.append("Yes")
                    else:
                        ic_arr.append("No")
                data_reset[col] = ic_arr
                col += 'a'
    rsie_arr = []
    bbe_arr = []
    macde_arr = []
    mfie_arr = []
    roce_arr = []
    srsie_arr = []
    wile_arr = []
    smae_arr = []
    emae_arr = []
    ppe_arr = []
    ice_arr = []

    # Exit data code
    for i in range(len(indicator_exit)):
        rsie_arr = []
        bbe_arr = []
        macde_arr = []
        mfie_arr = []
        roce_arr = []
        srsie_arr = []
        wile_arr = []
        smae_arr = []
        emae_arr = []
        ppe_arr = []
        ice_arr = []
        if indicator_exit[i] == "rsi":
            val = Indicator.RSI(close, 14)
            if parameter_exit[i] == "crossover":
                for c in range(14):
                    rsie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_exit[i]) < val[j] != 0 and val[j - 1] != 0:
                        rsie_arr.append("Yes")
                    else:
                        rsie_arr.append("No")
                data_reset[col] = rsie_arr
                col += 'a'

            elif parameter_exit[i] == "crossunder":
                for c in range(14):
                    rsie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_exit[i]) > val[j] != 0 and val[j - 1] != 0:
                        rsie_arr.append("Yes")
                    else:
                        rsie_arr.append("No")
                data_reset[col] = rsie_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(14):
                    rsie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_exit[i]):
                        rsie_arr.append("Yes")
                    else:
                        rsie_arr.append("No")
                data_reset[col] = rsie_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(14):
                    rsie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_exit[i]):
                        rsie_arr.append("Yes")
                    else:
                        rsie_arr.append("No")
                data_reset[col] = rsie_arr
                col += 'a'

        elif indicator_exit[i] == "clo" and (value_exit[i] == "lb" or value_exit[i] == "mb" or value_exit[i] == "up"):
            upper, lower, middle = Indicator.bollinger_band(close, 20, 2)
            if parameter_exit[i] == "crossover":
                for c in range(20):
                    bbe_arr.append("No")
                for j in range(20, len(close)):
                    if value_exit[i] == "lb":
                        if close[j - 1] <= lower[j] < close[j] and lower[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "up":
                        if close[j - 1] <= upper[j] < close[j] and upper[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "mb":
                        if close[j - 1] <= middle[j] < close[j] and middle[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                data_reset[col] = bbe_arr
                col += 'a'

            elif parameter_exit[i] == "crossunder":
                for c in range(20):
                    bbe_arr.append("No")
                for j in range(20, len(close)):
                    if value_exit[i] == "lb":
                        if close[j - 1] >= lower[j] > close[j] and lower[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "up":
                        if close[j - 1] >= upper[j] > close[j] and upper[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "mb":
                        if close[j - 1] >= middle[j] > close[j] and middle[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                data_reset[col] = bbe_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(20):
                    bbe_arr.append("No")
                for j in range(20, len(close)):
                    if value_exit[i] == "lb":
                        if close[j] > lower[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "up":
                        if close[j] > upper[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "mb":
                        if close[j] > middle[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                data_reset[col] = bbe_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(20):
                    bbe_arr.append("No")
                for j in range(20, len(close)):
                    if value_exit[i] == "lb":
                        if close[j] < lower[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "up":
                        if close[j] < upper[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                    elif value_exit[i] == "mb":
                        if close[j] < middle[j] != 0:
                            bbe_arr.append("Yes")
                        else:
                            bbe_arr.append("No")
                data_reset[col] = bbe_arr
                col += 'a'

        elif indicator_exit[i] == "macd":
            macd_line, signal_line, macd_histogram = Indicator.MACD(close, 12, 26, 9)
            if parameter_exit[i] == "crossover":
                for c in range(26):
                    macde_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_exit[i] == "sig":
                        if macd_line[j - 1] <= signal_line[j] < macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                    elif value_exit[i] == "zero":
                        if macd_line[j - 1] <= 0 < macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                data_reset[col] = macde_arr
                col += 'a'

            elif parameter_exit[i] == "crossunder":
                for c in range(26):
                    macde_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_exit[i] == "sig":
                        if macd_line[j - 1] >= signal_line[j] > macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                    elif value_exit[i] == "zero":
                        if macd_line[j - 1] >= 0 > macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                data_reset[col] = macde_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(26):
                    macde_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_exit[i] == "sig":
                        if signal_line[j] < macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                    elif value_exit[i] == "zero":
                        if 0 < macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                data_reset[col] = macde_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(26):
                    macde_arr.append("No")
                for j in range(26, len(signal_line)):
                    if value_exit[i] == "sig":
                        if signal_line[j] > macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                    elif value_exit[i] == "zero":
                        if 0 > macd_line[j]:
                            macde_arr.append("Yes")
                        else:
                            macde_arr.append("No")
                data_reset[col] = macde_arr
                col += 'a'

        elif indicator_exit[i] == "mfi":
            val = Indicator.MFI(high, low, close, volume, 14)  # aiyan t
            if parameter_exit[i] == "crossover":
                for c in range(14):
                    mfie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_exit[i]) < val[j] != 0 and val[j - 1] != 0:
                        mfie_arr.append("Yes")
                    else:
                        mfie_arr.append("No")
                data_reset[col] = mfie_arr
                col += 'a'

            elif parameter_exit[i] == "crossunder":
                for c in range(14):
                    mfie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_exit[i]) > val[j] != 0 and val[j - 1] != 0:
                        mfie_arr.append("Yes")
                    else:
                        mfie_arr.append("No")
                data_reset[col] = mfie_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(14):
                    mfie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_exit[i]):
                        mfie_arr.append("Yes")
                    else:
                        mfie_arr.append("No")
                data_reset[col] = mfie_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(14):
                    mfie_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_exit[i]):
                        mfie_arr.append("Yes")
                    else:
                        mfie_arr.append("No")
                data_reset[col] = mfie_arr
                col += 'a'

        elif indicator_exit[i] == "roc":
            val = Indicator.ROC(close, 9)  # aiyan t
            if parameter_exit[i] == "crossover":
                for c in range(14):
                    roce_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_exit[i]) < val[j] != 0 and val[j - 1] != 0:
                        roce_arr.append("Yes")
                    else:
                        roce_arr.append("No")
                data_reset[col] = roce_arr
                col += 'a'

            elif parameter_exit[i] == "crossunder":
                for c in range(14):
                    roce_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_exit[i]) > val[j] != 0 and val[j - 1] != 0:
                        roce_arr.append("Yes")
                    else:
                        roce_arr.append("No")
                data_reset[col] = roce_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(14):
                    roce_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_exit[i]):
                        roce_arr.append("Yes")
                    else:
                        roce_arr.append("No")
                data_reset[col] = roce_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(14):
                    roce_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_exit[i]):
                        roce_arr.append("Yes")
                    else:
                        roce_arr.append("No")
                data_reset[col] = roce_arr
                col += 'a'

        elif indicator_exit[i] == "srsi":
            k_line, d_line = Indicator.S_RSI(close, 14, 3, 3, 14)
            if parameter_exit[i] == "crossover":
                for c in range(14):
                    srsie_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_exit[i] == "slow":
                        if k_line[j - 1] <= d_line[j] < k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                    else:
                        if k_line[j - 1] <= int(value_exit[i]) < k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                data_reset[col] = srsie_arr
                col += 'a'
            elif parameter_exit[i] == "crossunder":
                for c in range(14):
                    srsie_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_exit[i] == "slow":
                        if k_line[j - 1] >= d_line[j] > k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                    else:
                        if k_line[j - 1] >= int(value_exit[i]) > k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                data_reset[col] = srsie_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(14):
                    srsie_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_exit[i] == "slow":
                        if d_line[j] < k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                    else:
                        if int(value_exit[i]) < k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                data_reset[col] = srsie_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(14):
                    srsie_arr.append("No")
                for j in range(14, len(d_line)):
                    if value_exit[i] == "slow":
                        if d_line[j] > k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                    else:
                        if int(value_exit[i]) > k_line[j]:
                            srsie_arr.append("Yes")
                        else:
                            srsie_arr.append("No")
                data_reset[col] = srsie_arr
                col += 'a'

        elif indicator_exit[i] == "wil":
            val = Indicator.WILLIAM_R(close, 14, high, low)  # aiyan t
            if parameter_exit[i] == "crossover":
                for c in range(14):
                    wile_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] <= int(value_exit[i]) < val[j] != 0 and val[j - 1] != 0:
                        wile_arr.append("Yes")
                    else:
                        wile_arr.append("No")
                data_reset[col] = wile_arr
                col += 'a'

            elif parameter_exit[i] == "crossunder":
                for c in range(14):
                    wile_arr.append("No")
                for j in range(14, len(val)):
                    if val[j - 1] >= int(value_exit[i]) > val[j] != 0 and val[j - 1] != 0:
                        wile_arr.append("Yes")
                    else:
                        wile_arr.append("No")
                data_reset[col] = wile_arr
                col += 'a'

            elif parameter_exit[i] == "above":
                for c in range(14):
                    wile_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] > int(value_exit[i]):
                        wile_arr.append("Yes")
                    else:
                        wile_arr.append("No")
                data_reset[col] = wile_arr
                col += 'a'

            elif parameter_exit[i] == "below":
                for c in range(14):
                    wile_arr.append("No")
                for j in range(14, len(val)):
                    if val[j] < int(value_exit[i]):
                        wile_arr.append("Yes")
                    else:
                        wile_arr.append("No")
                data_reset[col] = wile_arr
                col += 'a'

        elif indicator_exit[i] == "sma10" or indicator_exit[i] == "sma20" or indicator_exit[i] == "sma50" or \
                indicator_exit[i] == "sma100" or indicator_exit[i] == "sma200" or (
                indicator_exit[i] == "clo" and (
                value_exit[i] == "sma10" or value_exit[i] == "sma20" or value_exit[i] == "sma50" or value_exit[
            i] == "sma100" or value_exit[i] == "sma200")):
            val2 = []
            val = []
            if value_exit[i] == "sma20":
                val2 = Indicator.SMA(close, 20)
            elif value_exit[i] == "sma50":
                val2 = Indicator.SMA(close, 50)
            elif value_exit[i] == "sma100":
                val2 = Indicator.SMA(close, 100)
            elif value_exit[i] == "sma200":
                val2 = Indicator.SMA(close, 200)
            elif value_exit[i] == "sma10":
                val2 = Indicator.SMA(close, 10)

            if indicator_exit[i] == "sma20":
                val = Indicator.SMA(close, 20)
            elif indicator_exit[i] == "sma50":
                val = Indicator.SMA(close, 50)
            elif indicator_exit[i] == "sma100":
                val = Indicator.SMA(close, 100)
            elif indicator_exit[i] == "sma200":
                val = Indicator.SMA(close, 200)
            elif indicator_exit[i] == "sma10":
                val = Indicator.SMA(close, 10)
            elif indicator_exit[i] == "clo":
                val = close

            ty = int(value_exit[i].split("a")[1])

            if parameter_exit[i] == "crossover":
                for c in range(ty):
                    smae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] < val2[j] < val[j]:
                        smae_arr.append("Yes")
                    else:
                        smae_arr.append("No")
                data_reset[col] = smae_arr
                col += 'a'
            elif parameter_exit[i] == "crossunder":
                for c in range(ty):
                    smae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] > val2[j] > val[j]:
                        smae_arr.append("Yes")
                    else:
                        smae_arr.append("No")
                data_reset[col] = smae_arr
                col += 'a'
            elif parameter_exit[i] == "above":
                for c in range(ty):
                    smae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] < val[j]:
                        smae_arr.append("Yes")
                    else:
                        smae_arr.append("No")
                data_reset[col] = smae_arr
                col += 'a'
            elif parameter_exit[i] == "below":
                for c in range(ty):
                    smae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] > val[j]:
                        smae_arr.append("Yes")
                    else:
                        smae_arr.append("No")
                data_reset[col] = smae_arr
                col += 'a'

        elif indicator_exit[i] == "ema10" or indicator_exit[i] == "ema20" or indicator_exit[i] == "ema50" or \
                indicator_exit[i] == "ema100" or indicator_exit[i] == "ema200" or (indicator_exit[i] == "clo" and (
                value_exit[i] == "ema10" or value_exit[i] == "ema20" or value_exit[i] == "ema50" or value_exit[
            i] == "ema100" or value_exit[i] == "ema200")):
            val2 = []
            val = []
            if value_exit[i] == "ema20":
                val2 = Indicator.EMA(close, 20)
            elif value_exit[i] == "ema50":
                val2 = Indicator.EMA(close, 50)
            elif value_exit[i] == "ema100":
                val2 = Indicator.EMA(close, 100)
            elif value_exit[i] == "ema200":
                val2 = Indicator.EMA(close, 200)
            elif value_exit[i] == "ema10":
                val2 = Indicator.EMA(close, 10)

            if indicator_exit[i] == "ema20":
                val = Indicator.EMA(close, 20)
            elif indicator_exit[i] == "ema50":
                val = Indicator.EMA(close, 50)
            elif indicator_exit[i] == "ema100":
                val = Indicator.EMA(close, 100)
            elif indicator_exit[i] == "ema200":
                val = Indicator.EMA(close, 200)
            elif indicator_exit[i] == "ema10":
                val = Indicator.EMA(close, 10)
            elif indicator_exit[i] == "clo":
                val = close

            ty = int(value_exit[i].split("a")[1])

            if parameter_exit[i] == "crossover":
                for c in range(ty):
                    emae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] < val2[j] < val[j]:
                        emae_arr.append("Yes")
                    else:
                        emae_arr.append("No")
                data_reset[col] = emae_arr
                col += 'a'
            elif parameter_exit[i] == "crossunder":
                for c in range(ty):
                    emae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val[j - 1] > val2[j] > val[j]:
                        emae_arr.append("Yes")
                    else:
                        emae_arr.append("No")
                data_reset[col] = emae_arr
                col += 'a'
            elif parameter_exit[i] == "above":
                for c in range(ty):
                    emae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] < val[j]:
                        emae_arr.append("Yes")
                    else:
                        emae_arr.append("No")
                data_reset[col] = emae_arr
                col += 'a'
            elif parameter_exit[i] == "below":
                for c in range(ty):
                    emae_arr.append("No")
                for j in range(ty, len(val2)):
                    if val2[j] > val[j]:
                        emae_arr.append("Yes")
                    else:
                        emae_arr.append("No")
                data_reset[col] = emae_arr
                col += 'a'

        elif indicator_exit[i] == "clo" and (
                value_exit[i] == "pp" or value_exit[i] == "s1" or value_exit[i] == "s2" or value_exit[i] == "s3" or
                value_exit[i] == "r1" or value_exit[i] == "r2" or value_exit[i] == "r3"):

            pp, s1, s2, s3, r1, r2, r3 = Indicator.pivot_points(close, high, low, date)
            val = close

            for jj in range(abs(len(close) - len(pp))):
                pp.insert(0, 0)
                s1.insert(0, 0)
                s2.insert(0, 0)
                s3.insert(0, 0)
                r1.insert(0, 0)
                r2.insert(0, 0)
                r3.insert(0, 0)

            ppe_arr.append("No")
            if parameter_exit[i] == "crossover":
                if value_exit[i] == "pp":
                    for j in range(1, len(pp)):
                        if val[j - 1] < pp[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s1":
                    for j in range(1, len(pp)):
                        if val[j - 1] < s1[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s2":
                    for j in range(1, len(pp)):
                        if val[j - 1] < s2[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s3":
                    for j in range(1, len(pp)):
                        if val[j - 1] < s3[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r1":
                    for j in range(1, len(pp)):
                        if val[j - 1] < r1[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r2":
                    for j in range(1, len(pp)):
                        if val[j - 1] < r1[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r3":
                    for j in range(1, len(pp)):
                        if val[j - 1] < r3[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'

            elif parameter_exit[i] == "crossunder":
                if value_exit[i] == "pp":
                    for j in range(1, len(pp)):
                        if val[j - 1] > pp[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s1":
                    for j in range(1, len(pp)):
                        if val[j - 1] > s1[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s2":
                    for j in range(1, len(pp)):
                        if val[j - 1] > s2[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s3":
                    for j in range(1, len(pp)):
                        if val[j - 1] > s3[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r1":
                    print(len(r1))
                    print(len(val))
                    for j in range(1, len(pp)):

                        if val[j - 1] > r1[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r2":
                    for j in range(1, len(pp)):
                        if val[j - 1] > r2[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r3":
                    for j in range(1, len(pp)):
                        if val[j - 1] > r3[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'

            elif parameter_exit[i] == "above":
                if value_exit[i] == "pp":
                    for j in range(1, len(pp)):
                        if pp[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s1":
                    for j in range(1, len(pp)):
                        if s1[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s2":
                    for j in range(1, len(pp)):
                        if s2[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s3":
                    for j in range(1, len(pp)):
                        if s3[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r1":
                    for j in range(1, len(pp)):
                        if r1[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r2":
                    for j in range(1, len(pp)):
                        if r2[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r3":
                    for j in range(1, len(pp)):
                        if r3[j] < val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'

            elif parameter_exit[i] == "below":
                if value_exit[i] == "pp":
                    for j in range(1, len(pp)):
                        if pp[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s1":
                    for j in range(1, len(pp)):
                        if s1[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s2":
                    for j in range(1, len(pp)):
                        if s2[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "s3":
                    for j in range(1, len(pp)):
                        if s3[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r1":
                    for j in range(1, len(pp)):
                        if r1[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r2":
                    for j in range(1, len(pp)):
                        if r2[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'
                elif value_exit[i] == "r3":
                    for j in range(1, len(pp)):
                        if r3[j] > val[j]:
                            ppe_arr.append("Yes")
                        else:
                            ppe_arr.append("No")
                    data_reset[col] = ppe_arr
                    col += 'a'

        elif indicator_exit[i] == "cl" or indicator_exit[i] == "ls" or (indicator_exit[i] == "clo" and (
                value_exit[i] == "cl" or value_exit[i] == "bl" or value_exit[i] == "ls" or value_exit[i] == "gc" or
                value_exit[i] == "rc")):
            val2 = []
            val = []
            cl, bl, sa, sb, ls = Indicator.Icloud(high, low, close, 9, 26, 52, 26)
            if value_exit[i] == "cl":
                val2 = cl
            elif value_exit[i] == "bl":
                val2 = bl
            elif value_exit[i] == "ls":
                val2 = ls
            elif value_exit[i] == "gc":
                for jk in range(len(sa)):
                    val2.append(sa[jk] - sb[jk])
            elif value_exit[i] == "rc":
                for jk in range(len(sa)):
                    val2.append(sb[jk] - sa[jk])

            if indicator_exit[i] == "cl":
                val = cl
            elif indicator_exit[i] == "ls":
                val = ls
            elif indicator_exit[i] == "clo":
                val = close
            ice_arr.append("No")
            if parameter_exit[i] == "crossover":
                for j in range(1, len(val)):
                    if val[j - 1] < val2[j] < val[j]:
                        ice_arr.append("Yes")
                    else:
                        ice_arr.append("No")
                data_reset[col] = ice_arr
                col += 'a'
            elif parameter_exit[i] == "crossunder":
                for j in range(1, len(val)):
                    if val[j - 1] > val2[j] > val[j]:
                        ice_arr.append("Yes")
                    else:
                        ice_arr.append("No")
                data_reset[col] = ice_arr
                col += 'a'
            elif parameter_exit[i] == "above":
                for j in range(1, len(val2)):
                    if val2[j] < val[j] and val2[j] != -1 and val2[j] != 0:
                        ice_arr.append("Yes")
                    else:
                        ice_arr.append("No")
                data_reset[col] = ice_arr
                col += 'a'
            elif parameter_exit[i] == "below":
                for j in range(1, len(val2)):
                    if val2[j] > val[j]:
                        ice_arr.append("Yes")
                    else:
                        ice_arr.append("No")
                data_reset[col] = ice_arr
                col += 'a'

    entry_dt_points = []
    exit_dt_points = []
    entry_date_points = []
    exit_date_points = []
    entry_close_points = []
    exit_close_points = []

    for i in range(len(close)):
        ce = 0
        if data_reset.iloc[i, 8] == "Yes":
            for j in range(count_entry):
                if data_reset.iloc[i, 7 + 1 + j] == "Yes":
                    ce += 1
                if ce == count_entry:
                    entry_dt_points.append(dt[i])
                    entry_date_points.append(date[i])
                    entry_close_points.append(close[i])

        cex = 0
        if data_reset.iloc[i, 7 + count_entry + 1] == "Yes":
            for j in range(count_exit):
                if data_reset.iloc[i, 7 + count_entry + 1 + j] == "Yes":
                    cex += 1
                if cex == count_exit:
                    exit_dt_points.append(dt[i])
                    exit_date_points.append(date[i])
                    exit_close_points.append(close[i])

    total = []
    ref = 0
    #choice = input("Do you want multiple entries for single exit , Enter Yes/No : ")
    choice = "Yes"
    if choice == "No":
        if len(entry_date_points) == 0 or len(exit_date_points) == 0:
            print(" No Match for this Strategy")
            return "no","no","no"
        else:
            for i in range(len(entry_date_points)):
                if entry_dt_points[i] > ref:
                    price_entry = entry_close_points[i]
                    for j in range(len(exit_date_points)):
                        if exit_dt_points[j] > entry_dt_points[i]:
                            price_exit = exit_close_points[j]
                            total.append(((price_exit - price_entry) / price_exit) * 100)
                            ref = exit_dt_points[j]
                            break
            print(f'Your Profit/Loss is {statistics.mean(total):.2f} %')
    else:
        if len(entry_date_points) == 0 or len(exit_date_points) == 0:
            print(" No Match for this Strategy")
            return "no","no","no"
        else:
            for i in range(len(entry_date_points)):
                price_entry = entry_close_points[i]
                for j in range(len(exit_date_points)):
                    if exit_dt_points[j] > entry_dt_points[i]:
                        price_exit = exit_close_points[j]
                        total.append(((price_exit - price_entry) / price_exit) * 100)
                        break
            print(f'Your Profit/Loss is {statistics.mean(total):.2f} %')
    print(entry_date_points)
    print(entry_dt_points)
    return statistics.mean(total),entry_date_points,exit_date_points