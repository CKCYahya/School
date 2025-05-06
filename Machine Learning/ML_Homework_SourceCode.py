from PIL import Image
import random
import matplotlib.pyplot as plt

# Load and convert the image to grayscale
def load_image(image_path, size=(300, 300)):
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    resized_image = image.resize(size)  # Resize for manageability
    resized_image.save("C:/Users/User/Desktop/ML/resized_image.jpeg")  # Save resized image
    return resized_image

# Split image into tiles and save them
def split_image(image, matrix_size=3):
    tile_width = image.width // matrix_size
    tile_height = image.height // matrix_size
    tiles = [
        image.crop((j * tile_width, i * tile_height, (j + 1) * tile_width, (i + 1) * tile_height))
        for i in range(matrix_size) for j in range(matrix_size)
    ]
    for idx, tile in enumerate(tiles):
        tile.save(f"C:/Users/User/Desktop/ML/tile_{idx + 1}.jpeg")  # Save each tile
    return tiles, tile_width, tile_height

# Fitness function
def calculate_fitness(individual, original_tiles):
    correct_tiles = sum(1 for ind_tile, orig_tile in zip(individual, original_tiles) if ind_tile == orig_tile)
    return correct_tiles / len(original_tiles)

# Uniform crossover
def uniform_crossover(parent1, parent2):
    offspring1, offspring2 = [], []
    for gene1, gene2 in zip(parent1, parent2):
        if random.random() < 0.5:
            offspring1.append(gene1)
            offspring2.append(gene2)
        else:
            offspring1.append(gene2)
            offspring2.append(gene1)
    return offspring1, offspring2

# Swap mutation
def swap_mutation(individual, mutation_rate):
    mutated = individual.copy()
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated

# Combine tiles into a full image
def combine_image(individual, tile_width, tile_height, image_size):
    combined_image = Image.new('L', image_size)
    for i, tile in enumerate(individual):
        x_offset = (i % 3) * tile_width
        y_offset = (i // 3) * tile_height
        combined_image.paste(tile, (x_offset, y_offset))
    return combined_image

# Create the next generation
def create_next_generation(elite_individuals, population_size, mutation_rate):
    next_generation = [individual for individual, _ in elite_individuals]
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample([ind for ind, _ in elite_individuals], 2)
        offspring1, offspring2 = uniform_crossover(parent1, parent2)
        offspring1 = swap_mutation(offspring1, mutation_rate)
        offspring2 = swap_mutation(offspring2, mutation_rate)
        next_generation.append(offspring1)
        if len(next_generation) < population_size:
            next_generation.append(offspring2)
    return next_generation

# Plot and save fitness evolution
def plot_fitness_evolution(generations, fitness_values):
    plt.figure(figsize=(10, 6))
    plt.plot(generations, fitness_values, marker='o', linestyle='-', label='Best Fitness')
    plt.title("Fitness Evolution Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.legend()
    plt.grid()
    plt.savefig("C:/Users/User/Desktop/ML/fitness_evolution.png")
    plt.show()

# Main genetic algorithm
def genetic_algorithm(image_path, matrix_size=3, population_size=20, mutation_rate=0.2, max_no_improvement=50):
    resized_image = load_image(image_path)
    original_tiles, tile_width, tile_height = split_image(resized_image, matrix_size)
    current_population = [random.sample(original_tiles, len(original_tiles)) for _ in range(population_size)]
    generation = 0
    best_fitness = 0
    no_improvement_generations = 0
    fitness_values = []
    generations = []

    while best_fitness < 1.0:  # Continue until perfect match
        generation += 1
        fitness_scores = [calculate_fitness(ind, original_tiles) for ind in current_population]
        population_with_fitness = list(zip(current_population, fitness_scores))
        sorted_population = sorted(population_with_fitness, key=lambda x: x[1], reverse=True)

        # Record fitness evolution
        current_best_fitness = sorted_population[0][1]
        fitness_values.append(current_best_fitness)
        generations.append(generation)


        # Save improved solutions
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            no_improvement_generations = 0
            best_individual = sorted_population[0][0]
            combined_image = combine_image(best_individual, tile_width, tile_height, resized_image.size)
            combined_image.save(f"C:/Users/User/Desktop/ML/improved_gen_{generation}_fitness_{best_fitness:.2f}.jpeg")


        else:
            no_improvement_generations += 1

        # Reinitialize if no improvement for too long
        if no_improvement_generations >= max_no_improvement:
            print("Reinitializing population...")
            current_population = [random.sample(original_tiles, len(original_tiles)) for _ in range(population_size)]
            no_improvement_generations = 0
            continue

        # Create the next generation
        elite_individuals = sorted_population[:2]
        current_population = create_next_generation(elite_individuals, population_size, mutation_rate)

    # Save the best individual
    best_individual, best_fitness = sorted_population[0]
    best_image = combine_image(best_individual, tile_width, tile_height, resized_image.size)
    best_image.save(f"C:/Users/User/Desktop/ML/best_solution_fitness_{best_fitness:.2f}.jpeg")

    # Plot fitness evolution
    plot_fitness_evolution(generations, fitness_values)

    return f"C:/Users/User/Desktop/ML/best_solution_fitness_{best_fitness:.2f}.jpeg", "C:/Users/User/Desktop/ML/fitness_evolution.png"

# Run the algorithm
image_path = "C:/Users/User/Desktop/ML/photo-1474511320723-9a56873867b5.jpeg"  # Replace with your image path
genetic_algorithm(image_path)
