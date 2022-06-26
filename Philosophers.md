# Parallel Philosophers Project

In my Parallism and Concurrency class I worked on a project with a few other teammates.

## Problem Statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can only eat spaghetti when they have both left and right forks. Each fork can be held by only one philosopher and so a philosopher can use the fork only if it is not being used by another philosopher. After an individual philosopher finishes eating, they need to put down both forks so that the forks become available to others. A philosopher can only take the fork on their right or the one on their left as they become available and they cannot start eating before getting both forks.

Eating is not limited by the remaining amounts of spaghetti or stomach space; an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm) such that no philosopher will starve; i.e., each can forever continue to alternate between eating and thinking, assuming that no philosopher can know when others may want to eat or think.

## Our Solution
```python
# James Hall
# Joshua Capron
# Matthew James



"""
Course: CSE 251
Lesson Week: 09
File: team1.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat
"""


import time
import threading
import random


class EndState:
  def __init__(self,num_meals,lock):
    self.num_meals_left = num_meals
    self.lock=lock
PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5
class Philosopher(threading.Thread):
  def __init__(self, id,left_fork,right_fork,end_state):
    super().__init__()
    self.id = id
    self.left_fork=left_fork
    self.right_fork=right_fork
    self.end_state=end_state
  def dining(self):
    if not (self.left_fork.locked() or self.right_fork.locked()):
      self.end_state.num_meals_left-=1
      self.left_fork.acquire()
      self.right_fork.acquire()
      self.end_state.lock.release()
      print(f"Philosopher {self.id} starts to eat.\n", end="")
      time.sleep(random.uniform(1, 3) / 1000)
      print(f"Philosopher {self.id} finishes eating and leaves to think.\n", end="")
      self.left_fork.release()
      self.right_fork.release()
    else:
      self.end_state.lock.release()
 
  def run(self):
    while True:
      self.end_state.lock.acquire()
      if self.end_state.num_meals_left==0:
        self.end_state.lock.release()
        break
      else:
        self.dining()
        self.thinking()


  def thinking(self):
    time.sleep(random.uniform(1, 3) / 1000)

def main():
  # TODO - create the forks
  # TODO - create PHILOSOPHERS philosophers
  # TODO - Start them eating and thinking
  # TODO - Display how many times each philosopher ate
  forks = []
  end_state = EndState(MAX_MEALS,threading.Lock())
  for _ in range(PHILOSOPHERS):
    forks.append(threading.Lock())
  philosophers = []
  for i in range(PHILOSOPHERS):
    philosophers.append(Philosopher(i,forks[i-1],forks[i],end_state))
  for ph in philosophers:
    ph.start()
  for ph in philosophers:
    ph.join()

if __name__ == '__main__':
    main()

```

Now the code works overall, although there is no particular reason any given philosopher will always be fed, although all of the philosophers should be fed the same amount. The particular reason I wanted to revise this is because I despise the code in the following functions
```python

  def dining(self):
    if not (self.left_fork.locked() or self.right_fork.locked()):
      self.end_state.num_meals_left-=1
      self.left_fork.acquire()
      self.right_fork.acquire()
      self.end_state.lock.release()
      print(f"Philosopher {self.id} starts to eat.\n", end="")
      time.sleep(random.uniform(1, 3) / 1000)
      print(f"Philosopher {self.id} finishes eating and leaves to think.\n", end="")
      self.left_fork.release()
      self.right_fork.release()
    else:
      self.end_state.lock.release()
 
  def run(self):
    while True:
      self.end_state.lock.acquire()
      if self.end_state.num_meals_left==0:
        self.end_state.lock.release()
        break
      else:
        self.dining()
        self.thinking()
```

For one thing, why are we acquiring a lock in the run method and releasing it in the dining method? The dining method, for instance, should be as follows:
```python

  def dining(self):
    if self.pickUpForksAndMeal():
      self.eat()
      self.dropForks()
```
This is clear and simple: if we are able to get the forks and a meal, we eat and then drop our forks.
Of course, this requires three new functions:
```python
  def pickUpForksAndMeal(self):
    # locking meals will prevent philosophers from fighting over forks
    with self.meals.lock:
        if meals.hasNext() and not (self.left_fork.locked() or self.right_fork.locked()):
            meals.getNext()
            left_fork.acquire()
            right_fork.acquire()
    
  def eat(self):
    # From the original dining function: just in a different place
    print(f"Philosopher {self.id} starts to eat.\n", end="")
    time.sleep(random.uniform(1, 3) / 1000)
    print(f"Philosopher {self.id} finishes eating and leaves to think.\n", end="")

  def dropForks(self):
    left_fork.release()
    right_fork.release()
```
And this requires a different class definition for EndState
```python
# more intuitive name
class Meals:
  def __init__(self,num_meals,lock):
    self.num_meals_left = num_meals
    self.lock=lock
  
  def getNext():
    num_meals_left-=1

  def hasNext():
    return num_meals_left>0

```
And a small rewriting of the init and run methods
```python
  def __init__(self, id,left_fork,right_fork,meals):
    # only change is to meals
    super().__init__()
    self.id = id
    self.left_fork=left_fork
    self.right_fork=right_fork
    self.meals=meals

  def run(self):
    # only change is to end_state or meals
    while meals.hasNext():
        self.dining()
        self.thinking()
```

Attempting to put my changes into practice, I found a the following errors:
1. Failed to mark __self__ in many places
2. Required an additional change in Main
3. Failed to return True or False in pickUpForksAndMeal

My cleaned code solution can be found here.
[Philosophers.py](Philosophers.py)