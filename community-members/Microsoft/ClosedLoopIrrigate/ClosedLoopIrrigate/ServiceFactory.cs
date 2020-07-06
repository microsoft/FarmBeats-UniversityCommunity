using System;
using System.Collections.Generic;
using System.Text;
using Services.Implementation;
using Services.Interfaces;

namespace ClosedLoopIrrigate
{
    public static class ServiceFactory
    {
        public static IIrrigationControl GetIrrigationControl(string apiKey, string location)
        {
            return new Rachio(apiKey, location);
        }

        public static ISensorStations GetSensorStations()
        {
            return new FarmBeats();
            
        }
    }
}
