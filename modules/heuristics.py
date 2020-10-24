


def Routing(assignment, parent):
    #Routing.Dijkstra(assignment.getOrN(), assignment.getDeN());
    #Routing.Yen(assignment.getOrN(), assignment.getDeN(), parent.routing.KYEN)
    routeSet = parent.topology.getRoutes(assignment.getOrN(), assignment.getDeN()) #Assume routeSet is already ordered

    #TODO: Fazer essa parte
    # for(unsigned int i = 0; i < routeSet->size(); i++){
    #     route = routeSet->at(i);
    #     netLayer = Topology::checkSlotNumberDisp(route, assignment->getNumSlots());
    #     phyLayer = Topology::checkOSNR(route, assignment->getOSNRth());
    #     if(netLayer && phyLayer)
    #         assignment->setRoute(route);
    # }