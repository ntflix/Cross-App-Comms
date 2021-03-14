# from PyComms.router import Router
from typing import Optional


ID = int


class Peer:
    __peersTable: dict[ID, "Peer"]
    __id: ID
    __peers: dict[ID, int]

    def __init__(self, peersTable: dict[ID, "Peer"], id: ID) -> None:
        self.__peersTable = peersTable
        self.__id = id
        self.__peers = dict[ID, int]()
        # add an entry in the routing table for itself of hops amount 0
        self.__peers[self.__id] = 0

        peersTable[self.__id] = self
        # self.__router.addPeer(self)

    def addNeighbour(self, peerID: ID) -> None:
        self.__peers[peerID] = 1

    def getHopsForPeerByID(self, peerID: ID, exclude: set[ID]) -> Optional[int]:
        exclude.add(self.__id)
        try:
            # check whether it's in this peer's neighbours list
            return self.__peers[peerID]
        except:
            # iterate through all the peers EXCEPT SELF
            for thisPeerID in set(self.__peers.keys()) - exclude:
                # get the peer object from the router
                # thisPeer = self.__router.getPeerByID(thisPeerID)
                thisPeer: Optional[Peer] = None
                try:
                    thisPeer = self.__peersTable[thisPeerID]
                except:
                    thisPeer = None
                # check it was returned as a real peer, and not None
                if thisPeer is not None:
                    # get the hops from the returned peer to the desired peer
                    thisHops = thisPeer.getHopsForPeerByID(peerID, exclude)
                    if thisHops is not None:
                        # add 1 because we've gone through a neighbour
                        return thisHops + 1
            #  wasn't found, return None
            return None

    def getID(self) -> ID:
        return self.__id


peersTable = dict[ID, "Peer"]()

peer0 = Peer(peersTable, 0)
peer1 = Peer(peersTable, 1)

peer2 = Peer(peersTable, 2)
peer3 = Peer(peersTable, 3)

peer0.addNeighbour(peer1.getID())
peer1.addNeighbour(peer0.getID())

peer1.addNeighbour(peer2.getID())
peer2.addNeighbour(peer1.getID())

peer2.addNeighbour(peer3.getID())
peer3.addNeighbour(peer2.getID())

print(peer0.getHopsForPeerByID(peer3.getID(), set()))
print(peer3.getHopsForPeerByID(peer0.getID(), set()))
print(peer3.getHopsForPeerByID(peer1.getID(), set()))
print(peer1.getHopsForPeerByID(peer3.getID(), set()))
