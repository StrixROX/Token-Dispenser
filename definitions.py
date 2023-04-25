class MealTimings:
  def __init__(self, is_weekend:bool = False) -> None:
    if is_weekend:
      self.breakfastSlot = ('7:45:00', '11:00:00')
      self.lunchSlot = ('12:15:00', '15:00:00')
      self.dinnerSlot = ('19:45:00', '23:00:00')
    else:
      self.breakfastSlot = ('7:45:00', '10:30:00')
      self.lunchSlot = ('12:15:00', '14:30:00')
      self.dinnerSlot = ('19:45:00', '22:30:00')
    
    self.slots = (self.breakfastSlot, self.lunchSlot, self.dinnerSlot)