# NASA C-MAPSS Dataset

## Overview

This directory contains the NASA Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) dataset used for Remaining Useful Life (RUL) prediction in aircraft engines.

## Dataset Description

**Source:** NASA Ames Prognostics Data Repository
**URL:** https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/

### What is C-MAPSS?

The Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) is a tool for the simulation of realistic large commercial turbofan engine data. The dataset consists of multiple multivariate time series collected from a fleet of engines.

### Data Scenarios

| Dataset | Train Engines | Test Engines | Operating Conditions | Fault Modes |
|---------|---------------|--------------|---------------------|-------------|
| FD001   | 100           | 100          | ONE (Sea Level)     | ONE (HPC)   |
| FD002   | 260           | 259          | SIX                 | ONE (HPC)   |
| FD003   | 100           | 100          | ONE (Sea Level)     | TWO         |
| FD004   | 249           | 248          | SIX                 | TWO         |

**For this project, we use FD001** (simplest scenario with single operating condition and single fault mode).

## Data Structure

### File Format

Each row in the dataset is a snapshot of data taken during a single operational cycle:

```
unit_id | cycle | operational_setting_1 | operational_setting_2 | operational_setting_3 | sensor_1 | sensor_2 | ... | sensor_21
```

### Column Descriptions

#### Operational Settings (3 columns)
- `setting1`: Altitude (ft)
- `setting2`: Mach number
- `setting3`: Throttle resolver angle (%)

#### Sensor Measurements (21 columns)

| Sensor | Description | Unit |
|--------|-------------|------|
| sensor1 | Total temperature at fan inlet | °R |
| sensor2 | Total temperature at LPC outlet | °R |
| sensor3 | Total temperature at HPC outlet | °R |
| sensor4 | Total temperature at LPT outlet | °R |
| sensor5 | Pressure at fan inlet | psia |
| sensor6 | Total pressure in bypass-duct | psia |
| sensor7 | Total pressure at HPC outlet | psia |
| sensor8 | Physical fan speed | rpm |
| sensor9 | Physical core speed | rpm |
| sensor10 | Engine pressure ratio (P50/P2) | - |
| sensor11 | Static pressure at HPC outlet | psia |
| sensor12 | Ratio of fuel flow to Ps30 | pps/psi |
| sensor13 | Corrected fan speed | rpm |
| sensor14 | Corrected core speed | rpm |
| sensor15 | Bypass Ratio | - |
| sensor16 | Burner fuel-air ratio | - |
| sensor17 | Bleed Enthalpy | - |
| sensor18 | Demanded fan speed | rpm |
| sensor19 | Demanded corrected fan speed | rpm |
| sensor20 | HPT coolant bleed | lbm/s |
| sensor21 | LPT coolant bleed | lbm/s |

### Files

- **train_FD001.txt**: Training data with run-to-failure sequences
- **test_FD001.txt**: Testing data (engines stopped before failure)
- **RUL_FD001.txt**: True Remaining Useful Life values for test set

## How to Download

### Option 1: Automatic Download (Recommended)

Run the download script:

```bash
cd scripts
chmod +x download-nasa-data.sh
./download-nasa-data.sh
```

### Option 2: Manual Download

1. Visit: https://ti.arc.nasa.gov/c/6/
2. Download `CMAPSSData.zip`
3. Extract to this directory
4. Verify files exist:
   - train_FD001.txt
   - test_FD001.txt
   - RUL_FD001.txt

## Data Usage

### Training Data

Each engine in the training set runs until complete failure. The RUL at each cycle can be calculated as:

```python
RUL = max_cycle - current_cycle
```

### Test Data

Engines in the test set are stopped sometime before failure. The true RUL values are provided in `RUL_FD001.txt`.

## Data Preprocessing

Before training, the data requires preprocessing:

1. **Normalization**: Scale sensor values to [0, 1] or standardize
2. **Feature Engineering**: Create rolling averages, rates of change
3. **RUL Calculation**: Compute remaining useful life for each cycle
4. **Sequence Creation**: Group data by engine unit

See `models/preprocessing.py` for implementation.

## Sample Data

### Example Row (train_FD001.txt)

```
1 1 -0.0007 -0.0004 100.0 518.67 641.82 1589.70 1400.60 14.62 21.61 554.36 2388.06 9046.19 1.30 47.47 521.66 2388.02 8138.62 8.4195 0.03 392 2388 100.0 39.06 23.4190
```

**Interpretation:**
- Unit ID: 1
- Cycle: 1 (first cycle)
- Settings: -0.0007, -0.0004, 100.0
- 21 sensor readings follow

## Citation

If you use this dataset in your research, please cite:

```
A. Saxena, K. Goebel, D. Simon, and N. Eklund,
"Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation,"
in the Proceedings of the 1st International Conference on Prognostics and Health Management (PHM08),
Denver CO, Oct 2008.
```

## License

This dataset is provided by NASA Ames Research Center for research purposes.

## Contact

For questions about the Aero-Sense project:
- GitHub: https://github.com/aero-sense
- Email: team@aero-sense.com

---

**Note:** Dataset files (.txt, .csv) are gitignored. Run the download script to populate this directory.
