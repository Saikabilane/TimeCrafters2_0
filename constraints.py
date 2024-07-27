class Teacher:
    #To check the vacancy of a faculty in a timeslot
    def __init__(self, timeslots):
        self.timeslots = timeslots
        self.status = {slot: 'free' for slot in timeslots.values()}
    
    # Returns the status of the faculty at that timeslot/period -- 'free' or 'occupied'
    # Given a particular timeslot/period as an argument
    def display(self, period):
        if period in self.status:
            return self.status[period]
        else:
            return f'{period} is not a valid period'
        
    # To change the status of the faculty at a timeslot/period to another
    # 'free' to 'occupied' or 'occupied' to 'free'
    def change(self, period, new):
        if period in self.status:
            self.status[period] = new
        else:
            return f'{period} is not a valid period'