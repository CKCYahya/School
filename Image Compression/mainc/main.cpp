#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <cmath>
#include <chrono>
#include <opencv2/opencv.hpp> // OpenCV for image processing

using namespace std;
using namespace cv;

// Huffman Node structure
struct HuffmanNode {
    int value;
    int frequency;
    HuffmanNode* left;
    HuffmanNode* right;

    HuffmanNode(int val, int freq) : value(val), frequency(freq), left(nullptr), right(nullptr) {}
};

// Compare function for priority queue
struct Compare {
    bool operator()(HuffmanNode* a, HuffmanNode* b) {
        return a->frequency > b->frequency;
    }
};

// Function to build Huffman Tree
HuffmanNode* buildHuffmanTree(const unordered_map<int, int>& frequencies) {
    priority_queue<HuffmanNode*, vector<HuffmanNode*>, Compare> pq;

    for (const auto& pair : frequencies) {
        pq.push(new HuffmanNode(pair.first, pair.second));
    }

    while (pq.size() > 1) {
        HuffmanNode* left = pq.top(); pq.pop();
        HuffmanNode* right = pq.top(); pq.pop();

        HuffmanNode* merged = new HuffmanNode(-1, left->frequency + right->frequency);
        merged->left = left;
        merged->right = right;

        pq.push(merged);
    }

    return pq.top();
}

// Function to generate Huffman Codes
void generateHuffmanCodes(HuffmanNode* root, const string& prefix, unordered_map<int, string>& huffmanCodes) {
    if (!root) return;

    if (root->value != -1) { // Leaf node
        huffmanCodes[root->value] = prefix;
    }

    generateHuffmanCodes(root->left, prefix + "0", huffmanCodes);
    generateHuffmanCodes(root->right, prefix + "1", huffmanCodes);
}

// Lossless Prediction
void losslessPrediction(const Mat& image, Mat& errorImage, Mat& reconstructedImage) {
    errorImage = Mat::zeros(image.size(), CV_32S);
    reconstructedImage = Mat::zeros(image.size(), CV_32S);

    for (int i = 1; i < image.rows - 1; ++i) {
        for (int j = 1; j < image.cols - 1; ++j) {
            // Tahmini değeri iki komşu kullanarak hesapla
            int prediction = (image.at<uchar>(i-1, j) + image.at<uchar>(i, j-1)) / 2;
            int error = image.at<uchar>(i, j) - prediction;
            errorImage.at<int>(i, j) = error;
            reconstructedImage.at<int>(i, j) = prediction + error;
        }
    }
}


// Integer Wavelet Transform (IWT)
void forwardTransform(const Mat& errorImage, Mat& lowCoefficients, Mat& highCoefficients) {
    int rows = errorImage.rows / 2;
    int cols = errorImage.cols / 2;
    lowCoefficients = Mat::zeros(rows, cols, CV_32S);
    highCoefficients = Mat::zeros(rows, cols, CV_32S);

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            int x = i * 2;
            int y = j * 2;
            lowCoefficients.at<int>(i, j) = (errorImage.at<int>(x, y) + errorImage.at<int>(x, y+1) +
                                             errorImage.at<int>(x+1, y) + errorImage.at<int>(x+1, y+1)) / 4;
            highCoefficients.at<int>(i, j) = errorImage.at<int>(x, y) - errorImage.at<int>(x+1, y+1);
        }
    }
}

// Process Wavelet Coefficients
void processCoefficients(const Mat& coefficients, Mat& processedCoefficients, vector<Point>& zeroPositions, vector<Point>& negativePositions) {
    processedCoefficients = coefficients.clone();

    for (int i = 0; i < coefficients.rows; ++i) {
        for (int j = 0; j < coefficients.cols; ++j) {
            int value = coefficients.at<int>(i, j);

            if (value == 0) {
                zeroPositions.emplace_back(i, j);
            } else if (value < 0) {
                negativePositions.emplace_back(i, j);
                processedCoefficients.at<int>(i, j) = abs(value);
            }
        }
    }
}

int main() {
    // Load the image
    string imagePath = "1.jpg"; // Replace with the actual image path
    Mat image = imread(imagePath, IMREAD_GRAYSCALE);
    if (image.empty()) {
        cerr << "Error: Could not load image!" << endl;
        return -1;
    }

    auto start = chrono::high_resolution_clock::now();

    Mat errorImage, reconstructedImage;
    losslessPrediction(image, errorImage, reconstructedImage);

    Mat lowCoefficients, highCoefficients;
    forwardTransform(errorImage, lowCoefficients, highCoefficients);

    Mat processedCoefficients;
    vector<Point> zeroPositions, negativePositions;
    processCoefficients(highCoefficients, processedCoefficients, zeroPositions, negativePositions);

    // Huffman Coding
    unordered_map<int, int> frequencies;
    for (int i = 0; i < processedCoefficients.rows; ++i) {
        for (int j = 0; j < processedCoefficients.cols; ++j) {
            frequencies[processedCoefficients.at<int>(i, j)]++;
        }
    }

    HuffmanNode* huffmanTree = buildHuffmanTree(frequencies);
    unordered_map<int, string> huffmanCodes;
    generateHuffmanCodes(huffmanTree, "", huffmanCodes);

    // Calculate Compression Ratio
    int originalSize = processedCoefficients.rows * processedCoefficients.cols * 8;
    int compressedSize = 0;
    for (const auto& pair : frequencies) {
        compressedSize += pair.second * huffmanCodes[pair.first].length();
    }
    double compressionRatio = static_cast<double>(originalSize) / compressedSize;

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    // Display Results
    cout << "Huffman Coding Results:" << endl;
    cout << "Original Size (bits): " << originalSize << endl;
    cout << "Compressed Size (bits): " << compressedSize << endl;
    cout << "Compression Ratio: " << compressionRatio << endl;
    cout << "Execution Time: " << elapsed.count() << " seconds" << endl;

return 0;
}