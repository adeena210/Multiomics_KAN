# Multiomics_KAN

## Overview
**Multiomics_KAN** is a bioinformatics project that leverages **Kolmogorov-Arnold Networks (KANs)** to analyze omic data. This project currently focuses on analyzing **scRNA-seq** from hippocampal cells of patients of **Alzheimer’s Disease**.
I'm currently attempting to compare the performance of **Multi-layer Perceptron (MLPs)** and **KANs** in a Variational Autoencoder (VAE). Once I complete this for a single omic, I'd like to move on to scATAC data and attempt their integration.

## Progress
This project is in progress, these are the things I've completed:
- created a VAE w/ MLP
- created a VAE w/ KAN using efficientKAN
- wrote some preprocessing scripts
- implemented a training pipeline to run locally (super slow, see enhancements below)

## Planned Enhancements
I'm currently working on transforming my project into a distributed training system to address the long training times. This system will:
- Implement a FastAPI backend to manage training jobs 
- Utilize S3 for storing datasets and model checkpoints 
- Process large datasets in memory-efficient chunks 
- Enable monitoring of training progress in real-time
- Try doing all of this with AWS' free tier :) 