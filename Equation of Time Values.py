from math import degrees,radians,tan,sin,acos,cos,floor,atan2,sqrt,asin,pi
# -----------------------------------------------------------------------------------
# EQUATION OF TIME
# -----------------------------------------------------------------------------------
# Python Code written by Kevin Karney, Winter 2024
# Should work on all releases of Python
# Free for anyone to use without any guarantees!
#
# NOTA BENE
# where Time is input, it is local STANDARD time (i.e. no Daylight saving). 
# Hence Time Zone occurs in many routines to correct to UTC,

# The code performs calculates the essential Solar parameters 
# for a given location and date
#     calculated by subroutine Sun_JD(JD)
#     its output is an array comprising:
#          EoT, Longitude Corrected EoT,
#          Right Ascension, Declination
#          Solar Altitude, Azimuth
#          approx time of Sunrise, Sunset
#     Main routines are 
#          Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone) which calls Sun_JD(JD)
#          Sun_Year(Year,Longitude,Zone) which gives values for noon over a year
#     output is a tab-delimited which can be pasted into any spreadsheet

# There are a number of service routines
#     Julian(Year,Month,Day,Hour,Zone) which gives the Julian Day
#     Get_Calendar_Date(The_JD,Zone) which converts between Julian Day and normal calendar values
#     EoT_Dec_MMSS(The_EoT) which formats decimal minutes to mins and second 
#     Dec_Deg_DMS(The_Degs) which formats decimal degrees to degrees, mins and secs
#     Dec_Hrs_HMS(The_Hrs) which formats decimal hours to degrees, mins and secs

# Much of the code in routines Sun, EoT_Decl_Fourier
# relates to printing out all the calculation steps for interest 
# or debugging purposes.
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# What is Wanted 
# ---------------------------------------------------------------------------------------
global Detail_Print 
Year_Calc      = False   # if True,  provides values for a whole year at noon 
                        # if False, provides a single set of calculations for specified date and time
Detail_Print   = False   # Prints detailed calculation steps for single day calculation
rounder        = 5      # rounds output to these number of decimals to results
# ---------------------------------------------------------------------------------------
# Location Input 
# ---------------------------------------------------------------------------------------
Place          = 'Athens'
Longitude      = 23.71667 # Degrees : +ve East of Greenwich
Latitude       = 37.96667 # Degrees : +ve East of Greenwich
Zone           = 2        # Hrs     : +ve East of Greenwich

Year           = 2025
Month          = 2
Day            = 13
Hour           = 12       # Local Standard Clock Time (no DST)

def Calculate():
    # -----------------------------------------------------
    # This is routine called from the last line of this code
    # It selects the task required 
    # -----------------------------------------------------
    if Year_Calc == True:
        Detail_Print = False
        print ('Year Result from Sun routine')
        Sun_Year(Year,Longitude,Zone) 
        print ("\rThis output can copied and pasted into any spreadsheet")
    else: 
        Results = Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone)
        print ('Location                = ',Place)
        print ('Lat : Long : Zone       = ',Dec_Deg_DMS(Latitude),' : ',Dec_Deg_DMS(Longitude),' : ',Zone)
        print ('EoT                     = ',round(Results[0],rounder),EoT_Dec_MMSS(Results[0    ]))
        print ('EoT Longitude Corrected = ',round(Results[1],rounder),EoT_Dec_MMSS(Results[1]))
        print ('Right Ascension         = ',round(Results[2],rounder),Dec_Hrs_HMS (Results[2]))
        print ('Solar Declination       = ',round(Results[3],rounder),Dec_Deg_DMS (Results[3]))
        print ('Altitude                = ',round(Results[4],rounder),Dec_Deg_DMS (Results[4]))
        print ('Azimuth                 = ',round(Results[5],rounder),Dec_Deg_DMS (Results[5]))
        print ('approx Sunrise          = ',round(Results[6],rounder),Dec_Hrs_HMS (Results[6]))
        print ('approx Sunrise Az       = ',round(Results[7],rounder),Dec_Deg_DMS (Results[7]))
        print ('approx Sunset           = ',round(Results[8],rounder),Dec_Hrs_HMS (Results[8]))
        print ('approx Sunset Az        = ',round(Results[9],rounder),Dec_Deg_DMS (Results[9]))

def Sun_JD(JD):
    # -----------------------------------------------------
    # This does the main astronomical calculations
    # It returns the EoT, Longitude Corrected EoT & Declination
    # but these may be changed to any other parameter that has been calculated
    # -----------------------------------------------------
    # -------------------
    global Detail_Print
    X = JD -.5
    UTC_hrs = ((X-int(X)) * 24) % 24 # Extract UTC_hrs from Julian Day
 
    D0                  = JD - 2451545.
    T                   = D0 / 36525
    
    GMST_deg            = 280.46061837 + 360.98564736629 * D0  + 0.000387933 *T**2 - T**3/38710000.
    GMST_deg            = GMST_deg % 360
    GMST_hrs            = GMST_deg / 15.
    LMST_Hrs            = GMST_hrs + Longitude / 15.
    
    Mean_Longitude_hrs  = GMST_hrs + 12. - UTC_hrs
    Mean_Longitude_deg  = Mean_Longitude_hrs * 15
    #-------------------
    # These values obtained from the Astronmical Almanac vols between 2000 and 2023
    Perihelion_deg      = 282.938     + 1.7     * T
    Eccentricity        = 0.016708617 - 0.00004 * T 
    Obliquity_deg       = 23.43929111 - 0.013   * T
    Obliquity_rad       = radians(Obliquity_deg)
    #-------------------
    Mean_Anomaly_deg    = Mean_Longitude_deg - Perihelion_deg
    Mean_Anomaly_rad    = radians(Mean_Anomaly_deg)
    E0 = Mean_Anomaly_rad
    E1 = E0 + (Mean_Anomaly_rad + Eccentricity*sin(E0)- E0)/(1 - Eccentricity*cos(E0))
    # p.s. second Newton Raphson iteration not really needed
    E2 = E1 + (Mean_Anomaly_rad + Eccentricity*sin(E1)- E1)/(1 - Eccentricity*cos(E1))
    Eccentric_Anomaly   = E2
    True_Anomaly_rad    = atan2(sqrt(1 - Eccentricity**2) * sin(Eccentric_Anomaly), (cos(Eccentric_Anomaly)- Eccentricity))
    True_Anomaly_deg    = degrees(True_Anomaly_rad)
    True_Long_deg       = True_Anomaly_deg + Perihelion_deg
    True_Long_rad       = radians(True_Long_deg)
    Eccent_Effect_deg   = True_Long_deg - Mean_Longitude_deg 
    Eccent_Effect_min   = 4 * Eccent_Effect_deg 
    #-------------------
    Right_Ascension_rad = atan2(cos(Obliquity_rad) * sin(True_Long_rad),cos(True_Long_rad)) % (2*pi)
    Right_Ascension_deg = (degrees(Right_Ascension_rad)) % 360.
    Right_Ascension_hrs = Right_Ascension_deg / 15.
    Declination_rad     = asin(sin(Obliquity_rad) * sin(True_Long_rad))
    Declination_deg     = degrees(Declination_rad)
    #-------------------
    EoT_deg             = Right_Ascension_deg - Mean_Longitude_deg
    if EoT_deg >  180.: EoT_deg = EoT_deg-360.
    if EoT_deg < -180.: EoT_deg = EoT_deg+360.
    EoT_min             = 4 * EoT_deg
    Obliq_Effect_min    = EoT_min - Eccent_Effect_min
    Long_Corr           = 4 * (Zone * 15 - Longitude)
    EoT_Corr_min        = EoT_min + Long_Corr

    Solar_Noon_hrs      = 12 + EoT_Corr_min/60
    Hour_Angle_hrs      = GMST_hrs + Longitude/15. - Right_Ascension_hrs
    Hour_Angle_rad      = radians(Hour_Angle_hrs * 15.)
    Latitude_rad        = radians(Latitude)
    Altitude_rad        = asin((sin(Latitude_rad) * sin(Declination_rad) + cos(Latitude_rad) * cos(Declination_rad) * cos(Hour_Angle_rad)))
    Altitude_deg        = degrees(Altitude_rad)
    a                   =-cos(Declination_rad) * cos(Latitude_rad) * sin(Hour_Angle_rad)
    b                   = sin(Declination_rad) - sin(Latitude_rad) * sin(Altitude_rad)
    Azimuth_rad         = atan2(a,b)
    Azimuth_deg         = degrees(Azimuth_rad)%360
    q_hrs               =(degrees(acos(-tan(Latitude_rad) * tan(Declination_rad)))) / 15
    SR_hrs              = Solar_Noon_hrs - q_hrs
    SS_hrs              = Solar_Noon_hrs + q_hrs
    r_deg               = degrees(acos(-sin(Declination_rad) / cos(Latitude_rad)))
    SRA_deg             = 180 - r_deg
    SSA_deg             = 180 + r_deg

    if Detail_Print:
        print ('--------------')
        print ('Time Related Parameters')
        print ('--------------')
        print ('D0                    = ',round(D0,rounder))
        print ('T                     = ',round(T,rounder))
        print ('GMST_deg              = ',round(GMST_deg,rounder))
        print ('GMST_hrs              = ',round(GMST_hrs,rounder))
        print ('LMST_Hrs              = ',round(LMST_Hrs,rounder))   
        print ('Mean_Longitude_hrs    = ',round(Mean_Longitude_hrs,rounder))
        print ('Mean_Longitude_deg    = ',round(Mean_Longitude_deg,rounder))
        print ('--------------')
        print ('Astronomical Fact')
        print ('--------------')
        print ('Perihelion_deg        = ',round(Perihelion_deg,rounder))
        print ('Eccentricity          = ',round(Eccentricity,rounder))
        print ('Obliquity_deg         = ',round(Obliquity_deg,rounder))
        print ('Obliquity_rad         = ',round(Obliquity_rad,rounder))
        print ('--------------')
        print ('Solving Kepler')
        print ('--------------')
        print ('Mean_Anomaly_deg      = ',round(Mean_Longitude_hrs,rounder))
        print ('Mean Anomaly rad      = ',round(Mean_Anomaly_rad,rounder))
        print ('Eccent Anomaly Iter 1 = ',round(E1,rounder))
        print ('Eccent Anomaly Iter 2 = ',round(E2,rounder))
        print ('True_Anomaly_rad      = ',round(True_Anomaly_rad,rounder))
        print ('True_Anomaly_deg      = ',round(True_Anomaly_deg,rounder))
        print ('True_Longitude_deg    = ',round(True_Long_deg,rounder))
        print ('True_Longitude_rad    = ',round(True_Long_rad,rounder))
        print ('Eccent_Efft_deg       = ',round(Eccent_Effect_deg,rounder))
        print ('Eccent_Efft_min       = ',round(Eccent_Effect_min,rounder))
        print ('                      = ',EoT_Dec_MMSS(Eccent_Effect_min))
        print ('--------------')
        print ('Right Ascension, Declination and EoT')
        print ('--------------')
        print ('Right_Ascension_rad   = ',round(Right_Ascension_rad,rounder))
        print ('Right_Ascension_deg   = ',round(Right_Ascension_deg,rounder))
        print ('                      = ',Dec_Deg_DMS(Right_Ascension_deg))
        print ('Right_Ascension_hrs   = ',round(Right_Ascension_hrs,rounder))
        print ('                      = ',Dec_Hrs_HMS(Right_Ascension_hrs))
        print ('Declination_rad       = ',round(Declination_rad,rounder))
        print ('Declination_deg       = ',round(Declination_deg,rounder))
        print ('                      = ',Dec_Deg_DMS(Declination_deg))
        print ('--------------')
        print ('EoT_deg               = ',round(EoT_deg,rounder))
        print ('EoT_min               = ',round(EoT_min,rounder))
        print ('                      = ',EoT_Dec_MMSS(EoT_min))
        print ('Obliq_Effect_min      = ',round(Obliq_Effect_min,rounder))
        print ('                      = ',EoT_Dec_MMSS(Obliq_Effect_min))
        print ('---------------------')
        print ('Long_Corr             = ',round(Long_Corr,rounder))
        print ('                      = ',EoT_Dec_MMSS(Long_Corr))
        print ('EoT_Corr_min          = ',round(EoT_Corr_min,rounder))
        print ('                      = ',EoT_Dec_MMSS(EoT_Corr_min))
        print ('---------------------')
        print ('Solar_Noon_hrs        = ',round(Solar_Noon_hrs,rounder))
        print ('                      = ',Dec_Hrs_HMS(Solar_Noon_hrs))
        print ('Hour_Angle_hrs        = ',round(Hour_Angle_hrs,rounder))
        print ('Hour_Angle_rad        = ',round(Hour_Angle_rad,rounder))
        print ('Latitude_rad          = ',round(Latitude_rad,rounder))
        print ('Altitude_rad          = ',round(Altitude_rad,rounder))
        print ('Altitude_deg          = ',round(Altitude_deg,rounder))
        print ('                      = ',Dec_Deg_DMS(Altitude_deg))
        print ('a                     = ',round(a,rounder))
        print ('b                     = ',round(b,rounder))
        print ('Azimuth_rad           = ',round(Azimuth_rad,rounder))
        print ('Azimuth_deg           = ',round(Azimuth_deg,rounder))
        print ('                      = ',Dec_Deg_DMS(Azimuth_deg))
        print ('q_hrs                 = ',round(q_hrs,rounder))
        print ('SR_hrs                = ',round(SR_hrs,rounder))
        print ('                      = ',Dec_Hrs_HMS(SR_hrs))
        print ('SS_hrs                = ',round(SS_hrs,rounder))
        print ('                      = ',Dec_Hrs_HMS(SS_hrs))
        print ('r_deg                 = ',round(r_deg,rounder))
        print ('SRA_deg               = ',round(SRA_deg,rounder))
        print ('SSA_deg               = ',round(SSA_deg,rounder))
        print ()
    return EoT_min,EoT_Corr_min,Right_Ascension_hrs,Declination_deg,Altitude_deg,Azimuth_deg,SR_hrs,SRA_deg,SS_hrs,SSA_deg

def Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone):
    JD = Julian (Year,Month,Day,Hour,Zone)     
    Ans = Sun_JD(JD)
    return Ans

def Sun_Year(Year,Longitude,Zone):
    # ---------------------------------------------------------------
    # Routine to Calculate... 
    #      Equation of Time,Longitude Corrected Equation of Time, 
    #      Right Ascension, Declination, Altitude and Azimuth
    # It contains much of the same code as routine Sun
    # ---------------------------------------------------------------
    global Detail_Print
    Detail_Print = False
    JD     = Julian(Year,1,1,12,Zone)
    print ('Date ' + '\t' + 'EoT '+ '\t' + 'Long Corr EoT '+ '\t' + 'RA '+ '\t' + 'Decl ' +  '\t' + 'Alt '+  '\t' + 'Az '  + '\r' )
    Days_in_Year = 366 if Year % 4 == 0 else 365
    for i in range(Days_in_Year):
        EoT_min,EoT_Corr_min,Right_Ascension_hrs,Declination_deg,Altitude_deg,Azimuth_deg,XXX,YYY = Sun_JD(JD)
        print (Get_Calendar_Date(JD,Zone)[6] + '\t ' + str(round(EoT_min,rounder))+ '\t' + str(round(EoT_Corr_min,rounder))+ '\t ' + str(round(Right_Ascension_hrs,rounder))+ '\t ' + str(round(Declination_deg,rounder))+ '\t ' + str(round(Altitude_deg,rounder))+ '\t ' + str(round(Azimuth_deg,rounder))  + '\r' )
        JD += 1

def Julian(Year,Month,Day,Hour,Zone) :
    #===========================================
    # ROUTINE TO GET JULIAN DAY FROM DATE & TIME
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 60-61
    YY                  = Year
    MM                  = Month
    UTC_hrs             = Hour - Zone
    if UTC_hrs<0:  Day -=1
    if UTC_hrs>24: Day +=1
    UTC_hrs             = UTC_hrs % 24
    if Month   <= 2: Month,Year = Month + 12,Year - 1
    a           = int(Year / 100)
    b           = 2 - a + int(a / 4)
    c           = int(365.25 * Year) ;
    d           = int(30.6001 * (Month + 1)) ;
    Julian_Day  = b + c + d + Day + 1720994.5 + (UTC_hrs)/24.

    if Detail_Print:
        print ('---------------------')
        print ('Input')
        print ('---------------------')
        print ('Place                = ',Place)
        print ('Longitude            = ',round(Longitude,rounder))
        print ('Latitude             = ',round(Latitude,rounder))
        print ('Zone                 = ',Zone)
        print ('Year                 = ',YY)
        print ('Month                = ',MM)
        print ('Day                  = ',Day)
        print ('Civil Time           = ',Hour)
        print ('---------------------')
        print ('Julian Day Calculations')
        print ('---------------------')
        print ('UTC_hrs              = ',round(UTC_hrs,rounder))
        print ('a                    = ',a)
        print ('b                    = ',b)
        print ('c                    = ',c)
        print ('c                    = ',d)
        print ('Julian Day           = ',round(Julian_Day,rounder))
    return Julian_Day

def Get_Calendar_Date(The_JD,Zone) :
    #======================================================
    # ROUTINE TO GET CALENDAR DATE AND TIME FROM JULIAN DAY
    # Reference: Practical Astronomy with your Calculator 3rd Edn : Duffet Smith - Page 8
    Month_List = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    JDD                = The_JD + .5 
    III                = int(JDD)
    FFF                = JDD - III
    if III > 2299160 :
        AA             = int((III - 1867216.25) / 36524.25)
        BB             = III + 1 + AA - int(AA / 4)
    else :
        BB             = III
    CC                 = BB + 1524
    DD                 = int((CC - 122.1) / 365.25)
    EE                 = int(365.25 * DD)
    GG                 = int((CC - EE) / 30.6001)
    Day_inc_Frac       = CC - EE + FFF - int(30.6001 * GG)
    Dayo               = int(Day_inc_Frac)
    Hour               = 24 * (Day_inc_Frac - Dayo) + Zone
    Houro              = int(Hour)
    Minute             = 60. * (Hour - Houro)
    Minuteo            = int(Minute)
    Second             = 60. * (Minute-Minuteo)
    if round(Second,3) == 60.:
        Second = 0
        Minuteo += 1
    if Minuteo == 60:
        Minuteo = 0
        Houro +=1
    if GG < 13.5 :
        Montho         = GG - 1
    else :
        Montho         = GG - 13
    if Montho > 2.5 :
        Yearo          = DD - 4716
    else :
        Yearo          = DD - 4715
    Txt = str(Dayo) + '-' + Month_List[Montho-1]
    X = The_JD-.5
    UTC_hrs = ((X-int(X)) * 24) % 24 # Extract UTC_hrs from Julian Day

    Txt = str(Year) + '-' + Month_List[Montho-1] + '-' + str(Dayo) + ' ' + str(Houro) + 'hrs'
    return Yearo,Montho,Dayo,Houro,Minuteo,Second,Txt

def EoT_Dec_MMSS(The_EoT):
    # -----------------------------------------------------
    # Routine to convert Decimal Minutes to Minutes & Seconds
    Sign = '+'
    if The_EoT < 0 : Sign = '-'
    M0   = abs(The_EoT)
    M1   = int(M0)
    S0   = 60 * (M0 - M1)
    return Sign + '%02.0f' % M1 + ':' + '%02.1f' % S0 + ' mm:ss'

def Dec_Deg_DMS(The_Degs) :
    # -----------------------------------------------------
    # Routine to convert Decimal Degrees to Degrees,Minutes & Seconds
    D0 = abs(The_Degs)
    Sign = '+'
    if (The_Degs < 0) : Sign = '-'
    D1 = int(D0)
    M0 = 60. * (D0 - D1)
    M1 = int (M0)
    S0 = 60. * (M0 - M1)
    return Sign + str(round(D1,2)) + u'° ' +str(round(M1,2)) + "' "  + str(round(S0,2))  + "\""

def Dec_Hrs_HMS(The_Hrs) :
    # -----------------------------------------------------
    # Routine to convert Decimal Hours to Hours,Minutes & Seconds
    D0 = abs(The_Hrs)
    Sign = '+'
    if (The_Hrs < 0) : Sign = '-'
    D1 = int(D0)
    M0 = 60. * (D0 - D1)
    M1 = int (M0)
    S0 = 60. * (M0 - M1)
    return Sign + '%.02d' % D1 + u':' +'%.02d' % M1 + u':' + '%2.1f' % S0 + u' hh:mm:ss'

Calculate()

print ('\rDone')
