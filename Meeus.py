from math import degrees, radians, atan, atan2, tan, asin, sin, acos, cos, sqrt, pi,floor,modf

def Calc_Meeus():
    Year,Month,Day,Hour,Minute,Second,Zone = 2025,2,13,12,0,0,2
    Topo_Long,Topo_Lat,Height =  23.71667,37.96667,156
    JD = Get_Julian(Year,Month,Day,Hour,Minute,Second)
    x = Meeus (JD,Topo_Long,Topo_Lat,Height,Zone)
    Date_String,Topo_RA_hrs,Topo_Decl_deg,EoT_min,Sol_to_Civil_min,Alt_Airless_deg,Azim_deg = x
    print ("Date String                            = ",Date_String)
    print ("Topocentric RA                 : hrs   = ",Topo_RA_hrs,Dec_to_HH_MM_SS(Topo_RA_hrs))
    print ("Topocentric Declination        : deg   = ",Topo_Decl_deg,Dec_to_DD_MM_SS(Topo_Decl_deg))
    print ("Geocentric EoT                 : mins  = ",EoT_min,Dec_to_MM_SS(EoT_min))
    print ("Solar to Civil                 : mins  = ",Sol_to_Civil_min,Dec_to_MM_SS(Sol_to_Civil_min))
    print ("Solar Altitude (no refraction) : deg   = ",Alt_Airless_deg,Dec_to_DD_MM_SS(Alt_Airless_deg))
    print ("Solar Azimuth                  : deg   = ",Azim_deg,Dec_to_DD_MM_SS(Azim_deg))

def Meeus (JD,Topo_Long,Topo_Lat,Height,Zone):
    X = JD
    X -= 0.5
    fractional_part, UT1_hrs = modf(X * 24)
    UT1_hrs %= 24
    UT1_deg = UT1_hrs * 15.

    Leap_secs = 28
    if JD >2433347.75 and JD <=2434375.5  : Leap_secs = 29
    if JD >2434375.5  and JD <=2435639.5  : Leap_secs = 30
    if JD >2435639.5  and JD <=2436187    : Leap_secs = 31
    if JD >2436187    and JD <=2436859    : Leap_secs = 32
    if JD >2436859    and JD <=2437684    : Leap_secs = 33
    if JD >2437684    and JD <=2438433.75 : Leap_secs = 34
    if JD >2438433.75 and JD <=2438896.25 : Leap_secs = 35
    if JD >2438896.25 and JD <=2439320.75 : Leap_secs = 36
    if JD >2439320.75 and JD <=2439706.75 : Leap_secs = 37
    if JD >2439706.75 and JD <=2440131.5  : Leap_secs = 38
    if JD >2440131.5  and JD <=2440517.25 : Leap_secs = 39
    if JD >2440517.25 and JD <=2440903    : Leap_secs = 40
    if JD >2440903    and JD <=2441288.5  : Leap_secs = 41
    if JD >2441288.5  and JD <=2441499.75 : Leap_secs = 42
    if JD >2441499.75 and JD <=2441683.75 : Leap_secs = 43
    if JD >2441683.75 and JD <=2442048.75 : Leap_secs = 44
    if JD >2442048.75 and JD <=2442413.75 : Leap_secs = 45
    if JD >2442413.75 and JD <=2442778.75 : Leap_secs = 46
    if JD >2442778.75 and JD <=2443144.75 : Leap_secs = 47
    if JD >2443144.75 and JD <=2443509.75 : Leap_secs = 48
    if JD >2443509.75 and JD <=2443874.75 : Leap_secs = 49
    if JD >2443874.75 and JD <=2444239.75 : Leap_secs = 50
    if JD >2444239.75 and JD <=2444786.75 : Leap_secs = 51
    if JD >2444786.75 and JD <=2445151.75 : Leap_secs = 52
    if JD >2445151.75 and JD <=2445516.75 : Leap_secs = 53
    if JD >2445516.75 and JD <=2446247.75 : Leap_secs = 54
    if JD >2446247.75 and JD <=2447161.75 : Leap_secs = 55
    if JD >2447161.75 and JD <=2447892.75 : Leap_secs = 56
    if JD >2447892.75 and JD <=2448257.75 : Leap_secs = 57
    if JD >2448257.75 and JD <=2448804.75 : Leap_secs = 58
    if JD >2448804.75 and JD <=2449169.75 : Leap_secs = 59
    if JD >2449169.75 and JD <=2449534.75 : Leap_secs = 60
    if JD >2449534.75 and JD <=2450083.75 : Leap_secs = 61
    if JD >2450083.75 and JD <=2450630.75 : Leap_secs = 62
    if JD >2450630.75 and JD <=2451179.75 : Leap_secs = 63
    if JD >2451179.75 and JD <=2453736.75 : Leap_secs = 64
    if JD >2453736.75 and JD <=2454832.75 : Leap_secs = 65
    if JD >2454832.75 and JD <=2456109.75 : Leap_secs = 66
    if JD >2456109.75 and JD <=2457204.75 : Leap_secs = 67
    if JD >2457204.75 and JD <=2457754.75 : Leap_secs = 68
    if JD >2457754.75  : Leap_secs = 69
    # Leap_secs=0

    JD_TT_days   = JD + Leap_secs/30./3600.
    tau          = (JD_TT_days - 2451545.)/365250.
    TT_Cent      = tau * 10
    # GET ECLIPTIC LONGITUDE OF SUN using VSOP THEORY
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 166,
    # which uses pages 217 - 219 & Appendix III

    L0  = 175347046
    L0 += 3341656 * cos(4.6692568 + 6283.07585  * tau)
    L0 += 34894   * cos(4.6261    + 12566.15170 * tau)
    L0 +=  3497   * cos(2.7441    + 5753.38490  * tau)
    L0 +=  3418   * cos(2.8289    + 3.52310     * tau)
    L0 +=  3136   * cos(3.6277    + 77713.77150 * tau)
    L0 +=  2676   * cos(4.4181    + 7860.41940  * tau)
    L0 +=  2343   * cos(6.1352    + 3930.20970  * tau)
    L0 +=  1324   * cos(0.7425    + 11506.76980 * tau)
    L0 +=  1273   * cos(2.0371    + 529.69100   * tau)
    L0 +=  1199   * cos(1.1096    + 1577.34350  * tau)
    L0 +=   990   * cos(5.233     + 5884.92700  * tau)
    L0 +=   902   * cos(2.045     + 26.29800    * tau)
    L0 +=   857   * cos(3.508     + 398.14900   * tau)
    L0 +=   780   * cos(1.179     + 5223.69400  * tau)
    L0 +=   753   * cos(2.533     + 5507.55300  * tau)
    L0 +=   505   * cos(4.583     + 18849.22800 * tau)
    L0 +=   492   * cos(4.205     + 775.52300   * tau)
    L0 +=   357   * cos(2.92      + 0.06700     * tau)
    L0 +=   317   * cos(5.849     + 11790.62900 * tau)
    L0 +=   284   * cos(1.899     + 796.29800   * tau)
    L0 +=   271   * cos(0.315     + 10977.07900 * tau)
    L0 +=   243   * cos(0.345     + 5486.77800  * tau)
    L0 +=   206   * cos(4.806     + 2544.31400  * tau)
    L0 +=   205   * cos(1.869     + 5573.14300  * tau)
    L0 +=   202   * cos(2.458     + 6069.77700  * tau)
    L0 +=   156   * cos(0.833     + 213.29900   * tau)
    L0 +=   132   * cos(3.411     + 2942.46300  * tau)
    L0 +=   126   * cos(1.083     + 20.77500    * tau)
    L0 +=   115   * cos(0.645     + 0.98000     * tau)
    L0 +=   103   * cos(0.636     + 4694.00300  * tau)
    L0 +=   102   * cos(0.976     + 15720.83900 * tau)
    L0 +=   102   * cos(4.267     + 7.11400     * tau)
    L0 +=   99    * cos(6.21      + 2146.17000  * tau)
    L0 +=   98    * cos(0.68      + 155.42000   * tau)
    L0 +=   86    * cos(5.98      + 161000.6900 * tau)
    L0 +=   85    * cos(1.3       + 6275.96000  * tau)
    L0 +=   85    * cos(3.67      + 71430.70000 * tau)
    L0 +=   80    * cos(1.81      + 17260.15000 * tau)
    L0 +=   79    * cos(3.04      + 12036.46000 * tau)
    L0 +=   75    * cos(1.76      + 5088.63000  * tau)
    L0 +=   74    * cos(3.50      + 3154.69000  * tau)
    L0 +=   74    * cos(4.68      + 801.82000   * tau)
    L0 +=   70    * cos(0.83      + 9437.76000  * tau)
    L0 +=   62    * cos(3.98      + 8827.39000  * tau)
    L0 +=   61    * cos(1.82      + 7084.90000  * tau)
    L0 +=   57    * cos(2.78      + 6286.60000  * tau)
    L0 +=   56    * cos(4.39      + 14143.50000 * tau)
    L0 +=   56    * cos(3.47      + 6279.55000  * tau)
    L0 +=   52    * cos(0.19      + 12139.55000 * tau)
    L0 +=   52    * cos(1.33      + 1748.02000  * tau)
    L0 +=   51    * cos(0.28      + 5856.48000  * tau)
    L0 +=   49    * cos(0.49      + 1194.45000  * tau)
    L0 +=   41    * cos(5.37      + 8429.24000  * tau)
    L0 +=   41    * cos(2.40      + 19651.05000 * tau)
    L0 +=   39    * cos(6.17      + 10447.39000 * tau)
    L0 +=   37    * cos(6.04      + 10213.29000 * tau)
    L0 +=   37    * cos(2.57      + 1059.38000  * tau)
    L0 +=   36    * cos(1.71      + 2352.87000  * tau)
    L0 +=   36    * cos(1.78      + 6812.77000  * tau)
    L0 +=   33    * cos(0.59      + 17789.85000 * tau)
    L0 +=   30    * cos(0.44      + 83996.85000 * tau)
    L0 +=   30    * cos(2.74      + 1349.87000  * tau)
    L0 +=   25    * cos(3.16      + 4690.48000  * tau)
    L1  = 628331966747
    L1 += 206059  * cos(2.678235  + 6283.07585  * tau)

    L1 += 4303 * cos(2.6351+ 12566.1517 * tau)
    L1 +=  425 * cos(1.59  + 3.523      * tau)
    L1 +=  119 * cos(5.796 + 26.298     * tau)
    L1 +=  109 * cos(2.966 + 1577.344   * tau)
    L1 +=   93 * cos(2.59  + 18849.23   * tau)
    L1 +=   72 * cos(1.14  + 529.69     * tau)
    L1 +=   68 * cos(1.87  + 398.15     * tau)
    L1 +=   67 * cos(4.41  + 5507.55    * tau)
    L1 +=   59 * cos(2.89  + 5223.69    * tau)
    L1 +=   56 * cos(2.17  + 155.42     * tau)
    L1 +=   45 * cos(0.40  + 796.3      * tau)
    L1 +=   36 * cos(0.47  + 775.52     * tau)
    L1 +=   29 * cos(2.65  + 7.11       * tau)
    L1 +=   21 * cos(5.34  + 0.98       * tau)
    L1 +=   19 * cos(1.85  + 5486.78    * tau)
    L1 +=   19 * cos(4.97  + 213.3      * tau)
    L1 +=   17 * cos(2.99  + 6275.96    * tau)
    L1 +=   16 * cos(0.03  + 2544.31    * tau)
    L1 +=   16 * cos(1.43  + 2146.17    * tau)
    L1 +=   15 * cos(1.21  + 10977.08   * tau)
    L1 +=   12 * cos(2.83  + 1748.02    * tau)
    L1 +=   12 * cos(3.26  + 5088.63    * tau)
    L1 +=   12 * cos(5.27  + 1194.45    * tau)
    L1 +=   12 * cos(2.08  + 4694       * tau)
    L1 +=   11 * cos(0.77  + 553.57     * tau)
    L1 +=   10 * cos(1.30  + 6286.6     * tau)
    L1 +=   10 * cos(4.24  + 1349.87    * tau)
    L1 +=    9 * cos(2.70  + 242.73     * tau)
    L1 +=    9 * cos(5.64  + 951.72     * tau)
    L1 +=    8 * cos(5.30  + 2352.87    * tau)
    L1 +=    6 * cos(2.65  + 9437.76    * tau)
    L1 +=    6 * cos(4.67  + 4690.48    * tau)

    L2  = 52919
    L2 += 8720* cos(1.0721 + 6283.0758 * tau)
    L2 += 309 * cos(0.867  + 12566.152 * tau)
    L2 +=  27 * cos(0.05   + 3.52      * tau)
    L2 +=  16 * cos(5.19   + 26.3      * tau)
    L2 +=  16 * cos(3.68   + 155.42    * tau)
    L2 +=  10 * cos(0.76   + 18849.23  * tau)
    L2 +=  9  * cos(2.06   + 77713.77  * tau)
    L2 +=  7  * cos(0.83   + 775.52    * tau)
    L2 +=  5  * cos(4.66   + 1577.34   * tau)
    L2 +=  4  * cos(1.03   + 7.11      * tau)
    L2 +=  4  * cos(3.44   + 5573.14   * tau)
    L2 +=  3  * cos(5.14   + 796.3     * tau)
    L2 +=  3  * cos(6.05   + 5507.55   * tau)
    L2 +=  3  * cos(1.19   + 242.73    * tau)
    L2 +=  3  * cos(6.12   + 529.69    * tau)
    L2 +=  3  * cos(0.31   + 398.15    * tau)
    L2 +=  3  * cos(2.28   + 553.57    * tau)
    L2 +=  2  * cos(4.38   + 5223.69   * tau)
    L2 +=  2  * cos(3.75   + 0.98      * tau)

    L3  = 289 * cos(5.844  + 6283.076  * tau)
    L3 += 35  * cos(0      + 0         * tau)
    L3 += 17  * cos(5.49   + 12566.15  * tau)
    L3 += 3   * cos(5.2    + 155.42    * tau)
    L3 += 1   * cos(4.72   + 3.52      * tau)
    L3 += 1   * cos(5.3    + 18849.23  * tau)
    L3 += 1   * cos(5.97   + 242.73    * tau)

    L4      = 114 * cos(3.142  + 0         * tau)
    L4     += 8   * cos(4.13   + 6283.08   * tau)
    L4     += 1   * cos(3.84   + 12566.15  * tau)

    L5      = 1   * cos(3.14   + 0         * tau)

    XX = (L0 + tau * (L1 + tau * (L2 + tau * (L3 + tau * (L4 + tau * L5))))) / 100000000
    
    Longitude_Ecliptic_VSOP_deg = (degrees(XX) + 180) % 360
    # *************************************************************************
    # GET ECLIPTIC LATITUDE OF SUN USING VSOP THEORY
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 166,
    # which uses pages 217 - 219 & Appendix III

    B0  = 280 * cos(3.199 + 84334.662 * tau)
    B0 += 102 * cos(5.422 + 5507.553  * tau)
    B0 += 80  * cos(3.88  + 5223.69   * tau)
    B0 += 44  * cos(3.7   + 2352.87   * tau)
    B0 += 32  * cos(4     + 1577.34   * tau)
    B1  = 9   * cos(3.9   + 5507.553  * tau)
    B1 += 6   * cos(1.73  + 5223.69   * tau)

    XX = (B0 + tau * B1) / 100000000
    Latitude_Ecliptic_VSOP_deg = -degrees(XX)

    #*************************************************************************
    # GET DISTANCE FROM EARTH TO SUN
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 166,
    # which uses pages 217 - 219 & Appendix III

    R0  = 100013989
    R0 += 1670700   * cos(3.0984635 + 6283.07585 * tau)
    R0 += 13956     * cos(3.05525   + 12566.1517 * tau)
    R0 += 3084      * cos(5.1985    + 77713.7715 * tau)
    
    R0 += 1628 * cos(1.1739  + 5753.3849  * tau)
    R0 += 1576 * cos(2.8469  + 7860.4194  * tau)
    R0 += 925  * cos(5.453   + 11506.77   * tau)
    R0 += 542  * cos(4.564   + 3930.21    * tau)
    R0 += 472  * cos(3.661   + 5884.927   * tau)
    R0 += 346  * cos(0.964   + 5507.553   * tau)
    R0 += 329  * cos(5.9     + 5223.694   * tau)
    R0 += 307  * cos(0.299   + 5573.143   * tau)
    R0 += 243  * cos(4.273   + 11790.629  * tau)
    R0 += 212  * cos(5.847   + 1577.344   * tau)
    R0 += 186  * cos(5.022   + 10977.079  * tau)
    R0 += 175  * cos(3.012   + 18849.228  * tau)
    R0 += 110  * cos(5.055   + 5486.778   * tau)
    R0 += 98   * cos(0.89    + 6069.78    * tau)
    R0 += 86   * cos(5.69    + 15720.84   * tau)
    R0 += 86   * cos(1.27    + 161000.69  * tau)
    R0 += 65   * cos(0.27    + 17260.15   * tau)
    R0 += 63   * cos(0.92    + 529.69     * tau)
    R0 += 57   * cos(2.01    + 83996.85   * tau)
    R0 += 56   * cos(5.24    + 71430.7    * tau)
    R0 += 49   * cos(3.25    + 2544.31    * tau)
    R0 += 47   * cos(2.58    + 775.52     * tau)
    R0 += 45   * cos(5.54    + 9437.76    * tau)
    R0 += 43   * cos(6.01    + 6275.96    * tau)
    R0 += 39   * cos(5.36    + 4694       * tau)
    R0 += 38   * cos(2.39    + 8827.39    * tau)
    R0 += 37   * cos(0.83    + 19651.05   * tau)
    R0 += 37   * cos(4.9     + 12139.55   * tau)
    R0 += 36   * cos(1.67    + 12036.46   * tau)
    R0 += 35   * cos(1.84    + 2942.46    * tau)
    R0 += 33   * cos(0.24    + 7084.9     * tau)
    R0 += 32   * cos(0.18    + 5088.63    * tau)
    R0 += 32   * cos(1.78    + 398.15     * tau)
    R0 += 28   * cos(1.21    + 6286.6     * tau)
    R0 += 28   * cos(1.9     + 6279.55    * tau)
    R0 += 26   * cos(4.59    + 10447.39   * tau)

    R1  = 103019   * cos(1.10749 + 6283.07585 * tau)
    R1 += 1721 * cos(1.0644  + 12566.1517 * tau)
    R1 += 702  * cos(3.142   + 0          * tau)
    R1 += 32   * cos(1.02    + 18849.23   * tau)
    R1 += 31   * cos(2.84    + 5507.55    * tau)
    R1 += 25   * cos(1.32    + 5223.69    * tau)
    R1 += 18   * cos(1.42    + 1577.34    * tau)
    R1 += 10   * cos(5.91    + 10977.08   * tau)
    R1 += 9    * cos(1.42    + 6275.96    * tau)
    R1 += 9    * cos(0.27    + 5486.78    * tau)

    R2  = 4359  * cos(5.7846  + 6283.0758  * tau)
    R2 += 124   * cos(5.579   + 12566.152  * tau)
    R2 += 12    * cos(3.14    + 0          * tau)
    R2 +=  9    * cos(3.63    + 77713.77   * tau)
    R2 +=  6    * cos(1.87    + 5573.14    * tau)
    R2 +=  3    * cos(5.47    + 18849.23   * tau)

    R3  = 145   * cos(4.273   + 6283.076   * tau)
    R3 += 7     * cos(3.92    + 12566.15   * tau)

    R4  = 4     * cos(2.56    + 6283.08    * tau)

    Radius_Vector_AU = (R0 + tau * (R1 + tau * (R2 + tau * (R3 + tau * R4)))) / 100000000

    # *************************************************************************
    # GET NUTATION IN LONGITUDE CORRECTION
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 143 - 145
    # Output is Nutation in Longitude in Seconds of Arc
    # T is Centuries from Epoch J2000.0
    # MEM is Mean Elongation of Moon from Sun
    # MAS is Mean Anomaly of Sun (w.r.t Earth)
    # MAM is Mean Anomaly of Moon
    # MAS is Moon#s Argument of Latitude
    # LAN is Longitude of Ascending Node of Moon
    T = tau * 10.
    MEM = radians(297.85036 + T * (445267.11148  + T * (-0.0019142 + T / 189474)))
    MAS = radians(357.52772 + T * (35999.05034   + T * (-0.0001603 - T / 300000)))
    MAM = radians(134.96298 + T * (477198.867398 + T * (0.0086972  + T / 56250)))
    MAL = radians(93.27191  + T * (483202.017538 + T * (-0.0036825 + T / 327270)))
    LAN = radians(125.04452 + T * (-1934.136261  + T * (0.0020708  + T / 450000)))
    
    Nut_in_Long_deg  = (-171996 - 174.2 * T) * sin(LAN)
    Nut_in_Long_deg += (-13187 - 1.6 * T) * sin(-2 * MEM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-2274 - 0.2 * T) * sin(2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (2062 + 0.2 * T) * sin(2 * LAN)
    Nut_in_Long_deg += (1426 - 3.4 * T) * sin(MAS)
    Nut_in_Long_deg += (712 + 0.1 * T) * sin(MAM)

    Nut_in_Long_deg += (-517 + 1.2 * T) * sin(-2 * MEM + MAS + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-386 - 0.4 * T) * sin(2 * MAL + LAN)
    Nut_in_Long_deg += (-301) * sin(MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (217 - 0.5 * T) * sin(-2 * MEM - MAS + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-158) * sin(-2 * MEM + MAM)
    Nut_in_Long_deg += (129 + 0.1 * T) * sin(-2 * MEM + 2 * MAL + LAN)
    Nut_in_Long_deg += (123) * sin(-MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (63) * sin(2 * MEM)
    Nut_in_Long_deg += (63 + 0.1 * T) * sin(MAM + LAN)
    Nut_in_Long_deg += (-59) * sin(2 * MEM - MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-58 - 0.1 * T) * sin(-MAM + LAN)
    Nut_in_Long_deg += (-51) * sin(MAM + 2 * MAL + LAN)
    Nut_in_Long_deg += (48) * sin(-2 * MEM + 2 * MAM)
    Nut_in_Long_deg += (46) * sin(-2 * MAM + 2 * MAL + LAN)
    Nut_in_Long_deg += (-38) * sin(2 * MEM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-31) * sin(2 * MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (29) * sin(2 * MAM)
    Nut_in_Long_deg += (29) * sin(-2 * MEM + MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (26) * sin(2 * MAL)
    Nut_in_Long_deg += (-22) * sin(-2 * MEM + 2 * MAL)
    Nut_in_Long_deg += (21) * sin(-MAM + 2 * MAL + LAN)
    Nut_in_Long_deg += (17 - 0.1 * T) * sin(2 * MAS)
    Nut_in_Long_deg += (16) * sin(2 * MEM - MAM + LAN)
    Nut_in_Long_deg += (-16 + 0.1 * T) * sin(-2 * MEM + 2 * MAS + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-15) * sin(MAS + LAN)
    Nut_in_Long_deg += (-13) * sin(-2 * MEM + MAM + LAN)
    Nut_in_Long_deg += (-12) * sin(-MAS + LAN)
    Nut_in_Long_deg += (11) * sin(2 * MAM - 2 * MAL)
    Nut_in_Long_deg += (-10) * sin(2 * MEM - MAM + 2 * MAL + LAN)
    Nut_in_Long_deg += (-8) * sin(2 * MEM + MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (7) * sin(MAS + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-7) * sin(-2 * MEM + MAS + MAM)
    Nut_in_Long_deg += (-7) * sin(-MAS + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-7) * sin(2 * MEM + 2 * MAL + LAN)
    Nut_in_Long_deg += (6) * sin(2 * MEM + MAM)
    Nut_in_Long_deg += (6) * sin(-2 * MEM + 2 * MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (6) * sin(-2 * MEM + MAM + 2 * MAL + LAN)
    Nut_in_Long_deg += (-6) * sin(2 * MEM - 2 * MAM + LAN)
    Nut_in_Long_deg += (-6) * sin(2 * MEM + LAN)
    Nut_in_Long_deg += (5) * sin(-MAS + MAM)
    Nut_in_Long_deg += (-5) * sin(-2 * MEM - MAS + 2 * MAL + LAN)
    Nut_in_Long_deg += (-5) * sin(-2 * MEM + LAN)
    Nut_in_Long_deg += (-5) * sin(2 * MAM + 2 * MAL + LAN)
    Nut_in_Long_deg += (4) * sin(-2 * MEM + 2 * MAM + LAN)
    Nut_in_Long_deg += (4) * sin(-2 * MEM + MAS + 2 * MAL + LAN)
    Nut_in_Long_deg += (4) * sin(MAM - 2 * MAL)
    Nut_in_Long_deg += (-4) * sin(-MEM + MAM)
    Nut_in_Long_deg += (-4) * sin(-2 * MEM + MAS)
    Nut_in_Long_deg += (-4) * sin(MEM)
    Nut_in_Long_deg += (3) * sin(MAM + 2 * MAL)
    Nut_in_Long_deg += (-3) * sin(-2 * MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-3) * sin(-MEM - MAS + MAM)
    Nut_in_Long_deg += (-3) * sin(MAS + MAM)
    Nut_in_Long_deg += (-3) * sin(-MAS + MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-3) * sin(2 * MEM - MAS - MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-3) * sin(3 * MAM + 2 * MAL + 2 * LAN)
    Nut_in_Long_deg += (-3) * sin(2 * MEM - MAS + 2 * MAL + 2 * LAN)

    Nut_in_Long_deg = Nut_in_Long_deg * 0.0001 / 3600.

    #*************************************************************************
    # GET NUTATION IN OBLIQUITY CORRECTION
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 143 - 145
    MEM = radians(297.85036 + T * (445267.11148  + T * (-0.0019142 + T / 189474)))
    MAS = radians(357.52772 + T * (35999.05034   + T * (-0.0001603 - T / 300000)))
    MAM = radians(134.96298 + T * (477198.867398 + T * ( 0.0086972 + T /  56250)))
    MAL = radians( 93.27191 + T * (483202.017538 + T * (-0.0036825 + T / 327270)))
    LAN = radians(125.04452 + T * (-1934.136261  + T * ( 0.0020708 + T / 450000)))
    
    Nut_in_Obl_deg     = (92025 + 8.9 * T) * cos( LAN)
    Nut_in_Obl_deg    += ( 5736 - 3.1 * T) * cos(-2 * MEM + 2 * MAL + 2 * LAN)
    
    Nut_in_Obl_deg += (  977 - 0.5 * T) * cos(2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (- 895 + 0.5 * T) * cos(   2 * LAN)
    Nut_in_Obl_deg += (   54 - 0.1 * T) * cos(MAS)
    Nut_in_Obl_deg += (-  7)* cos(MAM)
    Nut_in_Obl_deg += (  224 - 0.6 * T) * cos(-2 * MEM + MAS + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (  200)   * cos(2 * MAL + LAN)
    Nut_in_Obl_deg += (  129 - 0.1 * T) * cos(MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-  95 + 0.3 * T) * cos(-2 * MEM - MAS + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-  70)   * cos(-2 * MEM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (-  53)   * cos(-MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-  33)   * cos(MAM + LAN)
    Nut_in_Obl_deg += (   26)   * cos(2 * MEM - MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (   32)   * cos(-MAM + LAN)
    Nut_in_Obl_deg += (   27)   * cos(MAM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (-  24)   * cos(-2 * MAM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (   16)   * cos(2 * MEM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (   13)   * cos(2 * MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-  12)   * cos(-2 * MEM + MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-10) * cos(-MAM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (-8)  * cos(2 * MEM - MAM + LAN)
    Nut_in_Obl_deg += (7)   * cos(-2 * MEM + 2 * MAS + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (9)   * cos(MAS + LAN)
    Nut_in_Obl_deg += (7)   * cos(-2 * MEM + MAM + LAN)
    Nut_in_Obl_deg += (6)   * cos(-MAS + LAN)
    Nut_in_Obl_deg += (5)   * cos(2 * MEM - MAM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (3)   * cos(2 * MEM + MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-3)  * cos(MAS + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (3)   * cos(-MAS + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (3)   * cos(2 * MEM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (-3)  * cos(-2 * MEM + 2 * MAM + 2 * MAL + 2 * LAN)
    Nut_in_Obl_deg += (-3)  * cos(-2 * MEM + MAM + 2 * MAL + LAN)
    Nut_in_Obl_deg += (3)   * cos(2 * MEM - 2 * MAM + LAN)
    Nut_in_Obl_deg += (3)   * cos(2 * MEM + LAN)
    Nut_in_Obl_deg += (3)   * cos(-2 * MEM - MAS + 2 * MAL + LAN)
    Nut_in_Obl_deg += (3)   * cos(-2 * MEM + LAN)
    Nut_in_Obl_deg += (3)   * cos(2 * MAM + 2 * MAL + LAN)

    Nut_in_Obl_deg = Nut_in_Obl_deg * 0.0001 / 3600

    #*************************************************************************
    # GET MEAN OBLIQUITY OF ECLIPTIC
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 147
    tau0 = tau/10.
    U0   = 23. + 26. / 60. + 21.448 / 3600.
    U1   = -4680.93
    U2   = -1.55
    U3   = 1999.25
    U4   = -51.38
    U5   = -249.67
    U6   = -39.05
    U7   = 7.12
    U8   = 27.87
    U9   = 5.79
    U10  = 2.45
    
    deli = (tau0 * (U1 + tau0 * (U2 + tau0 *(U3 + tau0 * (U4 + tau0 * (U5 + tau0 * (U6 + tau0 * (U7 + tau0 *(U8 + tau0 * (U9 + tau0 * U10))))))))))
    Obliquity_Mean_deg = U0 + deli / 3600
    
    # Convert to FK5 system
    # Meeus page 166
    Lambda_Dash_rad  = radians(Longitude_Ecliptic_VSOP_deg - 1.397 * tau*10 - 0.00031 * UT1_hrs**2)
    Long_Corr        = (-0.09033 + 0.03916 * (cos(Lambda_Dash_rad) + sin(Lambda_Dash_rad)) * tan(radians(Latitude_Ecliptic_VSOP_deg))) / 3600.
    Lat_Corr         = (           0.03916 * (cos(Lambda_Dash_rad) - sin(Lambda_Dash_rad))  ) / 3600.
    Sol_Long_F_deg   = Longitude_Ecliptic_VSOP_deg + Long_Corr
    Sol_Lat_F_deg    = Latitude_Ecliptic_VSOP_deg  + Lat_Corr
    
    # Correct for Nutation & Aberation_deg
    Obl_True_deg     = Obliquity_Mean_deg + Nut_in_Obl_deg
    Aberation_deg    = -20.4898 / Radius_Vector_AU /3600.
    Sol_Long_Appt_deg= Sol_Long_F_deg + Nut_in_Long_deg + Aberation_deg
    
    # Convert >> Radians
    Sol_Long_rad     = radians(Sol_Long_Appt_deg)
    Sol_Lat_rad      = radians(Sol_Lat_F_deg)
    Obl_rad          = radians(Obl_True_deg)
    
    # Convert from Ecliptic to Equatorial
    RA_denom         = sin(Sol_Long_rad) * cos(Obl_rad) - tan(Sol_Lat_rad) * sin(Obl_rad)
    RA_num           = cos(Sol_Long_rad)
    RA_rad           = atan2(RA_denom,RA_num)
    Decl_rad         = asin(sin(Sol_Lat_rad) * cos(Obl_rad) + cos(Sol_Lat_rad) * sin(Obl_rad) *sin(Sol_Long_rad))
    RA_deg = degrees(RA_rad) %360
    RA_hrs = RA_deg/15.
    Decl_deg = degrees(Decl_rad)

    # *************************************************************************
    # Calculate Greenwich Mean Sidereal Time
    # Reference: USNO Circular 179 by G.H. Kaplan
    # The IAU Resolutions on Astronomical Reference Systems, Time Scales,
    # and Earth Rotation Models - Eqns 2.11 & 2.12
    DU               = JD  - 2451545.0
    Theta            = 0.7790572732640 + 0.00273781191135448 * DU + JD % 1.
    GMST_base        = (86400. * Theta)  % 86400.
    GMST_base        = (86400. * Theta)
    Extra            = (0.014506 + TT_Cent * (4612.156534 + TT_Cent * (1.3915817 + TT_Cent * (-0.00000044 + TT_Cent * (-0.000029956 - TT_Cent * 0.0000000368)))))
    GMST_hrs         = ((GMST_base + Extra / 15.) % 86400.)/3600.
    GMST_deg         = 15. * GMST_hrs
    
    #*************************************************************************
    # Calculate Equation of the Equinoxs & Greenwich Apparent Sidereal Time
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 88
    Eqn_of_Equi_deg = Nut_in_Long_deg * cos(Obl_rad)
    GAST_deg        = GMST_hrs * 15. + Eqn_of_Equi_deg
    GAST_hrs        = GAST_deg / 15.
    
    #*************************************************************************
    # Calculate Geocentric Equation of Time
    EoT_deg         = (GMST_deg - UT1_deg - RA_deg + 180. + Eqn_of_Equi_deg ) % 360.
    if EoT_deg  < -180 : EoT_deg = EoT_deg + 360.
    if EoT_deg  >  180 : EoT_deg = EoT_deg - 360.
    EoT_min         = EoT_deg * 4.
    
    #*************************************************************************
    # Local Apparent Siderial Time and Hour Angle
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 92
    LAST_deg        = GAST_deg + Topo_Long - Zone *15
    HA_deg          = (LAST_deg - RA_deg) % 360.
    if HA_deg > 180 : HA_deg -= 360.
    HA_rad          = radians(HA_deg)
    
    #*************************************************************************
    # Calculate Parallax Correction Parameters
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 82 & 279
    Topo_Lat_rad   = radians(Topo_Lat)
    tanu           = 0.99664719 * tan(Topo_Lat_rad)
    u              = atan(tanu)
    Rho_sin_Phi_   = 0.99664719 * sin(u) + sin(Topo_Lat_rad) * Height / 6378140
    if Topo_Lat_rad < 0  : Rho_sin_Phi_ = -Rho_sin_Phi_
    Rho_cos_Phi_   = cos(u) + cos(Topo_Lat_rad) * Height / 6378140
    sin_Pi_        = 3.14159265358979 * 8.794 / Radius_Vector_AU / 180 / 3600
    
    #*************************************************************************
    # Convert Geocentric RA >> Topocentric RA
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 279
    tan_Del_RA     = (-Rho_cos_Phi_ * sin_Pi_ * sin(HA_rad)) / (cos(Decl_rad) - Rho_cos_Phi_ * sin_Pi_ * cos(HA_rad))
    RA_Parallax_rad = atan(tan_Del_RA)
    Topo_RA_deg    = (RA_deg + degrees(RA_Parallax_rad)) % 360
    Topo_RA_hrs    = Topo_RA_deg / 15.
      
    #*************************************************************************
    # Convert Geocentric Declination >> Topocentric Declination
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 279
    tan_dec1       = (sin(Decl_rad) - Rho_sin_Phi_ * sin_Pi_) * cos(RA_Parallax_rad)
    tan_dec2       = (cos(Decl_rad) - Rho_cos_Phi_ * sin_Pi_ * cos(HA_rad))
    Topo_Decl_rad  = atan(tan_dec1 / tan_dec2)
    Topo_Decl_deg  = degrees(Topo_Decl_rad)

    #*************************************************************************
    # Calculate Topocentric Equation of Time
    print (Zone)
    Topo_EoT_deg   = (GAST_deg - UT1_deg - Topo_RA_deg) % 360. - 180.
    Topo_EoT_min   = Topo_EoT_deg * 4.
    
    Sol_to_Civil_min = -Topo_EoT_min + Zone * 60. - Topo_Long * 4.

    #*************************************************************************
    # Calculate Topocentric Hour Angle
    Sol_Hr_Ang_hrs = GAST_hrs + Topo_Long/15 - Topo_RA_hrs
    Sol_Hr_Ang_rad = radians(Sol_Hr_Ang_hrs * 15)
    Sol_Hr_Ang_deg = degrees(Sol_Hr_Ang_rad)

    Topo_HA_deg    = (LAST_deg - Topo_RA_deg) % 360.
    Topo_HA_hrs    = Topo_HA_deg / 15.
    if Topo_HA_deg > 180 : Topo_HA_deg = Topo_HA_deg - 360.
    Topo_HA_rad    = radians(Topo_HA_deg)
    
    #*************************************************************************
    # Convert Hour Angle, Latitude & Declination to Solar Azimuth & Altitude
    # Reference: Astronomical Algorithms 2nd Edition 1998 by Jean Meeus - Page 93
    Alt_rad       = asin(sin(Topo_Lat_rad) * sin(Topo_Decl_rad) + cos(Topo_Lat_rad) * cos(Topo_Decl_rad) * cos(Topo_HA_rad))
    Alt_Airless_deg = degrees(Alt_rad)

    cos_Azim      = (sin(Topo_Decl_rad) - sin(Alt_rad) * sin(Topo_Lat_rad) ) / ( cos(Alt_rad) * cos(Topo_Lat_rad))
    sin_Azim      = - cos(Topo_Decl_rad) * sin(Topo_HA_rad)  /   cos(Alt_rad)
    Azim_rad      = atan2(sin_Azim, cos_Azim)
    Azim_deg      = degrees(Azim_rad) % 360

    Date_String = Get_Date(JD)[5]
    return Date_String,Topo_RA_hrs,Topo_Decl_deg,EoT_min,Sol_to_Civil_min,Alt_Airless_deg,Azim_deg
 
def Get_Date(JD):
    #*************************************************************************
    # G E T   D A T E  F R O M   J U L I A N   D A Y
    # ref Duffet Smith Page 8
    # returns array of [Year,Month,Day,Hour,Minute,Long Date String, Short Date Sring]
    #*************************************************************************
    Month_Names = [" ","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    JD       += .5
    I         = int(JD)
    F         = JD - I
    if I > 1199160:
        A     = int((I - 1867216.25)/36524.25)
        B     = I + 1 + A - int(A/4.)
    else:
        B     = I
    C         = B + 1524
    D         = int((C - 122.1) / 365.25)
    E         = int(365.25 * D)
    G         = int((C - E)  / 30.60001)
    d         = C - E + F - int(30.6001 * G)
    Hour      = 24 * (d - int(d))

    Minute    = int(round(60 * (Hour - int(Hour)),0))
    Hour      = int(Hour)
    Day       = int(d)
    if G < 13.5:
        Month = G - 1
    else:
        Month = G - 13
    if Month > 2.5:
        Year  = D - 4716
    else:
        Year  = D - 4715
        
    Hour_String       = str(Hour)   if Hour   >= 10 else "0" + str(Hour)
    Minute_String     = str(Minute) if Minute >= 10 else "0" + str(Minute)
    Second_String     = "0" + str(Day) if Day<10  else  str(Day)
    Date_String       = Second_String + "-" + Month_Names[Month]  + "-" + str(Year) +" " + Hour_String +":" + Minute_String + " hh:mm"
    Short_Date_String = str(Day) + " " + Month_Names[Month]  + " " + str(Year)
    return [Year,Month,Day,Hour,Minute,Date_String,Short_Date_String]

def Get_Julian(Year,Month,Day,Hour,Minute,Second):
    #*************************************************************************
    # G E T   J U L I A N   D A Y
    # ref Duffet Smith Page 7
    #*************************************************************************
    if Month  <= 2 :
        Year  = Year - 1
        Month = Month + 12
    
    AAAA      = int(Year / 100)
    BBBB      = 2 - AAAA + int(AAAA / 4)
    CCCC      = int(365.25 * Year)
    DDDD      = int(30.6001 * (Month + 1))
    JD        = BBBB + CCCC + DDDD + Day + Hour/24.+ Minute/24./60. + Second/24./60./60. + 1720994.5
    return JD

def Dec_to_DD_MM_SS(Val):
    #*************************************************************************
    # C O N V E R T   D E C I M A L   V A L U E
    # T O   H O U R - M I N U T E - S E C O N D
    #*************************************************************************
    Sign = "-" if Val < 0 else "+"
    
    Vala = abs(Val)
    Degs = int(Vala)
    Degs_string =  ("0"if Degs < 10 else "") + str(Degs)

    Minsa = 60.*(Vala - Degs)
    Mins = int(Minsa)
    Mins_string = ("0"if Mins < 10 else "") + str(Mins)

    Secs = round(60*(Minsa - Mins),2)
    Secs_string = ("0"if Secs < 10 else "") + str(round(Secs,2))
    
    Answer = Sign + Degs_string + ":" + Mins_string  + ":" + Secs_string + " dd:mm:ss.ss"
    return Answer
    
def Dec_to_HH_MM_SS(Val):
    #*************************************************************************
    # C O N V E R T   D E C I M A L   V A L U E
    # T O   H O U R - M I N U T E - S E C O N D
    #*************************************************************************
    Sign = "-" if Val < 0 else "+"
    
    Vala = abs(Val)
    Degs = int(Vala)
    Degs_string =  ("0"if Degs < 10 else "") + str(Degs)

    Minsa = 60.*(Vala - Degs)
    Mins = int(Minsa)
    Mins_string = ("0"if Mins < 10 else "") + str(Mins)

    Secs = round(60*(Minsa - Mins),2)
    Secs_string = ("0"if Secs < 10 else "") + str(round(Secs,2))
    
    Answer = Sign + Degs_string + ":" + Mins_string  + ":" + Secs_string + " hh:mm:ss.ss"
    return Answer

def Dec_to_MM_SS(Val):
    #*************************************************************************
    # C O N V E R T   D E C I M A L   V A L U E
    # T O   M I N U T E - S E C O N D
    #*************************************************************************
    Sign = "-" if Val < 0 else "+"
    
    Vala = abs(Val)
    Mins = int(Vala)
    Mins_string =  ("0"if Mins < 10 else "") + str(Mins)
    
    Secsa = 60.*(Vala - Mins)
    Secs = round(Secsa,2)
    Secs_string = str(Secs)

    Answer = Sign + Mins_string  + ":" + Secs_string + " mm:ss"
    return Answer

Calc_Meeus()
