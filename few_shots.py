# few_shots.py

few_shots = [
    {
        'User Question': "Show all t-shirts with their discount percentage",
        'SQL Query': '''
        SELECT t.t_shirt_id, t.brand, t.color, t.size, t.price, d.pct_discount
        FROM t_shirts t
        LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id;
    '''
    },
    {
        'User Question': "How many white color Levis t-shirts?",
        'SQL Query': "SELECT SUM(stock_quantity) FROM t_shirts WHERE color = 'White' AND brand = 'Levi';"
    },

    {
        'User Question': "how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
        'SQL Query': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
        group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
        """
    },

    {
        'User Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?",
        'SQL Query': '''SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
                        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
                        group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id'''
    },

    {
        'User Question': "How much is the total price of the inventory for all S-size t-shirts?",
        'SQL Query': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'"
    }
]
