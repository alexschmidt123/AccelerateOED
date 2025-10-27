# AccelerateOED

Code for paper **"Neural Message Passing for Objective-Based Uncertainty Quantification and Optimal Experimental Design"**

This repository implements MOCU-OED framework using neural message passing to accelerate optimal experimental design for coupled oscillator systems by **100-1000×**.

## Environment Requirements

- **OS**: Linux (Ubuntu 18.04+)
- **Python**: 3.10
- **GPU**: NVIDIA GPU with CUDA 12.1+
- **Hardware**: Tested on GeForce RTX 2080 Ti

## Installation

### 1. Create Environment

```bash
conda create -n mocu python=3.10
conda activate mocu
```

### 2. Install CUDA Toolkit

```bash
conda install -c nvidia cuda-toolkit=12.1
nvcc --version
```

### 3. Install PyCUDA

```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get install -y build-essential python3-dev libboost-python-dev libboost-thread-dev

# PyCUDA
pip install pycuda
```

### 4. Install PyTorch & PyTorch Geometric

```bash
# PyTorch with CUDA 12.1
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# PyTorch Geometric
pip install torch-geometric==2.6.1
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv -f https://data.pyg.org/whl/torch-2.5.1+cu121.html
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```
AccelerateOED/
├── configs/                      # Configuration files
│   ├── N5_config.yaml           # 5-oscillator system
│   ├── N7_config.yaml           # 7-oscillator system
│   └── N9_config.yaml           # 9-oscillator system
├── run.sh                       # Main automation script
├── scripts/
│   ├── data_generation.py      # Generate & convert dataset
│   ├── training.py             # Train GNN model
│   ├── evaluation.py           # Run OED experiments
│   └── visualization.py        # Generate plots
├── src/                         # Source code
├── data/                        # [Auto-created] Datasets
├── models/                      # [Auto-created] Trained models
└── results/                     # [Auto-created] Results
```

## Quick Start

Run complete experiment with one command:

```bash
# For N=5 oscillators
bash run.sh configs/N5_config.yaml

# For N=7 oscillators
bash run.sh configs/N7_config.yaml

# For N=9 oscillators
bash run.sh configs/N9_config.yaml
```

**First run:** The script will update `N_global` in `src/core/mocu_cuda.py` and exit. Just run the command again.

The script automatically:
1. ✓ Configures CUDA `N_global`
2. ✓ Generates dataset (~3-5 hours)
3. ✓ Trains model (~1-2 hours)
4. ✓ Configures model paths
5. ✓ Runs experiments (~10 min to 30 hours depending on methods)
6. ✓ Generates visualizations

## Configuration

Edit `configs/N*_config.yaml` to customize parameters:

```yaml
# System parameters
N: 5                  # Number of oscillators
N_global: 6           # N + 1 for CUDA

# Dataset generation
dataset:
  samples_per_type: 37500  # Total = 2 × samples_per_type
  train_size: 70000
  K_max: 20480            # Monte Carlo samples

# Training
training:
  model_name: "cons5"
  epochs: 400
  constrain_weight: 0.0001

# Experiments
experiment:
  num_simulations: 10    # Number of random systems
  update_count: 10       # Experiments per system
  methods:
    - "iMP"              # Iterative message passing (best)
    - "MP"               # Message passing (fast)
    - "ODE"              # ODE-based (very slow!)
    - "ENTROPY"          # Entropy-based
    - "RANDOM"           # Random baseline
```

**Tip:** Comment out `"ODE"` to save 20+ hours of computation time.

## Output

After running `bash run.sh configs/N5_config.yaml`:

- **Dataset**: `data/70000_5o_train.pth`, `data/5000_5o_test.pth`
- **Model**: `models/cons5/model.pth`, `models/cons5/statistics.pth`
- **Results**: `results/{METHOD}_MOCU.txt`, `results/{METHOD}_timeComplexity.txt`
- **Plots**: `results/MOCU_5.png`, `results/timeComplexity_5.png`

## Citation

```bibtex
@article{accelerateOED,
  title={Neural Message Passing for Objective-Based Uncertainty Quantification and Optimal Experimental Design},
  author={Your Authors},
  journal={Your Journal},
  year={2024}
}
```

## Acknowledgments

- Original: [Levishery/AccelerateOED](https://github.com/Levishery/AccelerateOED)
- PyTorch Geometric & PyCUDA
