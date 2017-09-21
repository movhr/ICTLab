using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using System.IO;
using System;

public static class TimeFrameParser
{
    public class Entity
    {
        public string SensorName { get; set; }
        public string Loc_x { get; set; }
        public string Loc_y { get; set; }
        public string Loc_z { get; set; }
        public string SensorType { get; set; }
        public string TypeColor { get; set; }
        public string ParentName { get; set; }
    }

    public class Series
    {
        public string name { get; set; }
        public List<string> columns { get; set; }
        public List<List<object>> values { get; set; }
    }

    public class Result
    {
        public int statement_id { get; set; }
        public List<Series> series { get; set; }
    }

    public class ActivityLog
    {
        public List<Result> results { get; set; }
    }

    public class RootObject
    {
        public List<Entity> entities { get; set; }
        public ActivityLog activity_log { get; set; }
    }
    public class ParserResult
    {
        public List<TimeFrame> TimeFrames;
        public Dictionary<string, SimObject> SimObjects;

        public ParserResult(List<TimeFrame> timeFrames, Dictionary<string, SimObject> simObjects)
        {
            this.TimeFrames = timeFrames;
            this.SimObjects = simObjects;
        }
    }

    private static string filepath;

    public static ParserResult Upload(Stream stream)
    {
        //First read the file that is given
        UnityEngine.Debug.Log("TimeFrameParser.Upload called.");
        RootObject response;

        UnityEngine.Debug.Log("Reading stream...");
        using (var sr = new StreamReader(stream))
        {
            UnityEngine.Debug.Log("Deserializing json object...");
            response = JsonConvert.DeserializeObject<RootObject>(sr.ReadToEnd());
            stream.Close();
            UnityEngine.Debug.Log("Deserialization done. Stream has been closed.");
        }

        //Start parsing timeframes
        var targetList = response.activity_log.results[0].series[0].values;
        var timeFrames = new List<TimeFrame>(targetList.Count);
        UnityEngine.Debug.Log("Started converting objects to timeframes...");
        foreach (var unparsedTimeFrame in targetList)
            timeFrames.Add(new TimeFrame(unparsedTimeFrame));

        // Parse sim object entities
        var entities = new Dictionary<string, SimObject>();//response.entities[0].Count);
        UnityEngine.Debug.Log("Started converting objects to entities...");
        foreach (var unparsedEntity in response.entities)
        {
            if (!entities.ContainsKey(unparsedEntity.SensorName))
                entities.Add(unparsedEntity.SensorName, new SimObject(unparsedEntity.SensorName, unparsedEntity.SensorType, Convert.ToUInt32(unparsedEntity.TypeColor), unparsedEntity.ParentName, new Vector3((float)Convert.ToDouble(unparsedEntity.Loc_x), (float)Convert.ToDouble(unparsedEntity.Loc_y), (float)Convert.ToDouble(unparsedEntity.Loc_z))));
            else
                entities[unparsedEntity.SensorName].AddProperty(unparsedEntity.SensorType, Convert.ToUInt32(unparsedEntity.TypeColor));
        }
        UnityEngine.Debug.Log("Returning result...");
        return new ParserResult(timeFrames, entities);
    }
}
