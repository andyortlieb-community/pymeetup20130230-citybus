from flask import request

from db import session
from models import BusRoute
from rest import Success, NotFound
from app import app, Constants

@app.route('/version/')
def version():
    return Success(Constants).render()


@app.route('/v1/busroutes', methods=['GET'])
def busroutes():
    routes = BusRoute.query.all()
    if (routes):
        return Success(routes).render()
    return NotFound().render()


@app.route('/v1/busroutes', methods=['POST'])
def busroutesPOST():
    route = BusRoute()
    route.fromDict(request.json)
    session.add(route)
    try:
        session.commit()
    finally:
        session.rollback()

    return Success(route).render()


@app.route('/v1/busroutes', methods=['PUT'])
def busroutesPUT():
    routeId = request.json.get('id')

    if routeId: 
        routeId = '%s'%routeId
        route = BusRoute.query.filter(BusRoute.id==routeId).all()

    else:
        route = False

    if not route: 
        return NotFound().render()
    
    route = route[0]

    route.fromDict(request.json)
    session.add(route)
    session.flush()

    return Success(route).render()
    