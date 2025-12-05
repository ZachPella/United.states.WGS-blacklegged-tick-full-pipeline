# U.S. Whole-Genome Sequence Tick Population Genomics Pipeline

**Comprehensive population genomics analysis of *Ixodes scapularis* across the United States**

## Overview

This repository contains a comprehensive 17-step bioinformatics pipeline for analyzing population structure and genetic diversity in blacklegged ticks (*Ixodes scapularis*) using whole-genome sequencing data across the United States. The pipeline processes tick samples from multiple states through quality control, variant calling, filtering, and population genetic analysis to reveal continental-scale population structure and evolutionary patterns.

<img width="1382" height="989" alt="tick_pca_colored_by_NE_county" src="https://github.com/user-attachments/assets/a7f618e0-ae9a-4497-af83-90e5a31ac07f" />
<img width="1377" height="989" alt="tick_pca_all_samples_NE_north_and_south_all_else_black_or_white" src="https://github.com/user-attachments/assets/25273d05-fe59-42de-bbf9-4d78ef688af8" />
<img width="1377" height="989" alt="download" src="https://github.com/user-attachments/assets/b88e61a6-f5d8-43b9-abda-127c239288ed" />
<img width="1907" height="335" alt="Screenshot 2025-11-13 144235" src="https://github.com/user-attachments/assets/b4905ade-aa87-405e-a28c-bbaed2b5d4e4" />
<img width="957" height="764" alt="Screenshot 2025-10-30 100745" src="https://github.com/user-attachments/assets/4ff031a5-357d-4f97-b17d-33218361a5fa" />
<img width="2190" height="1282" alt="download" src="https://github.com/user-attachments/assets/92e809c3-39d0-4be3-95cd-0d00551ff875" />


## Pipeline Workflow

### 🔵 QC, Alignment, Preprocessing with Picard (Steps 1-8)
1. **Concatenate Reads** - Combine multi-lane sequencing files
2. **Fastp QC** - Quality control and adapter trimming  
3. **FastQC** - Post-cleaning quality assessment
4. **BWA Alignment** - Map reads to *I. scapularis* reference genome
5. **SAM to BAM** - Convert and coordinate-sort alignments
6. **Add Read Groups** - GATK metadata preparation for multi-sample analysis
7. **Remove Duplicates** - PCR artifact removal and library complexity assessment
8. **Summary Statistics** - Comprehensive quality control reporting

### 🟢 Variant Calling/GATK (Steps 9-11)
9. **HaplotypeCaller** - Individual sample variant discovery with scatter-gather optimization
10. **GenomicsDB** - Consolidate variant data for scalable joint calling
11. **Joint Genotyping** - Population-scale variant calling across all US samples

### 🟠 Filtering/GATK (Steps 12-15)
12. **Select SNPs** - Extract SNPs for population genetic analysis
13. **Hard Filtering** - Apply GATK best practices quality filters
14. **Select PASS** - Retain only high-confidence variants
15. **Population Filters** - MAF ≥5% and missingness ≤30% optimization

### 🟣 Analysis (Steps 16-17)
16. **Population Structure Analysis** - Multiple complementary approaches for comprehensive genetic characterization:
    - **PLINK2 + PCA** - Principal component analysis for genetic structure and diversity
    - **fastStructure** - Model-based ancestry inference with K=1-10 populations
    - **DAPC** - Discriminant Analysis of Principal Components for cluster identification
17. **Visualization** - Publication-quality plots with geographic context and statistical interpretation

## Key Features

- **Continental Scale**: Designed for large-scale analysis across the entire US range of *I. scapularis*
- **GATK Best Practices**: Rigorous variant calling following current genomics standards
- **Scalable Architecture**: Optimized scatter-gather processing for hundreds of samples
- **Multiple Analysis Methods**: Integrated PCA, fastStructure, and DAPC for robust population inference
- **Geographic Integration**: Population structure analysis with spatial context across states
- **Publication Ready**: High-quality visualizations and comprehensive documentation
- **Reproducible Methodology**: Detailed step-by-step documentation for transparency

## Dataset Scope

- **Geographic Coverage**: Multi-state sampling across the *I. scapularis* range (Maine to Florida, Iowa to Texas)
- **Sample Scale**: 193 tick samples with expandable architecture for larger cohorts
- **Sequencing Platform**: NovaSeq whole-genome sequencing (8× coverage)
- **Data Volume**: Multi-TB genomic dataset processing capability
- **Population Focus**: Continental population structure and phylogeography

## Scientific Applications

This pipeline enables investigation of:
- **Population Structure**: Geographic patterns of genetic differentiation across the US
- **Gene Flow**: Migration and connectivity across the species range
- **Demographic History**: Population expansion, bottlenecks, and founder effects
- **Local Adaptation**: Genetic signatures of adaptation to regional environments
- **Disease Ecology**: Population genetic context for pathogen transmission dynamics
- **Conservation Genetics**: Genetic diversity assessment for species management

## Technical Specifications

- **Platform**: SLURM-based HPC cluster environments (tested on SWAN cluster)
- **Core Tools**: GATK4, BWA-MEM, PLINK2, fastStructure, R/adegenet, VCFtools, samtools
- **Languages**: Bash scripting, Python visualization, R statistical analysis
- **Memory Optimization**: Scalable memory allocation based on sample size
- **Processing Strategy**: Scatter-gather parallelization for computational efficiency

## Repository Structure

```
├── scripts/
│   ├── preprocess_*.sh              # Steps 1-8: Data preparation and QC
│   ├── variant_*.sh                 # Steps 9-11: GATK variant calling
│   ├── filter_*.sh                  # Steps 12-15: Quality filtering
│   ├── analysis_01_plink.sh         # Step 16a: PCA analysis
│   └── analysis/                    # Step 16b-c: Advanced population genetics
│       ├── run_faststructure.sh     # fastStructure execution (K=1-10)
│       ├── chooseK.py               # Optimal K selection
│       ├── extract_metrics.py       # Model selection metrics
│       ├── plot_faststructure.py    # Admixture visualization
│       └── DAPC.R                   # DAPC analysis workflow
├── docs/
│   ├── pipeline-documentation.md    # Comprehensive methodology guide
│   ├── faststructure.md             # fastStructure analysis guide
│   ├── explain_dapc.md              # DAPC workflow documentation
│   ├── VCF_to_Structure_to_harvester.md  # STRUCTURE analysis guide
│   ├── parameter-optimization.md    # Sample size scaling guidelines
│   └── troubleshooting.md           # Common issues and solutions
├── visualization/
│   ├── pca_generation.py            # Advanced PCA plotting
│   ├── geographic_analysis.R        # Spatial population genetics
│   └── diversity_metrics.py         # Population genetic statistics
├── config/
│   ├── sample_template.txt          # Sample list format
│   └── cluster_configs/             # HPC-specific configurations
└── README.md                        # This overview
```

## Quick Start Guide

### Prerequisites
- SLURM-based HPC cluster access
- Required software modules: GATK4, BWA, PLINK2, fastStructure, R (with adegenet), VCFtools, samtools, fastp, FastQC
- Reference genome: *I. scapularis* masked reference assembly

### Basic Usage
1. **Prepare sample list**: Create `sample_list.txt` with one sample name per line
2. **Configure paths**: Update base directory paths in all scripts for your environment  
3. **Run preprocessing**: Execute steps 1-8 sequentially
4. **Variant calling**: Run steps 9-11 for population variant discovery
5. **Filter variants**: Complete steps 12-15 for high-quality SNP dataset
6. **Population analysis**: Run multiple complementary analyses:
   - Execute `analysis_01_plink.sh` for PCA
   - Run `run_faststructure.sh` for model-based inference
   - Execute `DAPC.R` for discriminant analysis
7. **Visualize results**: Generate publication-quality figures with provided scripts

### Scaling for Large Datasets
The pipeline automatically scales resource allocation based on sample size:
- **Memory**: Increases proportionally with sample count
- **Processing time**: Array job optimization for sample-parallel steps
- **Storage**: Compressed intermediate files and organized directory structure
- **Quality control**: Sample size-aware statistical thresholds

## Population Genetic Analysis Methods

### PCA (Principal Component Analysis)
**Purpose**: Unsupervised dimensionality reduction revealing population structure

**Workflow**:
1. LD pruning (r² < 0.1)
2. Extract pruned variants
3. PCA calculation (20 components)

**Outputs**:
- Eigenvalues and eigenvectors
- PC loadings per sample
- Geographic visualization

**Best for**: Initial exploration, detecting outliers, visualizing genetic relationships

---

### fastStructure
**Purpose**: Model-based ancestry inference assuming K ancestral populations

**Workflow**:
1. Convert VCF to Structure format
2. Run K=1-10 in parallel (SLURM array)
3. Determine optimal K via marginal likelihood and model components
4. Visualize admixture proportions

**Key Features**:
- Variational Bayesian inference (faster than STRUCTURE)
- Marginal likelihood for K selection
- Geographic grouping in plots
- UNMC color palette

**Outputs**:
- Admixture proportions (Q matrices)
- Allele frequencies (P matrices)
- Model selection plots
- Geographic admixture plots

**Best for**: Identifying admixed individuals, quantifying ancestry proportions

---

### DAPC (Discriminant Analysis of Principal Components)
**Purpose**: Maximize between-group genetic variance while minimizing within-group variance

**Workflow**:
1. Find clusters via K-means on PCs
2. BIC-based K selection
3. Optimize a-score (PC retention)
4. Final DAPC with optimized parameters

**Key Features**:
- No genetic model assumptions
- Optimized PC retention prevents overfitting
- Posterior membership probabilities
- Custom UNMC colors (#AD122A, #129DBF)

**Outputs**:
- BIC plot for K selection
- A-score optimization curve
- DAPC scatter plots
- Posterior probability matrix

**Best for**: Clear cluster visualization, fine-scale population differentiation

---

### Method Comparison

| Method | Assumptions | K Selection | Admixture | Computational Cost |
|--------|-------------|-------------|-----------|-------------------|
| **PCA** | None | N/A | No | Low |
| **fastStructure** | HWE, ancestral populations | Marginal likelihood | Yes | Medium |
| **DAPC** | None (discriminant) | BIC | No | Low |

**Recommendation**: Use all three methods for comprehensive analysis:
1. **PCA** for initial exploration
2. **fastStructure** for ancestry quantification
3. **DAPC** for maximizing group separation

## Key Methodological Advances

### Computational Optimization
- **Scatter-gather processing**: Parallel variant calling across genomic intervals
- **Memory-efficient joint calling**: GenomicsDB-based population analysis
- **Resource scaling**: Dynamic allocation based on dataset size
- **I/O optimization**: Scratch space utilization for intensive operations
- **Array jobs**: Parallel K-value testing for population structure

### Quality Control Rigor
- **Multi-stage filtering**: Technical and population-level quality assessment
- **Comprehensive statistics**: Detailed metrics at every pipeline stage
- **Comparative analysis**: Before/after filtering assessment for parameter optimization
- **Sample-level QC**: Individual sample quality evaluation and outlier detection

### Population Genetic Focus
- **Multiple analytical frameworks**: PCA, model-based (fastStructure), and discriminant (DAPC) approaches
- **Geographic integration**: Spatial context for population structure analysis
- **Evolutionary interpretation**: Population genetic statistics with biological meaning
- **Visualization excellence**: Publication-ready figures with statistical annotations
- **Scalable analysis**: Methods that work from regional to continental scales

## Expected Outputs

### Data Products
- **High-quality variant dataset**: Population-filtered SNPs suitable for genetic analysis
- **Population structure results**: 
  - PCA analysis revealing geographic genetic patterns
  - fastStructure admixture proportions and ancestry inference
  - DAPC cluster assignments and membership probabilities
- **Quality control reports**: Comprehensive metrics documenting pipeline performance
- **Visualization suite**: Publication-ready figures and interactive plots

### Biological Insights
- **Continental population structure**: Major genetic divisions across the US range
- **Regional differentiation**: Fine-scale population genetic patterns
- **Admixture patterns**: Individual ancestry quantification and hybrid zone identification
- **Migration patterns**: Gene flow and connectivity between populations
- **Demographic history**: Population expansion and colonization patterns
- **Adaptive potential**: Genetic diversity distribution across populations

## Population Structure Results Preview

### PCA Results
- Continental-scale structure visible in PC1 and PC2
- Nebraska samples show internal differentiation by county
- Clear separation of northern and southern populations

### fastStructure Results
- Optimal K determined via marginal likelihood maximization
- Geographic pattern in ancestry proportions
- Admixture evident in transition zones
- State-level grouping reveals regional patterns

### DAPC Results
- BIC suggests K=2 optimal for dataset
- High discrimination between clusters
- Membership probabilities quantify assignment confidence
- Results concordant with PCA and fastStructure

## Citation and Usage

If you use this pipeline in your research, please cite:
- **Pipeline methodology**: [Repository DOI]
- **Key software**: 
  - GATK: McKenna et al. 2010, Genome Research
  - BWA-MEM: Li & Durbin 2009, Bioinformatics
  - PLINK2: Chang et al. 2015, GigaScience
  - fastStructure: Raj et al. 2014, Genetics
  - adegenet (DAPC): Jombart et al. 2010, BMC Genetics
- **Reference genome**: *I. scapularis* genome assembly citation

## Support and Contributing

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Comprehensive guides in `/docs` directory  
- **Community**: Contributions welcome via pull requests

---

**Input:** Multi-state NovaSeq FASTQ files → **Output:** Comprehensive population structure insights

*Transforming raw sequencing data into biological understanding of tick population dynamics across the United States through complementary analytical approaches*
