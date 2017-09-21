using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

public class SimProperty
{
    public string Name;
    public Color Color;
    public double Value;

    public SimProperty(string name, Color color)
    {
        this.Name = name;
        this.Color = color;
        this.Value = 0;
    }

    public void SetValue(double value)
    {
        this.Value = value;
    }
}

