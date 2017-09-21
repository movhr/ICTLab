#define DEBUG
#undef DEBUG

using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Diagnostics;
using UnityEngine.UI;
using System.Net;
using System.Threading;


public class Core : MonoBehaviour
{
    private long MAX_FRAMES;

    public float SimSpeed { private set; get; }
    public DateTime TimeNow { private set; get; }
    public float Progress { private set; get; }
    public long TimeMinutes { private set; get; }

    private bool InitSuccess = false;
    private ulong errCount = 0;
    private long FrameIndex;
    private long LastFrameIndex;
    private DateTime StartTime;
    private TimeFrame[] TimeFrames;

    private Text SimConsole;
    private Scrollbar ProgressBar;

    private bool[] TagActiveArray;
    private Dictionary<string, SimObject> SimObjectTagMap;

    private void ParseSimFile(Stream stream)
    {
        var parseResult = TimeFrameParser.Upload(stream);
        UnityEngine.Debug.Log("Parsing done.");
        TimeFrames = parseResult.TimeFrames.ToArray();
        SimObjectTagMap = parseResult.SimObjects;
        MAX_FRAMES = TimeFrames.Length - 1;
        FrameIndex = 0;
        LastFrameIndex = 0;
        StartTime = TimeFrames[0].SimTime;
        TagActiveArray = new bool[SimObjectTagMap.Count];
        TimeMinutes = TimeFrames[MAX_FRAMES].SimTime.Subtract(TimeFrames[0].SimTime).Minutes;
        InitSuccess = true;
        UnityEngine.Debug.Log("Parsed sim file successfully.");
    }

    private bool FetchSimFile()
    {
        try
        {
            SimConsole.text = "Fetching simulation data...";
            //Get sample simulation file
            UnityEngine.Debug.Log("Sending web request...");

#if DEBUG
            var request = WebRequest.Create("http://192.168.0.35:3001/api3/getsimsample");
#else
            var request = WebRequest.Create("http://api3.localhost:3001/getsimsample");
#endif

            request.Timeout = 1500;
            var response = request.GetResponse();
            if (response == null)
                return false;
            UnityEngine.Debug.Log("Got response...");

            //Run it through parser and init required fields
            UnityEngine.Debug.Log("Uploading to parser...");
            ParseSimFile(response.GetResponseStream());
            SimConsole.text = "Successfully fetched data file.";
            return true;
        }
        catch (WebException ex)
        {
            SimConsole.text = String.Format("{0}.\nRetrying... ({1})\n", ex.Message, errCount);
            return false;
        }
    }

    // Use this for initialization
    void Start()
    {
        UnityEngine.Debug.Log("Starting core...");
        // Initialize necessary fields
        SimConsole = GameObject.FindGameObjectWithTag("SimConsole").GetComponent<Text>();
        ProgressBar = GameObject.FindGameObjectWithTag("Progressbar").GetComponent<Scrollbar>();
        SimSpeed = 2f;

        SimConsole.text = "Initializing...";

        //Get simulation data
        if (TimeFrames == null || SimObjectTagMap == null)
            InitSuccess = FetchSimFile();
    }

    void UpdateGui(DateTime datetime, bool isEnded = false)
    {
        if (isEnded)
            SimConsole.text = "[END REACHED] Clock: " + datetime.ToString();
        else
            SimConsole.text = "Clock: " + datetime.ToString();
    }

    // Update is called once per frame
    void Update()
    {
        // Retry initializing if there was an error during previous initialization.
        if (!InitSuccess)
        {
            if (errCount > 5)
            {
                try
                {
#if DEBUG
                    using (var fs = File.OpenRead("./Assets/Resources/sample_historics_small.json"))
                    {
                        ParseSimFile(fs);
                        return;
                    }
#else
                    using (var fs = File.OpenRead("./sample_historics_small.json"))
                    {
                        ParseSimFile(fs);
                        return;
                    }
#endif
                }
                catch (Exception ex)
                {
                    UnityEngine.Debug.Log("Could not get file from either remote or local path. Exiting...");
                    Application.Quit();
                }
            }

            UnityEngine.Debug.Log("Retrying to fetch data from server...");    
            InitSuccess = FetchSimFile();
            if (!InitSuccess)
            {
                errCount++;
                return;
            }
        }

        // Quit if the end of the simulation has been reached.
        if (this.FrameIndex >= MAX_FRAMES)
        {
            UpdateGui(TimeFrames[MAX_FRAMES].SimTime, true);
            return;
        }

        // Creates the current simulated datetime from starting and running time
        DateTime simTime = new DateTime(StartTime.Ticks);
        simTime = simTime.AddSeconds(Time.time * 60 * SimSpeed);

        // Keep sensor names that are turned on apart.
        HashSet<string> usedTags = new HashSet<string>();

        // Regulate simTime if it lags behind
        if (DateTime.Compare(simTime, TimeFrames[this.FrameIndex].SimTime) > 0)
            simTime = TimeFrames[this.FrameIndex].SimTime;

        // Display the date and time of the current time frame
        UpdateGui(simTime);

        // Main block that edits halos according to the historic time frames.
        // Gets all time frames that equal this simulated moment
        while (DateTime.Compare(simTime, TimeFrames[this.FrameIndex].SimTime) == 0)
        {
            // Make a reference to current time frame for easier access.
            var curTF = TimeFrames[this.FrameIndex];

            // Notify the sensor that covers the sensor in the historic time frame.
            SimObjectTagMap[curTF.SensorName].On(curTF.SensorType, curTF.SensorValue);

            // Make sure that the sensor won't be turned off.
            usedTags.Add(curTF.SensorName);

            // Move to next time frame
            if (FrameIndex < MAX_FRAMES)
                this.FrameIndex++;
            else
                break;
        }

        // When all sensors turned on, mix colors and display halo.
        // For sensors that are turned off, turn them off or let them remain off.
        if (LastFrameIndex < FrameIndex)
        {
            foreach (var sensor in SimObjectTagMap.Values)
            {
                if (usedTags.Contains(sensor.goSelf.tag))
                    sensor.CommitProperties();
                else
                    sensor.Off();
            }
            LastFrameIndex = FrameIndex;
        }

        Progress = ((float)FrameIndex / (float)MAX_FRAMES);
        ProgressBar.size = Progress;
    }
}
