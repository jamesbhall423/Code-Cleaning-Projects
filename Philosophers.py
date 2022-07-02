
import time
import threading
import random


PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5

class Meals:
  def __init__(self,num_meals,lock):
    self.num_meals_left = num_meals
    self.lock=lock
  
  def getNext(self):
    self.num_meals_left-=1

  def hasNext(self):
    return self.num_meals_left>0
class Philosopher(threading.Thread):
  def __init__(self, id,left_fork,right_fork,meals):
    super().__init__()
    self.id = id
    self.left_fork=left_fork
    self.right_fork=right_fork
    self.meals=meals
  def dining(self):
    if self.pickUpForksAndMeal():
      self.eat()
      self.dropForks()
 
  def run(self):
    while self.meals.hasNext():
        self.dining()
        self.thinking()


  def thinking(self):
    time.sleep(random.uniform(1, 3) / 1000)
  
  def pickUpForksAndMeal(self):
    # locking meals will prevent philosophers from fighting over forks
    with self.meals.lock:
        if self.meals.hasNext() and not (self.left_fork.locked() or self.right_fork.locked()):
            self.meals.getNext()
            self.left_fork.acquire()
            self.right_fork.acquire()
            return True
    return False
    
  def eat(self):
    # From the original dining function: just in a different place
    print(f"Philosopher {self.id} starts to eat.\n", end="")
    time.sleep(random.uniform(1, 3) / 1000)
    print(f"Philosopher {self.id} finishes eating and leaves to think.\n", end="")

  def dropForks(self):
    self.left_fork.release()
    self.right_fork.release()

def main():
  # TODO - create the forks
  # TODO - create PHILOSOPHERS philosophers
  # TODO - Start them eating and thinking
  # TODO - Display how many times each philosopher ate
  forks = []
  meals = Meals(MAX_MEALS,threading.Lock())
  for _ in range(PHILOSOPHERS):
    forks.append(threading.Lock())
  philosophers = []
  for i in range(PHILOSOPHERS):
    philosophers.append(Philosopher(i,forks[i-1],forks[i],meals))
  for ph in philosophers:
    ph.start()
  for ph in philosophers:
    ph.join()

if __name__ == '__main__':
    main()
