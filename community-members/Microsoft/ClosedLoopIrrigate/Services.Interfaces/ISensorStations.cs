using System;

namespace Services.Interfaces
{
    public interface ISensorStations
    {
        double GetMoisture(string stationName);
        double GetTemperature(string stationName);
    }
}
