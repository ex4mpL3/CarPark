# CarPark
This is a classic simple REST API which handles all CRUD operations.
As an example, developed an API for a fleet of cars with drivers.

## Note:
1. There should be no business logic in the view, but placed separately in files (services, etc.)
2. Working with the database should be moved to the repository, in order to avoid overlapping modules and creating confusion
+ I know all this, but due to lack of time I did not have time to do it as it should.

## Endpoints
Endpoints have been created for such operations:

### Driver:
+ GET /drivers/driver/ - output of the list of drivers
+ GET /drivers/driver/?created_at__gte=10-11-2021 - output a list of drivers that are created after 10-11-2021
+ GET /drivers/driver/?created_at__lte=16-11-2021 - display a list of drivers created before 16-11-2021

+ GET /drivers/driver/<driver_id>/ - show info on a particular driver
+ POST /drivers/driver/ - create driver
+ UPDATE /drivers/driver/<driver_id>/ - edit driver
+ DELETE /drivers/driver/<driver_id>/ - remove driver

### Vehicle:
+ GET /vehicles/vehicle/ - output of the list of vehicle
+ GET /vehicles/vehicle/?with_drivers=yes - show the list of vehicle with drivers
+ GET /vehicles/vehicle/?with_drivers=no - show the list of vehicle without drivers

+ GET /vehicles/vehicle/<vehicle_id> - show info on a prticular vehicle
+ POST /vehicles/vehicle/ - create vehicle
+ UPDATE /vehicles/vehicle/<vehicle_id>/ - edit vehicle
+ POST /vehicles/set_driver/<vehicle_id>/ - садимо водія в машину / висаджуємо водія з машини  
+ DELETE /vehicles/vehicle/<vehicle_id>/ - remove vehicle

## Example:
```
POST /vehicles/vehicle/
```
#### request:
```
{
    "driver_id": 3,
    "make": "2000",
    "model": "Mercedes AMG GT63",
    "plate_number": "АE 7777 АК"
}
```

# Setup
## Cloning the repository
```
git clone -c https://github.com/ex4mpL3/YalantisTest.git
```
You can create a new environment by using virtualenv,
and then install the dependencies by referring to the requirements.txt:
```
# This installs the modules
pip install -r requirements.txt
```
