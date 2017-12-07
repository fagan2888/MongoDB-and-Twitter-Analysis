<h1 align="center">CS 660 - Introduction to Database Systems<br><br>PA3: NoSQL Databases</h1>

<p align="right">Zuoqi Zhang</p>
<p align="right">U98670811</p>

---

1. Find the restaurant ID of "Caffe Dante".

		> db.restaurants.find({"name": "Caffe Dante"}, {"restaurant_id": 1, "_id": 0})
		{ "restaurant_id" : "40373149" }

2. Find all restaurants whose name has "Ice Cream" in it, return only the restaurant’s ids and names.

		> db.restaurants.find({"name": /.*Ice Cream.*/}, {"restaurant_id": 1, "name": 1, "_id": 0})
		{ "name" : "Taste The Tropics Ice Cream", "restaurant_id" : "40356731" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40360076" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40361322" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40363093" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40363834" }
		{ "name" : "Egger'S Ice Cream Parlor", "restaurant_id" : "40394644" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40550801" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40639953" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40794321" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40814300" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40827606" }
		{ "name" : "Brooklyn Ice Cream Factory", "restaurant_id" : "40853290" }
		{ "name" : "Igloo Ice Cream Cafe", "restaurant_id" : "40865501" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40959012" }
		{ "name" : "Uncle Louie G'S Italian Ices & Ice Cream", "restaurant_id" : "40965048" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40970176" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40972457" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "40973500" }
		{ "name" : "Subway, Carvel Ice Cream", "restaurant_id" : "41001182" }
		{ "name" : "Carvel Ice Cream", "restaurant_id" : "41066646" }
		Type "it" for more

3. Find the names of all restaurants that serve either Italian or American cuisine and are located in the Brooklyn borough.

		> db.restaurants.distinct("name", {"cuisine": {$in: ["Italian", "American"]}, "borough": "Brooklyn"})
		[
		    "Riviera Caterer",
		    "Regina Caterers",
		    "C & C Catering Service",
		    "The Movable Feast",
		    "Mejlander & Mulgannon",
		    ...
		    "Denny'S",
		    "Pair Wine And Cheese",
		    "Aura Bar & Lounge",
		    "Lefeu Lounge5",
		    "Sofia Pizzeria"
		]

4. Return the list of boroughs ranked by the number of American restaurants in it. That is, for each borough, find how many restaurants serve American cuisine and print the borough and the number of such restaurants sorted by this number.

		> db.restaurants.aggregate( [
		...     { $match: { "cuisine": "American" } },
		...     { $group: { _id: "$borough", cnt: { $sum: 1 } } },
		...     { $sort: { cnt: -1 } }
		... ] )
		{ "_id" : "Manhattan", "cnt" : 3205 }
		{ "_id" : "Brooklyn", "cnt" : 1273 }
		{ "_id" : "Queens", "cnt" : 1040 }
		{ "_id" : "Bronx", "cnt" : 411 }
		{ "_id" : "Staten Island", "cnt" : 244 }
		{ "_id" : "Missing", "cnt" : 10 }

5. Find the top 5 American restaurants in Manhattan that have the highest total score. Return for each restaurant the restaurants’ name and the total score. Hint: You can use "$unwind".

		> db.restaurants.aggregate( [
		...     { $unwind: "$grades" },
		...     { $match: { "cuisine": "American", "borough": "Manhattan" } },
		...     { $group: { _id: "$name", total_score: { $sum: "$grades.score" } } },
		...     { $sort: { total_score: -1 } },
		...     { $limit: 5 }
		... ] )
		{ "_id" : "Mcdonald'S", "total_score" : 426 }
		{ "_id" : "Subway", "total_score" : 343 }
		{ "_id" : "Cafe Metro", "total_score" : 315 }
		{ "_id" : "Pret A Manger", "total_score" : 308 }
		{ "_id" : "Guy & Gallard", "total_score" : 290 }

6. Consider a rectangle area on the location field, in which the vertices are [ -74 , 40.5 ] , [ -74 , 40.7 ] , [ -73.5 , 40.5 ] and [ -73.5 , 40.7 ]. Find the number of restaurants in this area that have received a grade score (at least one) more than 50. Hint: Use the $geoWithin and $box.

		> db.restaurants.find( {
		...     "address.coord": { $geoWithin: { $box:  [ [ -74, 40.5 ], [ -73.5, 40.7 ] ] } },
		...     "grades.score": { $gt: 50}
		... } ).count()
		75