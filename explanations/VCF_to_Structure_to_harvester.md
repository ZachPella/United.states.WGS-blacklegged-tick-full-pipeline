# VCF_to_STRUCTURE_to_HARVESTER

A population genetics pipeline for converting VCF files to STRUCTURE format and performing population structure analysis on tick genomic data.

<img width="1812" height="461" alt="Screenshot 2025-10-23 111117" src="https://github.com/user-attachments/assets/c6370f8c-060a-4a31-8766-92f2ff546279" />





## Overview

This pipeline processes genomic variant data through several steps:
1. **Linkage Disequilibrium Pruning** - Removes linked SNPs to create an independent marker set
2. **Format Conversion** - Converts VCF to STRUCTURE format using PGDSpider
3. **Population Structure Analysis** - Runs STRUCTURE analysis using structure-threader
4. **Results Harvesting** - Processes STRUCTURE output to determine optimal K
5. **Visualization** - Generates publication-ready admixture plots

## Prerequisites

### Required Software
- **PLINK2** - For LD pruning and data filtering
- **PGDSpider** - For VCF to STRUCTURE format conversion
- **STRUCTURE** (v2.3+) - Population structure analysis
- **structure-threader** (v1.3+) - Parallel STRUCTURE execution
- **structureHarvester** - For processing STRUCTURE results and Evanno method
- **Python 3** - For visualization scripts (matplotlib, pandas, numpy)

### System Requirements
- High-performance computing cluster with SLURM scheduler
- Minimum 32GB RAM for large datasets
- Multiple CPU cores recommended (12+ for STRUCTURE analysis)

## File Structure

```
VCF_to_STRUCTURE/
├── scripts/
│   ├── plink.sh                 # LD pruning with PLINK2
│   ├── pgd_spider.sh            # VCF to STRUCTURE conversion
│   ├── structure.sh             # STRUCTURE analysis execution
│   ├── structureHarvester.py    # Process STRUCTURE results
│   ├── plot_county.py           # Generate admixture plots
│   ├── mainparams               # STRUCTURE main parameters
│   ├── extraparams              # STRUCTURE advanced parameters
│   └── spid.spid                # PGDSpider configuration
└── README.md
```

## Usage

### Step 1: Linkage Disequilibrium Pruning

Remove linked SNPs to create an independent marker set suitable for population structure analysis.

```bash
sbatch scripts/plink.sh
```

**Parameters:**
- Window size: 50 SNPs
- Step size: 10 SNPs  
- r² threshold: 0.1

**Output:** `*_pruned.vcf` - VCF file with unlinked SNPs

### Step 2: Format Conversion

Convert the pruned VCF file to STRUCTURE format using PGDSpider.

```bash
sbatch scripts/pgd_spider.sh
```

**Configuration:** Uses `spid.spid` configuration file for:
- Diploid genotype handling
- SNP-only data export
- Missing data preservation (coded as -9)
- Monomorphic SNP exclusion

**Output:** `*.str` - STRUCTURE format file

### Step 3: Population Structure Analysis

Run STRUCTURE analysis using structure-threader for parallel execution.

```bash
sbatch scripts/structure.sh
```

**Analysis Settings:**
- K values: 1-10 (number of populations)
- Replicates: 10 per K value
- Burn-in: 50,000 iterations
- MCMC: 200,000 iterations
- Threads: 12 (parallel execution)

**Important Notes:**
- The script uses the `--params` flag to specify parameter files
- Both `mainparams` and `extraparams` must be in the working directory
- STRUCTURE binary path is defined explicitly in the script

### Step 4: Results Harvesting

Process STRUCTURE results to determine optimal K using the Evanno method.

```bash
python scripts/structureHarvester.py
```

**Outputs:**
- Evanno method statistics (ΔK values)
- CLUMPP-formatted files for downstream analysis
- Summary tables for K selection

### Step 5: Visualization

Generate labeled admixture plots grouped by geographic location.

```bash
python3 scripts/plot_county.py <K_value>
```

**Example:**
```bash
python3 scripts/plot_county.py 2
```

**Requirements:**
- Input file: `K{K}.indfile` (STRUCTURE output)
- Label file: `name_and_state_county.txt` (sample metadata)

**Features:**
- Hierarchical geographic grouping (State → County)
- Custom sample ordering by location
- Multi-level labeling for Nebraska counties
- High-resolution PDF output

**Geographic Grouping Order:**
1. Iowa (state-level)
2. Nebraska - Thurston County
3. Nebraska - Dodge County
4. Nebraska - Douglas County
5. Nebraska - Sarpy County
6. Kansas (state-level)
7. Other

## Configuration Files

### mainparams
Core STRUCTURE parameters including:
- **INFILE**: clean_structure_fixed.str
- **NUMINDS**: 61 (number of individuals)
- **NUMLOCI**: 299,218 (number of loci)
- **BURNIN**: 50,000 (burn-in period)
- **NUMREPS**: 200,000 (MCMC iterations)
- **MISSING**: -9 (missing data code)
- **PLOIDY**: 2 (diploid)

### extraparams
Advanced model parameters:
- **FREQSCORR**: 1 (correlated allele frequencies model)
- **INFERALPHA**: 1 (infer alpha parameter)
- **NOADMIX**: 0 (allow admixture)
- **MIGRPRIOR**: 0.05 (migration prior, range: 0.001-0.1)
- **POPALPHAS**: 0 (single alpha for all populations)

### spid.spid
PGDSpider conversion settings:
- Input: VCF format
- Output: STRUCTURE format
- Data type: SNP only
- Ploidy: Diploid
- Exclude monomorphic SNPs
- No population file

## Dataset Information

**Current Dataset:** Tick genomic data (June 2025 cohort)
- **Individuals:** 61 samples
- **Original SNPs:** ~299K loci
- **Filtering:** MAF ≥ 0.01, missingness = 0%, MAC ≥ 2, biallelic only
- **Final dataset:** LD-pruned SNP set
- **Geographic scope:** Iowa, Nebraska (multiple counties), Kansas

## Output Files

### PLINK Output
- `*.prune.in` - List of independent SNPs retained
- `*.prune.out` - List of SNPs removed during pruning
- `*_pruned.vcf` - Filtered VCF with unlinked SNPs

### PGDSpider Output
- `*.str` - STRUCTURE format file

### STRUCTURE Results
- `structure_results/` directory containing:
  - Individual K value result files (K1-K10)
  - `*.indfile` - Individual ancestry coefficients
  - Log-likelihood estimates
  - Parameter estimates per replicate

### structureHarvester Output
- `harvester_output_*/` directory containing:
  - `summary.txt` - Summary statistics for all K values
  - Evanno table with ΔK calculations
  - CLUMPP input files

### Visualization Output
- `Admixture_Labeled_K{K}_COUNTY_IOWA_NE_KS.pdf` - Publication-ready admixture plot

## Resource Requirements

| Step | Time | Memory | CPUs |
|------|------|--------|------|
| PLINK | 10h | 32GB | 1 |
| PGDSpider | 10h | 20GB | 1 |
| STRUCTURE | 7 days | 50GB | 12 |
| Harvester | <1h | 8GB | 1 |
| Plotting | <5min | 4GB | 1 |

## Troubleshooting

### Common Issues

1. **Memory errors during PLINK**
   - Increase `--mem` parameter in SLURM script
   - Consider chromosome-by-chromosome processing

2. **PGDSpider conversion fails**
   - Verify VCF file format and completeness
   - Check spid.spid configuration file
   - Ensure input VCF path is correct

3. **STRUCTURE crashes or parameter errors**
   - Ensure mainparams and extraparams are in working directory
   - Verify `--params` flag points to correct mainparams file
   - Check that NUMLOCI matches actual number of SNPs in .str file
   - Verify input file format matches STRUCTURE requirements
   - Check memory allocation for large datasets

4. **Plotting script errors**
   - Verify label file has same number of entries as samples
   - Check that K value matches available .indfile
   - Ensure matplotlib and pandas are installed

### File Format Requirements

- **VCF files:** Must be properly formatted with GT field
- **Missing data:** Should be coded consistently (-9 in STRUCTURE)
- **Sample names:** Avoid special characters and spaces
- **Label file:** One label per line, matching sample order

### Parameter Tuning

**For faster testing:**
- Reduce BURNIN to 10,000
- Reduce NUMREPS to 50,000
- Reduce number of replicates (-R flag)

**For publication-quality results:**
- Use recommended settings (BURNIN: 50,000, NUMREPS: 200,000)
- Run at least 10-20 replicates per K
- Test K range that brackets expected populations

## Workflow Example

Complete analysis workflow for new dataset:

```bash
# 1. LD pruning
sbatch scripts/plink.sh

# 2. Format conversion
sbatch scripts/pgd_spider.sh

# 3. Run STRUCTURE (wait for completion, ~7 days)
sbatch scripts/structure.sh

# 4. Harvest results
python scripts/structureHarvester.py

# 5. Generate plots for optimal K
python3 scripts/plot_county.py 2
python3 scripts/plot_county.py 3
```
