import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from pandas.util.testing import assert_frame_equal
from matplotlib.dates import date2num
import Indicator
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

stock_name = input("Enter Name of Stock : ")

# datetime is a pandas function to access data of that particular date
# datetime(year , month , day)
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

col = 'a'
i = 2
indicator_entry = []
parameter_entry = []
value_entry = []
indicator_exit = []
parameter_exit = []
value_exit = []

j = 2
count_entry = 0
print("Entry conditions")
while j != '0':
    indicator_entry.append(input("Enter the Name of Indicator: "))
    count_entry += 1
    if indicator_entry[len(indicator_entry) - 1] == "rsi":
        parameter_entry.append(input(" Crossover , Crosses_under , Above , Below: "))
        value_entry.append(int(input("enter value between 0 to 100 : ")))
    elif indicator_entry[len(indicator_entry) - 1] == "bollinger_band":
        parameter_entry.append(input(" Crossover , Crosses_under  , Above , Below: : "))
        value_entry.append(input("enter value upper_band , lower_band , middle_band : "))
    else:
        indicator_entry.pop()
    j = input("To add other indicator enter 1 , to go to exit rule enter 0 : ")

j = 2
count_exit = 0
print("Exit conditions")
while j != '0':
    indicator_exit.append(input("Enter the Name of Indicator: "))
    count_exit += 1
    if indicator_exit[len(indicator_exit) - 1] == "rsi":
        parameter_exit.append(input(" Crossover , Crosses_under , Above , Below : "))
        value_exit.append(int(input("enter value between 0 to 100 : ")))
    elif indicator_exit[len(indicator_exit) - 1] == "bollinger_band":
        parameter_exit.append(input(" Crossover , Crosses_under , Above , Below : "))
        value_exit.append(input("enter value upper_band , lower_band , middle_band : "))
    else:
        indicator_exit.pop()
    j = input("To add other indicator enter 1 , to see backtesting result enter 0 : ")

date_entry_pr = []
close_entry_pr = []
date_exit_pr = []
close_exit_pr = []
rsi_arr = []
bb_arr = []

for i in range(len(indicator_entry)):
    if indicator_entry[i] == "rsi":
        val = Indicator.RSI(close , 14)
        if parameter_entry[i] == "Crossover":
            for j in range(len(val)):
                if val[j - 1] <= value_entry[i] < val[j] != 0 and val[j - 1] != 0:
                    rsi_arr.append("Yes")
                else:
                    rsi_arr.append("No")
            data_reset[col] = rsi_arr
            col += 'a'

        elif parameter_entry[i] == "Crosses_under":
            for j in range(len(val)):
                if val[j - 1] >= value_entry[i] > val[j] != 0 and val[j - 1] != 0:
                    rsi_arr.append("Yes")
                else:
                    rsi_arr.append("No")
            data_reset[col] = rsi_arr
            col += 'a'

        elif parameter_entry[i] == "Above":
            for j in range(len(val)):
                if val[j] > value_entry[i]:
                    rsi_arr.append("Yes")
                else:
                    rsi_arr.append("No")
            data_reset[col] = rsi_arr
            col += 'a'

        elif parameter_entry[i] == "Below":
            for j in range(len(val)):
                if val[j] < value_entry[i]:
                    rsi_arr.append("Yes")
                else:
                    rsi_arr.append("No")
            data_reset[col] = rsi_arr
            col += 'a'


    elif indicator_entry[i] == "bollinger_band":
        upper, lower, middle = Indicator.bollinger_band(close, 20, 2)
        if parameter_entry[i] == "Crossover":
            for j in range(len(close)):
                if value_entry[i] == "lower_band":
                    if close[j - 1] <= lower[j] < close[j] and lower[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "upper_band":
                    if close[j - 1] <= upper[j] < close[j] and upper[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "middle_band":
                    if close[j - 1] <= middle[j] < close[j] and middle[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
            data_reset[col] = bb_arr
            col += 'a'
        elif parameter_entry[i] == "Crosses_under":
            for j in range(len(close)):
                if value_entry[i] == "lower_band":
                    if close[j - 1] >= lower[j] > close[j] and lower[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "upper_band":
                    if close[j - 1] >= upper[j] > close[j] and upper[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "middle_band":
                    if close[j - 1] >= middle[j] > close[j] and middle[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
            data_reset[col] = bb_arr
            col += 'a'

        elif parameter_entry[i] == "Above":
            for j in range(len(close)):
                if value_entry[i] == "lower_band":
                    if close[j] > lower[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "upper_band":
                    if close[j] > upper[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "middle_band":
                    if close[j] > middle[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
            data_reset[col] = bb_arr
            col += 'a'

        elif parameter_entry[i] == "Below":
            for j in range(len(close)):
                if value_entry[i] == "lower_band":
                    if close[j] < lower[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "upper_band":
                    if close[j] < upper[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
                elif value_entry[i] == "middle_band":
                    if close[j] < middle[j] != 0:
                        bb_arr.append("Yes")
                    else:
                        bb_arr.append("No")
            data_reset[col] = bb_arr
            col += 'a'

rsie_arr = []
bbe_arr = []

# Exit data code
for i in range(len(indicator_exit)):
    if indicator_exit[i] == "rsi":
        val = Indicator.RSI(close , 14)
        if parameter_exit[i] == "Crossover":
            for j in range(len(val)):
                if val[j - 1] <= value_exit[i] < val[j] != 0 and val[j - 1] != 0:
                    rsie_arr.append("Yes")
                else:
                    rsie_arr.append("No")
            data_reset[col] = rsie_arr
            col += 'a'

        elif parameter_exit[i] == "Crosses_under":
            for j in range(len(val)):
                if val[j - 1] >= value_exit[i] > val[j] != 0 and val[j - 1] != 0:
                    rsie_arr.append("Yes")
                else:
                    rsie_arr.append("No")
            data_reset[col] = rsie_arr
            col += 'a'

        elif parameter_exit[i] == "Above":
            for j in range(len(val)):
                if val[j] > value_exit[i]:
                    rsie_arr.append("Yes")
                else:
                    rsie_arr.append("No")
            data_reset[col] = rsie_arr
            col += 'a'

        elif parameter_exit[i] == "Below":
            for j in range(len(val)):
                if val[j] < value_exit[i]:
                    rsie_arr.append("Yes")
                else:
                    rsie_arr.append("No")
            data_reset[col] = rsie_arr
            col += 'a'


    elif indicator_exit[i] == "bollinger_band":
        upper, lower, middle = Indicator.bollinger_band(close, 20, 2)
        if parameter_exit[i] == "Crossover":
            for j in range(len(close)):
                if value_exit[i] == "lower_band":
                    if close[j - 1] <= lower[j] < close[j] and lower[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "upper_band":
                    if close[j - 1] <= upper[j] < close[j] and upper[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "middle_band":
                    if close[j - 1] <= middle[j] < close[j] and middle[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
            data_reset[col] = bbe_arr
            col += 'a'

        elif parameter_exit[i] == "Crosses_under":
            for j in range(len(close)):
                if value_exit[i] == "lower_band":
                    if close[j - 1] >= lower[j] > close[j] and lower[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "upper_band":
                    if close[j - 1] >= upper[j] > close[j] and upper[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "middle_band":
                    if close[j - 1] >= middle[j] > close[j] and middle[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
            data_reset[col] = bbe_arr
            col += 'a'

        elif parameter_exit[i] == "Above":
            for j in range(len(close)):
                if value_exit[i] == "lower_band":
                    if close[j] > lower[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "upper_band":
                    if close[j] > upper[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "middle_band":
                    if close[j] > middle[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
            data_reset[col] = bbe_arr
            col += 'a'

        elif parameter_exit[i] == "Below":
            for j in range(len(close)):
                if value_exit[i] == "lower_band":
                    if close[j] < lower[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "upper_band":
                    if close[j] < upper[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
                elif value_exit[i] == "middle_band":
                    if close[j] < middle[j] != 0:
                        bbe_arr.append("Yes")
                    else:
                        bbe_arr.append("No")
            data_reset[col] = bbe_arr
            col += 'a'

entry_dt_points = []
exit_dt_points = []
entry_date_points = []
exit_date_points = []
entry_close_points = []
exit_close_points = []
print(data_reset)
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
    if data_reset.iloc[i, 7 + count_entry ] == "Yes":
        for j in range(count_exit):
            if data_reset.iloc[i, 7 + count_entry  + j] == "Yes":
                cex += 1
            if cex == count_exit:
                exit_dt_points.append(dt[i])
                exit_date_points.append(date[i])
                exit_close_points.append(close[i])

total = []

if len(entry_date_points) == 0 or len(exit_date_points) == 0:
    print(" No Match for this Strategy")
else:
    for i in range(len(entry_date_points)):
        price_entry = entry_close_points[i]
        for j in range(len(exit_date_points)):
            if exit_dt_points[j] > entry_dt_points[i]:
                price_exit = exit_close_points[j]
                total.append(((price_exit - price_entry) / price_exit) * 100)
                break
    print(f'Your Profit/Loss is {statistics.mean(total):.2f} %')
