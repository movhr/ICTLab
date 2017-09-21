from world import World
from person.sleeping import wake_with_alarm
import masternode

def main():
    realm = World()
    homeJan = realm.CreateBuilding("TypicalSimulator")
    jan = realm.CreatePerson("Sapphira-chan", homeJan)
    jan.routine.create_event(wake_with_alarm, 7, 30)
    masternode.connect(realm)
    realm.Simulate()

if __name__ == "__main__":
    main()
