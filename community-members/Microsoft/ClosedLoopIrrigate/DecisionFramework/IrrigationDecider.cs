using System;
using Microsoft.Extensions.Logging;

namespace DecisionFramework
{
    public static class IrrigationDecider
    {
        /// <summary>
        /// Execute Irrigation Decision
        /// </summary>
        /// <param name="soilMoisture">The moisture at 6 inches, this could also change to be a spectrum of mositure in the soil profile</param>
        /// <param name="temperature">The ambient temperature, we don't want to irrigate in freezing temps(for now)</param>
        /// <param name="turnOnIrrigaton">An Action that will turn on the irrigation system for a set number of seconds</param>
        /// <param name="turnOffIrrigation">An Action that will turn off the irrigation system</param>
        public static void Irrigate(double soilMoisture, double temperature, Action<int> turnOnIrrigaton, ILogger log)
        {
            if (soilMoisture < 55 && temperature > 5)
            {
                log.LogInformation("Decision to Irrigate");
                var temperatureAdjustment = 1 + (temperature / 100);
                log.LogInformation($"Irrigation Temperature Adjustment: {temperatureAdjustment}");
                var irrigateDuration = (60 - soilMoisture) * temperatureAdjustment * 75;
                
                log.LogInformation($"Irrigation Duration: {irrigateDuration}");
                turnOnIrrigaton(Convert.ToInt32(irrigateDuration));
            }
        }
    }
}