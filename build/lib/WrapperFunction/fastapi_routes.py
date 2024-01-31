import fastapi
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import db
import os
from dotenv import load_dotenv

from models.cow import Cow as ModelCow
from models.cow import Weight as ModelWeight
from models.cow import Feeding as ModelFeeding
from models.cow import Milk_production as ModelMilk
from schemas.cow import CowInfo as SchemaCowInfo
from typing import List

load_dotenv('.env')

router = fastapi.APIRouter()

@router.get("/")
async def root():
    return {"message": "Please visit https://azure-cowshed.azurewebsites.net/docs for API calling documentation"}


@router.get(
    "/cows",
    summary="Retrieves all cows' info",
    description="Retrieves all available cows' info from the API")
async def get_cows():
    cows = db.session.query(ModelCow).all()
    cow_list = []
    for cow in cows:
        result = get_cow_info_dict(cow)
        cow_list.append(result)
    return cow_list

@router.get(
    "/cow/{cow_name}",
    summary="Retrieve a cow info by name",
    description="Retrieves a specific cow info by name, if no cow matches the filter criteria a 404 error is returned")
async def get_cows_name(cow_name: str):
    try:
        cows = db.session.query(ModelCow).filter(ModelCow.name==cow_name)
        cow_list = []
        for cow in cows:
            result = get_cow_info_dict(cow)
            cow_list.append(result)
        return cow_list
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get(
    "/cow/filter/{cow_sex}",
    summary="Retrieve cows info by sex",
    description="Retrieves a specific cow info by sex, it returns all of Male cows if condition is true. and returns Female cows if condition is false. otherwise a 500 error is returned")
async def get_cows_sex(cow_sex: str):
    try:
        if cow_sex not in ['true', 'false']:
            raise KeyError("Invalid filter condition. it must be  'false' or 'true'")
        if cow_sex == 'true':
            condition = "Male"
        else:
            condition = "Female"
        cows = db.session.query(ModelCow).filter(ModelCow.sex==condition)
        cow_list = []
        for cow in cows:
            result = get_cow_info_dict(cow)
            cow_list.append(result)
        if len(cow_list) == 0:
            return HTTPException(status_code=404, detail="There is no record that match the filter condition")
        return cow_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/cow",
    status_code=201,
    summary="Create a cow info.",
    description="Create new cow info based on the request.")
async def create_cow(cows: List[SchemaCowInfo]):
    try:
       
        for cow in cows:
            if cow.sex not in ["Male", "Female"]:
                raise KeyError("Invalid string in sex field. It should be 'Male' or 'Female'")

            if cow.condition not in ['healthy', 'sick']:
                raise KeyError("Invalid string in condition field. It should be 'healthy' or 'sick'")
                
            db_cow = ModelCow(
                name=cow.name, 
                sex=cow.sex, 
                condition=cow.condition, 
                birthdate=cow.birthdate, 
                has_calf=cow.has_calves
            )
            db.session.add(db_cow)
            db.session.commit()

            db_weight = ModelWeight(
                cow_id = db_cow.id,
                mass_kg = cow.weight.mass_kg,
                last_measured = cow.weight.last_measured
            )
            db.session.add(db_weight)
            db.session.commit()
            
            db_milk = ModelMilk(
                cow_id = db_cow.id,
                cron_schedule = cow.milk_production.cron_schedule,
                amount_l = cow.milk_production.amount_l,
                last_milk = cow.milk_production.last_milk
            )
            
            db.session.add(db_milk)
            db.session.commit()
            
            db_feed = ModelFeeding(
                cow_id = db_cow.id,
                amount_kg = cow.feeding.amout_kg,
                cron_schedule = cow.feeding.corn_schedule,
                last_measured = cow.feeding.last_measured
            )

            db.session.add(db_feed)
            db.session.commit()
        
        return {"message": "successfully created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create cow info: {str(e)}")
    

@router.put(
    "/cow/{cow_name}",
    summary="Update a cow info.",
    description="Update a cow's info by name")
async def update_cow(cow_name: str, extra_data: SchemaCowInfo):
    cow = db.session.query(ModelCow).filter(ModelCow.name == cow_name).first()
    if cow:
        for field, value in extra_data.items():
            setattr(cow, field, value)
        if 'weight' in extra_data.keys():
            weight = db.session.query(ModelWeight).filter(ModelWeight.cow_id == cow.id).first()
            if weight:
                for field, value in extra_data['weight'].items():
                    setattr(weight, field, value)
        if 'feeding' in extra_data.keys():
            feed = db.session.query(ModelFeeding).filter(ModelFeeding.cow_id == cow.id).first()
            if feed:
                for field, value in extra_data['feeding'].items():
                    setattr(feed, field, value)
        if 'milk_production' in extra_data.keys():
            milk = db.session.query(ModelMilk).filter(ModelMilk.cow_id == cow.id).first()
            if milk:
                for field, value in extra_data['milk_production'].items():
                    setattr(milk, field, value)
        try:
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return {"message": "successfully update cow info!"}

    else:
        raise HTTPException(status_code=404, detail="Cow not found")

@router.delete(
    "/cow/{cow_name}",
    summary="Delete a cow info.",
    description="Delete a cow's info by id")
async def delete_cow(cow_name: str):
    try:
        cow = db.session.query(ModelCow).filter(ModelCow.name == cow_name).first()

        db.session.query(ModelFeeding).filter(ModelFeeding.cow_id == cow.id).delete()
        db.session.query(ModelWeight).filter(ModelWeight.cow_id == cow.id).delete()
        db.session.query(ModelMilk).filter(ModelMilk.cow_id == cow.id).delete()
        
        db.session.delete(cow)
        db.session.commit()
        return {"message": "successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to delete cow info: {str(e)}")



def get_cow_info_dict(cow: ModelCow) -> dict:
    try:
        result = {key: cow.__dict__[key] for key in ['name', 'sex', 'condition','birthdate', 'has_calf']}
        
        weight = db.session.query(ModelWeight).filter(ModelWeight.cow_id == cow.id).first()
        result["weight"] = {key: weight.__dict__[key] for key in ['mass_kg', 'last_measured']}
        
        feeding = db.session.query(ModelFeeding).filter(ModelFeeding.cow_id== cow.id).first()
        result['feeding'] = {key: feeding.__dict__[key] for key in ['amount_kg', 'cron_schedule', 'last_measured']}
        
        milk = db.session.query(ModelMilk).filter(ModelMilk.cow_id == cow.id).first()
        result['milk_production'] = {key: milk.__dict__[key] for key in ['last_milk', 'cron_schedule', 'amount_l']}
        return result
    except:
        pass
  
