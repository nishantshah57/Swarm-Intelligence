import numpy as np

class Coupled_Oscillator:
    def __init__(self):
        self.Agents = np.array([])  # Array of 20 Agents
        self.c = np.random.randint(0, 100, size = 20)  # c is an internal counter and T = 100
        self.k = 0.105  # k is a constant between 0 and 1

    def create_Agents(self):
        self.Agents = [0 for _ in range(20)]
        self.Agents = np.array(self.Agents)

    def step(self):
        for i in range(len(self.Agents)):
            try:
                if self.Agents[i-1] == 1 or self.Agents[i+1] == 1:
                    self.c[i] = self.c[i] + self.k * self.c[i]
                else:
                    self.c[i] = self.c[i] + 1
            except IndexError:
                if self.Agents[i-1] == 1 or self.Agents[0] == 1:
                    self.c[i] = self.c[i] + self.k * self.c[i]
                else:
                    self.c[i] = self.c[i] + 1

        for j in range(len(self.c)):
            if self.c[j] >= 100:
                self.Agents[j] = 1
                self.c[j] = 0
            else:
                self.Agents[j] = 0

        return self.Agents

def main():
    count = 0
    execute = Coupled_Oscillator()
    execute.create_Agents()
    while True:
        count += 1
        Agent = execute.step()
        if 1 in execute.Agents:
            print(execute.Agents)
        b = all(map(lambda x: x == 1, Agent))
        if b:
            print("All Agents firing at the same time in {} iterations: \n".format(count), Agent)
            # print(count)
            break

if __name__ == "__main__":
    main()

