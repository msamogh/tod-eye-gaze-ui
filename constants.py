NAME_EMAIL_FOLDER = "name-emails"
GAZE_PATH_FOLDER = "gaze-paths"

MULTIWOZ_PRETTY_SLOTS = {
    "hotel": {
        "area": "What is the area the user wants?",
        "book day": "Which day does the user want the booking?",
        "book people": "How many people the user wants the booking for?",
        "book stay": "What is the duration of user's stay?",
        "internet": "Does the user need internet?",
        "name" : "Is the user looking for a hotel by Name?",
        "parking": "Does the user want parking available?",
        "pricerange": "What is the price range the user wants?",
        "stars": "What star rating of the ho",
        "type": "What is the hotel type the user wants?"
    },
    "hospital": {
        "department": "What department does the user want?"
    },
    "restaurant": {
        "area": "What area does the user want?",
        "book day": "Which day does the user want the booking?",
        "book people" : "How many people the user wants the booking for?",
        "book time": "What time does the user want to book?",
        "food": "What food cuisine does the user want?",
        "name": "Is the user looking for a restaurant by Name?",
        "pricerange": "What is the price range the user wants?"
    },
    "attraction": {
        "area": "What area does the user want?",
        "name": "Is the user looking for an attraction by Name?",
        "type": "Is the user looking for an attraction by Type?"
    },
    "taxi" : {
        "arriveBy" : "What time does the user want the taxi to arrive?",
        "departure" : "From where should the taxi depart?",
        "destination": "What should be the taxi destination?",
        "leaveAt" : "What time does the user want the taxi to leave?"
    }

}

STAR_PRETTY_SLOTS = {
    "apartment": {
        "Name": "Name of the apartment",
        "Level": "Level/Floor of the apartment",
        "MaxLevel": "Max Level/Floor of the apartment",
        "HasBalcony": "Apartment has balcony",
        "BalconySide": "Direction of the balcony",
        "HasElevator": "Apartment has elevator",
        "NumRooms": "Number of rooms in the apartment",
        "FloorSquareMeters": "Square Metres of the floor",
        "Price": "Price of the Apartment",
        "NearbyPOIs": "Nearby POIs to the apartment"
    },
    "bank": {
        "BankName": "Name of the Bank",
        "BankBalance": "Balance amount in the bank"
    },
    "hotel": {
        "Name": "Name of the hotel",
        "Cost": "Cost Category of the hotel",
        "TakesReservations": "Are Hotel Reservations allowed",
        "Service": "Is Hotel Service Available",
        "AverageRating": "Average Star Rating of the Hotel",
        "ServiceStartHour": "Hotel Service Start hour",
        "ServiceStopHour": "Hotel Service Stop hour",
        "Location": "Location of the hotel"
    },
    "movie": {
        "Name": "Name of the movie",
        "Actors": "Name the actors of the movie",
        "Director": "Name the director of the movie",
        "DurationMinutes": "Duration of the movie in minutes",
        "Genre": "Name the movie genre",
        "Platforms": "Name the platform the movie is available in"
    },
    "plane": {
        "DepartureCity": "Departure city of the plane",
        "ArrivalCity": "Arrival city of the plane",
        "Price": "What is the ticket price?",
        "Date": "Date of travel on the plane",
        "ArrivalTime": "Time of arrival of the plane",
        "Class": "Class of travel on the plane",
        "DurationHours": "Duration of travel on plane in hours",
        "Airline": "Airline company of the plane",
        "Name": "Plane number"
    },
    "ride": {
        "Price": "How much will the ride cost the user?",
        "AllowsChanges": "Are ride changes allowed?",
        "MinutesTillPickup": "How many minutes until ride pick up?",
        "ServiceProvider": "Ride service provider",
        "DriverName": "What is Driver's name?",
        "CarModel": "What is the car model?",
        "LicensePlate": "License plate number of the car booked",
        "id": "Ride number"
    }
}
