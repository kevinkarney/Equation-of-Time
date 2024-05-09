from math import degrees,radians,tan,sin,acos,cos,floor,atan2,sqrt,asin,pi
# -----------------------------------------------------------------------------------
# EQUATION OF TIME TABLES
# -----------------------------------------------------------------------------------
# Python Code written by Kevin Karney, Winter 2024
# Should work on all releases of Python
# Free for anyone to use without any guarantees!
#
# NOTA BENE
# where Time is input, it is local STANDARD time (i.e. no Daylight saving). 
# Hence Time Zone occurs in many routines to correct to UTC

# Calculates the values needed for a Equation table
#     it returns either a table, averaged over a leap cycle which starts on 1st March on a leap year 
#     Output is a spreadsheet-readable text file with dates and values
#  
# There are 3 number of routines that are called
#     Sun_JD(JD) which performs the astronomical calculations
#     Julian(Year,Month,Day,Hour,Zone) which gives the Julian Day
#     Get_Calendar_Date(The_JD,Zone) which converts between Julian Day and normal calendar values
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Location Input 
# ---------------------------------------------------------------------------------------
Place          = 'Athens'
Longitude      = 23.71667 # Degrees : +ve East of Greenwich
Latitude       = 37.96667 # Degrees : +ve East of Greenwich
Zone           = 2        # Hrs     : +ve East of Greenwich
Year           = 2024
Table_Fineness = 1        # 0 = every minute      (average over leap cycle)
                          # 1 = every half minute (average over leap cycle)
                          # 2 = every day         (average over leap cycle)

# n.b. Latitude is not required in this routine, but is a necessary parameter 
# for parts of rountine Sun(JD), which are not used in this application.
# Enter any value.

def Calculate(Year):
    # This is called by the last line of the code.
    # Build an empty Matrix to store the results
    Matrix_W = 24 # 2 columns per month
    Matrix_H = 31
    Matrix = [['' for x in range(Matrix_W)] for y in range(Matrix_H)] 
    Month_Names = ['January','February','March','April','May','June','July','August','September','October','November','December']

    if Year % 4 != 0:
        print ("Stopped, for an Equation Tables, Specified Year must be a Leap Year...")
        return

    # Calculations are done from 1st March on a Leap Year
    # until the next 29th Feb, 1461 days later
    JD_Start = Julian(Year  , 3,  1, 12, Zone)
    JD_End   = Julian(Year+4, 2, 29, 12, Zone)

    All_Days   = []
    All_Months = []
    All_EoTs   = []

    # Build arrays with days of months, month name & EoTs
    JD = JD_Start
    for i in range(365):
        All_Days  .append(Get_Calendar_Date(JD,Zone)[2])
        All_Months.append(Get_Calendar_Date(JD,Zone)[1])
        All_EoTs  .append((Sun_JD(JD)[1]+Sun_JD(JD+365)[1]+Sun_JD(JD+2*365)[1]+Sun_JD(JD+3*365)[1])/4)
        JD += 1
    # Get Values for 29th Feb at end of cycle
    All_Days.append(29)
    All_Months.append(2)
    All_EoTs.append(Sun_JD(JD_End)[1])
    
    # rotate the calculated values 60 days backwards to bring 1st Jan to start of array
    All_Days  [:] = All_Days  [-60:366] + All_Days  [0:-60]
    All_Months[:] = All_Months[-60:366] + All_Months[0:-60]
    All_EoTs  [:] = All_EoTs  [-60:366] + All_EoTs  [0:-60]
    
    # build values for table÷ 
    Days,Months,EoTs = [],[],[]
    Last_EoT = 999
    for i in range(366):
        This_Day      = All_Days[i]
        This_Month    = All_Months[i]
        if Table_Fineness == 0:
            This_EoT      = int(round(All_EoTs[i],0))
        elif Table_Fineness == 1:     
            This_EoT      = (round(2*All_EoTs[i],0))/2
        else:
            This_EoT      =  All_EoTs[i]   
            Mins          = int(This_EoT)
            Secs          = int(round(60*(This_EoT - Mins),0))
            if Secs == 60:
                Secs = 0
                Mins += 1
            xx = "0" if Secs < 10 else ""
            yy = "0" if Mins < 10 else ""
            This_EoT      = " " + yy + str(Mins)+ ":"+ xx + str(Secs)

        # Select the days when the appropriate value changes
        # or 1st Month
        if This_Day  == 1 or This_EoT != Last_EoT:
            Days  .append(This_Day)
            Months.append(This_Month)
            EoTs  .append(This_EoT)
            Last_EoT = This_EoT
  
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
    Year_String                = " for Years "  + str(Year) + " - " + str(Year+3)
    File.write("Equation-of-Time Table - Longitude Corrrected - averaged over a leap cycle starting 1st March " + Year_String  + '\r')
    File.write("Place"     + '\t' + Place          + '\r')
    File.write("Longitude" + '\t' + str(Longitude) + '\r')
    File.write("Zone"      + '\t' + str(Zone)      + '\r')
    File.write('\r')
    if Table_Fineness < 2:
        File.write("To read this Table, find the date that is less than or equal to today's date," + '\r') 
        File.write("then read the corresponding value of the Longitude Corrected Equation of Time in minutes" + '\r')
    else:
        File.write("EoT Values are in mm:ss")
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
    print ("Please find output in file " + Table_Filename) 
    print ("which should be in the same folder as this program.")
    print ("The file may be opened in any spreadsheet.")

def Sun_JD(JD):
    # -----------------------------------------------------
    # This does the main astronomical calculations
    # It returns an array containing
    #    EoT_min,EoT_Corr_min,Right_Ascension_hrs,Declination_deg,
    #    Altitude_deg,Azimuth_deg,SR_hrs,SS_hrs
    # -----------------------------------------------------
    # -------------------
    global Detail_Print
    # Extract UTC_hrs from Julian Day
    X = JD -.5
    UTC_hrs = ((X-int(X)) * 24) % 24 

    # Calculate Days since Epoch 2000
    D0                  = JD - 2451545.
    # Julian Centuries since Epoch 2000
    T                   = D0 / 36525

    # Greenwich and Local Mean Sidereal Time
    GMST_deg            = 280.46061837 + 360.98564736629 * D0  + 0.000387933 *T**2 - T**3/38710000.
    GMST_deg            = GMST_deg % 360
    GMST_hrs            = GMST_deg / 15.
    LMST_Hrs            = GMST_hrs + Longitude / 15.

    # Calculate Sun's Mean Longitude    
    Mean_Longitude_hrs  = GMST_hrs + 12. - UTC_hrs
    Mean_Longitude_deg  = Mean_Longitude_hrs * 15

    # Calculate the Sun's main orbital parameters as a function of T
    # These values obtained from the Astronmical Almanac vols between 2000 and 2023
    Perihelion_deg      = 282.938     + 1.7     * T
    Eccentricity        = 0.016708617 - 0.00004 * T 
    Obliquity_deg       = 23.43929111 - 0.013   * T
    Obliquity_rad       = radians(Obliquity_deg)

    # Solve Kepler's Equation to find Sun's True Longitude
    Mean_Anomaly_deg    = Mean_Longitude_deg - Perihelion_deg
    Mean_Anomaly_rad    = radians(Mean_Anomaly_deg)
    E0 = Mean_Anomaly_rad
    E1 = E0 + (Mean_Anomaly_rad + Eccentricity*sin(E0)- E0)/(1 - Eccentricity*cos(E0))
    # p.s.  thissecond Newton Raphson iteration not really needed
    E2 = E1 + (Mean_Anomaly_rad + Eccentricity*sin(E1)- E1)/(1 - Eccentricity*cos(E1))
    Eccentric_Anomaly   = E2
    True_Anomaly_rad    = atan2(sqrt(1 - Eccentricity**2) * sin(Eccentric_Anomaly), (cos(Eccentric_Anomaly)- Eccentricity))
    True_Anomaly_deg    = degrees(True_Anomaly_rad)
    True_Long_deg       = True_Anomaly_deg + Perihelion_deg
    True_Long_rad       = radians(True_Long_deg)
    
    # Calculate the Eccentricity Effect of the EoT
    Eccent_Effect_deg   = True_Long_deg - Mean_Longitude_deg 
    Eccent_Effect_min   = 4 * Eccent_Effect_deg
    
    # Calculate Right Ascension and Declination as a function of Obliquity
    Right_Ascension_rad = atan2(cos(Obliquity_rad) * sin(True_Long_rad),cos(True_Long_rad)) % (2*pi)
    Right_Ascension_deg = (degrees(Right_Ascension_rad)) % 360.
    Right_Ascension_hrs = Right_Ascension_deg / 15.
    Declination_rad     = asin(sin(Obliquity_rad) * sin(True_Long_rad))
    Declination_deg     = degrees(Declination_rad)
    
    # Calculate Equation of Time and Obliquity Effect of EoT
    EoT_deg             = Right_Ascension_deg - Mean_Longitude_deg
    if EoT_deg >  180.: EoT_deg = EoT_deg-360.
    if EoT_deg < -180.: EoT_deg = EoT_deg+360.
    EoT_min             = 4 * EoT_deg
    Obliq_Effect_min    = EoT_min - Eccent_Effect_min
    
    # Calculate Longitude Corrected EoT
    Long_Corr           = 4 * (Zone * 15 - Longitude)
    EoT_Corr_min        = EoT_min + Long_Corr

    # Calculate Time of Solar Noon
    Solar_Noon_hrs      = 12 + EoT_Corr_min/60
    
    # Calculate Solar Hour Angle
    Hour_Angle_hrs      = GMST_hrs + Longitude/15. - Right_Ascension_hrs
    Hour_Angle_rad      = radians(Hour_Angle_hrs * 15.)

    # Calculate Solar Altitude
    Latitude_rad        = radians(Latitude)
    Altitude_rad        = asin((sin(Latitude_rad) * sin(Declination_rad) + cos(Latitude_rad) * cos(Declination_rad) * cos(Hour_Angle_rad)))
    Altitude_deg        = degrees(Altitude_rad)
    
    # Calculate Solar Azimuth
    a                   =-cos(Declination_rad) * cos(Latitude_rad) * sin(Hour_Angle_rad)
    b                   = sin(Declination_rad) - sin(Latitude_rad) * sin(Altitude_rad)
    Azimuth_rad         = atan2(a,b)
    Azimuth_deg         = degrees(Azimuth_rad)%360
    
    # Calculate Approx Time Sunrise and Sunset
    q_hrs               =(degrees(acos(-tan(Latitude_rad) * tan(Declination_rad)))) / 15
    SR_hrs              = Solar_Noon_hrs - q_hrs
    SS_hrs              = Solar_Noon_hrs + q_hrs
    
    # Calculate Approx Solar Azimuth of  Sunrise and Sunset
    r_deg               = degrees(acos(-sin(Declination_rad) / cos(Latitude_rad)))
    SRA_deg             = 180 - r_deg
    SSA_deg             = 180 + r_deg
    
    return EoT_min,EoT_Corr_min,Right_Ascension_hrs,Declination_deg,Altitude_deg,Azimuth_deg,SR_hrs,SS_hrs

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

    Txt = str(Yearo) + '-' + Month_List[Montho-1] + '-' + str(Dayo) + ' ' + str(Houro) + 'hrs'
    return Yearo,Montho,Dayo,Houro,Minuteo,Second,Txt

Calculate(Year)

print ('\rDone')


