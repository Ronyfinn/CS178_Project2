# import modules
from flask import Flask, render_template, request, redirect, url_for
import boto3
import uuid # allows for generating unique IDs for each trip
from decimal import Decimal # allow numbers to be uploaded to DynamoDB as a decimal

app = Flask(__name__)

# connect to DynamoDb database and access RoadTripBudgets database
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
trip_table = dynamodb.Table('RoadTripBudgets')

# connect to S3 Bucket to upload itinerary/travel guide(s)
s3 = boto3.client('s3', region_name='us-east-1')
S3_BUCKET_NAME = 'rmf-roadtripbudget-project' 

@app.route('/') # establishing route to home page (index.html)
def index():
    return render_template('index.html') # render homepage template

# create new roadtrip
@app.route('/create-trip', methods=['GET', 'POST']) # establishing route to create_trip.html
def create_trip(): # creating function
    if request.method == 'POST':
        trip_id = str(uuid.uuid4()) # generates unique ID for trip
        trip_name = request.form['trip_name']
        mileage = float(request.form['mileage']) # miles per gallon
        gas_price = float(request.form['gas_price']) # price per gallon
        miles = float(request.form['miles']) # miles traveling
        hotel_cost = float(request.form['hotel_cost'])
        food_cost = float(request.form['food_cost'])
        activities_cost = float(request.form['activities_cost'])
        emergency_fund = float(request.form['emergency_fund'])
        buffer_fund = float(request.form['buffer_fund'])

        # calculate gas cost and total budget
        estimated_gas_cost = round((miles / mileage) * gas_price, 2)
        total_budget = round(hotel_cost + food_cost + activities_cost + emergency_fund + buffer_fund + estimated_gas_cost, 2)

        # optional upload for itinerary/travel guide(s) to s3 bucket
        #For this block of code https://chatgpt.com/share/68211c04-ff74-8011-bed2-69f1471b0f52
        itinerary_url = None
        if 'itinerary' in request.files:
            itinerary = request.files['itinerary']
            if itinerary and itinerary.filename:
                s3_key = f"itineraries/{trip_id}_{itinerary.filename}"
                s3.upload_fileobj(itinerary, S3_BUCKET_NAME, s3_key)
                itinerary_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        # Save trip data to DynamoDB
        trip_data = {
            'trip_id': trip_id,
            'trip_name': trip_name,
            'mileage': Decimal(str(mileage)), #use Decimal so DynamoDB can take in number(s)
            'gas_price': Decimal(str(gas_price)),
            'miles': Decimal(str(miles)),
            'estimated_gas_cost': Decimal(str(estimated_gas_cost)),
            'hotel_cost': Decimal(str(hotel_cost)),
            'food_cost': Decimal(str(food_cost)),
            'activities_cost': Decimal(str(activities_cost)),
            'emergency_fund': Decimal(str(emergency_fund)),
            'buffer_fund': Decimal(str(buffer_fund)),
            'total_budget': Decimal(str(total_budget)),
            'itinerary_url': itinerary_url
        }
        trip_table.put_item(Item=trip_data) # insert all at once

        # Redirect to trip summary page
        return redirect(url_for('trip_summary', trip_id=trip_id))
    
    return render_template('create_trip.html')

@app.route('/trip-summary/<trip_id>')
def trip_summary(trip_id):
    # Get the trip details from DynamoDB
    response = trip_table.get_item(Key={'trip_id': trip_id})
    trip = response.get('Item')
    
    if not trip:
        return "Trip not found", 404  # for when trip doesn't exist, return 404 error
    
    return render_template('trip_summary.html', trip=trip)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)