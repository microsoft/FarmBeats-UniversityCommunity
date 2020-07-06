using System;
using System.Collections.Generic;
using System.Text;
using Flurl;
using Flurl.Http;
using Services.Interfaces;

namespace Services.Implementation
{
    public class Rachio : IIrrigationControl
    {
        private string _apiKey;
        private string _location;
        private string _apiBaseUrl = "https://api.rach.io/1/public";

        public Rachio(string apiKey, string location)
        {
            _apiKey = apiKey;
            _location = location;
        }
        public void RunIrrigation(int seconds)
        {
            var result = _apiBaseUrl
                .AppendPathSegment("zone")
                .AppendPathSegment("start")
                .WithOAuthBearerToken(_apiKey)
                .PutJsonAsync(new { id = "6110cb25-a29d-4d30-87b2-01acffdd0541", duration = seconds}).Result;
        }

     
    }
}
