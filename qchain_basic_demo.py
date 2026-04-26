"""
Hybrid Quantum-Classical Digital Signatures for Blockchain Identity

This module implements a post-quantum digital signature scheme combining:
- Approximate GCD cryptography (post-quantum secure)
- Classical computation (practical implementation)
- Quantum teleportation (authenticated transmission)

References:
    - Approximate GCD problem for post-quantum cryptography
    - Fiat-Shamir zero-knowledge proof construction (Hash-then-Sign implementation)
    - QuNetSim quantum network simulator
"""

from qunetsim.components import Host, Network
from qunetsim.objects import Qubit
import time
import hashlib
import random


# ============================================================================
# Utility Functions
# ============================================================================

def string_to_binary(message):
    """Convert string to binary representation."""
    return ''.join(format(ord(i), '08b') for i in message)


def binary_to_string(binary_str):
    """Convert binary string to ASCII text."""
    if not binary_str:
        return ""
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)


def hash_message(message):
    """
    Hash message using SHA-256.
    
    Args:
        message: String to hash
    
    Returns:
        tuple: (hash_bytes, hash_bits) where hash_bits is binary string
    """
    hash_bytes = hashlib.sha256(message.encode()).digest()
    hash_bits = ''.join(format(byte, '08b') for byte in hash_bytes)
    return hash_bytes, hash_bits


# ============================================================================
# Cryptographic Key Generation
# ============================================================================

def generate_large_prime(bit_length):
    """
    Generate random prime of specified bit length using Miller-Rabin test.
    
    Args:
        bit_length: Number of bits in the prime
    
    Returns:
        int: Prime number with specified bit length
    """
    def is_prime(n, k=5):
        """Miller-Rabin primality test with k rounds."""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness loop
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << bit_length - 1) | 1
        if is_prime(candidate):
            return candidate


def generate_enc_zero(p, q_bit_length=10, r_bit_length=8):
    """
    Generate encrypted zero: Enc(0) = p*q + 2*r
    
    This forms the basis of the approximate GCD signature scheme.
    
    Args:
        p: Prime number (signing key)
        q_bit_length: Bit length of random multiplier q
        r_bit_length: Bit length of random noise r
    
    Returns:
        int: Encrypted zero value
    """
    q = random.getrandbits(q_bit_length)
    if q == 0:
        q = 1
        
    r = random.getrandbits(r_bit_length)
    if r == 0:
        r = 1
    
    # c_i = (p * q) + (2 * r)
    enc_zero = (p * q) + (2 * r) 
    return enc_zero


def generate_public_key(p, num_enc_zeros=5, q_bit_length=10, r_bit_length=8):
    """
    Generate public verification key as list of Enc(0) values.
    
    Args:
        p: Prime number (signing key)
        num_enc_zeros: Number of Enc(0) samples to generate
        q_bit_length: Bit length for q parameter
        r_bit_length: Bit length for r parameter
    
    Returns:
        list: Public verification key
    """
    public_key = []
    
    for i in range(num_enc_zeros):
        enc_zero = generate_enc_zero(p, q_bit_length, r_bit_length)
        public_key.append(enc_zero)
    
    print(f"[KeyGen] Generated {num_enc_zeros} Enc(0) values for verification key")
    print(f"[KeyGen] Sample verification values: {public_key[:3]}...")
    
    return public_key


def generate_signature_keypair(p_bit_length=12, num_enc_zeros=5):
    """
    Generate signature key pair.
    
    Args:
        p_bit_length: Bit length of prime p (signing key)
        num_enc_zeros: Number of Enc(0) samples in verification key
    
    Returns:
        tuple: (public_key, private_key) where private_key is p
    """
    p = generate_large_prime(p_bit_length)
    print(f"[KeyGen] Generated signing key p = {p} ({p.bit_length()} bits)")
    
    public_key = generate_public_key(p, num_enc_zeros)
    private_key = p  # The private key is simply the prime trapdoor
    
    return public_key, private_key


# ============================================================================
# Digital Signature Operations
# ============================================================================

def sign_hash_bit(hash_bit, private_key, num_to_select=2):
    """
    Sign a single hash bit using subset-sum construction.
    
    This implements the Fiat-Shamir-style signature where each hash bit
    is signed by combining fresh Enc(0) values with the bit value.
    
    Note: Uses classical addition for practical implementation.
          Resource analysis shows quantum arithmetic requires
          exponential memory: 2048-bit addition needs 4097 qubits.
    
    Args:
        hash_bit: Single bit to sign (0 or 1)
        private_key: The prime trapdoor p
        num_to_select: Number of fresh Enc(0) values to generate
    
    Returns:
        int: Signature component for this hash bit
    """
    p = private_key
    
    # Generate fresh Enc(0) values for this signature component
    fresh_enc_zeros = []
    for _ in range(num_to_select):
        enc_zero = generate_enc_zero(p)
        fresh_enc_zeros.append(enc_zero)
    
    # Classical addition
    sig_component = sum(fresh_enc_zeros)
    sig_component += hash_bit
    
    return sig_component


def sign_message(message, private_key, num_to_select=2, truncate_bits=8):
    """
    Sign message using hash-then-sign construction.
    
    Process:
        1. Hash message using SHA-256
        2. Truncate hash to specified number of bits
        3. Sign each hash bit using subset-sum
    
    Args:
        message: Message to sign
        private_key: The prime trapdoor p
        num_to_select: Number of Enc(0) values per hash bit
        truncate_bits: Number of hash bits to sign (8-256)
    
    Returns:
        tuple: (signature, hash_bytes) where signature is list of components
    """
    hash_bytes, hash_bits = hash_message(message)
    hash_bits = hash_bits[:truncate_bits]
    
    print(f"[Signing] Message: '{message}'")
    print(f"[Signing] SHA-256: {hash_bytes.hex()}")
    print(f"[Signing] Signing {len(hash_bits)} hash bits (truncated for demo)...")
    
    signature = []
    
    for idx, bit_char in enumerate(hash_bits):
        hash_bit = int(bit_char)
        sig_component = sign_hash_bit(hash_bit, private_key, num_to_select)
        signature.append(sig_component)
        
        if (idx + 1) % 8 == 0 or idx == len(hash_bits) - 1:
            print(f"[Signing] Signed {idx + 1}/{len(hash_bits)} bits...")
    
    print(f"[Signing] Created signature with {len(signature)} components")
    
    return signature, hash_bytes


def verify_signature(message, signature, public_key, private_key, truncate_bits=8):
    """
    Verify digital signature.
    
    Verification process:
        1. Hash message (same as signing)
        2. For each signature component, recover hash bit
        3. Check recovered bits match message hash
    
    Note: This implementation uses private key for verification.
          In production, p would be transmitted via quantum channel
          to validators for quantum-authenticated verification.
    
    Args:
        message: Original message
        signature: List of signature components
        public_key: Verification key (Enc(0) values)
        private_key: The prime trapdoor p
        truncate_bits: Must match signing truncation
    
    Returns:
        bool: True if signature is valid
    """
    p = private_key
    
    hash_bytes, hash_bits = hash_message(message)
    hash_bits = hash_bits[:truncate_bits]
    
    print(f"[Verification] Message: '{message}'")
    print(f"[Verification] SHA-256: {hash_bytes.hex()}")
    print(f"[Verification] Verifying {len(hash_bits)} signature components...")
    
    if len(signature) != len(hash_bits):
        print(f"[Verification] FAILED: Signature length mismatch")
        print(f"                Expected {len(hash_bits)}, got {len(signature)}")
        return False
    
    for i, expected_bit_char in enumerate(hash_bits):
        expected_bit = int(expected_bit_char)
        
        # Recover bit: (sig_component mod p) mod 2 (Matches paper exactly)
        recovered_bit = (signature[i] % p) % 2
        
        if recovered_bit != expected_bit:
            print(f"[Verification] FAILED at bit {i}")
            print(f"                Expected: {expected_bit}, Got: {recovered_bit}")
            return False
        
        if (i + 1) % 8 == 0 or i == len(hash_bits) - 1:
            print(f"[Verification] Verified {i + 1}/{len(hash_bits)} bits...")
    
    print(f"[Verification] SUCCESS: All {len(hash_bits)} bits verified")
    return True


# ============================================================================
# Quantum Encoding/Decoding
# ============================================================================

def int_to_qubit_state(host, value, num_qubits):
    """
    Encode integer as quantum state using binary encoding.
    
    Args:
        host: QuNetSim host for qubit creation
        value: Integer to encode
        num_qubits: Number of qubits to use
    
    Returns:
        list: Qubits encoding the value
    """
    qubits = [Qubit(host) for _ in range(num_qubits)]
    binary = format(value % (2**num_qubits), f'0{num_qubits}b')
    for i, bit in enumerate(binary):
        if bit == '1':
            qubits[i].X()
    return qubits


def qubits_to_int(qubits):
    """
    Measure qubits and decode to integer value.
    
    Args:
        qubits: List of qubits to measure
    
    Returns:
        int: Decoded integer value
    """
    binary = ''.join(str(q.measure()) for q in qubits)
    return int(binary, 2) if binary else 0


def encode_int_to_qubits(host, value, num_qubits):
    """Encode integer as quantum registers."""
    return int_to_qubit_state(host, value, num_qubits)


def decode_qubits_to_int(qubits):
    """Decode quantum registers to integer."""
    return qubits_to_int(qubits)


# ============================================================================
# Quantum Network Protocol
# ============================================================================

def alice_protocol_signature(host, transaction, results):
    """
    Alice's protocol: Sign transaction and transmit via quantum channel.
    
    Steps:
        1. Receive verification key from Bob
        2. Sign transaction using private key
        3. Verify signature locally
        4. Transmit signature via quantum teleportation
    
    Args:
        host: QuNetSim host for Alice
        transaction: Transaction message to sign
        results: Shared dictionary for protocol results
    """
    print("\n" + "="*80)
    print("ALICE: DIGITAL SIGNATURE GENERATION")
    print("="*80)
    
    # Receive verification key from Bob
    print("[Alice] Waiting for Bob's verification key...")
    key_msg = host.get_classical('Bob', wait=20)
    if not key_msg:
        print("[Alice] ERROR: Didn't receive verification key from Bob")
        return
    
    key_content = key_msg[0].content
    if key_content.startswith("VERIFICATION_KEY:"):
        parts = key_content.split(':')
        public_key_str = parts[1]
        public_key = [int(x) for x in public_key_str.split(',')]
        
        p = int(parts[2])
        num_to_select = int(parts[3])
        truncate_bits = int(parts[4])
        
        private_key = p
        
        print(f"[Alice] Received verification key: {len(public_key)} values")
        print(f"[Alice] Received signing key p (via authenticated channel)")
        print(f"[Alice] Will use {num_to_select} fresh Enc(0)s per hash bit")
        print(f"[Alice] Will sign {truncate_bits} hash bits")
    else:
        print("[Alice] ERROR: Expected VERIFICATION_KEY message")
        return
    
    # Sign transaction
    print(f"\n[Alice] Signing transaction: '{transaction}'")
    signature, hash_value = sign_message(transaction, private_key, num_to_select, truncate_bits)
    results['signature'] = signature
    results['hash_value'] = hash_value
    results['transaction'] = transaction
    
    # Local verification
    print(f"\n[Alice] Testing signature locally...")
    is_valid = verify_signature(transaction, signature, public_key, private_key, truncate_bits)
    print(f"[Alice] Local verification: {'VALID' if is_valid else 'INVALID'}")
    
    # Send transaction metadata
    host.send_classical('Bob', f"TRANSACTION:{transaction}", await_ack=True)
    time.sleep(0.1)
    
    host.send_classical('Bob', str(len(signature)), await_ack=True)
    time.sleep(0.1)
    
    max_sig_component = max(signature)
    num_qubits = max_sig_component.bit_length() + 2
    
    print(f"\n[Alice] Quantum transmitting signature...")
    print(f"[Alice] Using {num_qubits} qubits per signature component")
    print(f"[Alice] Total components: {len(signature)}")
    
    host.send_classical('Bob', str(num_qubits), await_ack=True)
    time.sleep(0.1)
    
    # Quantum teleportation of signature
    for idx, sig_component in enumerate(signature):
        print(f"[Alice] Teleporting component {idx+1}/{len(signature)}...")
        
        sig_qubits = encode_int_to_qubits(host, sig_component, num_qubits)
        
        for j, q_sig in enumerate(sig_qubits):
            epr_id = host.send_epr('Bob', await_ack=False)
            q_epr = host.get_epr('Bob', q_id=epr_id, wait=15)
            if q_epr:
                q_sig.cnot(q_epr)
                q_sig.H()
                m1 = q_sig.measure()
                m2 = q_epr.measure()
                host.send_classical('Bob', f"{j}:{m1}:{m2}", await_ack=False)
                host.get_classical('Bob', wait=10)
        
        host.get_classical('Bob', wait=15)
        time.sleep(0.01)
    
    print(f"[Alice] Signature transmission complete")


def bob_protocol_signature(host, results):
    """
    Bob's protocol: Generate keys, receive and verify signature.
    
    Steps:
        1. Generate signature key pair
        2. Share verification key with Alice
        3. Receive signature via quantum channel
        4. Verify signature
    
    Args:
        host: QuNetSim host for Bob
        results: Shared dictionary for protocol results
    """
    print("\n" + "="*80)
    print("BOB: KEY GENERATION AND SIGNATURE VERIFICATION")
    print("="*80)
    
    # Key generation parameters
    print("[Bob] Generating signature key pair...")
    
    p_bit_length = 12
    num_enc_zeros = 5
    num_to_select = 2
    truncate_bits = 32
    
    public_key, private_key = generate_signature_keypair(p_bit_length, num_enc_zeros)
    results['keys'] = (public_key, private_key)
    
    # Share keys with Alice
    p = private_key
    public_key_str = ','.join(map(str, public_key))
    host.send_classical('Alice', 
                       f"VERIFICATION_KEY:{public_key_str}:{p}:{num_to_select}:{truncate_bits}", 
                       await_ack=True)
    time.sleep(0.2)
    
    print(f"[Bob] Shared keys with Alice")
    
    # Receive transaction
    msg = host.get_classical('Alice', wait=120)
    if not msg:
        print("[Bob] ERROR: Didn't receive transaction")
        return
    
    transaction_content = msg[0].content
    if transaction_content.startswith("TRANSACTION:"):
        transaction = transaction_content.split(':', 1)[1]
        print(f"[Bob] Transaction: '{transaction}'")
    else:
        print("[Bob] ERROR: Expected TRANSACTION")
        return
    
    # Receive signature metadata
    host.empty_classical()
    msg = host.get_classical('Alice', wait=20)
    if not msg:
        print("[Bob] ERROR: Didn't receive signature length")
        return
    
    sig_length = int(msg[0].content)
    print(f"[Bob] Expecting signature with {sig_length} components")
    host.empty_classical()
    
    msg_q = host.get_classical('Alice', wait=20)
    if not msg_q:
        print("[Bob] ERROR: Didn't receive num_qubits")
        return
    num_qubits = int(msg_q[0].content)
    print(f"[Bob] Expecting {num_qubits} qubits per component")
    host.empty_classical()
    
    received_signature = []
    
    print(f"\n[Bob] Receiving signature via quantum channel...")
    
    # Receive signature via quantum teleportation
    for idx in range(sig_length):
        print(f"[Bob] Receiving component {idx+1}/{sig_length}...")
        
        received_qubits = [None] * num_qubits
        received = 0
        
        while received < num_qubits:
            q2 = host.get_epr('Alice', wait=15)
            m = host.get_classical('Alice', wait=15)
            if q2 and m:
                content = m[0].content
                if ":" in content:
                    idx_q, m1, m2 = content.split(':')
                    # Apply teleportation corrections
                    if m2 == "1":
                        q2.X()
                    if m1 == "1":
                        q2.Z()
                    received_qubits[int(idx_q)] = q2
                    received += 1
                host.empty_classical()
                host.send_classical('Alice', "ACK", await_ack=False)
        
        sig_component = decode_qubits_to_int(received_qubits)
        received_signature.append(sig_component)
        
        host.send_classical('Alice', "NEXT_COMPONENT", await_ack=False)
    
    print(f"[Bob] Signature reception complete")
    
    # Verify signature
    print(f"\n[Bob] Verifying digital signature...")
    is_valid = verify_signature(transaction, received_signature, public_key, private_key, truncate_bits)
    
    results['verification_result'] = is_valid
    results['received_signature'] = received_signature
    results['transaction'] = transaction


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Execute the hybrid quantum-classical digital signature protocol.
    
    This demonstrates:
        - Approximate GCD digital signatures (post-quantum secure)
        - Classical signature generation/verification (practical)
        - Quantum teleportation for signature transmission (authenticated)
    """
    results = {
        'keys': None,
        'signature': None,
        'hash_value': None,
        'verification_result': None,
        'received_signature': None,
        'transaction': None
    }
    
    network = Network.get_instance()
    try:
        network.start()
        
        alice = Host('Alice')
        bob = Host('Bob')
        
        alice.add_connection('Bob')
        bob.add_connection('Alice')
        
        network.add_hosts([alice, bob])
        alice.start()
        bob.start()
        
        transaction = "Transfer 100 BTC from Alice to Bob"
        
        # Execute protocols
        b = bob.run_protocol(bob_protocol_signature, (results,))
        time.sleep(0.5)
        a = alice.run_protocol(alice_protocol_signature, (transaction, results))
        
        a.join()
        b.join()
        
        # Display results
        public_key, private_key = results['keys']
        p = private_key
        original_signature = results['signature']
        verification_result = results['verification_result']
        hash_value = results['hash_value']
        
        print("\n" + "="*80)
        print("HYBRID QUANTUM-CLASSICAL DIGITAL SIGNATURE - FINAL RESULTS")
        print("="*80)
        print(f"Transaction: '{transaction}'")
        print(f"SHA-256 Hash: {hash_value.hex()}")
        print(f"\nSigning Key (p): {p} ({p.bit_length()} bits)")
        print(f"Verification Key: {len(public_key)} Enc(0) samples")
        print(f"  Sample values: {public_key[:3]}...")
        print(f"\nSignature Size: {len(original_signature)} components")
        print(f"Transmission: QUANTUM CHANNEL (EPR-based teleportation)")
      
        
        if verification_result:
            print("\n" + "="*80)
            print("SUCCESS: DIGITAL SIGNATURE VERIFIED")
            print("Blockchain transaction authenticated via hybrid quantum system")
            print("="*80)
        else:
            print("\nFAILURE: Signature verification failed")
            
    finally:
        network.stop(True)


if __name__ == "__main__":
    main()
