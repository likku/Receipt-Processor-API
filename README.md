# Receipt-Processor-API

A simple receipt processor

1. Install Flask / create it with a virtual env:

   `pip install Flask`

2. From project directory, we can build and run using docker-compose:

   `docker-compose up --build`

3. The above command should start the application on port 3000. If its running you should able to see "Pong" when you provide this URL in the browser.

   `http://localhost:3000/ping`

4. We can use curl to test the endpoints.

   eg: `curl -X POST http://localhost:3000/receipts/process \  
   -H "Content-Type: application/json" \
   -d '{  
    "retailer": "M&M Corner Market",
   "purchaseDate": "2022-03-20",  
    "purchaseTime": "14:33",  
    "items": [
    {
    "shortDescription": "Gatorade",
    "price": "2.25"
    },{
    "shortDescription": "Gatorade",
   "price": "2.25"
   },{
   "shortDescription": "Gatorade",
   "price": "2.25"
   },{
   "shortDescription": "Gatorade",
   "price": "2.25"
   }
   ],
   "total": "9.00"
   }'`

   That should give a receipt ID after a successful request.

5. Then we can use that ID to get the points using the /points endpoint.

   eg: `curl http://localhost:3000/receipts/67610c04-5df6-40e2-820e-a943284addae/points`

   That should give us the points after successful request.
