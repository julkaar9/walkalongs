# W3SCHOOL SQL exercises using Django ORM
[https://www.w3schools.com/sql/exercise.asp](https://www.w3schools.com/sql/exercise.asp)

This walkalong consists of W3SCHOOL sql exercise solutions written in both **SQL** and **django
ORM**, They query results are also compared for equality.  
The Insert, Update and Delete queries are not included to keep database consistent.

## Try it yourself
The notebook (Django Shell-plus) is located in [here](https://github.com/julkaar9/walkalongs/blob/main/server/notebooks/ws3school.ipynb)   
First cd into the notebook directory `cd server/notebook`  
Then open the notebook using `python ../manage.py shell_plus --notebook`  

(Note the preformatted tables are intentional)

## Testing some basic queries
```py
sqlq = sql_raw("SELECT * FROM Customers limit 3") 
```

    |    |   customerNumber | customerName               | contactLastName   | contactFirstName   | phone        | addressLine1      | city      | state    |   postalCode | country   |
    |---:|-----------------:|:---------------------------|:------------------|:-------------------|:-------------|:------------------|:----------|:---------|-------------:|:----------|
    |  0 |              103 | Atelier graphique          | Schmitt           | Carine             | 40.32.2555   | 54, rue Royale    | Nantes    |          |        44000 | France    |
    |  1 |              112 | Signal Gift Stores         | King              | Jean               | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |        83030 | USA       |
    |  2 |              114 | Australian Collectors, Co. | Ferguson          | Peter              | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |         3004 | Australia |
    


```python
ormq = Customers.objects.all().values()[:3]
```

    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone        | address_line1     | city      | state    |   postal_code | country   |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:-------------|:------------------|:----------|:---------|--------------:|:----------|
    |  0 |               103 | Atelier graphique          | Schmitt             | Carine               | 40.32.2555   | 54, rue Royale    | Nantes    |          |         44000 | France    |
    |  1 |               112 | Signal Gift Stores         | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |         83030 | USA       |
    |  2 |               114 | Australian Collectors, Co. | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |          3004 | Australia |
    


```python
equal(sqlq, ormq)
```

Equal ✔️
## SELECT
### Exercise 1
Insert the missing statement to get all the columns FROM the Customers table.


```python
sqlq =  sql_raw("SELECT * FROM Customers")
ormq =  Customers.objects.all().values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone        | address_line1     | city      | state    |   postal_code | country   |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:-------------|:------------------|:----------|:---------|--------------:|:----------|
    |  0 |               103 | Atelier graphique          | Schmitt             | Carine               | 40.32.2555   | 54, rue Royale    | Nantes    |          |         44000 | France    |
    |  1 |               112 | Signal Gift Stores         | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |         83030 | USA       |
    |  2 |               114 | Australian Collectors, Co. | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |          3004 | Australia |
    

### Exercise 2
Write a statement that will SELECT the City column FROM the Customers table.


```py
sqlq = sql_raw("SELECT city FROM Customers;")
ormq =  Customers.objects.all().values("city")
equal(sqlq, ormq)
```

Equal ✔️


    |    | city      |
    |---:|:----------|
    |  0 | Nantes    |
    |  1 | Las Vegas |
    |  2 | Melbourne |
    

### Exercise 3


```python
sqlq =  sql_raw("SELECT DISTINCT country FROM Customers;")
ormq =  Customers.objects.all().values("country").distinct()
equal(sqlq, ormq)
```

Equal ✔️


    |    | country   |
    |---:|:----------|
    |  0 | France    |
    |  1 | USA       |
    |  2 | Australia |
    

## WHERE
### Exercise 1
Select all records WHERE the City column has the value "Berlin".


```python
sqlq =  sql_raw("SELECT * FROM Customers WHERE city='Berlin';")
ormq =  Customers.objects.filter(city='Berlin').values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name    | contact_last_name   | contact_first_name   | phone       | address_line1   | city   | state   |   postal_code | country   |
    |---:|------------------:|:-----------------|:--------------------|:---------------------|:------------|:----------------|:-------|:--------|--------------:|:----------|
    |  0 |               307 | Der Hund Imports | Andersen            | Mel                  | 030-0074555 | Obere Str. 57   | Berlin |         |         12209 | Germany   |
    

### Exercise 2


```python
sqlq =  sql_raw("SELECT * FROM Customers WHERE NOT city='Berlin';")
ormq =  Customers.objects.exclude(city='Berlin').values()
equal(sqlq, ormq)
```

Equal ✔️
    


```python
ormq1 =  Customers.objects.filter(~Q(city="Berlin")).values()
equal(sqlq, ormq1)
```

Equal ✔️


    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone        | address_line1     | city      | state    |   postal_code | country   |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:-------------|:------------------|:----------|:---------|--------------:|:----------|
    |  0 |               103 | Atelier graphique          | Schmitt             | Carine               | 40.32.2555   | 54, rue Royale    | Nantes    |          |         44000 | France    |
    |  1 |               112 | Signal Gift Stores         | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |         83030 | USA       |
    |  2 |               114 | Australian Collectors, Co. | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |          3004 | Australia |
    

### Exercise 3
Select all records WHERE the Customer_number column has the value 320.


```python
sqlq =  sql_raw("SELECT * FROM Customers WHERE customerNumber='320';")
ormq =  Customers.objects.filter(customer_number=320).values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name       | contact_last_name   | contact_first_name   |      phone | address_line1     | city        | state   |   postal_code | country   |
    |---:|------------------:|:--------------------|:--------------------|:---------------------|-----------:|:------------------|:------------|:--------|--------------:|:----------|
    |  0 |               320 | Mini Creations Ltd. | Huang               | Wing                 | 5085559555 | 4575 Hillside Dr. | New Bedford | MA      |         50553 | USA       |
    

### Exercise 4
Select all records WHERE the City column has the value 'Berlin' and the PostalCode column has the value 12209.


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city='Berlin' AND postalCode=12209;")
ormq =  Customers.objects.filter(city="Berlin", postal_code=12209).values() 
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name    | contact_last_name   | contact_first_name   | phone       | address_line1   | city   | state   |   postal_code | country   |
    |---:|------------------:|:-----------------|:--------------------|:---------------------|:------------|:----------------|:-------|:--------|--------------:|:----------|
    |  0 |               307 | Der Hund Imports | Andersen            | Mel                  | 030-0074555 | Obere Str. 57   | Berlin |         |         12209 | Germany   |
    

### Exercise 5
Select all records WHERE the City column has the value 'Berlin' or 'London'. 


```python
sqlq =  sql_raw("SELECT * FROM Customers WHERE city='Berlin' OR city='London'")
ormq =  Customers.objects.filter(Q(city="Berlin") | Q(city="London") ).values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name                  | contact_last_name   | contact_first_name   | phone          | address_line1   | city   | state   | postal_code   | country   |
    |---:|------------------:|:-------------------------------|:--------------------|:---------------------|:---------------|:----------------|:-------|:--------|:--------------|:----------|
    |  0 |               307 | Der Hund Imports               | Andersen            | Mel                  | 030-0074555    | Obere Str. 57   | Berlin |         | 12209         | Germany   |
    |  1 |               324 | Stylish Desk Decors, Co.       | Brown               | Ann                  | (171) 555-0297 | 35 King George  | London |         | WX3 6FW       | UK        |
    |  2 |               489 | Double Decker Gift Stores, Ltd | Smith               | Thomas               | (171) 555-7555 | 120 Hanover Sq. | London |         | WA1 1DP       | UK        |
    

## ORDER BY
### Exercise 1
Select all records FROM the Customers table, sort the result alphabetically by the column City.


```python
sqlq =  sql_raw("SELECT * FROM Customers ORDER BY city")
ormq =  Customers.objects.all().order_by("city").values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name         | contact_last_name   | contact_first_name   | phone           | address_line1    | city      | state   | postal_code   | country     |
    |---:|------------------:|:----------------------|:--------------------|:---------------------|:----------------|:-----------------|:----------|:--------|:--------------|:------------|
    |  0 |               459 | Warburg Exchange      | Ottlieb             | Sven                 | 0241-039123     | Walserweg 21     | Aachen    |         | 52066         | Germany     |
    |  1 |               157 | Diecast Classics Inc. | Leong               | Kelvin               | 2155551555      | 7586 Pompton St. | Allentown | PA      | 70267         | USA         |
    |  2 |               303 | Schuyler Imports      | Schuyler            | Bradley              | +31 20 491 9555 | Kingsfordweg 151 | Amsterdam |         | 1043 GR       | Netherlands |
    

### Exercise 2
Select all records FROM the Customers table, sort the result reversed alphabetically by the column City.


```python
sqlq =  sql_raw("SELECT * FROM Customers ORDER BY city desc")
ormq =  Customers.objects.all().order_by("-city").values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name                 | contact_last_name   | contact_first_name   | phone       | address_line1             | city         | state   |   postal_code | country     |
    |---:|------------------:|:------------------------------|:--------------------|:---------------------|:------------|:--------------------------|:-------------|:--------|--------------:|:------------|
    |  0 |               227 | Heintze Collectables          | Ibsen               | Palle                | 86 21 3555  | Smagsloget 45             | ┼rhus        |         |          8200 | Denmark     |
    |  1 |               319 | Mini Classics                 | Frick               | Steve                | 9145554562  | 3758 North Pendale Street | White Plains | NY      |         24067 | USA         |
    |  2 |               412 | Extreme Desk Decorations, Ltd | McRoy               | Sarah                | 04 499 9555 | 101 Lambton Quay          | Wellington   |         |               | New Zealand |
    

### Exercise 3
Select all records FROM the Customers table, sort the result alphabetically,
first by the column Country, then, by the column City.


```python
sqlq =  sql_raw("SELECT * FROM Customers ORDER BY country, city")
ormq =  Customers.objects.all().order_by("country", "city").values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name                | contact_last_name   | contact_first_name   | phone           | address_line1          | city         | state    |   postal_code | country   |
    |---:|------------------:|:-----------------------------|:--------------------|:---------------------|:----------------|:-----------------------|:-------------|:---------|--------------:|:----------|
    |  0 |               282 | Souveniers And Things Co.    | Huxley              | Adrian               | +61 2 9495 8555 | Monitor Money Building | Chatswood    | NSW      |          2067 | Australia |
    |  1 |               471 | Australian Collectables, Ltd | Clenahan            | Sean                 | 61-9-3844-6555  | 7 Allen Street         | Glen Waverly | Victoria |          3150 | Australia |
    |  2 |               114 | Australian Collectors, Co.   | Ferguson            | Peter                | 03 9520 4555    | 636 St Kilda Road      | Melbourne    | Victoria |          3004 | Australia |
    

## NULL
### Exercise 1
Select all records FROM the Customers WHERE the PostalCode column is empty.


```python
sqlq =  sql_raw("SELECT * FROM Customers WHERE postalCode IS NULL")
ormq =  Customers.objects.filter(postal_code=None).values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name               | contact_last_name   | contact_first_name   | phone          | address_line1        | city              | state    | postal_code   | country     |
    |---:|------------------:|:----------------------------|:--------------------|:---------------------|:---------------|:---------------------|:------------------|:---------|:--------------|:------------|
    |  0 |               211 | King Kong Collectables, Co. | Gao                 | Mike                 | +852 2251 1555 | Bank of China Tower  | Central Hong Kong |          |               | Hong Kong   |
    |  1 |               323 | Down Under Souveniers, Inc  | Graham              | Mike                 | +64 9 312 5555 | 162-164 Grafton Road | Auckland          |          |               | New Zealand |
    |  2 |               348 | Asian Treasures, Inc.       | McKenna             | Patricia             | 2967 555       | 8 Johnstown Road     | Cork              | Co. Cork |               | Ireland     |
    

### Exercise 2
Select all records FROM the Customers WHERE the PostalCode column is NOT empty.


```python
sqlq = sql_raw("SELECT * FROM Customers WHERE postalCode IS NOT NULL")
ormq = Customers.objects.exclude(postal_code=None).values()
equal(sqlq, ormq)
```

Equal ✔️
    


```python
ormq1 =  Customers.objects.filter(~Q(postal_code=None)).values()
equal(sqlq, ormq1)
```

Equal ✔️
    


```python
ormq2 =  Customers.objects.filter(postal_code__isnull=False).values()
equal(sqlq, ormq2)
```

Equal ✔️


    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone        | address_line1     | city      | state    |   postal_code | country   |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:-------------|:------------------|:----------|:---------|--------------:|:----------|
    |  0 |               103 | Atelier graphique          | Schmitt             | Carine               | 40.32.2555   | 54, rue Royale    | Nantes    |          |         44000 | France    |
    |  1 |               112 | Signal Gift Stores         | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |         83030 | USA       |
    |  2 |               114 | Australian Collectors, Co. | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |          3004 | Australia |
    

## FUNCTION
### Exercise 1
Use the MIN function to SELECT the record with the smallest value of the Price column.


```python
sqlq = sql_raw("SELECT MIN(buyPrice) mn FROM products")
ormq =  Products.objects.aggregate(mn=Min('buy_price')) 
equal(sqlq, ormq)
```

Equal ✔️


    |    |    mn |
    |---:|------:|
    |  0 | 15.91 |
    

### Exercise 2
Use an SQL function to SELECT the record with the highest value of the Price column.


```python
sqlq = sql_raw("SELECT MAX(buyPrice) mn FROM products")
ormq = dec_to_float(Products.objects.aggregate(mn=Max('buy_price')))
equal(sqlq, ormq)
```

Equal ✔️


    |    |     mn |
    |---:|-------:|
    |  0 | 103.42 |
    

### Exercise 3
Use the correct function to return the number of records that have the Price value set to 15.91.


```python
sqlq = sql_raw("SELECT COUNT(*) cnt FROM products WHERE buyPrice=15.91")
ormq = Products.objects.filter(buy_price=15.91).annotate(cnt=Count("product_code")).values("cnt")
equal(sqlq, ormq)
```

Equal ✔️
    


```python
ormq1 = Products.objects.filter(buy_price=15.91).count()
ormq1 = [{'cnt':ormq1}]
equal(sqlq, ormq1)
```

Equal ✔️


    |    |   cnt |
    |---:|------:|
    |  0 |     1 |
    

### Exercise 4
Use an SQL function to calculate the average price of all products.


```python
sqlq = dec_to_float(sql_raw("SELECT AVG(buyPrice) mean FROM products;"))
ormq = dec_to_float(Products.objects.aggregate(mean=Avg('buy_price')))
equal(sqlq, ormq)
```

Equal ✔️


    |    |    mean |
    |---:|--------:|
    |  0 | 54.3952 |
    

### Exercise 5
Use an SQL function to calculate the sum of all the Price column values in the Products table.


```python
sqlq = dec_to_float(sql_raw("SELECT SUM(buyPrice) sum_ FROM products;"))
ormq = dec_to_float(Products.objects.aggregate(sum_=Sum('buy_price')))
equal(sqlq, ormq)
```

Equal ✔️


    |    |    sum_ |
    |---:|--------:|
    |  0 | 5983.47 |
    

## LIKE
### Exercise 1
Select all records WHERE the value of the City column starts with the letter "a".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city LIKE 'a%'")
ormq =  Customers.objects.filter(city__istartswith='a').values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone           | address_line1        | city      | state   | postal_code   | country     |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:----------------|:---------------------|:----------|:--------|:--------------|:------------|
    |  0 |               157 | Diecast Classics Inc.      | Leong               | Kelvin               | 2155551555      | 7586 Pompton St.     | Allentown | PA      | 70267         | USA         |
    |  1 |               303 | Schuyler Imports           | Schuyler            | Bradley              | +31 20 491 9555 | Kingsfordweg 151     | Amsterdam |         | 1043 GR       | Netherlands |
    |  2 |               323 | Down Under Souveniers, Inc | Graham              | Mike                 | +64 9 312 5555  | 162-164 Grafton Road | Auckland  |         |               | New Zealand |
    

### Exercise 2
Select all records WHERE the value of the City column ends with the letter "a".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city LIKE '%a'")
ormq =  Customers.objects.filter(city__iendswith='a').values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name      | contact_last_name   | contact_first_name   | phone         | address_line1          | city     | state   | postal_code   | country   |
    |---:|------------------:|:-------------------|:--------------------|:---------------------|:--------------|:-----------------------|:---------|:--------|:--------------|:----------|
    |  0 |               125 | Havel & Zbyszek Co | Piestrzeniewicz     | Zbyszek              | (26) 642-7555 | ul. Filtrowa 68        | Warszawa |         | 01-012        | Poland    |
    |  1 |               169 | Porto Imports Co.  | de Castro           | Isabel               | (1) 356-5555  | Estrada da sa·de n. 58 | Lisboa   |         | 1756          | Portugal  |
    |  2 |               205 | Toys4GrownUps.com  | Young               | Julie                | 6265557265    | 78934 Hillside Dr.     | Pasadena | CA      | 90003         | USA       |
    

### Exercise 3
Select all records WHERE the value of the City column contains the letter "a".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city LIKE '%a%'")
ormq =  Customers.objects.filter(city__icontains='a').values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name      | contact_last_name   | contact_first_name   | phone      | address_line1                | city      | state   |   postal_code | country   |
    |---:|------------------:|:-------------------|:--------------------|:---------------------|:-----------|:-----------------------------|:----------|:--------|--------------:|:----------|
    |  0 |               103 | Atelier graphique  | Schmitt             | Carine               | 40.32.2555 | 54, rue Royale               | Nantes    |         |         44000 | France    |
    |  1 |               112 | Signal Gift Stores | King                | Jean                 | 7025551838 | 8489 Strong St.              | Las Vegas | NV      |         83030 | USA       |
    |  2 |               119 | La Rochelle Gifts  | Labrune             | Janine               | 40.67.8555 | 67, rue des Cinquante Otages | Nantes    |         |         44000 | France    |
    

### Exercise 4
Select all records WHERE the value of the City column starts with letter "a" and ends with the letter "b".
(Note no such rows exists, so we will use L%n


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city LIKE 'L%n'")
ormq =  Customers.objects.filter(Q(city__istartswith='L') & Q(city__endswith='n')).values()
equal(sqlq, ormq)
```

Equal ✔️
    


```python
ormq1 =  Customers.objects.filter(city__regex=r"^L.*n$").values()
equal(sqlq, ormq1)
```

Equal ✔️


    |    |   customer_number | customer_name                  | contact_last_name   | contact_first_name   | phone          | address_line1      | city   | state   | postal_code   | country   |
    |---:|------------------:|:-------------------------------|:--------------------|:---------------------|:---------------|:-------------------|:-------|:--------|:--------------|:----------|
    |  0 |               146 | Saveley & Henriot, Co.         | Saveley             | Mary                 | 78.32.5555     | 2, rue du Commerce | Lyon   |         | 69004         | France    |
    |  1 |               324 | Stylish Desk Decors, Co.       | Brown               | Ann                  | (171) 555-0297 | 35 King George     | London |         | WX3 6FW       | UK        |
    |  2 |               489 | Double Decker Gift Stores, Ltd | Smith               | Thomas               | (171) 555-7555 | 120 Hanover Sq.    | London |         | WA1 1DP       | UK        |
    

### Exercise 5
Select all records WHERE the value of the City column does NOT start with the letter "a".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city NOT LIKE 'a%'")
ormq =  Customers.objects.exclude(city__istartswith='a').values()
equal(sqlq, ormq)
```

Equal ✔️
    


```python
ormq1 =  Customers.objects.filter(city__regex=r"^[^aA]").values()
equal(sqlq, ormq1)
```

Equal ✔️
    


```python
ormq2 =  Customers.objects.filter(~Q(city__istartswith='a')).values()
equal(sqlq, ormq2)
```

Equal ✔️


    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone        | address_line1     | city      | state    |   postal_code | country   |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:-------------|:------------------|:----------|:---------|--------------:|:----------|
    |  0 |               103 | Atelier graphique          | Schmitt             | Carine               | 40.32.2555   | 54, rue Royale    | Nantes    |          |         44000 | France    |
    |  1 |               112 | Signal Gift Stores         | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |         83030 | USA       |
    |  2 |               114 | Australian Collectors, Co. | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |          3004 | Australia |
    

## WILDCARDS
### Exercise 1
Select all records WHERE the second letter of the City is an "a".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE city LIKE '_a%'")
ormq =  Customers.objects.filter(city__regex=r"^.[aA].*$").values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name      | contact_last_name   | contact_first_name   | phone      | address_line1                | city      | state   |   postal_code | country   |
    |---:|------------------:|:-------------------|:--------------------|:---------------------|:-----------|:-----------------------------|:----------|:--------|--------------:|:----------|
    |  0 |               103 | Atelier graphique  | Schmitt             | Carine               | 40.32.2555 | 54, rue Royale               | Nantes    |         |         44000 | France    |
    |  1 |               112 | Signal Gift Stores | King                | Jean                 | 7025551838 | 8489 Strong St.              | Las Vegas | NV      |         83030 | USA       |
    |  2 |               119 | La Rochelle Gifts  | Labrune             | Janine               | 40.67.8555 | 67, rue des Cinquante Otages | Nantes    |         |         44000 | France    |
    

### Exercise 2
Select all records WHERE the first letter of the City is an "a" or a "c" or an "s".


```python
# sqlq =  Customers.objects.raw("SELECT * FROM customers WHERE city LIKE '[acs]%'")
sqlq =  sql_raw("SELECT * FROM customers WHERE CITY LIKE 'a%' OR CITY LIKE 'c%' OR CITY LIKE 's%'")
query = Q()
for ch in ['a','c','s']:
    query = query | Q(city__istartswith=ch)
ormq =  Customers.objects.filter(query).values()
equal(sqlq, ormq) 
```

Equal ✔️
    


```python
ormq1 =  Customers.objects.filter(city__regex=r"^[acsACS].*$").values()
equal(sqlq, ormq1)
```

Equal ✔️


    |    |   customer_number | customer_name                | contact_last_name   | contact_first_name   | phone      | address_line1             | city          | state   |   postal_code | country   |
    |---:|------------------:|:-----------------------------|:--------------------|:---------------------|:-----------|:--------------------------|:--------------|:--------|--------------:|:----------|
    |  0 |               121 | Baane Mini Imports           | Bergulfsen          | Jonas                | 07-98 9555 | Erling Skakkes gate 78    | Stavern       |         |          4110 | Norway    |
    |  1 |               124 | Mini Gifts Distributors Ltd. | Nelson              | Susan                | 4155551450 | 5677 Strong St.           | San Rafael    | CA      |         97562 | USA       |
    |  2 |               129 | Mini Wheels Co.              | Murphy              | Julie                | 6505555787 | 5557 North Pendale Street | San Francisco | CA      |         94217 | USA       |
    

### Exercise 3
Select all records WHERE the first letter of the City starts with anything FROM an "a" to an "f".


```python
# sqlq =  Customers.objects.raw("SELECT * FROM customers WHERE city LIKE '[a-f]%'") # doesnt work in sqlite
sqlq =  sql_raw("SELECT * FROM customers WHERE city REGEXP '^[a-fA-F].*$'")
ormq =  Customers.objects.filter(city__regex=r"^[a-fA-F].*$").values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name         | contact_last_name   | contact_first_name   | phone             | address_line1     | city       | state   |   postal_code | country   |
    |---:|------------------:|:----------------------|:--------------------|:---------------------|:------------------|:------------------|:-----------|:--------|--------------:|:----------|
    |  0 |               128 | Blauer See Auto, Co.  | Keitel              | Roland               | +49 69 66 90 2555 | Lyonerstr. 34     | Frankfurt  |         |         60528 | Germany   |
    |  1 |               157 | Diecast Classics Inc. | Leong               | Kelvin               | 2155551555        | 7586 Pompton St.  | Allentown  | PA      |         70267 | USA       |
    |  2 |               161 | Technics Stores Inc.  | Hashimoto           | Juri                 | 6505556809        | 9408 Furth Circle | Burlingame | CA      |         94217 | USA       |
    

### Exercise 4
Select all records WHERE the first letter of the City is NOT an "a" or a "c" or an "f".


```python
# sqlq =  Customers.objects.raw("SELECT * FROM customers WHERE city LIKE '[!acf]%'")
sqlq =  sql_raw("SELECT * FROM customers WHERE CITY NOT LIKE 'a%' OR CITY NOT LIKE 'c%' OR CITY NOT LIKE 's%'")
query = Q()
for ch in ['a','c','d']:
    query = query | ~Q(city__istartswith=ch)
ormq =  Customers.objects.filter(query).values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name              | contact_last_name   | contact_first_name   | phone        | address_line1     | city      | state    |   postal_code | country   |
    |---:|------------------:|:---------------------------|:--------------------|:---------------------|:-------------|:------------------|:----------|:---------|--------------:|:----------|
    |  0 |               103 | Atelier graphique          | Schmitt             | Carine               | 40.32.2555   | 54, rue Royale    | Nantes    |          |         44000 | France    |
    |  1 |               112 | Signal Gift Stores         | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas | NV       |         83030 | USA       |
    |  2 |               114 | Australian Collectors, Co. | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne | Victoria |          3004 | Australia |
    

## IN
### Exercise 1
Use the IN operator to SELECT all the records WHERE Country is either "Norway" or "France".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE country IN ('Norway', 'France')")
ormq =  Customers.objects.filter(country__in=['Norway', 'France']).values()
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name      | contact_last_name   | contact_first_name   | phone      | address_line1                | city    | state   |   postal_code | country   |
    |---:|------------------:|:-------------------|:--------------------|:---------------------|:-----------|:-----------------------------|:--------|:--------|--------------:|:----------|
    |  0 |               103 | Atelier graphique  | Schmitt             | Carine               | 40.32.2555 | 54, rue Royale               | Nantes  |         |         44000 | France    |
    |  1 |               119 | La Rochelle Gifts  | Labrune             | Janine               | 40.67.8555 | 67, rue des Cinquante Otages | Nantes  |         |         44000 | France    |
    |  2 |               121 | Baane Mini Imports | Bergulfsen          | Jonas                | 07-98 9555 | Erling Skakkes gate 78       | Stavern |         |          4110 | Norway    |
    

### Exercise 2
Use the IN operator to SELECT all the records WHERE Country is NOT "Norway" and NOT "France".


```python
sqlq =  sql_raw("SELECT * FROM customers WHERE country NOT IN ('Norway', 'France')")
ormq =  Customers.objects.exclude(country__in=['Norway', 'France']).values()
equal(sqlq, ormq)
```

Equal ✔️
    


```python
ormq1 =  Customers.objects.filter(~Q(country__in=['Norway', 'France'])).values()
equal(sqlq, ormq1)
```

Equal ✔️


    |    |   customer_number | customer_name                | contact_last_name   | contact_first_name   | phone        | address_line1     | city       | state    |   postal_code | country   |
    |---:|------------------:|:-----------------------------|:--------------------|:---------------------|:-------------|:------------------|:-----------|:---------|--------------:|:----------|
    |  0 |               112 | Signal Gift Stores           | King                | Jean                 | 7025551838   | 8489 Strong St.   | Las Vegas  | NV       |         83030 | USA       |
    |  1 |               114 | Australian Collectors, Co.   | Ferguson            | Peter                | 03 9520 4555 | 636 St Kilda Road | Melbourne  | Victoria |          3004 | Australia |
    |  2 |               124 | Mini Gifts Distributors Ltd. | Nelson              | Susan                | 4155551450   | 5677 Strong St.   | San Rafael | CA       |         97562 | USA       |
    

## BETWEEN
### Exercise 1
Use the BETWEEN operator to SELECT all the records WHERE the value of the Price column is between 10 and 20.


```python
sqlq =  sql_raw("SELECT * FROM products WHERE buyPrice BETWEEN 10 AND 20;")
ormq =  Products.objects.filter(Q(buy_price__gte=10) & Q(buy_price__lte=20)).values()
equal(sqlq, ormq) 
```

Equal ✔️


    |    | product_code   | product_name                        | product_scale   | product_vendor           | product_description                                                                                                                                                                                                                                  |   quantity_in_stock |   buy_price |   msrp |
    |---:|:---------------|:------------------------------------|:----------------|:-------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|------------:|-------:|
    |  0 | S24_2840       | 1958 Chevy Corvette Limited Edition | 1:24            | Carousel DieCast Legends | The operating parts of this 1958 Chevy Corvette Limited Edition are particularly delicate due to their precise scale and require special care and attention. Features rotating wheels, working streering, opening doors and trunk. Color dark green. |                2542 |       15.91 |  35.36 |
    |  1 | S24_2972       | 1982 Lamborghini Diablo             | 1:24            | Second Gear Diecast      | This replica features opening doors, superb detail and craftsmanship, working steering system, opening forward compartment, opening rear trunk with removable spare, 4 wheel independent spring suspension as well as factory baked enamel finish.   |                7723 |       16.24 |  37.76 |
    

### Exercise 2
Use the BETWEEN operator to select all the records where the value of the Price column is NOT between 10 and 20.


```python
sqlq =  sql_raw("SELECT * FROM products WHERE buyPrice NOT BETWEEN 10 AND 20;")
ormq =  Products.objects.filter(~Q(buy_price__gte=10) | ~Q(buy_price__lte=20)).values()
equal(sqlq, ormq) 
```

Equal ✔️


    |    | product_code   | product_name                          | product_scale   | product_vendor           | product_description                                                                                                                                                                                                                                                                                                                                                                                     |   quantity_in_stock |   buy_price |   msrp |
    |---:|:---------------|:--------------------------------------|:----------------|:-------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|------------:|-------:|
    |  0 | S10_1678       | 1969 Harley Davidson Ultimate Chopper | 1:10            | Min Lin Diecast          | This replica features working kickstand, front suspension, gear-shift lever, footbrake lever, drive chain, wheels and steering. All parts are particularly delicate due to their precise scale and require special care and attention.                                                                                                                                                                  |                7933 |       48.81 |  95.7  |
    |  1 | S10_1949       | 1952 Alpine Renault 1300              | 1:10            | Classic Metal Creations  | Turnable front wheels; steering function; detailed interior; detailed engine; opening hood; opening trunk; opening doors; and detailed chassis.                                                                                                                                                                                                                                                         |                7305 |       98.58 | 214.3  |
    |  2 | S10_2016       | 1996 Moto Guzzi 1100i                 | 1:10            | Highway 66 Mini Classics | Official Moto Guzzi logos and insignias, saddle bags located on side of motorcycle, detailed engine, working steering, working suspension, two leather seats, luggage rack, dual exhaust pipes, small saddle bag located on handle bars, two-tone paint with chrome accents, superior die-cast detail , rotating wheels , working kick stand, diecast metal with plastic parts and baked enamel finish. |                6625 |       68.99 | 118.94 |
    

### Exercise 3
Use the BETWEEN operator to SELECT all the records
WHERE the value of the ProductName column is alphabetically between '1904 Buick Runabout' and '1928 Mercedes-Benz SSK'.


```python
sqlq =  sql_raw("SELECT * FROM products WHERE productName BETWEEN '1904 Buick Runabout' AND '1928 Mercedes-Benz SSK';")
ormq =  Products.objects.filter(Q(product_name__gte='1904 Buick Runabout') & Q(product_name__lte='1928 Mercedes-Benz SSK')).values()
equal(sqlq, ormq) 
```

Equal ✔️


    |    | product_code   | product_name             | product_scale   | product_vendor            | product_description                                                                                                                                                                                                                                                                                       |   quantity_in_stock |   buy_price |   msrp |
    |---:|:---------------|:-------------------------|:----------------|:--------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|------------:|-------:|
    |  0 | S18_1749       | 1917 Grand Touring Sedan | 1:18            | Welly Diecast Productions | This 1:18 scale replica of the 1917 Grand Touring car has all the features you would expect from museum quality reproductions: all four doors and bi-fold hood opening, detailed engine and instrument panel, chrome-look trim, and tufted upholstery, all topped off with a factory baked-enamel finish. |                2724 |       86.7  | 170    |
    |  1 | S18_2248       | 1911 Ford Town Car       | 1:18            | Motor City Art Classics   | Features opening hood, opening doors, opening trunk, wide white wall tires, front door arm rests, working steering system.                                                                                                                                                                                |                 540 |       33.3  |  60.54 |
    |  2 | S18_2432       | 1926 Ford Fire Engine    | 1:18            | Carousel DieCast Legends  | Gleaming red handsome appearance. Everything is here the fire hoses, ladder, axes, bells, lanterns, ready to fight any inferno.                                                                                                                                                                           |                2018 |       24.92 |  60.77 |
    

## ALIAS
### Exercise 1
When displaying the Customers table, make an ALIAS of the PostalCode column, the column should be called Pno instead.


```python
sqlq =  sql_raw("SELECT customerName, addressLine1, postalCode pno FROM customers;")
ormq =  Customers.objects.values("customer_name", "address_line1", pno=F("postal_code"))
equal(sqlq, ormq)
```

Equal ✔️


    |    | customer_name              | address_line1     |   pno |
    |---:|:---------------------------|:------------------|------:|
    |  0 | Atelier graphique          | 54, rue Royale    | 44000 |
    |  1 | Signal Gift Stores         | 8489 Strong St.   | 83030 |
    |  2 | Australian Collectors, Co. | 636 St Kilda Road |  3004 |
    

### Exercise 2
When displaying the Customers table, refer to the table as Consumers instead of Customers.


```python
# Couldn't find an answer
```

## JOIN
### Exercise 1
Insert the missing parts in the JOIN clause to join the two tables Orders and Customers,
using the CustomerID field in both tables as the relationship between the two tables.

`select_related` is unnecessary in these following queries, because we are manually specifying all the fields from
both tables. However it is kept as a guidance
see [select_related](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-related)


```python
q = """
Select * FROM orders o
LEFT OUTER JOIN customers c
on o.customerNumber == c.customerNumber
"""
sqlq =  sql_raw(q)
```

    (326, 16)
    |    |   orderNumber | orderDate   | requiredDate   | shippedDate   | status   | comments               |   customerNumber | customerName                 | contactLastName   | contactFirstName   | phone             | addressLine1             | city      | state   |   postalCode | country   |
    |---:|--------------:|:------------|:---------------|:--------------|:---------|:-----------------------|-----------------:|:-----------------------------|:------------------|:-------------------|:------------------|:-------------------------|:----------|:--------|-------------:|:----------|
    |  0 |         10100 | 2003-01-06  | 2003-01-13     | 2003-01-10    | Shipped  |                        |              363 | Online Diecast Creations Co. | Young             | Dorothy            | 6035558647        | 2304 Long Airport Avenue | Nashua    | NH      |        62005 | USA       |
    |  1 |         10101 | 2003-01-09  | 2003-01-18     | 2003-01-11    | Shipped  | Check on availability. |              128 | Blauer See Auto, Co.         | Keitel            | Roland             | +49 69 66 90 2555 | Lyonerstr. 34            | Frankfurt |         |        60528 | Germany   |
    


```python
def get_all_join_fields(lh_class, rh_class, fk):
    lh_class_fields = [field.name for field in lh_class._meta.local_fields]
    rh_class_fields =  {field.name: F(f"{fk}__{field.name}") for field in rh_class._meta.local_fields if field.name not in lh_class_fields}
    return lh_class_fields, rh_class_fields
```


```python
lh_fields, rh_field_dict = get_all_join_fields(Orders, Customers, 'customer_number')
# this will perform an inner join because customer_number is non nullable
ormq =  Orders.objects.select_related('customer_number').values( *lh_fields, **rh_field_dict)
```


```python
equal(sqlq, ormq)
```

Equal ✔️


    |    |   order_number | order_date   | required_date   | shipped_date   | status   | comments               |   customer_number | customer_name                | contact_last_name   | contact_first_name   | phone             | address_line1            | city      | state   |   postal_code | country   |
    |---:|---------------:|:-------------|:----------------|:---------------|:---------|:-----------------------|------------------:|:-----------------------------|:--------------------|:---------------------|:------------------|:-------------------------|:----------|:--------|--------------:|:----------|
    |  0 |          10100 | 2003-01-06   | 2003-01-13      | 2003-01-10     | Shipped  |                        |               363 | Online Diecast Creations Co. | Young               | Dorothy              | 6035558647        | 2304 Long Airport Avenue | Nashua    | NH      |         62005 | USA       |
    |  1 |          10101 | 2003-01-09   | 2003-01-18      | 2003-01-11     | Shipped  | Check on availability. |               128 | Blauer See Auto, Co.         | Keitel              | Roland               | +49 69 66 90 2555 | Lyonerstr. 34            | Frankfurt |         |         60528 | Germany   |
    |  2 |          10102 | 2003-01-10   | 2003-01-18      | 2003-01-14     | Shipped  |                        |               181 | Vitachrome Inc.              | Frick               | Michael              | 2125551500        | 2678 Kingston Rd.        | NYC       | NY      |         10022 | USA       |
    

### Exercise 2
Choose the correct JOIN clause to SELECT all records FROM the two tables WHERE there is a match in both tables.


```python
q = """
Select * FROM orders o
INNER JOIN customers c
on o.customerNumber == c.customerNumber
"""
sqlq =  sql_raw(q)
```

    (326, 16)
    |    |   orderNumber | orderDate   | requiredDate   | shippedDate   | status   | comments               |   customerNumber | customerName                 | contactLastName   | contactFirstName   | phone             | addressLine1             | city      | state   |   postalCode | country   |
    |---:|--------------:|:------------|:---------------|:--------------|:---------|:-----------------------|-----------------:|:-----------------------------|:------------------|:-------------------|:------------------|:-------------------------|:----------|:--------|-------------:|:----------|
    |  0 |         10100 | 2003-01-06  | 2003-01-13     | 2003-01-10    | Shipped  |                        |              363 | Online Diecast Creations Co. | Young             | Dorothy            | 6035558647        | 2304 Long Airport Avenue | Nashua    | NH      |        62005 | USA       |
    |  1 |         10101 | 2003-01-09  | 2003-01-18     | 2003-01-11    | Shipped  | Check on availability. |              128 | Blauer See Auto, Co.         | Keitel            | Roland             | +49 69 66 90 2555 | Lyonerstr. 34            | Frankfurt |         |        60528 | Germany   |
    


```python
lh_fields, rh_field_dict = get_all_join_fields(Orders, Customers, 'customer_number')
ormq =  Orders.objects.filter(customer_number__isnull=False)\
.select_related('customer_number').values( *lh_fields, **rh_field_dict)
```


```python
equal(sqlq, ormq)
```

Equal ✔️


    |    |   order_number | order_date   | required_date   | shipped_date   | status   | comments               |   customer_number | customer_name                | contact_last_name   | contact_first_name   | phone             | address_line1            | city      | state   |   postal_code | country   |
    |---:|---------------:|:-------------|:----------------|:---------------|:---------|:-----------------------|------------------:|:-----------------------------|:--------------------|:---------------------|:------------------|:-------------------------|:----------|:--------|--------------:|:----------|
    |  0 |          10100 | 2003-01-06   | 2003-01-13      | 2003-01-10     | Shipped  |                        |               363 | Online Diecast Creations Co. | Young               | Dorothy              | 6035558647        | 2304 Long Airport Avenue | Nashua    | NH      |         62005 | USA       |
    |  1 |          10101 | 2003-01-09   | 2003-01-18      | 2003-01-11     | Shipped  | Check on availability. |               128 | Blauer See Auto, Co.         | Keitel              | Roland               | +49 69 66 90 2555 | Lyonerstr. 34            | Frankfurt |         |         60528 | Germany   |
    |  2 |          10102 | 2003-01-10   | 2003-01-18      | 2003-01-14     | Shipped  |                        |               181 | Vitachrome Inc.              | Frick               | Michael              | 2125551500        | 2678 Kingston Rd.        | NYC       | NY      |         10022 | USA       |
    

### Exercise 3
Choose the correct JOIN clause to SELECT all the records FROM the Customers table plus all the matches in the Orders table.


```python
q = """
Select * FROM orders o
RIGHT OUTER JOIN customers c
on c.customerNumber == o.customerNumber
"""
sqlq =  sql_raw(q)
```

    (350, 16)
    |    |   orderNumber | orderDate   | requiredDate   | shippedDate   | status   | comments               |   customerNumber | customerName                 | contactLastName   | contactFirstName   | phone             | addressLine1             | city      | state   |   postalCode | country   |
    |---:|--------------:|:------------|:---------------|:--------------|:---------|:-----------------------|-----------------:|:-----------------------------|:------------------|:-------------------|:------------------|:-------------------------|:----------|:--------|-------------:|:----------|
    |  0 |         10100 | 2003-01-06  | 2003-01-13     | 2003-01-10    | Shipped  |                        |              363 | Online Diecast Creations Co. | Young             | Dorothy            | 6035558647        | 2304 Long Airport Avenue | Nashua    | NH      |        62005 | USA       |
    |  1 |         10101 | 2003-01-09  | 2003-01-18     | 2003-01-11    | Shipped  | Check on availability. |              128 | Blauer See Auto, Co.         | Keitel            | Roland             | +49 69 66 90 2555 | Lyonerstr. 34            | Frankfurt |         |        60528 | Germany   |
    


```python
# Couldnt find any proper right join in djorm
lh_fields, rh_field_dict = get_all_join_fields(Customers, Orders ,'orders')

# select_related doesn't work for reverse relationships
ormq = Customers.objects.order_by(F('orders__order_number').asc(nulls_last=True)).values( *lh_fields, **rh_field_dict)
ormdf = orm_to_df(ormq)
```


```python
equal(sqlq, ormq)
```

Equal ✔️


    |    |   customer_number | customer_name                | contact_last_name   | contact_first_name   | phone             | address_line1            | city      | state   |   postal_code | country   |   order_number | order_date   | required_date   | shipped_date   | status   | comments               |
    |---:|------------------:|:-----------------------------|:--------------------|:---------------------|:------------------|:-------------------------|:----------|:--------|--------------:|:----------|---------------:|:-------------|:----------------|:---------------|:---------|:-----------------------|
    |  0 |               363 | Online Diecast Creations Co. | Young               | Dorothy              | 6035558647        | 2304 Long Airport Avenue | Nashua    | NH      |         62005 | USA       |          10100 | 2003-01-06   | 2003-01-13      | 2003-01-10     | Shipped  |                        |
    |  1 |               128 | Blauer See Auto, Co.         | Keitel              | Roland               | +49 69 66 90 2555 | Lyonerstr. 34            | Frankfurt |         |         60528 | Germany   |          10101 | 2003-01-09   | 2003-01-18      | 2003-01-11     | Shipped  | Check on availability. |
    |  2 |               181 | Vitachrome Inc.              | Frick               | Michael              | 2125551500        | 2678 Kingston Rd.        | NYC       | NY      |         10022 | USA       |          10102 | 2003-01-10   | 2003-01-18      | 2003-01-14     | Shipped  |                        |
    

## GROUP BY
### Exercise 1
List the number of customers in each country.


```python
sqlq = sql_raw("SELECT count(customerNumber) as cnt FROM  customers GROUP BY country;")
ormq = Customers.objects.values("country").annotate(cnt=Count("country")).values("cnt")
equal(sqlq, ormq)
```

Equal ✔️


    |    |   cnt |
    |---:|------:|
    |  0 |     5 |
    |  1 |     2 |
    |  2 |     2 |
    

### Exercise 2
List the number of customers in each country, ordered by the country with the most customers first.


```python
sqlq = sql_raw("SELECT country, count(customerNumber) as cnt FROM customers GROUP BY country ORDER BY count(customerNumber) desc;")
ormq = Customers.objects.values("country").annotate(cnt=Count("country")).order_by("-cnt").values("country", "cnt")
equal(sqlq, ormq) 
```

Equal ✔️


    |    | country   |   cnt |
    |---:|:----------|------:|
    |  0 | USA       |    36 |
    |  1 | Germany   |    13 |
    |  2 | France    |    12 |
