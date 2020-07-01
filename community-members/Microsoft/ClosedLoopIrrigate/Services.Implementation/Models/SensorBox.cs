using System;
using System.Collections.Generic;
using System.Text;

namespace Services.Implementation.Models
{
    public class SensorBoxData
    {
        public DateTime farmTimeStampUTC { get; set; }
        public DateTime timeStamp { get; set; }
        public DateTime farmTimeStampLocal { get; set; }
        public string farmIanaAbbreviation { get; set; }
        public bool isFuture { get; set; }
        public string farmTimeStampLocalDisplay { get; set; }
        public double compChannel0 { get; set; }
        public double compChannel1 { get; set; }
        public double compChannel2 { get; set; }
        public double compChannel3 { get; set; }
        public double compChannel4 { get; set; }
        public double compChannel5 { get; set; }
        public double compChannel6 { get; set; }
        public double compChannel7 { get; set; }
        public double compChannel8 { get; set; }
        public double compChannel9 { get; set; }
        public double compChannel10 { get; set; }
        public double compChannel11 { get; set; }
        public double compChannel12 { get; set; }
        public double compChannel13 { get; set; }
        public double rawChannel5 { get; set; }
    }

    public class SensorBox
    {
        public string sensorBoxId { get; set; }
        public double timezoneOffset { get; set; }
        public double daylightSavingsOffset { get; set; }
        public bool daylightSavingsObserved { get; set; }
        public IList<string> columns { get; set; }
        public IList<SensorBoxData> sensorBoxData { get; set; }
        public IList<bool> enabled { get; set; }
        public IList<double> max { get; set; }
        public IList<double> min { get; set; }
        public IList<object> defaultInvalid { get; set; }
        public double latestReadingSeconds { get; set; }
        public int rssiColumn { get; set; }
        public string rssiStatusDescription { get; set; }
        public double rssiValue { get; set; }
    }
}
