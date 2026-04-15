# Q-CHAIN
**Quantum Cryptographic Hash and Authentication Identity Network**

> 📄 **Read the full academic paper:** [Insert Link to PDF/Paper Here]

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

This repository contains a single, self-contained simulation script. To run the hybrid quantum-classical signature protocol, execute:

```bash
python qchain_sim.py
```

---

## Expected Output

When executed, the script simulates two quantum network hosts (Alice and Bob). The output logs the chronological protocol execution:

Bob generates the AGCD signature keypair and shares the public verification key.
Alice classically signs a sample blockchain transaction ("Transfer 100 BTC from Alice to Bob") using the hybrid subset-sum protocol.
Alice encodes the signature into a qubit state and teleports it to Bob via EPR pairs.
Bob receives the state, decodes it, and validates the signature against the hash.

A successful run will conclude with the following terminal output:

```bash
--- Simulation Results ---
Transaction: Transfer 100 BTC from Alice to Bob
Signature Size: 32 components
Verification Result: Success
```

---

## Security Properties
- Post-Quantum Resistance: AGCD encryption is resistant to Shor's algorithm.
- Authentication & Non-Repudiation: Only the holder of the secret prime trapdoor (p) can generate valid subset-sum signatures.
- Tamper-Evident Delivery: Eavesdropping on the transmission channel forces wave-function collapse, destroying the data before it reaches the validator and exposing the attack.

---

## Author & Acknowledgements

Author: 2/C Ahan Bhattacharyya

Advisors/Mentors:
Professor Travis Mayberry, Cyber Science Department, United States Naval Academy

This project was developed as part of academic research within the USNA Cyber Science Department. Generative AI was utilized as an approved tool for pair-programming, research, and structural formatting.

---

## Citation
 
If you use this code in your research, please cite:
 
```bibtex
@misc{quantum-digital-signatures,
  title={Q-CHAIN},
  author={Ahan Bhattacharyya},
  year={2026},
  url={https://github.com/yourusername/Q-CHAIN}
}
```
## License

This project is licensed under the MIT License - see the LICENSE file for details.
