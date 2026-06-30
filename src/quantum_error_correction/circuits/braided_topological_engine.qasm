OPENQASM 3.0;
include "stdgates.inc";

qubit[5] q;
bit[10] syndrome;

reset q;
h q[4];

// Step 0
cx q[0], q[4];
cx q[1], q[4];
barrier q;
syndrome[0] = measure q[4];

if (syndrome[0] == true) {
    x q[0];
}

// Step 1
cx q[1], q[4];
cx q[2], q[4];
barrier q;
syndrome[1] = measure q[4];

if (syndrome[1] == true) {
    x q[1];
}

// Step 2
cx q[2], q[4];
cx q[3], q[4];
barrier q;

syndrome[9] = measure q[4];
// The 'output' keyword is removed for compatibility.   
