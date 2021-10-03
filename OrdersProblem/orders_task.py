class OrdersTask():
    def __init__(self, max_performance, orders_number, labour_intensity, est_profit):
        self.max_performance = max_performance
        self.orders_number = orders_number
        self.labour_intensity = labour_intensity
        self.est_profit = est_profit

    def __str__(self):
        return f"Orders task: {self.max_performance}, {self.orders_number}, {self.labour_intensity}, {self.est_profit}"
