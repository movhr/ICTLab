using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TimeFrame {
    
    public DateTime SimTime;
    public string SensorLocation;
    public string SensorName;
    public string SensorType;
    public double SensorValue;

    public TimeFrame() { }

    public TimeFrame(string actualTime, string simTime, string location, string name, string type, string value)
    {
        this.SimTime = DateTime.Parse(simTime);
        this.SensorLocation = location;
        this.SensorName = name;
        this.SensorType = type;
        this.SensorValue = Double.Parse(value);
    }

    public TimeFrame(IList<object> obj)
    {
        this.SimTime = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        this.SimTime = this.SimTime.AddMilliseconds(Convert.ToDouble(obj[1]));
        this.SensorLocation = (string)obj[2];
        this.SensorName = (string)obj[3];
        this.SensorType = (string)obj[4];
        this.SensorValue = Convert.ToDouble(obj[5]);
    }
}
