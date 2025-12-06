#!/bin/bash

#################################################
# NASA CMAPSS Dataset Download Script
# Aero-Sense - Google Cloud Partner Hackathon 2025
#################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DATA_DIR="../data"
NASA_BASE_URL="https://ti.arc.nasa.gov/c/6/"
DATASET_ZIP="CMAPSSData.zip"

echo -e "${GREEN}#################################################${NC}"
echo -e "${GREEN}# NASA CMAPSS Dataset Downloader${NC}"
echo -e "${GREEN}# Aero-Sense Project${NC}"
echo -e "${GREEN}#################################################${NC}\n"

# Create data directory if it doesn't exist
if [ ! -d "$DATA_DIR" ]; then
    echo -e "${YELLOW}Creating data directory...${NC}"
    mkdir -p "$DATA_DIR"
fi

cd "$DATA_DIR"

# Check if dataset already exists
if [ -f "train_FD001.txt" ] && [ -f "test_FD001.txt" ] && [ -f "RUL_FD001.txt" ]; then
    echo -e "${GREEN}Dataset already exists. Skipping download.${NC}"
    echo -e "${YELLOW}To re-download, delete the data directory first.${NC}"
    exit 0
fi

# Download dataset
echo -e "${YELLOW}Downloading NASA CMAPSS dataset...${NC}"
if command -v wget &> /dev/null; then
    wget -q --show-progress "${NASA_BASE_URL}${DATASET_ZIP}" -O "$DATASET_ZIP"
elif command -v curl &> /dev/null; then
    curl -# -L "${NASA_BASE_URL}${DATASET_ZIP}" -o "$DATASET_ZIP"
else
    echo -e "${RED}Error: Neither wget nor curl is installed.${NC}"
    echo -e "${YELLOW}Please install wget or curl and try again.${NC}"
    exit 1
fi

# Verify download
if [ ! -f "$DATASET_ZIP" ]; then
    echo -e "${RED}Error: Download failed!${NC}"
    exit 1
fi

echo -e "${GREEN}Download completed successfully!${NC}"

# Extract dataset
echo -e "${YELLOW}Extracting dataset...${NC}"
if command -v unzip &> /dev/null; then
    unzip -q -o "$DATASET_ZIP"
else
    echo -e "${RED}Error: unzip is not installed.${NC}"
    echo -e "${YELLOW}Please install unzip and try again.${NC}"
    exit 1
fi

# Cleanup
echo -e "${YELLOW}Cleaning up...${NC}"
rm "$DATASET_ZIP"

# Verify extracted files
echo -e "${YELLOW}Verifying extracted files...${NC}"
REQUIRED_FILES=(
    "train_FD001.txt"
    "train_FD002.txt"
    "train_FD003.txt"
    "train_FD004.txt"
    "test_FD001.txt"
    "test_FD002.txt"
    "test_FD003.txt"
    "test_FD004.txt"
    "RUL_FD001.txt"
    "RUL_FD002.txt"
    "RUL_FD003.txt"
    "RUL_FD004.txt"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo -e "${GREEN}All files extracted successfully!${NC}"
else
    echo -e "${RED}Warning: Some files are missing:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo -e "${RED}  - $file${NC}"
    done
fi

# Display dataset info
echo -e "\n${GREEN}#################################################${NC}"
echo -e "${GREEN}# Dataset Information${NC}"
echo -e "${GREEN}#################################################${NC}\n"

echo -e "${YELLOW}Dataset: NASA C-MAPSS (Commercial Modular Aero-Propulsion System Simulation)${NC}"
echo -e "Location: $PWD\n"

echo -e "${YELLOW}Available Datasets:${NC}"
echo -e "  FD001: 100 train engines, 100 test engines"
echo -e "  FD002: 260 train engines, 259 test engines"
echo -e "  FD003: 100 train engines, 100 test engines"
echo -e "  FD004: 249 train engines, 248 test engines\n"

echo -e "${YELLOW}For this project, we'll use FD001 (simplest scenario)${NC}\n"

# Count lines in main dataset
if [ -f "train_FD001.txt" ]; then
    TRAIN_LINES=$(wc -l < "train_FD001.txt" | tr -d ' ')
    echo -e "Training samples: ${GREEN}$TRAIN_LINES${NC}"
fi

if [ -f "test_FD001.txt" ]; then
    TEST_LINES=$(wc -l < "test_FD001.txt" | tr -d ' ')
    echo -e "Testing samples: ${GREEN}$TEST_LINES${NC}"
fi

echo -e "\n${GREEN}Dataset download and extraction completed!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Run data preprocessing: ${GREEN}python ../models/preprocessing.py${NC}"
echo -e "  2. Train model: ${GREEN}python ../models/train_xgboost.py${NC}"
echo -e "  3. Deploy to Vertex AI: ${GREEN}python ../models/vertex_deploy.py${NC}\n"
