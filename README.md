# Q-CHAIN
**Quantum Cryptographic Hash and Authentication Identity Network**

> 📄 **Read the full academic paper:** [Q-CHAIN: A Hybrid Quantum-Classical Identity Framework for Securing Decentralized Ledgers](Q-CHAIN_Paper.pdf)

Q-CHAIN is a Proof-of-Concept (PoC) simulation of a Quantum Blockchain Identity Framework designed to secure decentralized ledgers in the post-quantum era. This repository contains the QuNetSim implementation of the Q-CHAIN hybrid architecture.

---
## Table of Contents

- [Overview](#overview)
- [The RAM Bottleneck (Why a Hybrid Architecture?)](#the-ram-bottleneck-why-a-hybrid-architecture)
- [Requirements](#requirements)
- [Running the Simulation](#running-the-simulation)
- [Expected Output](#expected-output)
- [Security Properties](#security-properties)
- [Author & Acknowledgements](#author--acknowledgements)
- [License](#license)

---

## Overview

As quantum computers scale, traditional cryptographic protocols securing modern blockchains are vulnerable to Shor's Algorithm. Q-CHAIN provides a resilient blueprint for post-quantum decentralized networks by utilizing:

1. **Cryptography:** The Approximate Greatest Common Divisor (AGCD) problem combined with subset-sum mathematics.  
2. **Computation (Hybrid Approach):** Classical homomorphic addition to bypass the massive RAM bottleneck of pure quantum statevector simulations.  
3. **Transmission:** EPR-based quantum teleportation (Bell States) to deliver the signature components.  

Governed by the no-cloning theorem, any attempt to intercept the quantum transmission inherently collapses the state, ensuring physical-layer, tamper-evident security.

---

## The RAM Bottleneck (Why a Hybrid Architecture?)

A fully quantum network would conceptually require `>10^617 TB` of RAM for a 2048-bit statevector simulation—an impossible hardware constraint.

Q-CHAIN circumvents this by isolating the subset-sum math to classical hardware. This maintains a flat, efficient memory footprint of approximately **16 KiB** per 2048-bit message while preserving post-quantum mathematical security and tamper-evident quantum delivery.

---

## Requirements

This simulation requires Python 3.7+ and the `qunetsim` library.

```bash
pip install qunetsim
```

---

## Running the Simulation

To see the basic two node demo between Alice and Bob, run:

```bash
python qchain_basic_demo.py
```

To see the eavesdropper demo that adds Eve, run:

```bash
python qchain_eavesdropper_demo.py
```

---

## Expected Output
Expected Output
When executed, the scripts simulate a post-quantum network environment. The terminal will log the chronological protocol execution, detailing the AGCD key generation, the classical Hash-then-Sign subset-sum process, the quantum encoding, and the final verification math.

1. Normal Transmission (main.py)
In a secure environment, Alice and Bob successfully establish a quantum channel and verify the transaction. A successful run will conclude with the following terminal output:

```text
================================================================================
HYBRID QUANTUM-CLASSICAL DIGITAL SIGNATURE - FINAL RESULTS
================================================================================
Transaction: 'Transfer 100 BTC from Alice to Bob'
SHA-256 Hash: 8b4a3f8b... [truncated for readability]

Signing Key (p): 5883 (12 bits)
Verification Key: 5 Enc(0) samples
  Sample values: [47385, 12847, 94833]...

Signature Size: 32 components
Transmission: DIRECT QUANTUM CHANNEL

================================================================================
SUCCESS: DIGITAL SIGNATURE VERIFIED
Blockchain transaction authenticated via hybrid quantum system
================================================================================
```

2. Eavesdropper Detection (eavesdropper.py)
In the eavesdropping model, Eve actively intercepts the transmission. Because her active quantum sniffer forces an immediate wave-function collapse (No-Cloning Theorem), Bob receives corrupted data. The script will catch this mathematical failure and trigger the tamper-evident alarm:

```text
================================================================================
HYBRID QUANTUM-CLASSICAL DIGITAL SIGNATURE - FINAL RESULTS
================================================================================
Transaction: 'Transfer 100 BTC from Alice to Bob'
SHA-256 Hash: 8b4a3f8b... [truncated for readability]

Signing Key (p): 7499 (12 bits)
Verification Key: 5 Enc(0) samples
  Sample values: [83944, 29485, 11048]...

Signature Size: 32 components
Transmission: DIRECT QUANTUM CHANNEL (Routed via Eve)

[Security Event] Eve intercepted and measured 256 qubits.

================================================================================
FAILURE: Signature verification failed
TAMPER EVIDENCE DEMONSTRATED: Eavesdropping collapsed the quantum state,
destroying the signature before Bob could authenticate the transaction.
================================================================================
```

## Security Properties
- Post-Quantum Resistance: AGCD encryption is resistant to Shor's algorithm.
- Authentication & Non-Repudiation: Only the holder of the secret prime trapdoor (p) can generate valid subset-sum signatures.
- Tamper-Evident Delivery: Eavesdropping on the transmission channel forces wave-function collapse, destroying the data before it reaches the validator and exposing the attack.

---

## Author & Acknowledgements

Authors: 
- MIDN 2/C Ahan Bhattacharyya, Cyber Science Department, United States Naval Academy
- Dr. Travis Mayberry, Cyber Science Department, United States Naval Academy


Acknowledgements:
- This project was developed as part of academic research within the USNA Cyber Science Department. Generative AI was utilized as an approved tool for pair-programming, research, and structural formatting.

---

## Citation
 
If you use this code in your research, please cite:
 
```bibtex
@misc{quantum-digital-signatures,
  title={Q-CHAIN},
  author={Ahan Bhattacharyya},
  year={2026},
  url={https://github.com/ahanb123/Q-CHAIN}
}
```
## License

This project is licensed under the MIT License - see the LICENSE file for details.
