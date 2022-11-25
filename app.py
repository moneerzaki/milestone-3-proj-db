# importing 
from flask import Flask, render_template, request, redirect, url_for
import pymysql
import random
import queries

app = Flask(__name__)

# Configure Database (connecting to online database system)
host = "db4free.net"
user = "moneerzaki"
password = "12345678"
db = "projdb1"

projdb1 = pymysql.connect(
    host = host,
    user = user,
    password = password,
    db = db,
)

cursor = projdb1.cursor()


# sql query for distinct values; 
distinct_areas = """
select distinct property_area from properties_table;
"""
users = """
select distinct user_contact_number from users_table; 
"""
agents = """
select distinct agent_contact_number from agents_table;
"""
agents_reviewed = """
select distinct agent_reviewed from reviewes_table; 
"""
agents_first_name = """
select distinct agent_first_name from agents_table;
"""
agents_middle_name = """
select distinct agent_middle_name from agents_table;
"""
brokers = """
select distinct broker_name from brokers_table;
"""
brokers1  = """
select distinct agent_broker_name from reviewes_table r inner join agents_table a on r.agent_reviewed = a.agent_contact_number 
"""
developments = """
select distinct developer_name from developers_table;
"""
cities = """
select distinct property_city from properties_table;
"""
amenities = """
select distinct amenities_type from properties_amenities_table; 
"""
prices = """
select distinct property_price_EGP from properties_table
order by 1 asc;
"""

cursor.execute(distinct_areas)
areas_list = cursor.fetchall() 

cursor.execute(agents)
agents_list = cursor.fetchall() 

cursor.execute(agents_first_name)
agents_first_name_list = cursor.fetchall() 
 
cursor.execute(agents_middle_name)
agents_middle_name_list = cursor.fetchall() 

cursor.execute(agents_reviewed)
agents_reviewed_list = cursor.fetchall() 
# print(cursor.fetchall())
# print(agents_reviewed_list)

cursor.execute(brokers)
brokers_list = cursor.fetchall() 

cursor.execute(developments)
developments_list = cursor.fetchall() 

cursor.execute(cities)
cities_list = cursor.fetchall() 

cursor.execute(users)
users_list = cursor.fetchall() 

cursor.execute(amenities)
amenities_list = cursor.fetchall() 

cursor.execute(prices)
prices_list = cursor.fetchall() 

cursor.execute(brokers1)
brokers1_list = cursor.fetchall() 
# cursor.execute(command1)
# print( cursor.fetchall())

# connection.commit()


# main homepage.html
@app.route('/', methods=['GET','POST'])
def index(): 
    # agent_3q = str()

    return render_template('homepage.html', list_brokers1 = brokers1_list, list = agents_list, list_brokers = brokers_list, list_developments = developments_list, list_cities = cities_list, list_amenities = amenities_list , list_prices = prices_list, list_agents_first_name = agents_first_name_list, list_agents_middle_name = agents_middle_name_list)



# 1- create user
@app.route('/create_user', methods=['GET','POST'])
def create_user1(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        userDetails = request.form

        number = userDetails['phone_number']
        first_name = userDetails['first_name']
        middle_name = userDetails['middle_name']
        last_name = userDetails['last_name']
        BD = userDetails['BD']
        gender = userDetails['gender']
        age = userDetails['age']
        email = userDetails['email']
        # focus = userDetails['focus']
        
        insert_user = """
        INSERT INTO users_table VALUES ({}, {}, {}, {}, {}, {}, {}, {});
        """.format(number, first_name, middle_name, last_name, BD, gender, age, email)
        cursor.execute(insert_user)
        projdb1.commit()
    return render_template('homepage.html', list_brokers1 = brokers1_list, list = agents_list, list_brokers = brokers_list, list_developments = developments_list, list_cities = cities_list, list_amenities = amenities_list , list_prices = prices_list, list_agents_first_name = agents_first_name_list, list_agents_middle_name = agents_middle_name_list)

@app.route('/review', methods=['GET','POST'])
def create_user(): 
    return render_template('create_user.html', list = agents_list, list_brokers = brokers_list, list_developments = developments_list, list_cities = cities_list, list_amenities = amenities_list , list_prices = prices_list, list_agents_first_name = agents_first_name_list, list_agents_middle_name = agents_middle_name_list)

# 2- create agent review 
@app.route('/create_agent_review', methods=['GET','POST'])
def create_agent_review(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        reviewDetails = request.form

        user_reviewing = reviewDetails['user_reviewing']
        agent_reviewed = reviewDetails['agent_reviewed']
        rating = reviewDetails['rating']
        textual_review = reviewDetails['textual_review']
        insert_agent_review = """
        INSERT INTO reviewes_table VALUES ("{}", "{}", {}, "{}");
        """.format(user_reviewing, agent_reviewed, rating, textual_review)
        cursor.execute(insert_agent_review)
        projdb1.commit()
    return render_template('homepage.html', list = agents_list, list_brokers = brokers1_list, list_developments = developments_list, list_cities = cities_list, list_amenities = amenities_list , list_prices = prices_list, list_agents_first_name = agents_first_name_list, list_agents_middle_name = agents_middle_name_list)

@app.route('/review1', methods=['GET','POST'])
def review1():

    return render_template('create_agent_review.html', list = agents_list, llist = users_list)

    

# 3- view agent reviews 
# Select rating, textual_review from reviews_table
# Where agent_reviewed = “”; 

@app.route('/view_agent_reviews', methods=['GET','POST'])
def view_agent_reviews(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        agent = review1Details["agent"]

        review_agent_reviews = """
        select rating, textual_review from reviewes_table
        where agent_reviewed = "{}";
        """.format(agent)
        cursor.execute(review_agent_reviews)
        heading = ['rating', 'reviews']
        reviews = cursor.fetchall() 
        return render_template('view_agent_reviews.html', list = reviews, heading = heading)

# 4- View aggregated rating of a brokerage company
# query to be executed
#   Select avg(rating) from reviewes_table r inner join agents_table a on r.agent_reviewed = a.agent_contact_number 
#   Where a.agent_broker_name = “”;
@app.route('/view_broker_rating', methods=['GET','POST'])
def view_broker_rating(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        broker = review1Details["broker"]
        
        view_broker_rating_sql = """
        select avg(r.rating), a.agent_broker_name from reviewes_table r inner join agents_table a on r.agent_reviewed = a.agent_contact_number 
        Where a.agent_broker_name = "{}"
        group by a.agent_broker_name;   
        """.format(broker)
        cursor.execute(view_broker_rating_sql)
        heading = ['rating', 'broker_company']
        reviews = cursor.fetchall() 
        
        return render_template('view_broker_rating.html',  list = reviews, heading = heading)

# 5.Show the location of a given development, along with the average price/sqm and the number of listings for each unit type. 
@app.route('/view_dev_info', methods=['GET','POST'])
def view_dev_info(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        development = review1Details["development"]
        
        view_dev_info_sql = """
        select * from developers_table dt; 
        """.format(development)
        cursor.execute(view_dev_info_sql)
        heading = ['dev_name', 'contact_number', 'head_office_location', 'about']
        reviews = cursor.fetchall() 
        
    return render_template('view_dev_info.html',  list = reviews, heading = heading)

# 6. Show all the properties in a certain city, along with the average price / sqm for each unit type
# Select * from properties_table where city = “”;
#   Select property_type, avg(property_size_sqmt) from properties_table 
#   Where city = “”
#   Group by property_type;
@app.route('/view_prop_city_info', methods=['GET','POST'])
def view_prop_city_info(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        city1 = review1Details["city1"]
        
        view_prop_city_info_sql = """
        Select * from properties_table where property_city = "{}";
        """.format(city1)
        cursor.execute(view_prop_city_info_sql)
        heading = ['pk','option', 'area', 'governorate', 'city' , 'district', 'compound', 'description' ,'downpayment', 'type', 'size_sqft' , 'size_sqmt', 'bedrooms', 'maid' , 'bathrooms ' , 'price_USD', 'price_EGP', 'reference ' , 'listing date', 'agent_contact_number' , 'project_name' , 'developer_name']
        reviews = cursor.fetchall() 
        
        view_prop_city_info_sql1 = """
        Select property_type, avg(property_size_sqmt) from properties_table 
        Where property_city = "{}"
        Group by property_type;
        """.format(city1)
        cursor.execute(view_prop_city_info_sql1)
        heading1 = ['property_type', 'avg_size_sqmt']
        reviews1 = cursor.fetchall() 

    return render_template('view_prop_city_info.html',  list = reviews, heading = heading, list1 = reviews1, heading1 = heading1)


# 7. Show all the properties in a certain city in a given price range, with a given set of amenities 
## select * from properties_table pt inner join 
 #  (	select property_pk, count(amenities_type) from properties_amenities_table pat 
 #   	Where pat.amenities_type in ("Unfurnished", "Security", "PrivateGarden", "SharedGym")
 #      Group by property_pk 
 #      Having COUNT(`amenities_type`) = 4 
 #  ) nt on pt.property_pk = nt.property_pk 
 #  where (pt.property_price_EGP between '0' and '30000000' 
 #      AND pt.property_city = " New Cairo City")
@app.route('/view_prop_city_info1', methods=['GET','POST'])
def view_prop_city_info1(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        # amenities = []
        city2 = review1Details["city2"]
        min_price = review1Details["min_price"]
        max_price = review1Details["max_price"]
        amenity1 = review1Details["amenity1"]
        amenity2 = review1Details["amenity2"]
        amenity3 = review1Details["amenity3"]
        amenity4 = review1Details["amenity4"]
        amenity5 = review1Details["amenity5"]
        # amenities.push(amenity1)
        # amenities.push(amenity2)
        # amenities.push(amenity3)
        # amenities.push(amenity4)
        # amenities.push(amenity5)

        view_prop_city_info1_sql = """
        select * from properties_table pt inner join 
          (	select property_pk, count(amenities_type) from properties_amenities_table pat 
           	Where pat.amenities_type in ("{}", "{}", "{}", "{}", "{}")
              Group by property_pk 
              Having COUNT(`amenities_type`) >= 1
          ) nt on pt.property_pk = nt.property_pk 
          where (pt.property_price_EGP between {} and {} 
              AND pt.property_city = "{}")
        """.format(amenity1, amenity2, amenity3, amenity4, amenity5, min_price, max_price, city2)
        cursor.execute(view_prop_city_info1_sql)
        heading = ['pk','option', 'area', 'governorate', 'city' , 'district', 'compound', 'description' ,'downpayment', 'type', 'size_sqft' , 'size_sqmt', 'bedrooms', 'maid' , 'bathrooms ' , 'price_USD', 'price_EGP', 'reference ' , 'listing date', 'agent_contact_number' , 'project_name' , 'developer_name']
        reviews = cursor.fetchall() 
        
    return render_template('view_prop_city_info1.html',  list = reviews, heading = heading)



# 8. Show the top 10 areas in a given city by amount of inventory and price / sqm of a given unit type
#   select property_area, avg(pt.property_price_EGP/ pt.property_size_sqmt)as price_per_s, count(*) from properties_table pt
#   where pt.property_city = " New Capital City"
#   group by property_area 
#   order by count(*) desc, price_per_s desc
#   limit 10;
@app.route('/top_10_areas', methods=['GET','POST'])
def top_10_areas(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        city3 = review1Details["city3"]

        top_10_areas_sql = """
           select property_area, avg(pt.property_price_EGP/ pt.property_size_sqmt)as price_per_s, count(*) from properties_table pt
           where pt.property_city = "{}"
           group by property_area 
           order by count(*) desc, price_per_s desc
           limit 10;
        """.format(city3)
        cursor.execute(top_10_areas_sql)
        heading = ['property_area', 'avg (price(EGP)/sqmt)']
        reviews = cursor.fetchall() 
        
    return render_template('top_10_areas.html',  list = reviews, heading = heading)


# 9. Show the top 5 brokerage companies by the amount of listings they have, along with their avg price / sqm, number of agents, and average listings per agent
# select b.broker_name, count(a.agent_contact_number), avg(p.property_price_EGP/p.property_size_sqmt) as "avg (price/sqmt)" from brokers_table b inner join agents_table a on b.broker_name = a.agent_broker_name inner join properties_table p on a.agent_contact_number = p.property_agent_contact_number
# group by b.broker_name
# order by b.broker_available_properties desc, count(a.agent_contact_number) desc, "avg (price/sqmt)" desc;
#

@app.route('/top_5_brokers', methods=['GET','POST'])
def top_5_brokers(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        

        top_5_brokers_sql = """
            select b.broker_name, count(a.agent_contact_number), avg(p.property_price_EGP/p.property_size_sqmt) as "avg (price/sqmt)" from brokers_table b inner join agents_table a on b.broker_name = a.agent_broker_name inner join properties_table p on a.agent_contact_number = p.property_agent_contact_number
            group by b.broker_name
            order by b.broker_available_properties desc, count(a.agent_contact_number) desc, "avg (price/sqmt)" desc
            limit 5;
        """
        cursor.execute(top_5_brokers_sql)
        heading = ['broker']
        reviews = cursor.fetchall() 
        
    return render_template('top_5_brokers.html',  list = reviews, heading = heading)



# 10. Show all the properties listed by a specific agent (given their first and last name and / or phone no)
#   select * from properties_table pt inner_join agents_table aat on pt.property_agent_contact_number = aat.agent_contact_number  
#   Where aat.agent_first_name = "" AND aat.agent_middle_name = ""
#   OR aat.agent_contact_number = "";

@app.route('/q10_prop_info', methods=['GET','POST'])
def q10_prop_info(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        agent_first_name = review1Details["agent_first_name"]
        agent_middle_name = review1Details["agent_middle_name"]
        agent_contact_number = review1Details["agent_contact_number"]

        q10_prop_info_sql = """
          select * from properties_table pt inner join agents_table aat on pt.property_agent_contact_number = aat.agent_contact_number  
          Where aat.agent_first_name = "{}" AND aat.agent_middle_name = "{}"
          OR aat.agent_contact_number = "{}";
        """.format(agent_first_name, agent_middle_name, agent_contact_number)
        cursor.execute(q10_prop_info_sql)
        heading = ['pk','option', 'area', 'governorate', 'city' , 'district', 'compound', 'description' ,'downpayment', 'type', 'size_sqft' , 'size_sqmt', 'bedrooms', 'maid' , 'bathrooms ' , 'price_USD', 'price_EGP', 'reference ' , 'listing date', 'agent_contact_number' , 'project_name' , 'developer_name']
        reviews = cursor.fetchall() 
        
    return render_template('q10_prop_info.html',  list = reviews, heading = heading)


# 11. Estimate the cash discount per development based on the price differential between the cash price and the installment price for each unit type
@app.route('/q11', methods=['GET','POST'])
def q11(): 
    if request.method == 'POST':
        # RETREIVE data submitted in form
        review1Details = request.form
        agent_first_name = review1Details["agent_first_name"]
        agent_middle_name = review1Details["agent_middle_name"]
        agent_contact_number = review1Details["agent_contact_number"]

        q11_sql = """
        select * from devlopments_table;

        """.format()
        cursor.execute(q11_sql)
        heading = ['']
        reviews = cursor.fetchall() 
        
    return render_template('q11.html',  list = reviews, heading = heading)



# creating user 
@app.route('/viewusers')
def viewusers():
    cursor.execute("SELECT * FROM user")
    viewusers = cursor.fetchall()
    return render_template('viewusers.html', newuser=viewusers)

@app.route('/users')
def users():
    resultValue = cursor.execute("SELECT * from user")
    if resultValue > 0:
        userDetails = cursor.fetchall()
        return render_template('users.html',userDetails=userDetails)


if __name__ == '__main__':
    app.run(debug=True)