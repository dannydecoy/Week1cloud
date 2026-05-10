Route: GET /expenses
Description: Returns all expenses
Response: 200 OK
Example response:
{
    "expenses": [...]
}

Route: POST /expense
Description: Adds a new expense
Required fields: name, amount
Response: 201 Created
...
