-- Brian Halbur - UCI Data Analytics - October 2018 Cohort
-- SQL Homework - using 'sakila' database in MySQL

use sakila;

-- 1a. Display the first and last names of all actors from the table `actor`.
select first_name, last_name from actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column `Actor Name`.
select concat(upper(first_name),' ', upper(last_name)) as Actor_name from actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select actor_id, first_name, last_name from actor where first_name = 'Joe';

-- 2b. Find all actors whose last name contain the letters `GEN`:
select actor_id, first_name, last_name from actor where last_name like '%GEN%';

-- 2c. Find all actors whose last names contain the letters `LI`. This time, order the rows by last name and first name, in that order:
select actor_id, first_name, last_name from actor where last_name like '%LI%' order by last_name, first_name;

-- 2d. Using `IN`, display the `country_id` and `country` columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country from country where country in ('Afghanistan', 'Bangladesh', 'China');

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table `actor` named `description` and use the data type `BLOB` (Make sure to research the type `BLOB`, as the difference between it and `VARCHAR` are significant).
alter table actor
add column description blob;
select * from actor;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the `description` column.
alter table actor
drop column description;
select * from actor;

-- 4a. List the last names of actors, as well as how many actors have that last name.
select last_name, count(*) as num_actors from actor group by last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select last_name, count(*) as num_actors  from actor group by last_name having num_actors > 1;

-- 4c. The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`. Write a query to fix the record.
select * from actor where first_name = 'GROUCHO' and last_name = 'WILLIAMS';
SET SQL_SAFE_UPDATES = 0;
update actor set first_name = 'HARPO' where first_name = 'GROUCHO' and last_name = 'WILLIAMS';

-- 4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the correct name after all! In a single query, if the first name of the actor is currently `HARPO`, change it to `GROUCHO`.
select * from actor where first_name = 'HARPO';
update actor set first_name = 'GROUCHO' where first_name = 'HARPO';
select * from actor where first_name = 'GROUCHO';

-- 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?
 -- Hint: [https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html](https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html)
show create table address;

-- 6a. Use `JOIN` to display the first and last names, as well as the address, of each staff member. Use the tables `staff` and `address`:
select first_name, last_name, address from staff s 
	join address a on (s.address_id = a.address_id);

-- 6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. Use tables `staff` and `payment`.
select first_name, sum(amount) as total_rung_up from payment p 
	join staff s on (p.staff_id = s.staff_id) group by first_name;

-- 6c. List each film and the number of actors who are listed for that film. Use tables `film_actor` and `film`. Use inner join.
select title, count(*) as num_of_actors from film_actor a 
	inner join film f on (a.film_id = f.film_id) group by title;
-- alternate version using nested query
select title, (select count(*) from film_actor where film_id = f.film_id) as num_of_actors from film f;

-- 6d. How many copies of the film `Hunchback Impossible` exist in the inventory system?
select count(*) from inventory where film_id = (
	select film_id from film where title = 'Hunchback Impossible');

-- 6e. Using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer. List the customers alphabetically by last name:
select c.first_name, c.last_name, sum(p.amount) from customer c 
	inner join payment p on (c.customer_id=p.customer_id) 
    group by first_name, last_name 
    order by last_name;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters `K` and `Q` have also soared in popularity. 
-- Use subqueries to display the titles of movies starting with the letters `K` and `Q` whose language is English.
select title from film where title like 'Q%' or title like 'K%' and language_id = 
	(select language_id from language where name='English');

-- 7b. Use subqueries to display all actors who appear in the film `Alone Trip`.
select first_name, last_name from actor where actor_id in (
	select actor_id from film_actor where film_id = 
    (select film_id from film where title = 'Alone Trip'));

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
select c.first_name, c.last_name, c.email, y.country from customer c 
	join address a on (c.address_id = a.address_id)
	join city x on (a.city_id=x.city_id) 
    join country y on (x.country_id=y.country_id) 
    where country = 'Canada';

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as _family_ films.
select title from film where film_id in( 
	select film_id from film_category where category_id = 
    (select category_id from category where name='Family'));

-- 7e. Display the most frequently rented movies in descending order.
select f.title, count(*) as rental_count from rental r 
	join inventory i on (r.inventory_id = i.inventory_id) 
	join film f on (i.film_id = f.film_id) 
    group by f.title 
    order by rental_count desc limit 50;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
select s.store_id, sum(amount) as total_sales from payment p 
	join staff s on (p.staff_id = s.staff_id) 
    group by s.store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
select s.store_id, c.city, ctry.country from store s 
	join address a on (s.address_id = a.address_id) 
	join city c on (a.city_id = c.city_id)
    join country ctry on (c.country_id = ctry.country_id);

-- 7h. List the top five genres in gross revenue in descending order. 
-- (----Hint----: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
select c.name, sum(amount) as gross_revenue from payment p 
	join rental r on p.rental_id = r.rental_id
	join inventory i on r.inventory_id = i.inventory_id
    join film_category f on i.film_id = f.film_id
    join category c on f.category_id = c.category_id
    group by c.name
    order by gross_revenue desc limit 5;
    
-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
-- Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
create view top_5_genres as 
	select c.name, sum(amount) as gross_revenue from payment p 
	join rental r on p.rental_id = r.rental_id
	join inventory i on r.inventory_id = i.inventory_id
    join film_category f on i.film_id = f.film_id
    join category c on f.category_id = c.category_id
    group by c.name
    order by gross_revenue desc limit 5;
    
-- 8b. How would you display the view that you created in 8a?
select * from top_5_genres;

-- 8c. You find that you no longer need the view `top_five_genres`. Write a query to delete it.
drop view top_5_genres;

