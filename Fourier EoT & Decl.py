from math import degrees,radians,tan,sin,acos,cos,floor,atan2,sqrt,asin,pi
# -----------------------------------------------------------------------------------
# EQUATION OF TIME & DECLINATION BY FOURIER
# -----------------------------------------------------------------------------------
# Python Code written by Kevin Karney, Winter 2024
# Should work on all releases of Python
# Free for anyone to use without any guarantees!
#
# NOTA BENE
# where Time is input, it is local STANDARD time (i.e.no Daylight saving). 
# Hence Time Zone occurs in many routines to correct to UTC,

# The code quickly calculates noon EoT,Longitude Corrected EoT and Declination
#     calculated by subroutine EoT_Decl_JD_Fourier(JD)
#     Output is a 2 value array of Longitude Corrected EoT and Declination
#     Subservient routines are 
#         EoT_Decl_Fourier(Year,Month,Day,Hour,Longitude,Zone)
#         Year_Output_Fourier(Year,Longitude,Zone)
#     output is a tab-delimited which can be pasted into any spreadsheet
# 
# There are a number of service routines
#     Julian(Year,Month,Day,Hour,Zone) which gives the Julian Day
#     EoT_Dec_MMSS(The_EoT) which formats decimal minutes to mins and second 
#     Dec_Deg_DMS(The_Degs) which formats decimal degrees to degrees, mins and secs
#     Dec_Hrs_HMS(The_Hrs) which formats decimal hours to degrees, mins and secs

# Much of the code in routines EoT_Decl_JD_Fourier & Julian
# relates to printing out all the calculation steps for interest 
# or debugging purposes.
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# What is Wanted 
# ---------------------------------------------------------------------------------------
# global Detail_Print 
Year_Calc      = False  # if True,  provides values for a whole year at noon 
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

def Calculate():
    # -----------------------------------------------------
    # This is routine called from the last line of this code
    # It selects the task required 
    # -----------------------------------------------------
    if Year_Calc == True:
        Detail_Print = False
        print ('Year Results from Fourier routines')
        Year_Output_Fourier(Year,Longitude,Zone)
        print ("\rThis output can copied and pasted into any spreadsheet")
    else:
        print ('Results from EoT_Decl_Fourier routines')
        Results = EoT_Decl_Fourier(Year,Month,Day,Hour,Longitude,Zone)
        print ('Place                   = ',Place)
        print ('Longitude               = ',Longitude)
        print ('Zone                    = ',Zone)
        print ('Year                    = ',Year)
        print ('Month                   = ',Month)
        print ('Day                     = ',Day)
        print ('Local Standard Hour     = ',Hour)
        print ('EoT                     = ',round(Results[0],rounder))
        print ('                        = ',EoT_Dec_MMSS(Results[0]))
        print ('EoT Longitude Corrected = ',round(Results[1],rounder))
        print ('                        = ',EoT_Dec_MMSS(Results[1]))
        print ('Solar Declination       = ',round(Results[2],rounder))
        print ('                        = ',Dec_Deg_DMS (Results[2]))
 
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
        print ('Place          = ',Place)
        print ('Longitude      = ',Longitude)
        print ('Latitude       = ',Latitude)
        print ('Zone           = ',Zone)
        print ('Year           = ',Year)
        print ('Month          = ',Month)
        print ('Day            = ',Day)
        print ('Civil Time     = ',Hour)
        print ('---------------------')
        print ('Julian Day Calculations')
        print ('---------------------')
        print ('UTC_hrs        = ',UTC_hrs)
        print ('a              = ',a)
        print ('b              = ',b)
        print ('c              = ',c)
        print ('d              = ',d)
        print ('Julian Day     = ',round(Julian_Day,rounder))
    return Julian_Day

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

Calculate()

print ('\rDone')
