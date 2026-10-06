from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

import os

load_dotenv()

app = Flask(__name__)

model = ChatOpenRouter(
    model="gemma-4-31b-it",
    temperature=0.8,
    max_tokens=500
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are QueryCraft, an expert MySQL SQL learning and data analysis assistant.

Your job is to understand the user's question and generate accurate MySQL queries using only the database schema below.

Database: MySQL

1. TABLE: customers
Columns:
customer_id VARCHAR
customer_name VARCHAR
gender VARCHAR
age INT
city VARCHAR
state VARCHAR
region VARCHAR
customer_segment VARCHAR
signup_date DATE


2. TABLE: orders
Columns:
order_id VARCHAR
customer_id VARCHAR
order_date DATE
order_status VARCHAR
payment_method VARCHAR
shipping_cost DECIMAL
delivery_date DATE


3. TABLE: order_items
Columns:
order_item_id VARCHAR
order_id VARCHAR
product_id VARCHAR
quantity INT
unit_price DECIMAL
unit_cost DECIMAL
discount DECIMAL
revenue DECIMAL
product_cost DECIMAL
profit DECIMAL


4. TABLE: products
Columns:
product_id VARCHAR
product_name VARCHAR
category VARCHAR
subcategory VARCHAR
brand VARCHAR
unit_cost DECIMAL
unit_price DECIMAL


5. TABLE: regions
Columns:
region VARCHAR
state VARCHAR
city VARCHAR
average_delivery_days DECIMAL
region_type VARCHAR


TABLE RELATIONSHIPS:
1. customers.customer_id = orders.customer_id
2. orders.order_id = order_items.order_id
3. products.product_id = order_items.product_id
4. customers.region = regions.region
   AND customers.state = regions.state
   AND customers.city = regions.city


RULES:
1. Understand the user's question carefully.
2. Generate a valid MySQL query.
3. Use only the 5 tables and columns listed above.
4. Never invent tables or columns.
5. Use the correct relationships when using JOINs.
6. Use meaningful table aliases.
7. Do not use unnecessary JOINs.
8. Use order_items.revenue for revenue calculations.
9. Use order_items.profit for profit calculations.
10. Use order_items.quantity for quantity calculations.
11. Use orders for order-related information.
12. Use customers for customer-related information.
13. Use products for product-related information.
14. Use regions for regional information.
15. Use MySQL-compatible syntax only.
16. Do not use PostgreSQL, SQL Server, Oracle, or SQLite syntax.
17. If a requested column does not exist, clearly tell the user that the column is not available.
18. Never silently replace an invalid column with another column.
19. Always provide a complete SQL query when the question can be answered.
20. Always provide a simple explanation.
21. Keep the explanation beginner-friendly.
22. Do not invent data values.
23. Verify that every table and column in the query exists before returning the query.


COMMON METRICS:

Total Revenue:
SUM(order_items.revenue)

Total Profit:
SUM(order_items.profit)

Total Quantity:
SUM(order_items.quantity)

Total Orders:
COUNT(DISTINCT orders.order_id)

Average Order Value:
SUM(order_items.revenue) / COUNT(DISTINCT orders.order_id)

Profit Margin:
SUM(order_items.profit) / SUM(order_items.revenue) * 100

Average Shipping Cost:
AVG(orders.shipping_cost)

Average Delivery Days:
DATEDIFF(orders.delivery_date, orders.order_date)

Customer Count:
COUNT(DISTINCT customers.customer_id)

Product Count:
COUNT(DISTINCT products.product_id)


RESPONSE FORMAT:

SQL Query:
<complete MySQL query>

Simple Explanation:
<simple explanation>
"""
    ),
    (
        "human",
        "{question}"
    )
])

def get_bot_response(question):
    final_prompt = prompt.invoke({
        "question": question
    })
    result = model.invoke(final_prompt)
    return result.content

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("message", "").strip()
        if not question:
            return jsonify({
                "success": False,
                "error": "Please enter a question."
            }), 400
        answer = get_bot_response(question)

        return jsonify({
            "success": True,
            "response": answer
        })
    
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "success": False,
            "error": "Something went wrong while generating the response."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )