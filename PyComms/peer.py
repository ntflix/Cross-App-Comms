from typing import Any, Iterator, Optional


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

    def addNeighbour(self, peerID: ID) -> None:
        self.__peers[peerID] = 1

    def getPathToPeer(
        self,
        peerID: ID,
        exclude: Optional[set[ID]] = None,
    ) -> Iterator[ID]:
        if exclude is None:
            exclude = set()
        exclude.add(self.__id)

        try:
            if self.__peers[peerID]:
                # the peer is next to this one
                # send the desired peer's ID back
                yield peerID
                # send this peer's ID back
                yield self.__id
        except:
            # iterate through all the peers EXCEPT SELF
            for thisPeerID in set(self.__peers.keys()) - exclude:
                thisPeer: Optional[Peer] = None
                try:
                    thisPeer = self.__peersTable[thisPeerID]
                except:
                    thisPeer = None
                # check that the returned peer was not None
                if thisPeer is not None:
                    # get the hops from the returned peer to the desired peer
                    yield from thisPeer.getPathToPeer(peerID, exclude)
                    yield self.getID()

    def getHopsForPeerByID(
        self,
        peerID: ID,
    ) -> Optional[int]:
        path = set(self.getPathToPeer(peerID))
        return len(path) - 1

    def getID(self) -> ID:
        return self.__id

    def __onReceiveMessage(self, message: Any) -> None:
        print(message)

    def sendMessageToPeer(self, peer: ID, message: Any) -> None:
        if peer == self.getID():
            self.__onReceiveMessage(message)
        else:
            path = list(self.getPathToPeer(peer))
            if peer in path:
                # the path is valid
                # get the next peer by taking the penultimate Peer from the list of path peers
                nextPeer = path[0]
                self.__peersTable[nextPeer].sendMessageToPeer(peer, message)


if __name__ == "__main__":
    peersTable = dict[ID, "Peer"]()

    peersList = list[Peer]()
    for i in range(0, 10):
        peersList.append(Peer(peersTable, i))

    for i in range(0, 9):
        peersList[i].addNeighbour(i + 1)
        peersList[i + 1].addNeighbour(i)

    for peer in peersList:
        for destination in peersList:
            print(
                f"Hops from {peer.getID()} to {destination.getID()}: {peer.getHopsForPeerByID(destination.getID())}"
            )
            path = list(peer.getPathToPeer(destination.getID()))
            path.reverse()
            print(f"Path: {' -> '.join(map(str, path))}")
            peer.sendMessageToPeer(
                destination.getID(),
                f"Hello from {peer.getID()} to {destination.getID()}!",
            )
            print()
