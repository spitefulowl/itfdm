class DeliveryTask():
    def __init__(self, size, target_dates, delivery_matrix):
        self.size = size
        self.target_dates = target_dates
        self.delivery_matrix = delivery_matrix

    def __str__(self):
        return f"Delivery task: {self.size}, {self.target_dates}, \n{self.delivery_matrix}"
