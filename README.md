# Connect 4 AI Engine

A Connect 4 implementation featuring a custom-built game engine, multiple AI opponents, Alpha-Beta Pruned Minimax Search, and a custom Convolutional Neural Network (CNN) evaluator. The project includes a real-time Flask + Socket.IO web interface and demonstrates both classical game-search techniques and neural-network-based position evaluation.

---

### Gameplay

![Gameplay](Recordings/Connect_4_Gameplay.GIF)

🎥 **Full Gameplay Video:**  
[Click here to watch the complete demonstration](Recordings/Connect_4_Gameplay.mp4)

## Overview

This project explores different approaches to game-playing AI through Connect 4.

The system includes:

* Classical AI using Minimax Search with Alpha-Beta Pruning
* Custom heuristic board evaluation
* Real-time web gameplay using Flask and Socket.IO
* Multiple difficulty levels
* Human vs AI gameplay
* Human vs Human gameplay
* Custom CNN-based board-state evaluation
* Pure NumPy neural network inference engine

The objective was to investigate both search-based and neural-network-based approaches for decision-making in a deterministic board game environment.

---

## Features

### Classical AI Engine

* Minimax Search
* Alpha-Beta Pruning
* Center-first move ordering
* Dynamic search depth
* Custom board evaluation heuristics
* Offensive and defensive threat analysis
* Immediate win/loss detection

### Neural Network Evaluation

* Convolutional Neural Network trained for board-state evaluation
* Exported model weights
* Pure NumPy inference engine
* Custom implementations of:

  * Convolution
  * ReLU activation
  * Max Pooling
  * Dense Layers
  * Softmax Classification

### Web Application

* Flask backend
* Socket.IO real-time communication
* Interactive browser-based gameplay
* Game state synchronization
* Difficulty selection
* Game reset functionality

### Game Modes

* Human vs AI
* Human vs Human

### Difficulty Levels

* Easy (CNN-based evaluation)
* Medium (Reduced-depth Alpha-Beta Search)
* Hard (Deep Alpha-Beta Search)

---

## AI Architecture

### Minimax + Alpha-Beta Pruning

The primary AI engine uses Minimax Search with Alpha-Beta Pruning to reduce the number of explored game states while maintaining strong gameplay performance.

Additional optimizations include:

* Center-column prioritization
* Dynamic depth adjustment
* Immediate win/loss detection
* Custom heuristic scoring

### Heuristic Evaluation

Board positions are scored using a custom evaluation function based on:

* Potential connect-4 opportunities
* Threat creation
* Threat prevention
* Winning move detection
* Blocking opponent strategies

The heuristic balances both offensive and defensive play, allowing the AI to make strong positional decisions without relying solely on brute-force search.

### CNN Evaluation

An experimental neural network evaluator was also implemented.

The network performs:

1. Convolution
2. ReLU Activation
3. Max Pooling
4. Dense Layer Inference
5. Softmax Classification

Unlike most implementations that rely on deep-learning frameworks during inference, this project executes the entire forward pass using custom NumPy code.

---

## Technical Challenges

Some of the key challenges encountered during development included:

* Designing an effective heuristic evaluation function
* Optimizing Minimax Search using Alpha-Beta Pruning
* Reducing search complexity while maintaining strong gameplay
* Implementing custom CNN inference without TensorFlow or PyTorch runtime dependencies
* Synchronizing game state between frontend and backend
* Balancing AI response time against search depth
* Managing board-state evaluation efficiently for real-time gameplay

---

## Results

The Alpha-Beta AI consistently defeats casual human players on Hard difficulty and demonstrates significantly stronger decision-making than the CNN-only evaluator.

Key characteristics:

* Deep game-tree exploration
* Efficient pruning of non-promising branches
* Center-column prioritization strategy
* Threat detection and prevention
* Immediate win/loss recognition

The CNN evaluator serves as an experimental alternative to heuristic search and demonstrates neural-network-based board evaluation using a custom NumPy inference pipeline.

---

## Performance

A naive Minimax implementation explores an exponential number of game states.

This project improves performance through:

* Alpha-Beta Pruning
* Center-first move ordering
* Dynamic search depth
* Early win/loss detection

These optimizations allow deeper searches while maintaining responsive gameplay.

---

## Project Structure

```text
.
├── app.py
├── Backtracking.py
├── cnn_weights.npz
├── requirements.txt
├── LICENSE
├── README.md
├── Recordings
│   ├── Connect_4_Gameplay.GIF
│   └── Connect_4_Gameplay.mp4
├── screenshots
│   ├── Screenshot_20250805_140050.png
│   └── Screenshot_20250805_152948.png
├── static
│   └── socketio.min.js
└── templates
    └── index.html

```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Sachcith/Connect-4_Game.git
cd Connect-4_Game
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the server:

```bash
python app.py
```

Open your browser and navigate to:

```text
http://localhost:5000
```

---

## Technologies Used

### Programming Languages

* Python

### AI & Machine Learning

* NumPy
* Convolutional Neural Networks
* Minimax Search
* Alpha-Beta Pruning

### Web Technologies

* Flask
* Flask-SocketIO
* HTML
* CSS
* JavaScript

---

## Technical Highlights

This project demonstrates:

* Adversarial Search Algorithms
* Alpha-Beta Pruning
* Heuristic Evaluation Design
* Neural Network Inference
* Custom NumPy Deep Learning Operations
* Real-Time Client-Server Communication
* State Synchronization
* Search Optimization Techniques
* AI Decision-Making Systems

---

## Future Improvements

Planned enhancements include:

* Monte Carlo Tree Search (MCTS)
* Self-play reinforcement learning
* Hybrid CNN + Minimax evaluation
* Transposition tables
* Bitboard representation
* Stronger neural-network architectures
* Performance optimization
* Online multiplayer support

---

## Author

Developed as a personal exploration of:

* Game AI
* Search Algorithms
* Neural Network Inference
* Adversarial Decision Making
* Real-Time Web Applications

The project combines classical techniques with neural-network-based evaluation methods to explore multiple approaches to game-playing agents.
