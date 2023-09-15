# Description & Exanple Input to Routines
# -----------------------------------------------------------------------------------
# SOLAR ASTRONOMY
# -----------------------------------------------------------------------------------
# Python Code written by Kevin Karney, Summer 2023
# Should work on all releases of Python
# Free for anyone to use without any guarantees!
#
# Contains a number Main Sub_Routines - all called by subroutine Calculate
# ----Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone,DST)
#     calculates EoT, Longitude corrected EoT & Declination
#     NOTA BENE
#     by changing the return statement at the end of the routine,
#     any other parameter can be output. (Do not change if you are using the Analemma routines)
# ----Year_Output(Year,Longitude,Zone)
#     provides EoT,Longitude Corrected EoT, Right Ascension, Declination, Altitude & Azimuth
#     as a tab-delimited output copy and pastable into a spreadsheet
# ----EoT_Fourier(Year,Month,Day,Longitude,Zone) & EoT_JD_Fourier
#     provides EoT & Longitude Corrected EoT for any given date & time or Julian Day
# ----Decl_Fourier(Year,Month,Day,Longitude,Zone) & Decl_JD_Fourier 
#     provides Solar Declination for any given date & time or Julian Day
# -----------------------------------------------------
#-----Calculate_Analemma
#     sets up to draw Analemmas & Declination Lines
#     Analemmas - calculates analemma coordinates
#                 using subroutine Shadow 
#     Declination_Lines - calculates declination lines coordinates
#                         using subroutine Shadow 
#     Shadow - calculates the coordinates of the nodus’ shadow on any time & date
#              using subroutine Sun
#     Five Output Print subroutines
# -----------------------------------------------------
# Also contains service routines
# ----Get_Julian_Day            (Year,Month,Day,Hour)    
# ----Get_Calendar_Date         (The_JD)
# ----Get_Date_from_Day_in_Year (Year,Day) # where 1st Jan = 1, etc
# ----EoT_Dec_MMSS              (The_EoT)
# ----Dec_Deg_DMS               (The_Degs)

#     Much of the code in routines Sun, EoT_Fourier and Decl_Fourier
#     relates to printing out all the calculation steps for interest 
#     or debugging purposes.
# ---------------------------------------------------------------------------------------

from math import degrees,radians,tan,sin,acos,cos,floor,atan2,sqrt,asin,pi

# ---------------------------------------------------------------------------------------
# Input 
# ---------------------------------------------------------------------------------------
Place        = “Athens”
Longitude    = 23.71667 # Degrees : +ve East of Greenwich
Latitude     = 37.9666  # Degrees : +ve East of Greenwich
Zone         = 2        # Hrs     : +ve East of Greenwich
DST          = 0
Year         = 2025
Month        = 2
Day          = 13
Hour         = 12
DST          = 0
Detail_Print = False    # Prints detailed calculation steps for day calculation
rounder      = 5        # rounds output to these number of decimals
Year_Calc    = True     # if True, provides values for a whole year
Required     = 2        # 0 = Sun; 1 = Fourier; 2 = Analemma.

#========================================================================================
# FOLLOWING INPUT IS ONLY REQUIRED IF YOU WANT THE OUTPUT OF AN ANALEMMA
# from Robert Sagot and Denis Savoie of Commission des Cadrans Solaires
# Quoted in Meeus, Astronomical Algorithms - Chapter 58
# -----------------------------------------------------
Hour_Start            = 11 
Hour_End              = 14       #   e.g. will draw analemmas from 11 a.m. to 2 p.m.
Analemma_Minute_Inc   = 15       #   e.g 15 if you want analemmas every 15 minutes
Declination_Increment = 5        #   e.g 5 if you want declination points every 5 minutes
Want_Declination_Lines = True
Which_Analemma        = 0        # 0 = Full Analemma : 
                                 # 1 = Daylight Increasing (Winter and Spring) 
                                 # 2 = Daylight Shortening (Summer and Autumn)
Mean_or_Solar         = True     # if False, will produce results for traditional straight-line solar sundial
# -----------------------------------------------------
# Sizes are unitless: Output the same as input
Dial_Plate_Width      = 16 
Dial_Plate_Height     = 16
Nodus_Height          = 5  
Nodus_x               = 4   # Shift Nodus away from physical centre of the Dial Plate in x-direction
Nodus_y               = 4   # ditto in y-direction (+ve Up)
Zenithal_Dist         = 60  # Degrees :  0 = Horizontal, 90 = Vertical
Gnomonic_Decl         = 50  # Degrees :  0 = due South,  90 = due West, 
                            #          180 = due North, 270 = due East
# -----------------------------------------------------
# Input Dates of Solstices, Equinoxs, etc
# -----------------------------------------------------
Spring_Equinox    =  79 # where 1 for 1st Jan
Summer_Solstice   = 172
Autumn_Equinox    = 265
Winter_Solstice   = 355
Equinoxs          = (Spring_Equinox , Autumn_Equinox )
Solstices         = (Summer_Solstice, Winter_Solstice)
# following 2 items must include at lesat 2 items : use (999,999) if none required
Declination_Days  = (1,10,20,999) # e.g. lines on 1st, 10th, 20th of the month
Special_Days      = (40,999)   # use for birthdays, etc
Days_in_Year      = 366 if Year % 4 == 0 else 365
# -----------------------------------------------------
L                 = radians(Latitude)
D                 = radians(Gnomonic_Decl)
Z                 = radians(Zenithal_Dist)
P                 = sin(L) * cos(Z) - cos(L) * sin(Z)  * cos(D)
# X0 & Y0 are the coodinates from the dial Plate centre of ...
# ...the foot of a polar stylus passing through the nodus
# i.e. the centre of the traditional dial
X0                = Nodus_Height * cos(L) * sin(D) / P
Y0                = Nodus_Height * (sin(L) * sin(Z) + cos(L) * cos(Z) * cos(D)) / P
# -----------------------------------------------------
# Note Output File Folder & File will be specific to user’s operating system
# You may have to set sepecific permissions to write to file
Filename = ‘/Users/kevinkarney/Desktop/Annalemma.txt’

#========================================================================================
def Calculate():
    # -----------------------------------------------------
    # This is called from the last line of this code
    # -----------------------------------------------------
    # ACCESS TO SUN ROUTINE
    if Required == 0:
        if Year_Calc == True:
            print (“Year Result from Sun routine”)
            Year_Output(Year,Longitude,Zone)
        else:    
            print (“Results from Sun routine”)
            Results = Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone,DST)
            print (“EoT                     = “,EoT_Dec_MMSS(Results[0]))
            print (“EoT Longitude Corrected = “,EoT_Dec_MMSS(Results[1]))
    # ACCESS TO FOURIER ROUTINE
    elif Required == 1:
        if Year_Calc == True:
            print (“Year Results from Fourier routines”)
            Year_Output_Fourier(Year,Longitude,Zone)
        else:
            print (“Results from EoT_Fourier & Decl_Fourier routines”)
            Results = EoT_Fourier(Year, Month, Day, Longitude, Zone)
            print (“EoT                     = “,EoT_Dec_MMSS(Results[0]))
            print (“EoT Longitude Corrected = “,EoT_Dec_MMSS(Results[1]))
    # ACCESS TO ANALEMMA ROUTINE
    elif Required == 2:
        Calculate_Analemma()

# EoT & Declination Calculation 

def Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone,DST):
    # -----------------------------------------------------
    # This does the main astronomical calculations
    # It returns the EoT, Longitude Corrected EoT & Declination
    # but these may be changed to any other parameter that has been calculated
    # -----------------------------------------------------
    UTC_hrs             = Hour - Zone - DST
    if UTC_hrs<0:  Day -=1
    if UTC_hrs>24: Day +=1
    UTC_hrs             = UTC_hrs % 24
    if (Month <= 2) :
        Year           -= 1
        Month          += 12    
    A                   = floor(Year/100)
    B                   = 2 - A + floor(A/4)
    JD = int(365.25*(Year + 4716)) + int(30.6001*(Month+1)) + Day + B - 1524.5
    #-------------------
    T                   = (JD - 2451545.)/36525
    D0                  = JD - 2451545.
    GMST_hrs            = (6.697374834 + 0.0657098242761  * D0 + 1.00273790935 * UTC_hrs + 0.000026 * T**2) % 24
    Mean_Longitude_hrs  = GMST_hrs + 12. - UTC_hrs
    Mean_Longitude_deg  = Mean_Longitude_hrs * 15
    #-------------------
    # These values obtained from the Astronmical Almanac cvols between 2000 and 2023
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
        print (‘---------------------’)
        print (‘Routine Sun - input’)
        print (‘---------------------’)
        print (“Place                = “,Place)
        print (“Longitude            = “,Longitude)
        print (“Latitude             = “,Latitude)
        print (“Zone                 = “,Zone)
        print (“DST                  = “,DST)
        print (“Year                 = “,Year)
        if Month > 12:
            Year  +=1
            Month -= 12
        print (“Month                = “,Month)
        print (“Day                  = “,Day)
        print (“Civil Time           = “,Hour)
        print (“--------------”)
        print (“Time Related Parameters”)
        print (“--------------”)
        print (“UTC_Hrs               = “,UTC_hrs)
        print (“A                     = “,int(A))
        print (“B                     = “,int(B))
        print (“JD                    = “,round(JD,rounder))
        print (“D0                    = “,round(D0,rounder))
        print (“T                     = “,round(T,rounder))
        print (“GMST_hrs              = “,round(GMST_hrs,rounder))
        print (“Mean_Longitude_hrs    = “,round(Mean_Longitude_hrs,rounder))
        print (“Mean_Longitude_deg    = “,round(Mean_Longitude_deg,rounder))
        print (“--------------”)
        print (“Astronomical Fact”)
        print (“--------------”)
        print (“Perihelion_deg        = “,round(Perihelion_deg,rounder))
        print (“Eccentricity          = “,round(Eccentricity,rounder))
        print (“Obliquity_deg         = “,round(Obliquity_deg,rounder))
        print (“Obliquity_rad         = “,round(Obliquity_rad,rounder))
        print (“--------------”)
        print (“Solving Kepler”)
        print (“--------------”)
        print (“Mean_Anomaly_deg      = “,round(Mean_Longitude_hrs,rounder))
        print (“Mean Anomaly rad      = “,round(Mean_Anomaly_rad,rounder))
        print (“Eccent Anomaly Iter 1 = “,round(E1,rounder))
        print (“Eccent Anomaly Iter 2 = “,round(E2,rounder))
        print (“True_Anomaly_rad      = “,round(True_Anomaly_rad,rounder))
        print (“True_Anomaly_deg      = “,round(True_Anomaly_deg,rounder))
        print (“True_Longitude_deg    = “,round(True_Long_deg,rounder))
        print (“True_Longitude_rad    = “,round(True_Long_rad,rounder))
        print (“Eccent_Efft_deg       = “,round(Eccent_Effect_deg,rounder))
        print (“Eccent_Efft_min       = “,round(Eccent_Effect_min,rounder))
        print (“                      = “,EoT_Dec_MMSS(Eccent_Effect_min))
        print (“--------------”)
        print (“Right Ascension, Declination and EoT”)
        print (“--------------”)
        print (“Right_Ascension_rad   = “,round(Right_Ascension_rad,rounder))
        print (“Right_Ascension_deg   = “,round(Right_Ascension_deg,rounder))
        print (“                      = “,Dec_Deg_DMS(Right_Ascension_deg))
        print (“Right_Ascension_hrs   = “,round(Right_Ascension_hrs,rounder))
        print (“                      = “,Dec_Hrs_HMS(Right_Ascension_hrs))
        print (“Declination_rad       = “,round(Declination_rad,rounder))
        print (“Declination_deg       = “,round(Declination_deg,rounder))
        print (“                      = “,Dec_Deg_DMS(Declination_deg))
        print (“--------------”)
        print (“EoT_deg               = “,round(EoT_deg,rounder))
        print (“EoT_min               = “,round(EoT_min,rounder))
        print (“                      = “,EoT_Dec_MMSS(EoT_min))
        print (“Obliq_Effect_min      = “,round(Obliq_Effect_min,rounder))
        print (“                      = “,EoT_Dec_MMSS(Obliq_Effect_min))
        print (‘---------------------’)
        print (“Long_Corr             = “,round(Long_Corr,rounder))
        print (“                      = “,EoT_Dec_MMSS(Long_Corr))
        print (“EoT_Corr_min          = “,round(EoT_Corr_min,rounder))
        print (“                      = “,EoT_Dec_MMSS(EoT_Corr_min))
        print (‘---------------------’)
        print (“Solar_Noon_hrs        = “,round(Solar_Noon_hrs,rounder))
        print (“                      = “,Dec_Hrs_HMS(Solar_Noon_hrs))
        print (“Hour_Angle_hrs        = “,round(Hour_Angle_hrs,rounder))
        print (“Hour_Angle_rad        = “,round(Hour_Angle_rad,rounder))
        print (“Latitude_rad          = “,round(Latitude_rad,rounder))
        print (“Altitude_rad          = “,round(Altitude_rad,rounder))
        print (“Altitude_deg          = “,round(Altitude_deg,rounder))
        print (“                      = “,Dec_Deg_DMS(Altitude_deg))
        print (“a                     = “,round(a,rounder))
        print (“b                     = “,round(b,rounder))
        print (“Azimuth_rad           = “,round(Azimuth_rad,rounder))
        print (“Azimuth_deg           = “,round(Azimuth_deg,rounder))
        print (“                      = “,Dec_Deg_DMS(Azimuth_deg))
        print (“q_hrs                 = “,round(q_hrs,rounder))
        print (“SR_hrs                = “,round(SR_hrs,rounder))
        print (“                      = “,Dec_Hrs_HMS(SR_hrs))
        print (“SS_hrs                = “,round(SS_hrs,rounder))
        print (“                      = “,Dec_Hrs_HMS(SS_hrs))
        print (“r_deg                 = “,round(r_deg,rounder))
        print (“SRA_deg               = “,round(SRA_deg,rounder))
        print (“SSA_deg               = “,round(SSA_deg,rounder))
        print ()
    return EoT_min,EoT_Corr_min,Declination_deg

def Year_Output(Year,Longitude,Zone):
    # ---------------------------------------------------------------
    # Routine to Calculate... 
    #      Equation of Time,Longitude Corrected Equation of Time, 
    #      Right Ascension, Declination, Altitude and Azimuth
    # It contains much of the same code as routine Sun
    # ---------------------------------------------------------------
    Detail_Print = False
    JD_1_Jan     = Get_Julian_Day(Year,1,1,Hour)
    Days_in_Year = 365 if Year%4 != 0 else 366

    print (“Date “ + “\t” + “EoT “+ “\t” + “Long Corr EoT “+ “\t” + “RA “+ “\t” + “Decl “ +  “\t” + “Alt “+  “\t” + “Az “  + “\r” )

    for i in range(Days_in_Year): 
        JD                  = JD_1_Jan + i
        UTC_hrs             = Hour - Zone
        D0                  = JD - 2451545.
        T                   = D0/36525
        GMST_hrs            = (6.697374834 + 0.0657098242761  * D0 + 1.00273790935 * UTC_hrs + 0.000026 * T**2) % 24
        Mean_Longitude_hrs  = GMST_hrs + 12. - UTC_hrs
        Mean_Longitude_deg  = Mean_Longitude_hrs * 15

        Perihelion_deg      = 282.938     + 1.7     * T
        Eccentricity        = 0.016708617 - 0.00004 * T 
        Obliquity_deg       = 23.43929111 - 0.013   * T
        Obliquity_rad       = radians(Obliquity_deg)

        Mean_Anomaly_deg    = Mean_Longitude_deg - Perihelion_deg
        Mean_Anomaly_rad    = radians(Mean_Anomaly_deg)
        E0 = Mean_Anomaly_rad
        E1 = E0 + (Mean_Anomaly_rad + Eccentricity*sin(E0)- E0)/(1 - Eccentricity*cos(E0))
        E2 = E1 + (Mean_Anomaly_rad + Eccentricity*sin(E1)- E1)/(1 - Eccentricity*cos(E1))
        Eccentric_Anomaly   = E2
        True_Anomaly_rad    = atan2(sqrt(1 - Eccentricity**2) * sin(Eccentric_Anomaly), (cos(Eccentric_Anomaly)- Eccentricity))
        True_Anomaly_deg    = degrees(True_Anomaly_rad)

        True_Long_deg       = True_Anomaly_deg + Perihelion_deg
        True_Long_rad       = radians(True_Long_deg)

        Right_Ascension_rad = atan2(cos(Obliquity_rad) * sin(True_Long_rad),cos(True_Long_rad)) % (2*pi)
        Right_Ascension_deg = (degrees(Right_Ascension_rad)) % 360.
        Right_Ascension_hrs = Right_Ascension_deg / 15.
        Declination_rad     = asin(sin(Obliquity_rad) * sin(True_Long_rad))
        Declination_deg     = degrees(Declination_rad)

        EoT_deg             = Right_Ascension_deg - Mean_Longitude_deg
        if EoT_deg >  180.: EoT_deg = EoT_deg-360.
        if EoT_deg < -180.: EoT_deg = EoT_deg+360.
        EoT_min             = 4 * EoT_deg
        Long_Corr           = 4 * (Zone * 15 - Longitude)
        EoT_Corr_min        = EoT_min + Long_Corr
        Hour_Angle_hrs      = GMST_hrs + Longitude/15. - Right_Ascension_hrs
        Hour_Angle_rad      = radians(Hour_Angle_hrs * 15.)
        Latitude_rad        = radians(Latitude)
        Altitude_rad        = asin((sin(Latitude_rad) * sin(Declination_rad) + cos(Latitude_rad) * cos(Declination_rad) * cos(Hour_Angle_rad)))
        Altitude_deg        = degrees(Altitude_rad)
        a                   =-cos(Declination_rad) * cos(Latitude_rad) * sin(Hour_Angle_rad)
        b                   = sin(Declination_rad) - sin(Latitude_rad) * sin(Altitude_rad)
        Azimuth_rad         = atan2(a,b)
        Azimuth_deg         = degrees(Azimuth_rad)%360

        print (Get_Calendar_Date(JD) + “\t “ + str(round(EoT_min,rounder))+ “\t” + str(round(EoT_Corr_min,rounder))+ “\t “ + str(round(Right_Ascension_hrs,rounder))+ “\t “ + str(round(Declination_deg,rounder))+ “\t “ + str(round(Altitude_deg,rounder))+ “\t “ + str(round(Azimuth_deg,rounder))  + “\r” )

# Short Fourier Routines for EoT & Declination

def EoT_Fourier(Year, Month, Day, Longitude, Zone):
    if Month <= 2: Month,Year = Month + 12,Year - 1
    A = int(Year / 100)
    B = 2 - A + int(A / 4)
    Days_from_2000 = int(365.25 * (Year + 4716)) + int(30.6001 * (Month + 1)) + Day + B  - 2453069.
    Index = (4 * Days_from_2000) % 1461
    Theta = 0.004301 * Index # = 2 pi /1461
    EoT1 = 7.3529 * sin(1 * Theta + 6.2085)
    EoT2 = 9.9269 * sin(2 * Theta + 0.3704)
    EoT3 = 0.3337 * sin(3 * Theta + 0.3042)
    EoT4 = 0.2317 * sin(4 * Theta + 0.7158)
    EoT  = EoT1 + EoT2 + EoT3 + EoT4
    Long_Corr = 4 * (Zone * 15 - Longitude)
    EoT_Corr = EoT + Long_Corr
    if Detail_Print:
        print (“A              = “,A)
        print (“B              = “,B)
        print (“Days_from_2000 = “,round(Days_from_2000,rounder))
        print (“Index          = “,round(Index,rounder))
        print (“Theta          = “,round(Theta,rounder))
        print (“EoT1           = “,round(EoT1,rounder))
        print (“EoT2           = “,round(EoT2,rounder))
        print (“EoT3           = “,round(EoT3,rounder))
        print (“EoT4           = “,round(EoT4,rounder))
        print (“EoT            = “,round(EoT ,rounder))
        print (“               = “,EoT_Dec_MMSS(EoT))
        print (“Long_Corr      = “,round(Long_Corr,rounder))
        print (“               = “,EoT_Dec_MMSS(Long_Corr))
        print (“EoT_Corr       = “,round(EoT_Corr,rounder))
        print (“               = “,EoT_Dec_MMSS(EoT_Corr))
        print ()
    return EoT,EoT_Corr

def EoT_JD_Fourier(JD,Longitude,Zone):
    Days_from_2000 = JD - 2451545.0
    Index          = (4 * Days_from_2000) % 1461
    Theta          = 0.004301 * Index # = 2 pi /1461
    EoT1           = 7.3529 * sin(1 * Theta + 6.2085)
    EoT2           = 9.9269 * sin(2 * Theta + 0.3704)
    EoT3           = 0.3337 * sin(3 * Theta + 0.3042)
    EoT4           = 0.2317 * sin(4 * Theta + 0.7158)
    EoT_min        = EoT1 + EoT2 + EoT3 + EoT4
    Long_Corr      = 4 * (Zone * 15 - Longitude)
    EoT_Corr_min   = EoT_min + Long_Corr
    return EoT_min,EoT_Corr_min

def Decl_Fourier(Year, Month, Day, Hour):
    if Month <= 2: Month,Year = Month + 12,Year - 1
    A = int(Year / 100)
    B = 2 - A + int(A / 4)
    Days_from_2000 = int(365.25 * (Year + 4716)) + int(30.6001 * (Month + 1)) + Day + B + Hour / 24 - 2453069.5
    Index = (4 * Days_from_2000) % 1461
    Theta = 0.004301 * Index
    Aver = 0.3747
    Decl1 = 23.2802 * sin(1 * Theta + 4.8995)
    Decl2 = 0.422 * sin(2 * Theta + 4.8324)
    Decl3 = 0.2034 * sin(3 * Theta + 4.8995)
    Decl4 = 0.0415 * sin(4 * Theta + 4.8465)
    Decl  = Aver + Decl1 + Decl2 + Decl3 + Decl4
    if Detail_Print:
        print (“A              = “,A)
        print (“B              = “,B)
        print (“Days_from_2000 = “,round(Days_from_2000,rounder))
        print (“Index          = “,round(Index,rounder))
        print (“Theta          = “,round(Theta,rounder))
        print (“Aver           = “,round(Aver,rounder))
        print (“Decl1          = “,round(Decl1,rounder))
        print (“Decl2          = “,round(Decl2,rounder))
        print (“Decl3          = “,round(Decl3,rounder))
        print (“Decl4          = “,round(Decl4,rounder))
        print (“Decl           = “,round(Decl ,rounder))
        print (“               = “,Dec_Deg_DMS(Decl))
        print ()
    return Decl

def Decl_JD_Fourier(JD,Longitude,Zone):    
    Days_from_2000 = JD - 2451545.0
    Index          = (4 * Days_from_2000) % 1461
    Theta          = 0.004301 * Index # = 2 pi /1461
    Aver           = 0.3747
    Decl1          = 23.2802 * sin(1 * Theta + 4.8995)
    Decl2          = 0.422 * sin(2 * Theta + 4.8324)
    Decl3          = 0.2034 * sin(3 * Theta + 4.8995)
    Decl4          = 0.0415 * sin(4 * Theta + 4.8465)
    Decl_deg       = Aver + Decl1 + Decl2 + Decl3 + Decl4
    return Decl_deg

def Year_Output_Fourier(Year,Longitude,Zone):
    # ---------------------------------------------------------------
    # Routine to Calculate... 
    #      EoT Longitude Corrected EoT & Solar Declination
    #      at local noon over a whole year
    #      The output is tab delimited text which can be cut and pasted
    #      directly into a spreadsheet.
    # ---------------------------------------------------------------
    Detail_Print    = False
    JD_1_Jan        = Get_Julian_Day(Year,1,1,Hour)
    Days_in_Year    = 365 if Year%4 != 0 else 366
    print (“Date “ + “\t” + “EoT “+ “\t” + “Long Corr EoT “+ “\t” + “Declination “ + “\r” )
    for i in range(Days_in_Year): 
        JD           = JD_1_Jan + i
        Result       = EoT_JD_Fourier(JD, Longitude,Zone)
        EoT_min      = Result[0]
        EoT_Corr_min = Result[1]
        Decl_deg     = Decl_JD_Fourier(JD,Longitude,Zone)
        print (Get_Calendar_Date(JD) + “\t “ + str(round(EoT_min,rounder))+ “\t” + str(round(EoT_Corr_min,rounder))+ “\t “ + str(round(Decl_deg,rounder))  + “\r” )

# Analemma

def Calculate_Analemma():
    File = open(Filename,’w’)
    Print_Super_Header(File)
    Analemmas         (File)
    Declination_Lines (File)
    File.close()

def Analemmas(File):
    # ----------------------------------------------------------
    # Draw the Analemmas
    # Loop over the Hours requested in the day, then each day in the year 
    # It calls routine ‘Shadow’ (& various output formatting rountines)
    # ---------------------------------------------------------- 
    
    Print_Analemma_Header(Hour_Start,File)  

    Start_Minute = Hour_Start * 60
    End_Minute   = Hour_End   * 60
    for Minute in range(Start_Minute,End_Minute+1,Analemma_Minute_Inc) :
        Hour           = Minute / 60.
        Minute_in_Hour = Minute % 60
        Time_Text = str(int(Hour)) + “:” + (“0” if Minute_in_Hour < 10 else “”)+ str(Minute_in_Hour) + “ hh:mm”
        Print_Analemma_Sub_Header(Time_Text,File)
        
        for Day in range(1,Days_in_Year+1) :
            if Day > Summer_Solstice and Day < Winter_Solstice :
                aaa = True
            else:
                aaa = False
            if Day < Summer_Solstice or  Day > Winter_Solstice:
                bbb = True
            else:
                bbb = False
            # This skips out of the loop, if just half the analemma is requested
            if (Which_Analemma == 1 and aaa) or (Which_Analemma == 2 and bbb): 
                 continue
            xx = Get_Date_from_Day_in_Year(Year,Day)
            Day_of_Month = xx[0]
            Month        = xx[1]
            My_Date_Text = xx[2]
            # Find the Shadow Point
            q = Shadow(Year,Month,Day_of_Month,int(Hour),Minute_in_Hour,Longitude,Latitude,Zone,0,File)
 
def Declination_Lines(File):
    # ----------------------------------------------------------
    # Draw the Declination Lines
    # First: Loop over the Days in a Year day, looking for the days on which
    # a declination line is requested  -
    # Second: Loop over Hours during the day
    # It calls routine ‘Shadow’ (& various output formatting rountines)
    # ----------------------------------------------------------
    
    # Don’t try Declination Lines if only a Single Analemma
    if not (Want_Declination_Lines or Hour_Start != Hour_End) :
        return
    
    Print_Declination_Line_Header(File)
    for Day in range(1,Days_in_Year+1):
        xx = Get_Date_from_Day_in_Year(Year,Day)
        Day_in_Month = xx[0]
        Month        = xx[1]
        Date_Text    = xx[2]
        # Only Calculate the Declination Lines on Solstices, Equinoxs, Special Days & selected days of month
        if (Day in Solstices) or (Day in Equinoxs) or (Day in Special_Days) or (Day_in_Month in Declination_Days) :
            # This skips out of the loop, if just half the analemma is requested
            Winter_to_Summer = Day < Summer_Solstice or  Day > Winter_Solstice
            Summer_to_Winter = Day > Summer_Solstice and Day < Winter_Solstice
            if (Which_Analemma == 1 and Summer_to_Winter) or (Which_Analemma == 2 and Winter_to_Summer): 
                continue
    
            Last_Date_Text     = “”
            Minute_Start       = Hour_Start * 60
            Minute_End         = Hour_End   * 60
            for Minute in range (Minute_Start,Minute_End,Declination_Increment):
                Hour           = int(Minute / 60)
                Minute_in_Hour = Minute % 60
                if Date_Text  != Last_Date_Text: 
                    Print_Declination_Lines_Sub_Header(Date_Text,File)
                Last_Date_Text = Date_Text
                # Find the Shadow Point
                q = Shadow(Year,Month,Day_in_Month,Hour,Minute_in_Hour,Longitude,Latitude,Zone,0,File)

Shadow
def Shadow(The_Year,The_Month,The_Day,The_Hour,The_Minute,The_Longitude,The_Latitude,The_Time_Zone,The_DST,File):
    # ---------------------------------------------------------------
    # This is the Gnonomic Heart of the program
    # from Robert Sagot and Denis Savoie of Commission des Cadrans Solaires
    # Quoted in Meeus, Astronomical Algorithms - Chapter 58
    # It calls routine Sun to provide EoT & Decl
    # ---------------------------------------------------------------
    My_Decimal_Hour    = The_Hour + The_Minute/60.
    EoT_min,EoT_Corr_min,Decl_deg  = Sun(The_Year,The_Month,The_Day,The_Hour,The_Longitude,The_Latitude,The_Time_Zone,0)
    # Noon EoT & Decl used to estimate time of sunrise/set
    EoT_min,EoT_Corr_min_Noon,Decl_deg_Noon = Sun(The_Year,The_Month,The_Day,12,The_Longitude,The_Latitude,The_Time_Zone,0)        
    # Traditional Solar Time Sundial requested
    if Mean_or_Solar  == False : 
        EoT_Corr_min       = 4 * (Zone * 15 - Longitude)
        EoT_Corr_min_Noon  = 4 * (Zone * 15 - Longitude)

    Decl_radians       = radians(Decl_deg)
    Decl_radians_noon  = radians(Decl_deg_Noon)
    # ----------------------------------------------------------
    # Find Times of Sun Rise/Set
    # ----------------------------------------------------------
    HA_Sunrise_degrees = degrees(-acos(-tan(L) * tan(Decl_radians_noon)))
    Sunrise_hour       = 12. + HA_Sunrise_degrees/15. - EoT_Corr_min_Noon/60.
    Sunset_hour        = 12. - HA_Sunrise_degrees/15. - EoT_Corr_min_Noon/60.
    # ----------------------------------------------------------
    # Only Continue between Sun Rise and Sun Set
    # ----------------------------------------------------------
    if My_Decimal_Hour >= Sunrise_hour and My_Decimal_Hour <= Sunset_hour:
        H  = radians(((My_Decimal_Hour - EoT_Corr_min/60. - 12.) * 15.))

        Q1 = sin(D) * sin(Z) * sin(H)
        Q2 = (cos(L) * cos(Z) + sin(L) * sin(Z) * cos(D)) * cos(H)
        Q3 = P * tan(Decl_radians)
        Q  = Q1 + Q2 + Q3
        # ----------------------------------------------------------
        # Only Continue if Sun is in front of the surface of the dial plate
        # Reference Meeus Astronomical Algorithms Chapter 58
        # ----------------------------------------------------------
        if Q  > 0 :
            Nx1 = cos(D) * sin(H)
            Nx2 = sin(D) * (sin(L) * cos(H) - cos(L) * tan(Decl_radians))
            Nx = Nx1 - Nx2

            Ny1 = cos(Z)  * sin(D) * sin(H)
            Ny2 = (cos(L) * sin(Z) - sin(L) * cos(Z) * cos(Decl_radians)) * cos(H)
            Ny3 = (sin(L) * sin(Z) + cos(L) * cos(Z) * cos(D)) * tan(Decl_radians)
            Ny = Ny1 - Ny2 - Ny3
            # ----------------------------------------------------------
            # Find Coordinates of Shadow from nodus foot
            # Reference Meeus Astronomical Algorithms Chapter 58
            # ----------------------------------------------------------
            x = (Nodus_Height * Nx / Q)
            y = (Nodus_Height * Ny / Q)
            # ----------------------------------------------------------
            # Find Coordinates of Shadow from plate centre
            # ----------------------------------------------------------
            xx = x + Nodus_x
            yy = y + Nodus_y
            On_Plate = “ “ if ((xx >= -WIDTH/2 and xx <= WIDTH/2) and (yy >= -HEIGHT/2 and yy <= HEIGHT/2)) else “Off Plate”
            
            # Write the output to file
            File.write(str(The_Year) +”\t” + str(The_Month) + “\t” + str(The_Day) + “\t” + str(The_Hour) + “\t” + str(The_Minute) + “\t” + str(round(xx,3)) +”\t”+ str(round(yy,3))+”\t”+ On_Plate +”\r”)
            return
        else:
            File.write(str(The_Year) +”\t” + str(The_Month) + “\t” + str(The_Day) + “\t” + str(The_Hour) + “\t” + str(The_Minute) + “\t\t\t” + “Behind”+”\r”)
            return 
    else:
        File.write(str(My_Year) +”\t” + str(The_Month) + “\t” + str(The_Day) + “\t” + str(The_Hour) + “\t” + str(The_Minute) + “\t\t\t” + “Night”+”\r”)
        return

def Print_Super_Header(File) :
    File.write (“Zenithal_Distance    = “ + str(Zenithal_Dist)        + “ degrees”+”\r”)
    File.write (“Gnomonic_Declination = “ + str(Gnomonic_Decl)        + “ degrees”+”\r”)
    File.write (“Dial_Plate_Width     = “ + str(Dial_Plate_Width )    +”\r”)
    File.write (“Dial_Plate_Height    = “ + str(Dial_Plate_Height)    +”\r”)
    File.write (“Nodus_Height         = “ + str(Nodus_Height     )    +”\r”)
    File.write (“Nodus_x              = “ + str(round(Nodus_x,2))     + “ from plate centre (+ve to right)”+”\r”)
    File.write (“Nodus_y              = “ + str(round(Nodus_y,2))     + “ from plate centre (+ve up)”      +”\r”)
    File.write (“Latitude             = “ + str(Latitude)             + “ degrees +ve N”                       +”\r”)
    File.write (“Longitude            = “ + str(Longitude)            + “ degrees +ve E of Greenwich”          +”\r”)
    File.write (“Time Zone            = “ + str(Zone)                 + “ hours +ve E of Greenwich”            +”\r”)
    File.write (“Polar Style x,y      = “ + str(round(X0,2)) + “,” + str(round(Y0,2))                          +”\r”)                        
        
    if Which_Analemma == 0:
        File.write (“Results for Full Analemma\r”)
    elif Which_Analemma == 1:
        File.write (“Results for Daylight Increasing Days\r”)
    else:
        File.write (“Results for Daylight Decreasing Days\r”)
    File.write (“\r”)
    File.write (“Warnings may be...\r”)
    File.write (“   ‘Off Plate’ = nodus shadow is not on the dial plate\r”)
    File.write (“   ‘Behind’    = calculated nodus shadow behing the dial plate\r”)
    File.write (“   ‘Below’     = night time - sun below horizon\r”)
    File.write (“\r”)

def Print_Analemma_Header(The_Hour,File):
    File.write (“+++++++++++++++++++++++++++++++++++++++++++++++\r”)
    File.write (“A N A L E M M A   L I N E S\r”)
    File.write (“+++++++++++++++++++++++++++++++++++++++++++++++\r”)
    File.write (“Year”+”\t”+”Month”+”\t”+”Day”+”\t”+”Hour”+”\t”+”Minute”+”\t”+”X-Coords” +”\t”+”Y-Coords” +”\t” + “Warnings\r”)

def Print_Analemma_Sub_Header(Time_Text,File):
    File.write (“===============================================\r”)
    File.write (“Analemma for “ + Time_Text +”\r”)
    File.write (“===============================================\r”)

def Print_Declination_Line_Header(File):
    if not(Want_Declination_Lines or Hour_Start != Hour_End): 
        File.write (“\r”)
        File.write (“===============================================\r”)
        File.write (“D E C L I N A T I O N   L I N E S”+”\r”)
        File.write (“===============================================\r”)
        File.write (“Year”+”\t”+”Month”+”\t”+”Day”+”\t”+”Hour”+”\t”+”Minute”+”\t”+”\t”+”X-Coords” +”\t”+”Y-Coords” +”\t” + “Warnings\r”)

def Print_Declination_Lines_Sub_Header(My_Date_Text,File) :
    File.write (“===============================================\r”)
    File.write (“Declination Line for “ + My_Date_Text+”\r”)
    File.write (“===============================================\r”)

def Get_Julian_Day(Year, Month, Day, Hour) :
    #===========================================
    # ROUTINE TO GET JULIAN DAY FROM DATE & TIME
    #Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 60-61
    if Month <= 2 :
        YYear                    = Year - 1
        MMonth                    = Month + 12
    else :
        YYear                    = Year
        MMonth                    = Month
    a                            = int(YYear / 100)
    if YYear > 1582 :
        Switcher                = 1
    else :
        if YYear < 1582 :
            Switcher                = 0
        else :
            if MMonth > 10 :
                Switcher            = 1
            else :
                if MMonth < 10 :
                    Switcher        = 0
                else :
                    if Day >= 15 :
                        Switcher    = 1
                    else :
                        Switcher    = 0
    if Switcher == 0 :
        b                            = 0
    else :
        b                            = 2 - a + int(a / 4)
    c                                = int(365.25 * YYear) ;
    d                                 = int(30.6001 * (MMonth + 1)) ;
    return b + c + d + Day + 1720994.5 + Hour/24.

def Get_Calendar_Date(The_JD) :
    #======================================================
    # ROUTINE TO GET CALENDAR DATE AND TIME FROM JULIAN DAY
    #Reference: Practical Astronomy with your Calculator 3rd Edn : Duffet Smith - Page 8
    Month_List = [“Jan”,”Feb”,”Mar”,”Apr”,”May”,”Jun”,”Jul”,”Aug”,”Sep”,”Oct”,”Nov”,”Dec”]
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
    Hour               = 24 * (Day_inc_Frac - Dayo)
    Houro              = int(Hour)
    Minute             = 60. * (Hour - Houro)
    Minuteo            = int(Minute)
    Second             = 60. * (Minute-Minuteo)                   
    if GG < 13.5 :
        Montho         = GG - 1
    else :
        Montho         = GG - 13
    if Montho > 2.5 :
        Yearo          = DD - 4716
    else :
        Yearo          = DD - 4715
    return str(Dayo) + ‘-’ + Month_List[Montho-1] + ‘-’ + str(Yearo)

def Get_Date_from_Day_in_Year(Year,Day):
    # ---------------------------------------------------------------
    # Utility to provide the civil date from Day Number 
    # Input ‘Day’ is day in year starting with 1 on 1st Jan
    # Output is... 
    #           Day in Month e.g 6th, 13th etc
    #           Month Index e.g 2 for Frbruary
    #           Text Date e.g 27-Apr
    # ---------------------------------------------------------------
    Leap = True if Year % 4 == 0 else False
    if not Leap:
        First_of_Month   = [0,1,32,60,91,121,152,182,213,244,274,305,335]
        end = 365
    else:
        First_of_Month   = [0,1,32,61,92,122,153,183,214,245,275,306,336]
        end = 366
    Month_Names          = [“ “,”Jan”,”Feb”,”Mar”,”Apr”,”May”,”Jun”,
                                “Jul”,”Aug”,”Sep”,”Oct”,”Nov”,”Dec”]
    Month_Index          = 0
    Last_Month_Index     = 0
    for Day_in_Year in range(1,end+1):
        if (Day_in_Year in First_of_Month):
            Month_Index += 1
            Last_Month_Index = Day_in_Year 
        if Day_in_Year == Day:
            Day_in_Month = Day_in_Year - Last_Month_Index + 1
            return Day_in_Month, Month_Index, str(Day_in_Month) + “-” + Month_Names[Month_Index]

def EoT_Dec_MMSS(The_EoT):
    # -----------------------------------------------------
    # Routine to convert Decimal Minutes to Minutes & Seconds
    Sign = “+”
    if The_EoT < 0 : Sign = “-”
    M0   = abs(The_EoT)
    M1   = int(M0)
    S0   = 60 * (M0 - M1)
    return Sign + ‘%02.0f’ % M1 + “:” + ‘%02.1f’ % S0 + “ mm:ss”

def Dec_Deg_DMS(The_Degs) :
    # -----------------------------------------------------
    # Routine to convert Decimal Degrees to Degrees,Minutes & Seconds
    D0 = abs(The_Degs)
    Sign = “+”
    if (The_Degs < 0) : Sign = “-”
    D1 = int(D0)
    M0 = 60. * (D0 - D1)
    M1 = int (M0)
    S0 = 60. * (M0 - M1)
    return Sign + ‘%.02d’ % D1 + u”° “ +’%.02d’ % M1 + u”’ “ + ‘%2.1f’ % S0 + u”””

def Dec_Hrs_HMS(The_Hrs) :
    # -----------------------------------------------------
    # Routine to convert Decimal Hours to Hours,Minutes & Seconds
    D0 = abs(The_Hrs)
    Sign = “+”
    if (The_Hrs < 0) : Sign = “-”
    D1 = int(D0)
    M0 = 60. * (D0 - D1)
    M1 = int (M0)
    S0 = 60. * (M0 - M1)
    return Sign + ‘%.02d’ % D1 + u”:” +’%.02d’ % M1 + u”:” + ‘%2.1f’ % S0 + u” hh:mm:ss”

Calculate()

print (“Done”)