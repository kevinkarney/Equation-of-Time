from math import degrees,radians,tan,sin,acos,cos,floor,atan2,sqrt,asin,pi
# -----------------------------------------------------------------------------------
# SOLAR ASTRONOMY
# -----------------------------------------------------------------------------------
# Python Code written by Kevin Karney, Summer 2023
# Should work on all releases of Python
# Free for anyone to use without any guarantees!
#
# NOTA BENE
# where Time is input, it is local STANDARD time (i.e.no Daylight saving). 
# Hence Time Zone occurs in many routines to correct to UTC,

# The code performs four Main Tasks - each of which is chosen and
# specified at the beginning of the code

# FIRST TASK calculates the essential Solar parameters for a given location and date
#     calculated by subroutine Sun_JD(JD)
#     its output is an array comprising:
#          EoT, Longitude Corrected EoT,
#          Right Ascension, Declination
#          Solar Altitude, Azimuth
#          approx time of Sunrise, Sunset
#          NOTA BENE any other calculated solar parameter can be
#               output by changing the return parameters of this routine
#               but do not change if caulculating an analemma
#     Subservient routines are 
#          Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone) which calls Sun_JD(JD)
#          Sun_Year(Year,Longitude,Zone) which gives values for noon over a year
#     output is a tab-delimited which can be pasted into any spreadsheet
# 
# SECOND TASK quickly calculates noon EoT,Longitude Corrected EoT and Declination
#     calculated by subroutine EoT_Decl_JD_Fourier(JD)
#     Output is a 2 value array of Longitude Corrected EoT and Declination
#     Subservient routines are 
#         EoT_Decl_Fourier(Year,Month,Day,Hour,Longitude,Zone)
#         Year_Output_Fourier(Year,Longitude,Zone)
#     output is a tab-delimited which can be pasted into any spreadsheet
# 
# THIRD TASK the coordinates required to plot an Analemma on any plane surface
#     a full analemma or days-lengthening or days-shortening analemma can be chosen
#     calculated by subroutine Calculate_Analemma
#     four main subroutines are called
#         Analemmas         (File)
#         Declination_Lines (File)
#         each of which calls subroutine 
#            Sol(.....) which produces the x-y coordionates of the nodus shadow on the plane
#     Output is a spreadsheet-readable text file with the x-y coordinates

# FOURTH TASK calculate the values needed for a 'Victorian' equation table
#     it returns either a table for a given year -or- averages over a leap cycle 
#     Output is a spreadsheet-readable text file with dates and values
#  
# There are a number of service routines
#     Julian(Year,Month,Day,Hour,Zone) which gives the Julian Day
#     Get_Calendar_Date(The_JD,Zone) which converts between Julian Day and normal calendar values
#     EoT_Dec_MMSS(The_EoT) which formats decimal minutes to mins and second 
#     Dec_Deg_DMS(The_Degs) which formats decimal degrees to degrees, mins and secs
#     Dec_Hrs_HMS(The_Hrs) which formats decimal hours to degrees, mins and secs

# There a number of self explanatory print routines used by the Analemma routines

# Much of the code in routines Sun, EoT_Decl_Fourier
# relates to printing out all the calculation steps for interest 
# or debugging purposes.
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# What is Wanted 
# ---------------------------------------------------------------------------------------
global Detail_Print 
Required       = 2      # 0 = Sun - returns EoT, long corr EoT, RA & Decl, Azimuth & Altitude;
                        # 1 = Fourier - returns EoT, long corr EoT & Decl; 
                        # 2 = Analemma calculations
                        # 3 = Table Table
Which_Analemma = 2      # 0 = Full Analemma : 
                        # 1 = Daylight Increasing (Winter and Spring) 
                        # 2 = Daylight Shortening (Summer and Autumn)
Table_Type     = 0      # 0 = Single Year
                        # 1 = Leap Cycle Average
Table_Fineness = 1      # 0 = every minute
                        # 1 = every half minute
Year_Calc      = True   # if True,  provides values for a whole year at noon 
                        # if False, provides a single set of calculations
Detail_Print   = False  # Prints detailed calculation steps for single day calculation
rounder        = 5      # rounds output to these number of decimals to results
# ---------------------------------------------------------------------------------------
# Location Input 
# ---------------------------------------------------------------------------------------
Place          = 'Athens'
Longitude      = 23.71667 # Degrees : +ve East of Greenwich
Latitude       = 37.96667 # Degrees : +ve East of Greenwich
Zone           = 2        # Hrs     : +ve East of Greenwich

Year           = 2024
Month          = 2        # not required for Year calculation or analemma
Day            = 13       # not required for Year calculation or analemma
Hour           = 12       # not required for Year calculation or analemma

#========================================================================================
#========================================================================================
# FOLLOWING INPUT IS ONLY REQUIRED IF YOU WANT THE OUTPUT OF AN ANALEMMA
# from Robert Sagot and Denis Savoie of Commission des Cadrans Solaires
# Quoted in Meeus, Astronomical Algorithms - Chapter 58
# -----------------------------------------------------
# Note Output File Folder & File may be specific to user's operating system
# You may have to set sepecific permissions to write to file
# -----------------------------------------------------
Hour_Start             = 11
Hour_End               = 14       #   e.g. will draw analemmas from 11 a.m. to 2 p.m.
Analemma_Minute_Inc    = 30       #   e.g 15 if you want analemmas every 15 minutes
Declination_Increment  = 2        #   e.g 5 if you want declination points every 5 minutes
Want_Declination_Lines = True
Mean_or_Solar          = True     # if False, will produce results for traditional straight-line solar sundial
# -----------------------------------------------------
# Sizes are unitless: Output the same as input
Dial_Plate_Width       = 16 
Dial_Plate_Height      = 16
Nodus_Height           = 5  
Nodus_x                = 4   # Shift Nodus away from physical centre of the Dial Plate in x-direction
Nodus_y                = 4   # ditto in y-direction (+ve Up)
Zenithal_Dist          = 60  # Degrees :  0 = Horizontal, 90 = Vertical
Gnomonic_Decl          = 50  # Degrees :  0 = due South,  90 = due West, 
                             #          180 = due North, 270 = due East
# -----------------------------------------------------
# Input Dates of Solstices, Equinoxs, etc
# -----------------------------------------------------
Declination_Days  = [1,10,20]  # e.g. lines on 1st, 10th, 20th of the month
Special_Days      = ["12-May"] # use for birthdays, etc
Days_in_Year      = 366 if Year % 4 == 0 else 365
# -----------------------------------------------------
L                 = radians(Latitude)
D                 = radians(Gnomonic_Decl)
Z                 = radians(Zenithal_Dist)
P                 = sin(L) * cos(Z) - cos(L) * sin(Z)  * cos(D)
# X0 & Y0 are the coodinates from the dial Plate centre of ...
# ...the foot of a polar stylus passing through the nodus
# i.e. the centre of the traditional dial
X0                = Nodus_Height * cos(L)  * sin(D) / P
Y0                = Nodus_Height * (sin(L) * sin(Z) + cos(L) * cos(Z) * cos(D)) / P
#========================================================================================
#========================================================================================

def Calculate():
    # -----------------------------------------------------
    # This is routine called from the last line of this code
    # It selects the task required 
    # -----------------------------------------------------
    # ACCESS TO SUN ROUTINE
    if Required == 0:
        if Year_Calc == True:
            Detail_Print = False
            print ('Year Result from Sun routine')
            Sun_Year(Year,Longitude,Zone) 
            print ("\rThis output can copied and pasted into any spreadsheet")
        else:    
            Results = Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone)
            print ('EoT                     = ',EoT_Dec_MMSS(Results[0]))
            print ('EoT Longitude Corrected = ',EoT_Dec_MMSS(Results[1]))
            print ('Right Ascension         = ',Dec_Hrs_HMS (Results[2]))
            print ('Solar Declination       = ',Dec_Deg_DMS (Results[3]))
            print ('Altitude                = ',Dec_Deg_DMS (Results[4]))
            print ('Azimuth                 = ',Dec_Deg_DMS (Results[5]))

    # ACCESS TO FOURIER ROUTINE
    elif Required == 1:
        if Year_Calc == True:
            Detail_Print = False
            print ('Year Results from Fourier routines')
            Year_Output_Fourier(Year,Longitude,Zone)
            print ("\rThis output can copied and pasted into any spreadsheet")
        else:
            print ('Results from EoT_Decl_Fourier routines')
            Results = EoT_Decl_Fourier(Year,Month,Day,Hour,Longitude,Zone)
            print ('EoT                     = ',round(Results[0],rounder))
            print ('                        = ',EoT_Dec_MMSS(Results[0]))
            print ('EoT Longitude Corrected = ',round(Results[1],rounder))
            print ('                        = ',EoT_Dec_MMSS(Results[1]))
            print ('Solar Declination       = ',round(Results[2],rounder))
            print ('                        = ',Dec_Deg_DMS (Results[2]))
    
    # ACCESS TO ANALEMMA ROUTINE
    elif Required == 2:
        Detailed_Print = False
        Calculate_Analemma()

    # ACCESS TO Table TABLE ROUTINE
    elif Required == 3:
        Detailed_Print = False
        Calculate_Table(Year)
    else:
        print ("Wrong option. Set Required to between 0 & 3")

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
        print ('UTC_Hrs               = ',UTC_hrs)
        print ('JD                    = ',round(JD,rounder))
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
    return EoT_min,EoT_Corr_min,Right_Ascension_hrs,Declination_deg,Altitude_deg,Azimuth_deg,SR_hrs,SS_hrs

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

def EoT_Decl_JD_Fourier(JD):
    Days_from_2000 = JD - 2451545.0
    Index = (4 * Days_from_2000) % 1461
    Theta = 0.004301 * Index # = 2 pi /1461
    # Equation of Time
    EoT1 = 7.3529 * sin(1 * Theta + 6.2085)
    EoT2 = 9.9269 * sin(2 * Theta + 0.3704)
    EoT3 = 0.3337 * sin(3 * Theta + 0.3042)
    EoT4 = 0.2317 * sin(4 * Theta + 0.7158)
    EoT  = EoT1 + EoT2 + EoT3 + EoT4
    Long_Corr = 4 * (Zone * 15 - Longitude)
    EoT_Corr = EoT + Long_Corr
    # Declination
    Aver           = 0.3747
    Decl1          = 23.2802 * sin(1 * Theta + 4.8995)
    Decl2          = 0.422 * sin(2 * Theta + 4.8324)
    Decl3          = 0.2034 * sin(3 * Theta + 4.8995)
    Decl4          = 0.0415 * sin(4 * Theta + 4.8465)
    Decl_deg       = Aver + Decl1 + Decl2 + Decl3 + Decl4

    if Detail_Print : 
        print ('Days_from_2000 = ',round(Days_from_2000,rounder))
        print ('Index          = ',round(Index,rounder))
        print ('Theta          = ',round(Theta,rounder))
        print ('EoT1           = ',round(EoT1,rounder))
        print ('EoT2           = ',round(EoT2,rounder))
        print ('EoT3           = ',round(EoT3,rounder))
        print ('EoT4           = ',round(EoT4,rounder))
        print ('EoT            = ',round(EoT ,rounder))
        print ('               = ',EoT_Dec_MMSS(EoT))
        print ('Long_Corr      = ',round(Long_Corr,rounder))
        print ('               = ',EoT_Dec_MMSS(Long_Corr))
        print ('EoT_Corr       = ',round(EoT_Corr,rounder))
        print ('               = ',EoT_Dec_MMSS(EoT_Corr))
        print ('Aver           = ',round(Aver,rounder))
        print ('Decl1          = ',round(Decl1,rounder))
        print ('Decl2          = ',round(Decl2,rounder))
        print ('Decl3          = ',round(Decl3,rounder))
        print ('Decl4          = ',round(Decl4,rounder))
        print ('Decl           = ',round(Decl_deg ,rounder))
        print ('               = ',Dec_Deg_DMS(Decl_deg))
        print ()
        
    return EoT,EoT_Corr,Decl_deg

def EoT_Decl_Fourier(Year,Month,Day,Hour,Longitude,Zone):
    JD = Julian(Year,Month,Day,Hour,Zone)
    return EoT_Decl_JD_Fourier(JD)

def Year_Output_Fourier(Year,Longitude,Zone):
    # ---------------------------------------------------------------
    # Routine to Calculate the output of EoT_Decl_JD_Fourier routine
    #      at local noon over a whole year
    #      The output is tab delimited text which can be cut and pasted
    #      directly into a spreadsheet.
    # ---------------------------------------------------------------
    global Detail_Print
    Detail_Print    = False
    JD        = Julian(Year,1,1,Hour,Zone)
    Days_in_Year    = 366 if Year % 4 == 0 else 365
    print ('Date ' + '\t' + 'EoT '+ '\t' + 'Long Corr EoT '+ '\t' + 'Declination ' + '\r' )
    for i in range(Days_in_Year):
        EoT_min,EoT_Corr_min,Declination_deg = EoT_Decl_JD_Fourier(JD)
        print (Get_Calendar_Date(JD,Zone)[6] + '\t ' + str(round(EoT_min,rounder))+ '\t' + str(round(EoT_Corr_min,rounder))+ '\t ' + str(round(Declination_deg,rounder)))
        JD += 1

def Calculate_Analemma():
    
    if Which_Analemma == 0:
        Analemma_Filename      = 'Analemma whole year.txt' #this should write output file to same folder as this progran
    elif Which_Analemma == 1:
        Analemma_Filename      = 'Analemma days increasing.txt' #this should write output file to same folder as this progran
    else:
        Analemma_Filename      = 'Analemma days decreasing.txt' #this should write output file to same folder as this progran

    Detail_Print = False
    File = open(Analemma_Filename,'w')
    Print_Super_Header(File)
    Find_Solstices_and_Equinoxs(Year)
    File.close()
    print ("Please find output in file '" + Analemma_Filename+"',") 
    print ("which should be in the same folder as this program.")
    print ("The file may be opened in any spreadsheet.")

def Find_Solstices_and_Equinoxs(Year):
    # ----------------------------------------------------------
    # Finds the Julian Days for the Equinoxs & Solstices
    # for the specified Year, by looping through the dates that surround
    # surround that event
    # It calls routine 'Julian' & 'EoT_Decl_JD_Fourier(JD)'
    # The output is an array of the four Julian Days
    # ---------------------------------------------------------- 
    global Dates
    Dates = []
    # Find Winter Solstice for previous Year
    JD    = Julian(Year-1,12,18,12,Zone)
    Last  = -20
    for i in range(10):
        Decl = EoT_Decl_JD_Fourier(JD)[2]
        if Decl > Last :
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    # Find Spring Equinox for Year
    JD = Julian(Year,3,16,12,Zone)
    Last = -10
    for i in range(10):
        Decl = EoT_Decl_JD_Fourier(JD)[2]
        if Decl > 0:
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    # Find Summer Solstrice for Year
    JD = Julian(Year,6,16,12,Zone)
    Last=20
    for i in range(10):
        Decl = EoT_Decl_JD_Fourier(JD)[2]
        if Decl < Last :
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    # Find Autumnal Equinox for Year
    JD = Julian(Year,9,16,12,Zone)
    Last = 10
    for i in range(10):
        Decl = EoT_Decl_JD_Fourier(JD)[2]
        if Decl < 0:
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    JD = Julian(Year,12,18,12,Zone)
    Last=-20
    for i in range(10):
        Decl = EoT_Decl_JD_Fourier(JD)[2]
        if Decl > Last :
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    return Dates

def Analemmas(File):
    # ----------------------------------------------------------
    # Draw the Analemmas
    # Loop over the Hours requested in the day, then each day in the year 
    # It calls routine 'Shadow' (& various output print formatting rountines)
    # ---------------------------------------------------------- 
    global Dates
    Print_Analemma_Header(Hour_Start,File)  

    Start_Minute = Hour_Start * 60
    End_Minute   = Hour_End   * 60
    for Minute in range(Start_Minute,End_Minute+1,Analemma_Minute_Inc) :
        Hour           = Minute / 60.
        Minute_in_Hour = Minute % 60
        Time_Text = str(int(Hour)) + ':' + ('0' if Minute_in_Hour < 10 else '')+ str(Minute_in_Hour) + ' hh:mm'
        Hr = str(int(Hour))
        Min = str(Minute_in_Hour)
        Print_Analemma_Sub_Header(Hr,Min,File)
 
        if Which_Analemma == 0:
            Start = Dates[0]
            End   = Dates[4]
        elif Which_Analemma == 1:
            Start = Dates[0]
            End   = Dates[2]
        else:
            Start = Dates[2]
            End   = Dates[4]
        for JD in range(Start,End) :
            Inc_Dec = "I" if JD >= Dates[0] and JD < Dates[2] else "D"
            Answer = Get_Calendar_Date(JD,Zone)
            # Find the Shadow Point
            q = Shadow(Inc_Dec,Answer[0],Answer[1],Answer[2],int(Hour),Minute_in_Hour,Longitude,Latitude,Zone,File)
 
def Declination_Lines(File):
    global Dates
    # ----------------------------------------------------------
    # Draw the Declination Lines
    # First: Loop over the Days in a Year day, looking for the days on which
    # a declination line is requested  -
    # Second: Loop over Hours during the day
    # It calls routine 'Shadow' (& various output formatting rountines)
    # ----------------------------------------------------------
    
    # Don't try Declination Lines if only a Single Analemma
    if not (Want_Declination_Lines or Hour_Start != Hour_End) :
        return
    
    if Which_Analemma == 0:
        Start = Dates[0]
        End   = Dates[4]
    elif Which_Analemma == 1:
        Start = Dates[0]
        End   = Dates[2]
    else:
        Start = Dates[2]
        End   = Dates[4]

    Print_Declination_Line_Header(File)
    Last_Date = "xx-xxx"
    for JD in range(Start,End) :
        Year,Month,Day,Hour,Minute,Second,Date_Text = Get_Calendar_Date(JD,Zone)
        if Day in Declination_Days or Date_Text in Special_Days:
            Minute_Start       = Hour_Start * 60
            Minute_End         = Hour_End   * 60
            for Minute in range (Minute_Start,Minute_End+1,Declination_Increment):
                Hour_in_Day    = int(Minute / 60)
                Minute_in_Hour = Minute % 60
                if Date_Text != Last_Date: 
                    Print_Declination_Lines_Sub_Header(Date_Text,File)
                Last_Date = Date_Text
                # Find the Shadow Point
                Inc_Dec = "-"
                q = Shadow(Inc_Dec,Year,Month,Day,Hour_in_Day,Minute_in_Hour,Longitude,Latitude,Zone,File)

def Shadow(Inc_Dec,The_Year,The_Month,The_Day,The_Hour,The_Minute,The_Longitude,The_Latitude,The_Time_Zone,File):
    # ---------------------------------------------------------------
    # This is the Gnonomic Heart of the program
    # from Robert Sagot and Denis Savoie of Commission des Cadrans Solaires
    # Quoted in Meeus, Astronomical Algorithms - Chapter 58
    # It calls routine Sun to provide EoT & Decl
    # ---------------------------------------------------------------
    My_Decimal_Hour    = The_Hour + The_Minute/60.
    Answer  = Sun(The_Year,The_Month,The_Day,The_Hour,The_Longitude,The_Latitude,The_Time_Zone)
    EoT_min,EoT_Corr_min,Decl_deg = Answer[0],Answer[1],Answer[3]
    # Noon EoT & Decl used to estimate time of sunrise/set
    Answer = Sun(The_Year,The_Month,The_Day,12,The_Longitude,The_Latitude,The_Time_Zone)
    EoT_min,EoT_Corr_min_Noon,Decl_deg_Noon = Answer[0],Answer[1],Answer[3]       
    
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
            On_Plate = ' ' if ((xx >= -Dial_Plate_Width/2 and xx <= Dial_Plate_Width/2) and (yy >= -Dial_Plate_Height/2 and yy <= Dial_Plate_Height/2)) else 'Off Plate'
            
            # Write the output to file
            File.write(Inc_Dec + '\t' + str(The_Year) +'\t' + str(The_Month) + '\t' + str(The_Day) + '\t' + str(The_Hour) + '\t' + str(The_Minute) + '\t' + str(round(xx,3)) +'\t'+ str(round(yy,3))+'\t'+ On_Plate +'\r')
            return
        else:
            # Sun is Behind the Plate
            File.write("-" + '\t' + str(The_Year) +'\t' + str(The_Month) + '\t' + str(The_Day) + '\t' + str(The_Hour) + '\t' + str(The_Minute) + '\t\t\t' + 'Behind'+'\r')
            return 
    else:
        # Sun is below Horizons
        File.write("-" + '\t' + str(The_Year) +'\t' + str(The_Month) + '\t' + str(The_Day) + '\t' + str(The_Hour) + '\t' + str(The_Minute) + '\t\t\t' + 'Night'+'\r')
        return

def Calculate_Table(Year):
    # Build an empty Matrix to store the results
    Matrix_W = 24 # 2 columns per month
    Matrix_H = 60
    Matrix = [['' for x in range(Matrix_W)] for y in range(Matrix_H)] 
    Month_Names = ['January','February','March','April','May','June','July','August','September','October','November','December']

    Months,Days,EoTs             =[],[],[]
    Last = 99
    Total_Days = 366 if Year % 4 == 0 else 365
    if Table_Type and Year % 4 != 0:
        print ("Stopped, for Table Table, Specified Year must be Leap...")
    JD = Julian(Year, 1, 1, 12, Zone)
    for i in range (Total_Days):
        Ans = Get_Calendar_Date(JD,Zone)
        Year,Month,Day = Ans[0],Ans[1],Ans[2]
        # Find the Average Longitude Corrected EoT during daylight hours
        Ans = Sun(Year,Month,Day,12,Longitude,Latitude,Zone)
        EoT_Noon  = Ans[1]
        Dawn,Dusk = Ans[6],Ans[7] # these are approx
        EoT_Dawn = Sun(Year,Month,Day,Dawn,Longitude,Latitude,Zone)[1]
        EoT_Dusk = Sun(Year,Month,Day,Dusk,Longitude,Latitude,Zone)[1]
        EoT_Day = (EoT_Dawn + EoT_Dusk)/2
        if Table_Type:
            if Month != 2 or Day != 29:
                Ans = Sun(Year+1,Month,Day,Hour,Longitude,Latitude,Zone)
                Dawn,Dusk = Ans[6],Ans[7] # these are approx
                JD_dawn,JD_dusk = JD - Dawn/24.,JD + Dusk/24.
                EoT_Daw1,EoT_Dusk = Sun_JD(JD_dawn)[1],Sun_JD(JD_dusk)[1]
                EoT_Av = (EoT_Dawn + EoT_Dusk)/2
                EoT_Day_1 = (EoT_Dawn + EoT_Dusk)/2
                
                Ans = Sun(Year+2,Month,Day,Hour,Longitude,Latitude,Zone)
                Dawn,Dusk = Ans[6],Ans[7] # these are approx
                JD_dawn,JD_dusk = JD - Dawn/24.,JD + Dusk/24.
                EoT_Dawn,EoT_Dusk = Sun_JD(JD_dawn)[1],Sun_JD(JD_dusk)[1]
                EoT_Day_2 = (EoT_Dawn + EoT_Dusk)/2
                
                Ans = Sun(Year+3,Month,Day,Hour,Longitude,Latitude,Zone)
                Dawn,Dusk = Ans[6],Ans[7] # these are approx
                JD_dawn,JD_dusk = JD - Dawn/24.,JD + Dusk/24.
                EoT_Dawn,EoT_Dusk = Sun_JD(JD_dawn)[1],Sun_JD(JD_dusk)[1]
                EoT_Day_3 = (EoT_Dawn + EoT_Dusk)/2
                EoT_Day = (EoT_Day + EoT_Day_1 + EoT_Day_2  +EoT_Day_3)/4.
        if Table_Fineness == 0:
            EoT_Day = int(round(EoT_Day,0))
        else:
            EoT_Day = round(2*EoT_Day,0)/2.

        # Build the Values for an Equation Table
        if Day == 1 or EoT_Day != Last:
            Months.append(Month)
            Days  .append(Day)
            EoTs  .append(EoT_Day)
            Last = EoT_Day
        JD +=1
 
    # Build a 24 column matrix (2 cols per month) to store the results  
    The_Month  = 0
    Last_Month = 0
    Row        = -1
    Max_Row    = 1
    This_Day   = -1
    for i in range(len(EoTs)):
        This_Month   = Months[i]
        This_Day     = Days[i]
        This_EoT     = EoTs[i]
        if This_Day == 1:
            Row      = 0
            Kol_Day  = (This_Month-1) * 2 
            Kol_Val  = Kol_Day + 1
        if This_Day == 1:
            Matrix[Row][Kol_Day] = This_Day
            Matrix[Row][Kol_Val] = This_EoT
        else:
            if This_EoT != Last_EoT:
                Matrix[Row][Kol_Day] = This_Day
                Matrix[Row][Kol_Val] = This_EoT
        Max_Row  = max(Max_Row,Row)
        Row     += 1
        Last_EoT = This_EoT
        Max_Row  = max(Max_Row,Row)
    
    # Write Output File
    Table_Filename             = 'Table.txt'
    File                       = open(Table_Filename,'w')
    Year_String                = " for Year " + str(Year)
    if Table_Type: Year_String = " for Years "  + str(Year) + " - " + str(Year+3)
    File.write("Equation-of-Time Table - Longitude Corrrected " + Year_String  + '\r')
    File.write("Place"     + '\t' + Place          + '\r')
    File.write("Longitude" + '\t' + str(Longitude) + '\r')
    File.write("Zone"      + '\t' + str(Zone)      + '\r')
    File.write('\r')
    File.write("To read this Table, find the date that is less than or equal to today's date," + '\r') 
    File.write("then read the corresponding value of the Longitude Corrected Equation of Time in minutes" + '\r')
    File.write('\r')
    
    # Write Column Headings
    String1 = ''
    String2 = ''
    for i in range(12):
        String1 = String1 + str(Month_Names[i]) + '\t\t'
        String2 = String2 + "Day" + '\t'+ "EoT" + '\t'
    String1 = String1[:len(String1) - 1] # delete last tab mark
    String2 = String2[:len(String2) - 1] # delete last tab mark
    File.write(String1 +'\r')
    File.write(String2 +'\r')
    
    # Write Table Data
    for i in range(Max_Row):
        String = ''
        for j in range(24):
            String += str(Matrix[i][j]) + '\t'
        String = String[:len(String) - 1] # delete last tab mark
        File.write(String +'\r')
    File.close()
    print ("Please find output in file 'Table.txt',") 
    print ("which should be in the same folder as this program.")
    print ("The file may be opened in any spreadsheet.")

def Julian(Year,Month,Day,Hour,Zone) :
    #===========================================
    # ROUTINE TO GET JULIAN DAY FROM DATE & TIME
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 60-61
    
    UTC_hrs             = Hour - Zone
    if UTC_hrs<0:  Day -=1
    if UTC_hrs>24: Day +=1
    UTC_hrs             = UTC_hrs % 24
    if Month   <= 2: Month,Year = Month + 12,Year - 1
    a           = int(Year / 100)
    b           = 2 - a + int(a / 4)
    c           = int(365.25 * Year) ;
    d           = int(30.6001 * (Month + 1)) ;
    Julian_Day  = b + c + d + Day + 1720994.5 + (Hour-Zone)/24.

    if Detail_Print:
        print ('---------------------')
        print ('Input')
        print ('---------------------')
        print ('Place                = ',Place)
        print ('Longitude            = ',Longitude)
        print ('Latitude             = ',Latitude)
        print ('Zone                 = ',Zone)
        print ('Year                 = ',Year)
        print ('Month                = ',Month)
        print ('Day                  = ',Day)
        print ('Civil Time           = ',Hour)
        print ('---------------------')
        print ('Julian Day Calculations')
        print ('---------------------')
        print ('UTC_hrs              = ',UTC_hrs)
        print ('a                    = ',a)
        print ('b                    = ',b)
        print ('c                    = ',c)
        print ('c                    = ',d)
        print ('Julian Day           = ',Julian_Day)
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

def Print_Super_Header(File) :
    File.write ('Zenithal_Distance    = ' + "\t" + str(Zenithal_Dist)         + '\t' + ' degrees'+'\r')
    File.write ('Gnomonic_Declination = ' + "\t" + str(Gnomonic_Decl)         + '\t' + ' degrees'+'\r')
    File.write ('Dial_Plate_Width     = ' + "\t" + str(Dial_Plate_Width )     +'\r')
    File.write ('Dial_Plate_Height    = ' + "\t" +  str(Dial_Plate_Height)    +'\r')
    File.write ('Nodus_Height         = ' + "\t" +  str(Nodus_Height     )    +'\r')
    File.write ('Nodus_x              = ' + "\t" +  str(round(Nodus_x,2))     + "\t" + ' from plate centre (+ve to right)'+'\r')
    File.write ('Nodus_y              = ' + "\t" +  str(round(Nodus_y,2))     + "\t" + ' from plate centre (+ve up)'      +'\r')
    File.write ('Latitude             = ' + "\t" +  str(Latitude)             + "\t" + ' degrees +ve N'                   +'\r')
    File.write ('Longitude            = ' + "\t" +  str(Longitude)            + "\t" + ' degrees +ve E of Greenwich'      +'\r')
    File.write ('Time Zone            = ' + "\t" +  str(Zone)                 + "\t" + ' hours +ve E of Greenwich'        +'\r')
    File.write ('Polar Style x        = ' + "\t" + str(round(X0,2))                                                              +'\r')                        
    File.write ('Polar Style y        = ' + "\t" + str(round(Y0,2))                                                              +'\r')                        
        
    if Which_Analemma == 0:
        File.write ('Results for Full Analemma\r')
    elif Which_Analemma == 1:
        File.write ('Results for Daylight Increasing Days\r')
    else:
        File.write ('Results for Daylight Decreasing Days\r')
    File.write ('-\t\r')
    File.write ('Warnings may be...\r')
    File.write ('   Off Plate = nodus shadow is not on the dial plate\r')
    File.write ('   Behind    = calculated nodus shadow behing the dial plate\r')
    File.write ('   Below     = night time - sun below horizon\r')
    File.write ('-\t\r')

def Print_Analemma_Header(The_Hour,File):
    File.write ('+++++++++++++++++++++++++++++++++++++++++++++++\r')
    File.write ('A N A L E M M A   L I N E S\r')
    File.write ('+++++++++++++++++++++++++++++++++++++++++++++++\r')
    File.write ('Inc/Dec' + '\t' 'Year'+'\t'+'Month'+'\t'+'Day'+'\t'+'Hour'+'\t'+'Minute'+'\t'+'X-Coords' +'\t'+'Y-Coords' +'\t' + 'Warnings' +'\t\r')

def Print_Analemma_Sub_Header(Hr,Min,File):
    File.write ('===============================================\r')
    File.write ('Analemma for ' + Hr + ' hr ' + Min + ' min \r')
    File.write ('===============================================\r')

def Print_Declination_Line_Header(File):
    if not(Want_Declination_Lines or Hour_Start != Hour_End): 
        File.write ('\r')
        File.write ('===============================================\r')
        File.write ('D E C L I N A T I O N   L I N E S'+'\r')
        File.write ('===============================================\r')
        File.write ('Year'+'\t'+'Month'+'\t'+'Day'+'\t'+'Hour'+'\t'+'Minute'+'\t'+'\t'+'X-Coords' +'\t'+'Y-Coords' +'\t' + 'Warnings\r')

def Print_Declination_Lines_Sub_Header(My_Date_Text,File) :
    File.write ('===============================================\r')
    File.write ('Declination Line for ' + My_Date_Text+'\r')
    File.write ('===============================================\r')


Calculate()

print ('\rDone')
