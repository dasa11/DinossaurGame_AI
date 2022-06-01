import pygame
import os
import random
import math
import sys
import neat

#-------- STARTING THE PYGAME --------#
#-------- INICIANDO O PYGAME --------#
pygame.init()


#------------------------------STATISTICS------------------------------------------#
# What we are currently mapping at fetch_stats() function (around line 268).

#Feel free to create your own file with your own parameters at init_stats_file() function (around line 222).

# Right now we are gathering the following parameters:

#   GEN,GAME_SPEED,POINTS,SURVIVAL_THRESHOLD,POPULATION,ACT_FUNC
#   GEN, GAME_SPEED, POINTS and POPULATION we managed to map automatically.

#   SURVIVAL_THRESHOLD and ACT_FUNC (activation function) is hard coded yet, so please 
#   if you changed at config.txt, change the constant bellow 

#SET THE ACT_FUNC THAT WE ARE CURRENTLY USING AND THE SURVIVAL THRESHOLD FOR 
#STATISTICS MEASURES

ACT_FUNC = "tanh"
SURVIVAL_THRESHOLD = 0.1

#----------------------------------------------------------------------------------#

#-------- Setting the screen size--------#
#-------- Configurando o tamanho da tela--------#
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#-------- Setting the images of each dinossour state -------#
#-------- Definindo as imagens de cada estado do dinossauro -------#
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

#-------- Setting the font, BG and obstacles images -------#
#-------- Definindo a fonte, plano de fundo e as imagens de obstáculo -------#
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird3.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)


#-------- Setting the dinossout class-------#
#-------- Definindo a classe dinossauro-------#
class Dinosaur:
    #OBS: The zero point is on the top left and its value increase going down or going right
    #OBS: O marco zero é a ponta de cima a esqueda da tela e seu valor aumenta indo para baixo ou para a direita
    X_POS = 80          # Dino X middle point // Ponto medio do dinossauro em X
    Y_POS = 310         # Dino Y middle point  // Ponto medio do dinossauro em Y
    Y_POS_DUCK = 340    # Dino y middle point when it's in the duck position // Ponto medio em y do dinossauro enquanto está abaixado
    JUMP_VEL = 8.5      # Fall delay // Tempo de queda

    #-------- Starting the Dino-------#
    #-------- Iniciando o dinossauro------#
    def __init__(self, img=RUNNING[0]):
        self.image = img                # Setting the dino actual state image  // Definindo a imagem do estado atual do dinossauro
        self.dino_run = True            # Setting the initial states // Definindo os estados iniciais
        self.dino_jump = False          # Setting the initial states // Definindo os estados iniciais
        self.dino_duck = False          # Setting the initial states // Definindo os estados iniciais
        self.ducking = 0                # Flag to set the ducking state and allow it to jump after it // Flag para definir o estado de "abaixar" e permitir que ele possa pular depois disso
        self.jump_vel = self.JUMP_VEL   # Var to set the jumping time // Variavel para setar o tempo de pulo
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())      # Var used to save the actual dino status // Variavel usada para salvar todos status atuais do dinossauro
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))   # Var to set the square color // Variavel usada para definir a cor do quadrado
        self.step_index = 0             # Var used to make the motion // Variavel usada para fazer animação

    #-------- Update the dino state------#
    #-------- Alterando o estado do dinossauro ------#
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.step_index >= 10:                           # It is used to avoid multiple jumps without touching the ground // Usado para evitar multiplos pulos sem tocar o chao
            self.step_index = 0     
        if self.ducking > 0 and not self.dino_jump:         # Checking if dine is not jumping and if it's in the "ducking time". // Checa se o dinossauro nao esta pulando e esta no tempo de se manter abaixado
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            self.ducking -= 1                               # Flag to control the ducking time // Flag utilizada para controlar o tempo de se manter abaixado
        elif not (self.dino_jump or self.ducking == 10):    # When the dino is not om the ducking time and it's not jumping (change to running state) // Quando o dinossauro nao esta no tempo de se manter abaixado e nao esta pulando (mudar para estado correndo)
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False


    #-------- Ducking State-----#
    #-------- Estado abaixado ------#
    def duck(self):
        self.image = DUCKING[self.step_index // 5]  # Set the ducking image // Definindo a imagem abaixado
        self.step_index += 1                        # Var used to make the dino motion
        self.rect.y = self.Y_POS_DUCK               # Setting the duck state // Definindo o estado de abaixado

    #-------- Jumping State ------#
    #-------- Estado de Pulo------#
    def jump(self):
        self.image = JUMPING                    # Set the jumping image // Definindo a imagem de pulo
        if self.dino_jump:                      # Setting the fall delay after jumping (simulating the gravity) and the jumping height // Definindo o tempo de queda (simulando gravidade) e a altura do pulo
            self.rect.y -= self.jump_vel * 3    # Jumping height // Altura do pulo
            self.jump_vel -= 0.8                # Fall time // Tempo de queda
        if self.jump_vel <= -self.JUMP_VEL:     # Return to the original state after the fall delay // Voltando ao estado original após o tempo de queda
            self.dino_jump = False
            self.dino_run = True
            self.dino_duck = False
            self.jump_vel = self.JUMP_VEL

    #-------- Running state------#
    #-------- Estado correndo ------#
    def run(self):
        self.image = RUNNING[self.step_index // 5]  # Set the running image // Definindo a imagem correndo
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS                    # Going back to the orinal state // Voltando para o estado original
        self.step_index += 1                        # Var used to create the motion // Variavel usada para criar o movimento
        self.dino_jump = False
        self.dino_run = True
        self.dino_duck = False

    #-------- Draw the dino on the screen-----#
    #-------- Desenhando o dinossauro na tela ------#
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))                                                     # Printing dino on the screen // Exibindo o dinossauro na tela
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)  # Printing the square around the dino // Exibindo o quadrado em volta do dinossauro
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2) # Printing the dino vision // Printando a visão do dinossuaro


#-------- Setting the obstacle class-------#
#-------- Definindo a classe obstaculo-------#
class Obstacle:
    def __init__(self, image, number_of_cacti):         # Init the obstacles // Inicia os obstaculos
        self.image = image                              # Setting the imaage // Definindo a imagem
        self.type = number_of_cacti                     # Var used to change the cactus types // Variavel usada para mudar os tipos de cactos
        self.rect = self.image[self.type].get_rect()    # React is used to get some img info like width, height, beging, ending and other infos // React é usado para pegar algumas info da imagem como largura, altura, começo, fim e outras informações
        self.rect.x = SCREEN_WIDTH                      # X is based on the screen size // O x é definido de acordo com o tamanho da tela

    def update(self):                       # It is used to make the objects move // Usado para fazer os objetos se mover
        self.rect.x -= game_speed           # The obstacles move according to the game speed // Os obstaculos se movem de acordo com a velocidade do jogo
        if self.rect.x < -self.rect.width:
            obstacles.pop()                 # Removes the obstacle after it leaves the screen // Remove o obstaculo quando ele sai da tela

    def draw(self, SCREEN):                 # Draw the obstacles // Desenha os obstaculos
        SCREEN.blit(self.image[self.type], self.rect)


#-------- Setting the small cactus class-------#
#-------- Definindo a classe cactos pequeno -------#
class SmallCactus(Obstacle):                        # Obstacle 1 // Obstaculo 1
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)    # To start the class it needs to give the image and the image number // Para iniciar a classe voce precisa passar a imagem e o numero da imagem
        self.rect.y = 340                           # Setting the Y middle point // Definindo o ponto medio em Y da imagem

#-------- Setting the large cactus class-------#
#-------- Definindo a classe cactos grande -------#
class LargeCactus(Obstacle):                # Obstacle 2 // Obstaculo 2
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 320

#-------- Setting the bird class-------#
#-------- Definindo a classe passaro -------#
class Bird(Obstacle):                       # Obstacle 3 // Obstaculo 3
    def __init__(self, image, number_of_cacti):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 245 
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:                                 # It's used to make the bird motion // Usado para criar movimento do passaro
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)   # To print // Para exibir na tela
        self.index += 1


def remove(index):          # Remove the dino after colision // Remove o dinossauro apos a colisão
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b): # Function to calculate the distance between 2 points // Função para calcular a diferença entre 2 pontos
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def init_stats_file():

    #Statistics file name. Change here with you want to create another file
    #Aqui é definido o nome do arquivo
    global STATS_FILE
    STATS_FILE = "stats_ds.csv"

    #Here you create a file if doesn't exists, if it does, do nothing
    try:
        f = open(STATS_FILE, "x")
        f.write("GEN,GAME_SPEED,POINTS,SURVIVAL_THRESHOLD,POPULATION,ACT_FUNC")
        f.close()
    except:
        pass


#-------- Setting the game and AI------#
#-------- Definindo o jogo e a IA-------#
def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    clock = pygame.time.Clock()     # Game time // Tempo do jogo
    points = 0                      # Initial points // Ponto inicial

    obstacles = []      # Obstacles List // Lista de obstáculos
    dinosaurs = []      # Dino List // Lista de dinossauros
    ge = []             # Genome List // Lista de genomas
    nets = []           # Gen nest List // Lista de redes de genomas 

    x_pos_bg = 0        # Horizontal BG Start // Começo do background na horizontal
    y_pos_bg = 20       # Vertical BG Start // Inicio do background na vertical
    game_speed = 20     # Initial game speed // Velocidade inicial do jogo

    for genome_id, genome in genomes:   # Starting all the dinos with the genomes // Iniciar todos os dinossauros com todos os genmas
        dinosaurs.append(Dinosaur())    # Inserting dino into the dino list // Inserindo dinossauro na lista de dinossauros
        genome.fitness = 0              # Setting the initial dino fitness genome as zero // Definindo a eficiencia do genoma inicial como zero 
        ge.append(genome)               # Inserting dino genome into the genome list // Inserindo genoma na lista de genomas
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Creating the dino neural network // Criando a rede neural do dinossauro 
        nets.append(net)                # Inserting the neural network into the neural networks list // Inserindo a rede neural na lista de redes neurais
        

    def score():                        # Set and update the score and update game speed // Define e atualiza a pontuação e atualiza a velocidade do jogo 
        global points, game_speed
        points += 1                     # Increasing the poits // Aumentando a pontuação
        if points % 100 == 0:
            game_speed += 1             # Increase the game speed for each 100 points // Aumenta a velocidade do jogo a cada 100 pontos
        text = FONT.render(f'Points:  {str(points)}', True, (0, 0, 0))  # Saving the score into a var // Salvando a pontuação na variavel
        SCREEN.blit(text, (950, 50))                                    #Printing the score in the selected position on the screen // Imprimindo a pontuação na posição desejada da tela

    def statistics():                                                                       # Function to print the game statistics // Função para exibir as estatisticas do jogo
        global dinosaurs, game_speed, ge
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))   # Alive Dinos // Dinossauros vivos
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))           # Dino's generation // Geracão dos dinossauros
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))            # Game speed // Velocidade do jogo

        SCREEN.blit(text_1, (50, 450))  # Printing the info // Imprimindo as informações
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))

    def fetch_stats(file):
        f = open(file, "a")
        f.write("\n" + str(pop.generation+1) + "," + str(game_speed) + "," + str(points) + "," 
        + str(SURVIVAL_THRESHOLD) + "," + str(len(pop.population)) + "," + ACT_FUNC)
        f.close()

    def background():                                           # Set the backgound // Define o plano de fundo
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:                              # Game looping // Looping do jogo
        for event in pygame.event.get():    # X action to close the game // Ação do X para fechar o jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))        # Set the screen with white collor // Define a tela como cor branca

        for dinosaur in dinosaurs:          # Update the dinos // Atualiza os dinossauros
            dinosaur.update()
            dinosaur.draw(SCREEN)

        if len(dinosaurs) == 0:             # Reset the game if all dinos are dead // Reseta o jogo se todos os dinossauros estiverrem mortos
            fetch_stats(STATS_FILE)
            break

        if len(obstacles) == 0:                                                     # Creating the obstacles // Cria os obstáculos
            rand_int = random.randint(0, 2)
            if rand_int == 0:                                                       # Getting the random value to spawn the obstacle // Pega o valor aleatorio para gerar o obstaculo
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            elif rand_int == 2:
                obstacles.append(Bird(BIRD, random.randint(0, 2)))

        for obstacle in obstacles:                              # Check if any colision has happened // Checa se alguma colisão aconteceu
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):    # Check if there is any dino with the same position as an obstacle, in other words, colision // Checa se exite algum dinossauro com mesma posição de um obstaculo, ou seja, uma colisão
                    ge[i].fitness -= 1                          # Subtract 1 from the neural network // Subtrai um da rede neural
                    remove(i)                                   # Remove the dino // Remove o dinossauro

        for i, dinosaur in enumerate(dinosaurs):                # The neural network result for each dino // Resposta de cada rede neural para cada dinossauro
            output = nets[i].activate((dinosaur.rect.y, distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop), obstacle.rect.y, obstacle.rect.height))                                                             # 1 output with 4 inputs // Uma saida para 4 entradas
            output1 = nets[i].activate((dinosaur.rect.y, distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop),distance((dinosaur.rect.x, dinosaur.rect.y),(obstacle.rect.x, obstacle.rect.height)), game_speed))  # 1 output with 5 inputs // Uma saida para 5 entradas
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS: # Deciede if it (dino) is going to jump based on the neural network // Decide se ele (dinossauro) vai pular baseado na rede neural
                dinosaur.dino_jump = True
                dinosaur.dino_run = False
                dinosaur.dino_duck = False
                ge[i].fitness += 6
            if output1[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS and dinosaur.dino_jump == False: # Deciede if it (dino) is going to duck based on the neural network // Decide se ele (dinossauro) vai abaixar baseado na rede neural
                dinosaur.dino_jump = False
                dinosaur.dino_run = False
                dinosaur.dino_duck = True
                dinosaur.ducking = 15
                ge[i].fitness += 6


        statistics()
        score()
        background()
        clock.tick(30)
        pygame.display.update()


#-------- Setting the NEAT Neural Network ------#
#-------- Definindo a rede de redes neurais ------#
def run(config_path):               # Starting the neural network // Iniciando a rede neural
    global pop
    config = neat.config.Config(    # Neat config comming from the condig.txt (Each config is explained on the readMe file) // Configuração da rede vindo do arquivo config.txt (Cada confiruação está explicada no arquivo readMe)
        neat.DefaultGenome,         
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(eval_genomes, 50)


if __name__ == '__main__':                              # Starting the main // Iniciando a main
    local_dir = os.path.dirname(__file__)               # File path (main) // Caminho do arquivo (main)
    config_path = os.path.join(local_dir, 'config.txt') # Join with the config.txt // Junta com o config.txt
    
    init_stats_file()
    
    run(config_path)                                    # Run with config.txt // Execute com o config.txt
