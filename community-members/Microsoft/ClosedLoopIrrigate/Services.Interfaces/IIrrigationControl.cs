using System;
using System.Collections.Generic;
using System.Text;

namespace Services.Interfaces
{
    public interface IIrrigationControl
    {
        void RunIrrigation(int seconds);
    }
}
