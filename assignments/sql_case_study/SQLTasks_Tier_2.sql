/* Welcome to the SQL mini project. You will carry out this project partly in
the PHPMyAdmin interface, and partly in Jupyter via a Python connection.

This is Tier 2 of the case study, which means that there'll be less guidance for you about how to setup
your local SQLite connection in PART 2 of the case study. This will make the case study more challenging for you: 
you might need to do some digging, aand revise the Working with Relational Databases in Python chapter in the previous resource.

Otherwise, the questions in the case study are exactly the same as with Tier 1. 

PART 1: PHPMyAdmin
You will complete questions 1-9 below in the PHPMyAdmin interface. 
Log in by pasting the following URL into your browser, and
using the following Username and Password:

URL: https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

In this case study, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */


/* QUESTIONS 
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */
SELECT name
FROM Facilities
WHERE membercost =0

A) Badminton Court, Table Tennis, Snooker Table,Pool Table

/* Q2: How many facilities do not charge a fee to members? */
SELECT COUNT( name )
FROM Facilities
WHERE membercost =0
A) 4

/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */
SELECT facid, name, membercost, monthlymaintenance
FROM Facilities
WHERE membercost >0
AND membercost < ( .2 * monthlymaintenance )


facid	name	membercost	monthlymaintenance	
0	Tennis Court 1	5.0	200
1	Tennis Court 2	5.0	200
4	Massage Room 1	9.9	3000
5	Massage Room 2	9.9	3000
6	Squash Court	3.5	80

/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */
SELECT *	
FROM Facilities
WHERE facid % 2 = 1 AND NOT facid = 3 AND facid <6


facid	name	membercost	guestcost	initialoutlay	monthlymaintenance	
1	Tennis Court 2	5.0	25.0	8000	200
5	Massage Room 2	9.9	80.0	4000	3000

/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */
SELECT name, monthlymaintenance,
	CASE WHEN monthlymaintenance > 100 THEN 'expensive'
		ELSE 'cheap' END AS cost
FROM Facilities


name	monthlymaintenance	cost	
Tennis Court 1	200	expensive
Tennis Court 2	200	expensive
Badminton Court	50	cheap
Table Tennis	10	cheap
Massage Room 1	3000	expensive
Massage Room 2	3000	expensive
Squash Court	80	cheap
Snooker Table	15	cheap
Pool Table	15	cheap

/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */
SELECT memid, surname, firstname
FROM `Members`
WHERE memid = (
SELECT MAX( memid )
FROM Members )


memid	surname	firstname	
37	Smith	Darren

/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */
SELECT DISTINCT CONCAT(m.firstname,' ',m.surname) AS membername, f.name AS facilityname
	FROM Bookings AS b
     LEFT JOIN Facilities AS f
	ON b.facid = f.facid
     LEFT JOIN Members AS m
	ON b.memid = m.memid
WHERE b.facid = 0 OR b.facid = 1
ORDER BY membername

membername	facilityname	
Anne Baker	Tennis Court 2
Anne Baker	Tennis Court 1
Burton Tracy	Tennis Court 1
Burton Tracy	Tennis Court 2
Charles Owen	Tennis Court 2
Charles Owen	Tennis Court 1
Darren Smith	Tennis Court 2
David Farrell	Tennis Court 1
David Farrell	Tennis Court 2
David Jones	Tennis Court 2
David Jones	Tennis Court 1
David Pinker	Tennis Court 1
Douglas Jones	Tennis Court 1
Erica Crumpet	Tennis Court 1
Florence Bader	Tennis Court 2
Florence Bader	Tennis Court 1
Gerald Butters	Tennis Court 1
Gerald Butters	Tennis Court 2
GUEST GUEST	Tennis Court 2
GUEST GUEST	Tennis Court 1
Henrietta Rumney	Tennis Court 2
Jack Smith	Tennis Court 2
Jack Smith	Tennis Court 1
Janice Joplette	Tennis Court 1
Janice Joplette	Tennis Court 2
Jemima Farrell	Tennis Court 2
Jemima Farrell	Tennis Court 1
Joan Coplin	Tennis Court 1
John Hunt	Tennis Court 1
John Hunt	Tennis Court 2

/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */
SELECT b.bookid,
	   f.name, 
	   CONCAT(m.firstname,' ',m.surname) AS membername,
	   CASE WHEN b.memid = 0 THEN (slots * guestcost)
	   ELSE (slots * membercost) END AS cost
FROM Bookings AS b
LEFT JOIN Facilities AS f
ON b.facid = f.facid
LEFT JOIN Members AS m
ON b.memid = m.memid
WHERE starttime LIKE '2012-09-14%'
AND ((((slots * membercost) > 30) AND b.memid > 0) 
OR ((slots * guestcost) > 30 AND b.memid = 0))
ORDER BY cost DESC


bookid	name	membername	cost	
2946	Massage Room 2	GUEST GUEST	320.0
2937	Massage Room 1	GUEST GUEST	160.0
2940	Massage Room 1	GUEST GUEST	160.0
2942	Massage Room 1	GUEST GUEST	160.0
2926	Tennis Court 2	GUEST GUEST	150.0
2922	Tennis Court 1	GUEST GUEST	75.0
2920	Tennis Court 1	GUEST GUEST	75.0
2925	Tennis Court 2	GUEST GUEST	75.0
2948	Squash Court	GUEST GUEST	70.0
2941	Massage Room 1	Jemima Farrell	39.6
2949	Squash Court	GUEST GUEST	35.0
2951	Squash Court	GUEST GUEST	35.0

/* Q9: This time, produce the same result as in Q8, but using a subquery. */
SELECT b.bookid,
		f.name, 
		CONCAT(m.firstname,' ',m.surname) AS membername,
		CASE WHEN b.memid = 0 THEN (slots * guestcost)
    	ELSE (slots * membercost) END AS cost
FROM Bookings AS b
LEFT JOIN Facilities AS f
ON b.facid = f.facid
LEFT JOIN Members AS m
ON b.memid = m.memid
WHERE b.bookid IN (
    SELECT bookid
	FROM Bookings AS b
	LEFT JOIN Facilities AS f
	ON b.facid = f.facid
	WHERE b.starttime LIKE "2012-09-14%"
	AND ((b.memid = 0 AND (slots * guestcost) > 30) OR 	 (b.memid > 0 AND (slots * membercost) > 30)))
ORDER BY cost DESC

bookid	name	membername	cost	
2946	Massage Room 2	GUEST GUEST	320.0
2940	Massage Room 1	GUEST GUEST	160.0
2942	Massage Room 1	GUEST GUEST	160.0
2937	Massage Room 1	GUEST GUEST	160.0
2926	Tennis Court 2	GUEST GUEST	150.0
2920	Tennis Court 1	GUEST GUEST	75.0
2925	Tennis Court 2	GUEST GUEST	75.0
2922	Tennis Court 1	GUEST GUEST	75.0
2948	Squash Court	GUEST GUEST	70.0
2941	Massage Room 1	Jemima Farrell	39.6
2951	Squash Court	GUEST GUEST	35.0
2949	Squash Court	GUEST GUEST	35.0

/* PART 2: SQLite

Export the country club data from PHPMyAdmin, and connect to a local SQLite instance from Jupyter notebook 
for the following questions.  

QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */
SELECT f.name, 
		SUM(CASE WHEN b.memid = 0 THEN (slots * guestcost) 
		ELSE (slots * membercost) END) AS cost 
FROM Bookings AS b 
LEFT JOIN Facilities AS f 
ON b.facid = f.facid 
LEFT JOIN Members AS m 
ON b.memid = m.memid 
GROUP BY b.facid HAVING cost < 1000

('Table Tennis', 180), ('Snooker Table', 240), ('Pool Table', 270)

/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */
SELECT m.memid, 
	   (m.surname|| ' '|| m.firstname) AS membername, 
	   (m2.surname || ' ' ||m2.firstname) AS recommender
FROM Members AS m 
LEFT JOIN Members AS m2 
ON m.recommendedby = m2.memid
ORDER BY membername

memid	membername	recommender
15	Bader Florence	Stibbons Ponder
12	Baker Anne	Stibbons Ponder
16	Baker Timothy	Farrell Jemima
8	Boothe Tim	Rownam Tim
5	Butters Gerald	Smith Darren
22	Coplin Joan	Baker Timothy
36	Crumpet Erica	Smith Tracy
7	Dare Nancy	Joplette Janice
28	Farrell David	
13	Farrell Jemima	
0	GUEST GUEST	
20	Genting Matthew	Butters Gerald
35	Hunt John	Purview Millicent
11	Jones David	Joplette Janice
26	Jones Douglas	Jones David
4	Joplette Janice	Smith Darren
21	Mackenzie Anna	Smith Darren
10	Owen Charles	Smith Darren
17	Pinker David	Farrell Jemima
30	Purview Millicent	Smith Tracy
3	Rownam Tim	
27	Rumney Henrietta	Genting Matthew
24	Sarwin Ramnaresh	Bader Florence
1	Smith Darren	
37	Smith Darren	
14	Smith Jack	Smith Darren
2	Smith Tracy	
9	Stibbons Ponder	Tracy Burton
6	Tracy Burton	
33	Tupperware Hyacinth	
29	Worthington-Smyth Henry	Smith Tracy

/* Q12: Find the facilities with their usage by member, but not guests */
SELECT f.name, SUM(b.slots) AS totalmemberslots
FROM Facilities AS f
LEFT JOIN Bookings AS b
ON f.facid = b.facid
WHERE b.memid > 0
GROUP BY f.name
ORDER BY bookid

name	totalmemberslots
Table Tennis	794
Massage Room 1	884
Snooker Table	860
Pool Table	856
Tennis Court 1	957
Squash Court	418
Badminton Court	1086
Tennis Court 2	882
Massage Room 2	54

/* Q13: Find the facilities usage by month, but not guests */
SELECT f.name, strftime("%Y-%m", b.starttime) AS year_month, SUM(b.slots) AS totalmemberslots
FROM Facilities AS f
LEFT JOIN Bookings AS b
ON f.facid = b.facid
WHERE b.memid > 0
GROUP BY f.name, strftime("%Y-%m", b.starttime)
ORDER BY bookid

name	year_month	totalmemberslots
Table Tennis	2012-07	98
Massage Room 1	2012-07	166
Snooker Table	2012-07	140
Pool Table	2012-07	110
Tennis Court 1	2012-07	201
Squash Court	2012-07	50
Badminton Court	2012-07	165
Tennis Court 2	2012-07	123
Massage Room 2	2012-07	8
Tennis Court 1	2012-08	339
Tennis Court 2	2012-08	345
Badminton Court	2012-08	414
Table Tennis	2012-08	296
Massage Room 1	2012-08	316
Massage Room 2	2012-08	18
Squash Court	2012-08	184
Snooker Table	2012-08	316
Pool Table	2012-08	303
Tennis Court 1	2012-09	417
Tennis Court 2	2012-09	414
Badminton Court	2012-09	507
Table Tennis	2012-09	400
Massage Room 1	2012-09	402
Massage Room 2	2012-09	28
Squash Court	2012-09	184
Snooker Table	2012-09	404
Pool Table	2012-09	443
