import streamlit as st
from qiskit import IBMQ, QuantumCircuit, transpile
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor

def run_ibmq_circuit(api_token):
    # Save and load IBMQ account
    IBMQ.save_account(api_token, overwrite=True)
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    
    # Get the least busy backend with at least 5 qubits
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 5 and not x.configuration().simulator and x.status().operational==True))
    st.write("Least busy backend:", backend)

    # Create a simple quantum circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Transpile the circuit for the chosen backend
    transpiled_qc = transpile(qc, backend)

    # Run the job on the least busy backend
    job = backend.run(transpiled_qc)
    job_monitor(job)

    # Get the result
    result = job.result()
    counts = result.get_counts(qc)
    st.write("Result:", counts)

st.title("Quantum AI on Streamlit")

api_token = st.text_input("Enter your IBMQ API token:", type="password")

if st.button("Run Quantum Circuit"):
    if api_token:
        run_ibmq_circuit(api_token)
    else:
        st.error("Please enter your IBMQ API token.")
