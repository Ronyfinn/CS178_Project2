# Road Trip Budget Tracker
A functional Flask web application that allows users to budget for a road trip by entering estimated expenses and uploading optional itinerary images. This service was built with AWS services such as DynamoDB and S3 for secure data storage.

## Overview
I wanted to create a functional web application that incorporated AWS services I have learned about in class.

## Features
- Create and store road trip budget entries using UUIDs
- Upload itinerary or travel guide screenshots to AWS S3 bucket
- Calculate and summarize total estimated trip cost based on inputs

  ## How it works
1. Users land on a professional homepage and can create a new road trip estimation.

2. The form collects
- Trip Name  
- Miles per Gallon
- Estimated Gas Price
- Total Miles
- Hotel, Food, Activities, Emergency, and Buffer Costs
- Optional Itinerary Image Upload

3. A UUID is generated for the trip.

- Float values are converted to Decimal for DynamoDB compatibility.
- Estimated gas cost and total cost are calculated.
- Data is stored in DynamoDB.
- If an image is uploaded, it’s saved to S3 bucket

4. The user is redirected to a summary page showing a detailed cost breakdown using Jinja2 templating.

## Set up
- DynamoDB: Table with partition key set as trip_id (UUID)
- S3: Bucket used to store uploaded images using f-strings like itineraries/{trip_id}/{filename}

## My Takeaway
- How to structure a Flask application for deployment
- How to interact with AWS services securely and efficiently
- Python f-strings for dynamic key/path generation

## Next Steps
- User authentication system
- Edit/Delete trip entries
- Improved image handling and file type restrictions
- Error handling and bug fixes
