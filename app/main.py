from fastapi import  FastAPI
from app.routers import users, auth, admin, bookings, payments
from fastapi.middleware.cors import CORSMiddleware
from .tasks import add




# models.Base.metadata.create_all(bind=engine)# create tbls for us 



app = FastAPI(
    title= "fast-coach-api",
    description="Bus Ticketing System API ",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "fast-coach-api",
        "url": "https://github.com/flavian-anselmo/fast-coach-api",
        "email": "anselmo.flavian@cloudpro.club",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)




#cors
origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# routers 
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(bookings.router)
app.include_router(payments.router)


# root 
@app.get("/")
def read_root():
    res = add.delay(4,2)
    return {"message": f"Fast.Coach.API-----> {res}"}



