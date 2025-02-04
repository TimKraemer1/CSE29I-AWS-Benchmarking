from flask import Flask, jsonify, request
import utils
import time

app = Flask(__name__)

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

@app.route('/primes/<int:n>', methods=['GET'])
def calculate_primes(n):
    if n <= 0:
        return jsonify({"error": "Input must be a positive number"}), 400
    limit = n
    start_time = time.time()
    primes = [n for n in range(2, limit + 1) if is_prime(n)]
    time_elapsed = time.time() - start_time
    return jsonify({"limit": limit,  "primes_found": len(primes), "time_taken": time_elapsed})

@app.route('/matrix-multiply', methods=['POST'])
def multiply_matrices():
    try:
        # Extract matrices from the JSON request
        data = request.get_json()
        matrix1 = np.array(data['matrix1'])
        matrix2 = np.array(data['matrix2'])

        # Check if matrices can be multiplied
        if matrix1.shape[1] != matrix2.shape[0]:
            return jsonify({'error': 'Matrices cannot be multiplied due to incompatible dimensions.'}), 400

        # Perform matrix multiplication
        result = np.matmul(matrix1, matrix2)

        # Convert the result to a list for JSON serialization
        result_list = result.tolist()

        return jsonify({'result': result_list}), 200
    except KeyError:
        return jsonify({'error': 'Invalid input. Please provide both matrix1 and matrix2 in the request body.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)