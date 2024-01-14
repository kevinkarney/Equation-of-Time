from math import degrees,radians,tan,sin,acos,cos,floor,atan2,sqrt,asin,pi
# -----------------------------------------------------------------------------------
# ANALEMMAS
# -----------------------------------------------------------------------------------
# Python Code written by Kevin Karney, Winter 2024
# Should work on all releases of Python
# Free for anyone to use without any guarantees!
#
# NOTA BENE
# where Time is input, it is local STANDARD time (i.e.no Daylight saving). 
# Hence Time Zone occurs in many routines to correct to UTC,

# The code provides the coordinates required to plot an Analemma on any plane surface
#     a full analemma or days-lengthening or days-shortening analemma can be chosen
#     calculated by subroutine Calculate
#     four main subroutines are called
#         Analemmas         (File)
#         Declination_Lines (File)
#         each of which calls subroutine 
#            Sol(.....) which produces the x-y coordionates of the nodus shadow on the plane
#     Output is a spreadsheet-readable text file with the x-y coordinates
#  
# There are a number of service routines
#     Julian(Year,Month,Day,Hour,Zone) which gives the Julian Day
#     Get_Calendar_Date(The_JD,Zone) which converts between Julian Day and normal calendar values

# There a number of self explanatory print routines used by the Analemma routines

# Much of the code in routines Sun, EoT_Decl_Fourier
# relates to printing out all the calculation steps for interest 
# or debugging purposes.
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# What is Wanted 
# ---------------------------------------------------------------------------------------
global Detail_Print 
Which_Analemma = 2      # 0 = Full Analemma : 
                        # 1 = Daylight Increasing (Winter and Spring) 
#                       # 2 = Daylight Shortening (Summer and Autumn)
# ---------------------------------------------------------------------------------------
# Location Input 
# ---------------------------------------------------------------------------------------
Place          = 'Athens'
Longitude      = 23.71667 # Degrees : +ve East of Greenwich
Latitude       = 37.96667 # Degrees : +ve East of Greenwich
Zone           = 2        # Hrs     : +ve East of Greenwich

Year           = 2024

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
    # this should write output file to same folder as this progranm    
    if Which_Analemma == 0:
        Analemma_Filename      = 'Analemma whole year.txt' 
    elif Which_Analemma == 1:
        Analemma_Filename      = 'Analemma days increasing.txt' 
    else:
        Analemma_Filename      = 'Analemma days decreasing.txt' 
        
    File = open(Analemma_Filename,'w')
    Print_Super_Header(File)
    Find_Solstices_and_Equinoxs(Year)
    Analemmas(File) 
    Declination_Lines(File)
    File.close()
    print ("Please find output in file '" + Analemma_Filename+"',") 
    print ("which should be in the same folder as this program.")
    print ("The file may be opened in any spreadsheet.")

def Find_Solstices_and_Equinoxs(Year):
    # ----------------------------------------------------------
    # Finds the Julian Days for the Equinoxs & Solstices
    # for the specified Year, by looping through the dates that surround
    # surround that event
    # It calls routine 'Julian' & 'Sun(JD)'
    # The output is an array of the four Julian Days
    # ---------------------------------------------------------- 
    global Dates
    Dates = []
    # Find Winter Solstice for previous Year
    JD    = Julian(Year-1,12,18,12,Zone)
    Last  = 25
    for i in range(10):
        Decl = Sun_JD(JD)[3]
        if Decl > Last :
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
     # Find Spring Equinox for Year
    JD = Julian(Year,3,16,12,Zone)
    Last = -10
    for i in range(10):
        Decl = Sun_JD(JD)[3]       
        if Decl > 0:
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
     # Find Summer Solstrice for Year
    JD = Julian(Year,6,16,12,Zone)
    Last=20
    for i in range(10):
        Decl = Sun_JD(JD)[3]
        if Decl < Last :
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    # Find Autumnal Equinox for Year
    JD = Julian(Year,9,16,12,Zone)
    Last = 10
    for i in range(40):
        Decl = Sun_JD(JD)[3]
        if Decl < 0:
            Dates.append(int(JD))
            break
        Last=Decl
        JD+=1
    # Find Winter Solstice for Year
    JD = Julian(Year,12,18,12,Zone)
    Last=-20
    for i in range(10):
        Decl = Sun_JD(JD)[3]
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
    return EoT_min,EoT_Corr_min,Right_Ascension_hrs,Declination_deg,Altitude_deg,Azimuth_deg,SR_hrs,SS_hrs

def Sun(Year,Month,Day,Hour,Longitude,Latitude,Zone):
    JD = Julian (Year,Month,Day,Hour,Zone)     
    Ans = Sun_JD(JD)
    return Ans

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

    Txt = str(Year) + '-' + Month_List[Montho-1] + '-' + str(Dayo) + ' ' + str(Houro) + 'hrs'
    return Yearo,Montho,Dayo,Houro,Minuteo,Second,Txt

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
