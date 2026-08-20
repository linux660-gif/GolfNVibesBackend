from http import HTTPStatus
from fastapi import APIRouter, HTTPException,status,Query
from sqlalchemy import select, delete
import logging
from typing import Dict

from app.db.database import get_db
from app.schemas.trip_schema import (PlanTrip, PlanTripUpdate as PlanTripUpdateSchema, PlanTripResponse)
from app.models.trip import Trip as TripModel
from app.clients.email.email_service import EmailService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/trips", tags=["Trip"])
email_service = EmailService()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_custom_trip(trip:PlanTrip) -> Dict[str, str]:
    async with get_db() as db:

        result = await db.execute(select(TripModel).where((TripModel.email == trip.email) | (TripModel.phone_number == trip.phone_number)))

        existing_trip = result.scalars().first()

        if  existing_trip:

            logger.warning("Trip already exists")

            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip already exists")

        new_trip = TripModel(
            first_name=trip.first_name,
            last_name=trip.last_name,
            email=trip.email,
            phone_number=trip.phone_number,
            golfers=trip.golfers,
            non_golfers=trip.non_golfers,
            budget=trip.budget,
            rounds=trip.rounds,
            experiences=trip.experiences,
            additional_specifications=trip.additional_specifications,
            airport_transfers=trip.airport_transfers,
            date=trip.date,
            hotel=trip.hotel,
            flights=trip.flights,
            destination = trip.destination,
            other_destination = trip.other_destination,
            continent = trip.continent,
            flexible_dates = trip.flexible_dates
        )


        try:
            db.add(new_trip)
            await db.commit()
            await db.refresh(new_trip)
            email_service.send_plan_trip_confirmation(trip.email, trip.destination, trip.first_name, trip.last_name)
            logger.info("Trip Created")
            return {'message': "Trip successfully added"}


        except Exception:
            logger.exception(f"Database Error")
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PlanTripResponse])
async def get_trips(
    email: str | None = Query(default=None),
    phone: str | None = Query(default=None),
    trip_id:int | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    async with get_db() as db:

        query = select(TripModel)

        if email:
            query = query.where(TripModel.email == email)

        if phone:
            query = query.where(TripModel.phone_number == phone)
        if trip_id is not None:
            query = query.where(TripModel.trip_id == trip_id)

        query = query.limit(limit).offset(offset)

        result = await db.execute(query)

        trips = result.scalars().all()

        if not trips:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trips not found"
            )

        return trips

@router.patch("/{trip_id}", status_code=HTTPStatus.OK)
async def update_trip(trip_id: int, trip: PlanTripUpdateSchema):
    async with get_db() as db:
        result = await db.execute(select(TripModel).where(TripModel.trip_id == trip_id))
        available_trip = result.scalars().first()
        if not available_trip:
            logger.error("Trip Update Failed")

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="failed to Update: Trip not found")

        update_data = trip.model_dump(exclude_unset=True)
        allowed_fields = {
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "budget",
            "golfers",
            "non_golfers",
            "rounds",
            "experiences",
            "additional_specifications",
            "airport_transfers",
            "flexible_dates",
            "hotel",
            "flights",
            "other_destination"
        }
        for field, value in update_data.items():
            if field in allowed_fields:
                setattr(available_trip, field, value)
        try:
            await db.commit()
            await db.refresh(available_trip)
            logger.info("Trip Updated")
            return {
                "message": "Trip Updated Successfully"
            }
        except Exception:
            logging.exception("Database Error")
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.delete("/{trip_id}", status_code=status.HTTP_200_OK)
async def delete_trip(trip_id: int):
    async with get_db() as db:
        result = await db.execute(select(TripModel).where(TripModel.trip_id == trip_id))
        trip = result.scalars().first()
        if not trip:
            logger.error(f"Failed to delete trip with id: {trip_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to Delete: Trip not found")
        try:
            await db.delete(trip)
            await db.commit()
            return {
                "message": "Trip deleted successfully"
            }
        except Exception:
            logger.exception("Database Error")
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete('/all', status_code=status.HTTP_200_OK)
async def delete_trips():
    async with get_db() as db:
        try:
            await db.execute(delete(TripModel))
            await db.commit()
            return {
                "message": " trips deleted"
            }
        except Exception:
            await db.rollback()
            logger.exception("Database Error")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")




