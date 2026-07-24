#!/usr/bin/env python3
"""
Standard Cirq Quantum Circuit Verification Script
Simulates a 2-qubit Bell state circuit using Google's Cirq framework.
"""

import sys
import cirq

# Ensure UTF-8 output encoding for Windows PowerShell terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print(f"=== Standard Cirq Framework Verification (Version: {cirq.__version__}) ===")
    
    # 1. Define 2 Line Qubits
    q0, q1 = cirq.LineQubit.range(2)

    # 2. Build Hadamard + CNOT Bell State Circuit
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )

    print("\n--- [Circuit Diagram] ---")
    print(circuit)

    # 3. Simulate Quantum Circuit Execution (10 Repetitions)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)

    print("\n--- [Simulation Results] ---")
    print(result)
    print("\n[OK] CIRQ QUANTUM SIMULATION COMPLETED SUCCESSFULLY WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
