# Automating the Digitization & Diagnosis of Paper EKGs  
*A PTB‑XL case study*

---

## Introduction  

Heart disease remains the leading cause of death in the United States, yet millions of resting‑EKG records are still archived as static PDFs or paper printouts. These non‑interactive formats limit downstream analysis, large‑scale machine‑learning efforts, and seamless integration with electronic health records.�cite�turn0file1�ℹ

Our project tackles this bottleneck by:

1. **Digitizing** printed / PDF ECGs into cleaned, deskewed, grid‑free images.
2. **Reconstructing** the underlying 12‑lead time‑series signals.
3. **Classifying** cardiac conditions directly from (a) raw signals via 1‑D CNNs / Random Forests and (b) cleaned images via transfer‑learning CNNs.
4. **Benchmarking** each modelling route on the open‑access PTB‑XL dataset, generating insights on accuracy, computational cost, and class‑imbalance robustness.�cite�turn0file0�ℹ

Beyond academic curiosity, a scalable digitization pipeline could unlock decades of legacy ECG data for automated triage, tele‑cardiology, and retrospective research.

---

## Problem Statement  

* **Task.** Convert static ECG images into high‑fidelity digital signals, then predict clinically meaningful diagnostic labels.  
* **Motivation.** Unlock the *≈ 300 M* annual ECGs performed worldwide for AI‑driven decision support without re‑instrumenting every hospital scanner.  
* **Research Questions.**  
  1. Which pre‑processing pipeline best preserves waveform fidelity after binarisation, deskewing, grid removal, and spline‑based reconstruction?  
  2. Do image‑based CNNs outperform signal‑based models (1‑D CNN / Random Forest) once full digitization is possible?  
  3. How do class imbalance and limited computing resources shape final performance?

---

## Approach  

| Stage | Technique | Rationale |
|-------|-----------|-----------|
| **Binarisation** | Sauvola adaptive thresholding | Retains fine wave details under varying background tones�cite�turn0file1�ℹ |
| **Deskewing** | Probabilistic Hough Transform → affine rotation | Aligns grid lines horizontally before downstream masking |
| **Grid removal** | Progressive masking based on neighbourhood pixel counts | Keeps sharp waveform pixels while discarding grid noise |
| **Signal reconstruction** | Cubic‑spline interpolation across gaps; lead segmentation via intensity scanning | Recovers continuous 12‑lead traces for 1‑D models |
| **Modelling – Images** | *Baseline* 10‑layer CNN ➜ *Transfer* ResNet‑50 | Tests custom vs. pre‑trained CNNs |
| **Modelling – Signals** | 1‑D ResNet, + Random Forest on engineered features | Contrasts deep vs. shallow signal classifiers |

This hybrid strategy lets us compare end‑to‑end image models with fully digitized‑signal pipelines – a contrast rarely evaluated in prior ECG‑digitization literature.

---

## Experimental Setup  

* **Dataset.** PTB‑XL v1.0.3 (21,837 12‑lead records, 10 s each). Signals were rendered to PNGs, then processed through the pipeline above. Only diagnostic classes with ≥ 100 instances were retained to mitigate extreme imbalance (N = ~3.8 k images).�cite�turn0file1�ℹ  
* **Environment.**  
  * **Image models:** NVIDIA T4 (Colab) – ~20‑50 min / epoch.  
  * **Signal models:** Apple M1 Pro CPU & 16‑GB RAM (local).  
* **Hyper‑parameters.**  
  * CNN (images): Adam 1e‑4, batch 32, dropout 0.5, early‑stopping on val‑loss.  
  * 1‑D ResNet: 34 layers, global‑avg‑pool, cosine‑scheduler 30 epochs.  
  * Random Forest: 500 trees, max‑depth None, class‑weight “balanced”.  

---

## Results  

| Model | Input | Val Acc | Test Acc | Micro‑F1 |
|-------|-------|--------:|---------:|---------:|
| Basic CNN | Raw signal image | **64 %** | 61 % | – |
| CNN + Dropout/Reg | Raw signal image | **64 %** | 66 % | – |
| **1‑D ResNet** | Digitized signal | **68 %** | 66 % | **0.74** |
| ResNet‑50 TL | Cleaned image | **66 %** | 66 % | – |
| Random Forest | Engineered signal feats | – | – | **0.39** |

*1‑D ResNet beats classical Random Forest by +0.35 micro‑F1; transfer‑learning on images offers parity with custom CNN despite fewer trainable layers.*�cite�turn0file0�ℹ

---

## Discussion  

* **Strengths.**  
  * Fully automated end‑to‑end pipeline (image → signal → diagnosis).  
  * Demonstrates viability of lightweight 1‑D architectures on digitized signals.  
* **Limitations.**  
  1. **Compute‑heavy pre‑processing** – 2 h per 1 k images for full augmentation.  
  2. **Image bloat** – 50 kB ➜ 15 MB when aggressively augmenting.  
  3. **Class imbalance** – categories such as *HYP* had near‑zero recall under RF.  
* **Future work.**  
  * **Transfer learning on signals** (e.g., ECG‑Transformer) once larger digitized corpora exist.  
  * **Self‑supervised pretext tasks** to mitigate limited labelled data.  
  * **Edge deployment** feasibility on bedside monitors.

---

## Conclusion  

We built and benchmarked a pipeline that:  

1. **Digitizes** static ECGs via Sauvola → Hough → masking → spline.  
2. **Reconstructs** clinically sound 12‑lead signals ready for ML.  
3. **Classifies** diagnostic classes with up to **68 %** accuracy using 1‑D ResNet and **0.74** micro‑F1 – competitive with image‑only CNNs while reducing storage overhead.  

These findings support a shift toward large‑scale retrospective ECG mining without specialized acquisition hardware.

---

<details>
<summary>References (click to expand)</summary>

1. Stefanakis, A.; Zouzias, D.; Marsellos, A. *Groundwater Pollution: Human and Natural Sources and Risks* (2015).  
2. CDC. *Leading Causes of Death* (2024).  
3. Moores, D. *Electrocardiogram: Procedure, Risks & Results* (2022).  
4. Mishra, J. P. *Cardiologist or Computer: Who Can Read EKG Better?* Cardiac 1(1): 4 (2019).  
5. Mincholé, A.; Camps, J.; Lyon, A.; Rodríguez, B. *Machine learning in the electrocardiogram.* J Electrocardiol 57 (Suppl) S61–S64 (2019).  
6. Mayo Clinic Staff. *Electrocardiogram (ECG or EKG)* (2024).  
7. Baxter Intl. *Cardio Server ECG Management System* (2024).  
8. Philips Healthcare. *IntelliVue MX800 Bedside Patient Monitor* (2025).  
9. Badilini, F. *et al.* *Archiving and exchange of digital ECGs: A review of existing data formats.* J Electrocardiol 51 (6 S) S113–S115 (2018).  
10. Wagner, P. *et al.* *PTB‑XL, a large publicly available electrocardiography dataset.* PhysioNet (2022).  
11. Wu, H.; Patel, K.; Li, X.; *et al.* *A fully‑automated paper ECG digitisation algorithm using deep learning.* Sci Rep 12 (2022).  
12. Demolder, A.; *et al.* *High Precision ECG Digitization Using AI.* medRxiv (2024).  
13. Kim, H. E.; *et al.* *Transfer learning for medical image classification: A literature review.* BMC Med Imaging 22 (2022).

</details>
