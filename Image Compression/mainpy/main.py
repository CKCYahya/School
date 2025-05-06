import numpy as np
from collections import Counter
import heapq
from PIL import Image
import time

# Huffman Tree Node
class HuffmanNode:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


# Build Huffman Tree
def build_huffman_tree(frequencies):
    heap = [HuffmanNode(value, freq) for value, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = HuffmanNode(None, node1.frequency + node2.frequency)
        merged.left = node1
        merged.right = node2

        heapq.heappush(heap, merged)

    return heap[0]


# Generate Huffman Codes
def generate_huffman_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node:
        if node.value is not None:
            codebook[node.value] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)

    return codebook


# Lossless Prediction Function
def lossless_prediction(image):
    # Veri tipini int32'ye çevirerek overflow'u engelle
    image = image.astype(np.int32)

    rows, cols = image.shape
    error = np.zeros((rows, cols), dtype=np.int32)
    reconstructed_image = np.zeros((rows, cols), dtype=np.int32)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # Sadece iki komşunun ortalaması alınarak tahmini değer hesaplanır
            P_ij = (image[i - 1, j] + image[i, j - 1]) / 2
            P_ij_rounded = round(P_ij)
            error[i, j] = image[i, j] - P_ij_rounded
            reconstructed_image[i, j] = P_ij_rounded + error[i, j]

    # Kenar piksellerini orijinal değerleriyle koru
    reconstructed_image[0, :] = image[0, :]
    reconstructed_image[-1, :] = image[-1, :]
    reconstructed_image[:, 0] = image[:, 0]
    reconstructed_image[:, -1] = image[:, -1]

    return error, reconstructed_image


# Integer Wavelet Transform (IWT)
def forward_transform_2d(image):
    rows, cols = image.shape
    low = np.zeros((rows // 2, cols // 2), dtype=np.int32)
    high = np.zeros((rows // 2, cols // 2), dtype=np.int32)

    for i in range(0, rows, 2):
        for j in range(0, cols, 2):
            if i + 1 < rows and j + 1 < cols:
                low[i // 2, j // 2] = (
                                              image[i, j] + image[i, j + 1] + image[i + 1, j] + image[i + 1, j + 1]
                                      ) // 4
                high[i // 2, j // 2] = (
                        image[i, j] - image[i + 1, j + 1]
                )
    return low, high


# Process IWT Coefficients
def process_iwt_coefficients(coefficients):
    processed_coefficients = coefficients.copy()
    zero_positions = []
    negative_positions = []

    for i in range(coefficients.shape[0]):
        for j in range(coefficients.shape[1]):
            if coefficients[i, j] == 0:
                zero_positions.append((i, j))
                processed_coefficients[i, j] = 0
            elif coefficients[i, j] < 0:
                negative_positions.append((i, j))
                processed_coefficients[i, j] = abs(coefficients[i, j])

    return processed_coefficients, zero_positions, negative_positions


# Load Image
image_path = "2.jpg"  # Replace with your image path
original_image = Image.open(image_path).convert('L')  # Convert to grayscale
image_array = np.array(original_image)
start_time = time.time()
# Step 1: Lossless Prediction
error_image, reconstructed_image = lossless_prediction(image_array)

# Step 2: Integer Wavelet Transform (IWT)
low_coefficients, high_coefficients = forward_transform_2d(error_image)

# Step 3: Process IWT Coefficients
processed_coefficients, zero_positions, negative_positions = process_iwt_coefficients(high_coefficients)

# Step 4: Huffman Coding
flattened_coefficients = processed_coefficients.flatten()
frequencies = Counter(flattened_coefficients)
huffman_tree = build_huffman_tree(frequencies)
huffman_codes = generate_huffman_codes(huffman_tree)
original_size = len(flattened_coefficients) * 8
compressed_size = sum(len(huffman_codes[value]) * freq for value, freq in frequencies.items())
compression_ratio = original_size / compressed_size
end_time = time.time()
# Display Results
print("Huffman Coding Results:")
print(f"Original Size (bits): {original_size}")
print(f"Compressed Size (bits): {compressed_size}")
print(f"Compression Ratio: {compression_ratio:.2f}")
print(f"Execution Time: {end_time - start_time:.2f} seconds")