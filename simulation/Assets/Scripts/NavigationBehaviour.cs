using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class NavigationBehaviour : MonoBehaviour {
    
    public struct PathfindingLocations
    {
        public struct Bedroom
        {
            public static Vector3 BED = new Vector3(8.85f, 0, 11.17f);
        }

        public struct Kitchen
        {
            public static Vector3 STOVE = new Vector3(-14.5f, 0, 12.5f);
            public static Vector3 MICROWAVE = new Vector3(-5f, 0, 12.5f);
        }

        public struct LivingRoom
        {
            public static Vector3 DINER = new Vector3(-15.6f, 0, -1.5f);
            public static Vector3 SOFA = new Vector3(-16.5f, 0, -7.5f);
        }

        public struct Bathroom
        {
            public static Vector3 TOILET = new Vector3(-14f, 0, -1f);
            public static Vector3 SHOWER = new Vector3(17f, 0, -9f);
        }
    }

    GameObject player;
    NavMeshAgent playerNav;
    public Vector3 pathDestination;
    private NavMeshPath navPath;
    private bool isMoving;

    public void MoveTo(Vector3 position)
    {
        playerNav.destination = position;
        pathDestination = position;
    }

	// Use this for initialization
	void Start () {
        player = GameObject.FindGameObjectWithTag("Player");
        playerNav = player.GetComponent<NavMeshAgent>();

        player.transform.position = PathfindingLocations.Bedroom.BED;
        MoveTo(PathfindingLocations.LivingRoom.DINER);
	}
	
	// Update is called once per frame
	void Update () {
		if(playerNav.remainingDistance > 0 && !isMoving)
        {
            isMoving = true;
            player.GetComponent<Animator>().Play("walk");
        }
        if(playerNav.remainingDistance == 0 && isMoving)
        {
            isMoving = false;
            player.GetComponent<Animator>().Play("idle");
        }
	}
}
