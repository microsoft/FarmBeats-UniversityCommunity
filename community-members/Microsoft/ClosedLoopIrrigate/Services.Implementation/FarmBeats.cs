using System;
using System.Linq;
using Flurl;
using Flurl.Http;
using Services.Implementation.Models;
using Services.Interfaces;

namespace Services.Implementation
{
    public class FarmBeats : ISensorStations
    {
        private string _baseUrl = "https://nelsonwheatdemowebapp.azurewebsites.net/api/Devices/SensorBoxes/Data/";
        public double GetMoisture(string stationName)
        {
            var sensorData = GetData(stationName);
            return sensorData.compChannel3;
        }

        public double GetTemperature(string stationName)
        {
            var sensorData = GetData(stationName);
            return sensorData.compChannel0;
        }

        private SensorBoxData GetData(string stationName)
        {
            return _baseUrl
                .AppendPathSegment(stationName)
                .AppendPathSegments(new object[] {"1", "0", "true"})
                .GetJsonAsync<SensorBox>()
                .Result
                .sensorBoxData
                .OrderByDescending(s => s.farmTimeStampLocal)
                .First();
        }
    }
    
}
