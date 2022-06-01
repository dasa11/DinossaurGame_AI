# Objectives

Implement an A.I. to play and learn how to play the dinosour game

  
---

# Details

## Pygame
Pygame is a set of python modules designed for writting games.
We decided to use it because it can run on almost all operating system.

---
# Dependences
## Instalation for Ubuntu Users
- Install pygame: python3 -m pip install -U pygame --user
- Install neat: pip install neat-python

## Instalation for Windows Users
- Install pygame: pip install pygame
- Install neat: pip install neat-python
  
---
# Config.txt
## NEAT 
- Fitness criterion // Criterio do Fitness
```
fitness_criterion = min
```

- Fitness threshold // Fitness máximo
```
fitness_threshold = 1000
```

- Population size of each generation // Tamanho da população de cada geração
```
pop_size = 100
```

- If each generation wants to create new weight on the neural network // Se cada geração deseja criar novos pesoas na rede neural
```
reset_on_extinction = False
```


## DefaultGenome
\# node activation options

- Type of the function // Tipo da função
```
activation_default = tanh
```

- Function mutation rate // Taxa de mutação da função
```
activation_mutate_rate = 0.0
```

- Function to the mutation // Função para mutação
```
activation_options = tanh
```

  

## node aggregation options // Opções de agregação de nós
- What to do in each neuron evaluation // O que fazer em cada conta do neuronio
```
aggregation_default = sum
```

- Function mutation rate // Taxa de mutação da função
```
aggregation_mutate_rate = 0.0
```

- Function to the mutation // Função para mutação
```
aggregation_options = sum 
```
  

## node bias options // Opções de propensão de nós
- Bias initial mean // Propensão média inicial
```
bias_init_mean = 0.0
```

- Bias initial standard deviation // Propensão de desvio padrão
```
bias_init_stdev = 1.0
```

- Bias max value // Propensão máxima
```
bias_max_value = 30.0
``` 

- Bias min value // Propensão mínima
```
bias_min_value = -30.0
```

- bias mutate power // Porcentagem de mudança de propensão
```
bias_mutate_power = 0.5 
```

- Percentage of mutation rate // Porcentagem de acontecer uma mutação
```
bias_mutate_rate = 0.7
```

- Percentage of start a new bias // Porcentagem de inciar uma nova propensão
```
bias_replace_rate = 0.1
```
  

## genome compatibility options
- Configuration that defines if a dino belongs to that species // Configuração que define se um dinossauro faz parte daquela espécie
```
compatibility_disjoint_coefficient = 1.0
```

- Compatibility weight coefficient // Coeficiente de peso de compatibilidade
```
compatibility_weight_coefficient = 0.5
```
  

## connection add/remove rates
- adding conection percentage // Porcentagem de adicionar uma conexão
```
conn_add_prob = 0.5
```

- Removing conection percentage // Porcentagem de remover uma conexão
```
conn_delete_prob = 0.5
```
  

## connection enable options
- Enable connection // Habilitar conexão
```
enabled_default = True
```

- Mutate rate // Taxa de mutação
```
enabled_mutate_rate = 0.01
```

- Foward the previous node // Para passar o node anterior para frente
```
feed_forward = True
```

- To start with everybody connected // Começar com todos conectados
```
initial_connection = full
```


## node add/remove rates
- Probability to create a new node // Probabilidade de se criar um novo nó
```
node_add_prob = 0.2
```

- Probability to remove a node // Probabilidade de se remover um nó
```
node_delete_prob = 0.2
```
  

## network parameters
- Number of middle neurons // Numeros de neuronios intermediarios
```
num_hidden = 0
```

- Number of inputs // Numero de entradas
```
num_inputs = 3
```

- Number of outputs // Numero de saídas
```
num_outputs = 2
```
  

## node response options // Pesoas nos nós
- Weights average // Média dos pesos
```
response_init_mean = 1.0
```

- Initial standard deviation // Desvio padrão inicial
``` 
response_init_stdev = 0.0
```

- Max value // Peso máximo
```
response_max_value = 30.0
```

- Min value // Peso mínimo 
```
response_min_value = -30.0 
```

- Final value percentage after mutation // Porcentagem do valor final após a mutação
```
response_mutate_power = 0.0 # PORCENTAGEM DE VALOR FINAL APÓS A MUTAÇÃO
```

- Mutate rate // Taxa de mutação
```
response_mutate_rate = 0.0
```

- Percentage of start a new weight // Porcentagem de inciar um novo peso
```
response_replace_rate = 0.0
```
  

## Connection weight options // Peso das conexões
- Weight initial mean // Média inicial dos pesos
```
weight_init_mean = 0.0
```

- Weight initial standard deviation // Peso do desvio padrão inicial
```
weight_init_stdev = 1.0
```

- Max weight // Peso máximo
```
weight_max_value = 30
```

- Min weight // Peso mínimo
```
weight_min_value = -30
```

- Final value percentage after mutation // Porcentagem do valor final após a mutação
```
weight_mutate_power = 0.5
```

- Mutate rate // Taxa de mutação
```
weight_mutate_rate = 0.8 
```

- Percentage of start a new weight // Porcentagem de inciar um novo peso
```
weight_replace_rate = 0.1
```


## DefaultSpeciesSet
- Compatibility threshold of the specie // Limite de compatibilidade da espécie
```
compatibility_threshold = 3.0
```
  

## DefaultStagnation
- Species fitness function 
```
species_fitness_func = max
```

- Max number of stagnation species // Numero máximo de espécies que não evoluem em relação a antetior
```
max_stagnation = 20
```

- Min species number to be consider // Número minimo de espécies para serem levadas em consideração
```
species_elitism = 2
```


## DefaultReproduction
- Min number of specimen that can be coppied to the next generation // Número mínimo de indivíduos que podem ser copiados na proxima geração
```
elitism = 2
```

- Max percentage of speciman that can go to the next generation // Porcentagem minima de indivíduos que podem passar para proxima geração
```
survival_threshold = 0.2
```

# Statistics

To gather data from the application, the file main.py write into a file named stats_ds.txt. In this data file, it's possible to anylise some interesting variables, as the activation function, survival threshold, points accomplished at the end of each generation and so on. 

If you want to, you can change some settings on the file config.txt in order to anylise another dinossaur behavior. We just asked you that, after you do this, is important to check if you need to change the same information at the main.py file under section statistics, because this will provide you a correct measurement and storage of your data in the file stats_ds.txt.

What we are mapping about statistics is at the beginnig of the file main.py under section statistics.

- Right now we are gathering the following parameters:

  -  GEN,GAME_SPEED,POINTS,SURVIVAL_THRESHOLD,POPULATION,ACT_FUNC