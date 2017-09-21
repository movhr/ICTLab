using System;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

public class SimObject
{
    private static Dictionary<string, Color> Colors = new Dictionary<string, Color>();
    private static GameObject HaloPrefab = (GameObject)Resources.Load("HaloPrefab");
    private const int MinHaloSize = 2;
    private const int MaxHaloSize = 5;
    public Light Halo;
    public Light ParentLight;
    public GameObject goSelf;
    public readonly bool IsHaloSelf;
    public readonly bool IsParentLight;
    public bool IsActive { private set; get; }
    public List<SimProperty> Properties;
    public Dictionary<string, SimProperty> PropertyDict;

    public static Color INT2RGB(string type, uint val)
    {
        Color color;
        if (!Colors.TryGetValue(type, out color))
        {
            uint r = val >> 24;
            uint g = val << 16 >> 24;
            uint b = val % 256;
            color = new Color()
            {
                a = 1,
                g = g / 255f,
                b = b / 255f,
                r = r / 255f
            };
            Colors.Add(type, color);
        }
        return color;
    }

    public SimObject(string goTag, string type, uint color, string parentNode, Vector3 location)
    {
        // Try find GO for location
        this.goSelf = GameObject.FindGameObjectWithTag(goTag);

        // Create halo if none exist
        // Else get by component
        var newGo = GameObject.Instantiate<GameObject>(HaloPrefab);
        var newHalo = newGo.GetComponent<Light>();
        this.Halo = newHalo;
        this.Halo.enabled = false;

        if (this.goSelf)
        {
            var parentLight = this.goSelf.GetComponent<Light>();
            if(parentLight)
            {
                ParentLight = parentLight;
                IsParentLight = true;
                ParentLight.enabled = false;
            }
            this.IsHaloSelf = true;
            this.Halo.transform.parent = this.goSelf.transform;
            this.Halo.transform.position = this.Halo.transform.parent.position;
        }
        else
        {
            IsParentLight = false;
            this.IsHaloSelf = true;
            this.goSelf = newGo;
            this.goSelf.tag = goTag;
            this.goSelf.transform.position = location;
        }
        this.Properties = new List<SimProperty>();
        this.PropertyDict = new Dictionary<string, SimProperty>();
        this.AddProperty(type, color);
    }

    public void AddProperty(string type, uint color)
    {
        var newProp = new SimProperty(type, INT2RGB(type, color));
        this.PropertyDict.Add(type, newProp);
        this.Properties.Add(newProp);
    }

    public void SetProperty(string type, double value)
    {
        this.PropertyDict[type].SetValue(value);
    }

    public void CommitProperties()
    {
        var color_intensity = this.MixColorsAndIntensity();
        this.Halo.color = color_intensity.Item1;
        this.Halo.range = color_intensity.Item2;
    }

    public void On(string type, double strength)
    {
        if (!IsActive)
            this.Activate();
        this.SetProperty(type, strength);

    }

    public void Off()
    {
        if (IsActive)
            this.Deactivate();
    }

    private static bool IsBetween(double val, double min, double max)
    {
        return val > min && val <= max;
    }

    private float GetIntensity(double val)
    {
        if (IsBetween(val, 0, 15))
            return 2;
        if (IsBetween(val, 15, 50))
            return 3;
        if (IsBetween(val, 50, 100))
            return 4;
        else
            return 5;
    }

    private Tuple<Color, float> MixColorsAndIntensity()
    {
        double totalValue = 0;
        var colors = new Color[this.Properties.Count];
        var colorValues = new double[this.Properties.Count];
        int n = 0;
        for(int i = 0; i < colors.Length; i++) { 
            colors[i] = this.Properties[i].Color;
            colorValues[i] = this.Properties[i].Value;
            totalValue += colorValues[n];
            n++;
        }

        Color color = colors[0];
        for (int i = 1; i < n; i++)
            Color.Lerp(color, colors[i], (float)Math.Round(colorValues[i] / totalValue, 6));
        return new Tuple<Color, float>(color, GetIntensity(totalValue));
    }

    private double GetMeanValue()
    {
        double value = 0;
        foreach (var propertyKey in this.PropertyDict.Keys)
            value += this.PropertyDict[propertyKey].Value;
        return value;
    }

    private void Activate()
    {
        this.IsActive = true;
        UnityEngine.Debug.Log(string.Format("Activated {0}.", this.goSelf.tag));

        if (IsParentLight)
            ParentLight.enabled = true;

        this.Halo.enabled = true;
    }

    private void Deactivate()
    {
        this.IsActive = false;
        UnityEngine.Debug.Log(string.Format("Deactivated %s.", this.goSelf.tag));

        if (IsParentLight)
            ParentLight.enabled = false;

        this.Halo.enabled = false;
    }
}
