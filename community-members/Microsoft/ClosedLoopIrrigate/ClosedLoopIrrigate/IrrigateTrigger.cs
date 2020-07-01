using System;
using System.IO;
using System.Threading.Tasks;
using DecisionFramework;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace ClosedLoopIrrigate
{
    public static class IrrigateTrigger
    {
        [FunctionName("IrrigateTrigger")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation($"Irrigate trigger function executed at: {DateTime.Now}");
            
            //Create the connection to FarmBeats for Irrigation
            var sensorStations = ServiceFactory.GetSensorStations();
            var apiToken = Environment.GetEnvironmentVariable("IrrigationAPIToken");
            //Create the connection to the irrigation system
            var irrigationControl = ServiceFactory.GetIrrigationControl(apiToken, "location");

            IrrigationDecider.Irrigate(sensorStations.GetMoisture("F036"),
                sensorStations.GetTemperature("F036"), (int i)=> irrigationControl.RunIrrigation(i), log);
            return new OkObjectResult("Irrigation Decision Successful");
        }
    }
}
