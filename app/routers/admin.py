'''
all admin endpoints will be handled here

- setting up the routee table for the busses 
- registering new busses to the system 


TODO: GET ALL THE BUSES --> done 
TODO: GET ALL THE ROUTES  --> done 
TODO: GET SPECIFIC BUS WITH ITS ROUTE 
TODO: GET SPEPCIFIC ROUTE 
TODO: creat routes --> done 
TODO: CREATE BUSES --> done 

'''


from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2



router = APIRouter(
  
    prefix = '/admin',
    tags = ['Admin (Drivers, Buses & Routes)']
)



#----------------------------------------------------[BUS ROUTE ENDPOINTS]---------------------------------------------------------------

@router.post('/routes', status_code = status.HTTP_201_CREATED, response_model=schemas.TravelRouteResponse)
async def create_bus_route(route:schemas.TravelRouteCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''

    admin will be adding bus routes 

    '''
    try:
        new_route = models.TravelRoute(**route.dict(), user_id = curr_user.user_id)
        db.add(new_route)
        db.commit()
        db.refresh(new_route)
        return new_route

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    




@router.get('/routes', response_model= List[schemas.TravelRouteResponse])
async def get_all_travel_routes(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all the travel routes 

    '''
    try:
        routes = db.query(models.TravelRoute).all()
        if not routes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus routes available')
        return routes 
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    




@router.get('/routes/{route_id}', response_model=schemas.TravelRouteResponse)
async def get_route_by_id(route_id:int, curr_user:int = Depends(oauth2.get_current_user_logged_in), db:session = Depends(get_db)):
    '''
    get one route with id 
    '''
    try:
        route = db.query(models.TravelRoute).filter(models.TravelRoute.route_id == route_id ).first()

        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus route available')
        return route   
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
     


@router.put('/route/{route_id}', response_model = schemas.TravelRouteResponse)
async def update_route(route_id:int, route_update:schemas.TravelRouteCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    update route 

    '''
    
    update_route_query = db.query(models.TravelRoute).filter(models.TravelRoute.route_id == route_id)

    route = update_route_query.first()

    if route == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='route not found')  

    update_route_query.update(
        route_update.dict(),
        synchronize_session = False
    )  
    db.commit()
    return update_route_query.first()
    
    


@router.delete('/routes/{route_id}')
async def delete_route(route_id:int, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    delete a travel route 

    '''
    try:
        bus = db.query(models.TravelRoute).filter(models.TravelRoute.route_id == route_id)
        bus.delete(synchronize_session = False)
        db.commit()    
        return {"detail": "deleted route sucessfully "}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    






# -------------------------------- [BUS ENDPOINTS]------------------------------------------------------------------------------------------------------ 

@router.post('/buses', status_code=status.HTTP_201_CREATED, response_model=schemas.BusResponse)
async def create_bus (bus:schemas.BusCreate,db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    create a new bus and assign a driver 
    the user_id represents a driver 
    
    '''
    try:

        new_bus = models.Bus(**bus.dict())

        db.add(new_bus)
        db.commit()
        db.refresh(new_bus)
        return new_bus
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    



@router.get('/buses', response_model=List[schemas.BusResponse])
async def get_all_buses(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all the registered buses together with the route they take 

    '''
    try:
        buses  = db.query(models.Bus).all()

        if not buses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus routes available')
        return buses   
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    



@router.get('/buses/{bus_id}', response_model=schemas.BusResponse)
async def get_bus_by_id(bus_id:int, curr_user:int = Depends(oauth2.get_current_user_logged_in), db: session = Depends(get_db)):
    '''
    get one bus with routes 

    '''
    try:
        bus = db.query(models.Bus).filter(models.Bus.bus_id == bus_id ).first()

        if not bus:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus route available')
        return bus  
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    

@router.put('/buses', response_model=schemas.BusResponse)
async def update_bus(bus_id:int, bus_update:schemas.BusCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    update the buses 

    '''
    try:
        update_bus = db.query(models.Bus).filter(models.Bus.bus_id == bus_id)

        bus = update_bus.first()

        if bus== None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bus not found')  
            
        update_bus.update(
            # update 
            bus_update.dict(),
            synchronize_session = False 
        )  
        # commit changes 
        db.commit()
        return update_bus.first()
    except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    




@router.delete('/buses/{bus_id}')
async def delete_bus(bus_id:int, db: session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    delete  a registered bus 

    '''
    try:
        bus = db.query(models.Bus).filter(models.Bus.bus_id == bus_id)
        bus.delete(synchronize_session = False)
        db.commit()    
        return {"detail": "deleted bus sucessfully "}
    except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    



# ------------------------[DRIVER ENDPOINTS]-------------------------------------------------------------------------------------------------------------------------------
@router.post('/drivers', response_model=schemas.DriverResponse)
async def register_driver(driver:schemas.DriverCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    assign a driver a bus 
    '''
    try:

        new_driver = models.Driver(**driver.dict())
        db.add(new_driver)
        db.commit()
        db.refresh(new_driver)
        return new_driver
    except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    



@router.get('/drivers', response_model=List[schemas.DriverResponse])
async def get_all_drivers(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all the registered drivers together with the route they take 

    '''
    try:

        drivers  = db.query(models.Driver).all()

        if not drivers:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus routes available')
        return drivers 
    except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    
    


@router.put('/drivers', response_model=schemas.DriverResponse)
async def update_driver(driver_id:int, driver_update:schemas.DriverCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    update the driver 

    '''
    try:

        update_driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id)

        driver = update_driver.first()

        if driver == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='driver not found')  
            
        update_driver.update(
            # update 
            driver_update.dict(),
            synchronize_session = False 
        )  
        # commit changes 
        db.commit()
        return update_driver.first()
    except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    

        

@router.delete('/drivers/{driver_id}')
async def delete_driver(driver_id:int, db: session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    delete  a registered driver

    '''
    try:

        bus = db.query(models.Driver).filter(models.Driver.driver_id == driver_id)
        bus.delete(synchronize_session = False)
        db.commit()    
        return {"detail": "deleted driver sucessfully "}
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    




# -------------------------------[Depature Endpoints ]---------------------------------------------------

@router.post('/depature', status_code=status.HTTP_201_CREATED, response_model=schemas.DepatureResponse)
async def create_depature (depature:schemas.DepatureCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    Admin will be able to add a bus that is ready for depature for that day  
    
    '''
    try:

        new_depature = models.Depature(**depature.dict())
        db.add(new_depature)
        db.commit()
        db.refresh(new_depature)
        return new_depature

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    





@router.put('/depature', response_model=schemas.DepatureResponse)
async def update_depature(dep_id:int, depature_update:schemas.DepatureCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    update a depature 

    '''
    try:

        update_depature = db.query(models.Depature).filter(models.Depature.dep_id == dep_id)

        depature = update_depature.first()

        if depature == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='driver not found')  
            
        update_depature.update(
            # update 
            depature_update.dict(),
            synchronize_session = False 
        )  
        # commit changes 
        db.commit()
        return update_depature.first()
    except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))   




@router.delete('/depature/{dep_id}')
async def delete_driver(dep_id:int, db: session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    delete  a depature

    '''
    try:

        depature = db.query(models.Depature).filter(models.Depature.dep_id == dep_id)
        depature.delete(synchronize_session = False)
        db.commit()    
        return {"detail": "depature deleted sucessfully "}
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))    

