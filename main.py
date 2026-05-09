# Модель: Математичне моделювання перехідних процесів в електричному ланцюзі (RLC) (5 семестр)
# Автор: Борейчук Б.М., група АІ-235

from flask import Flask, request, jsonify
import numpy as np
from scipy.integrate import odeint

app = Flask(__name__)

class TransientModel:
    def __init__(self, R, L, C):
        self.R = R
        self.L = L
        self.C = C

    def system_equations(self, state, t, E_func):
        i, u_c = state
        E_val = E_func(t)
        didt = (E_val - self.R * i - u_c) / self.L
        ducdt = i / self.C
        return [didt, ducdt]

    def solve(self, t_span, initial_cond, E_func):
        return odeint(self.system_equations, initial_cond, t_span, args=(E_func,))

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True) or {}

    R = float(data.get('R', 10.0))
    L = float(data.get('L', 0.1))
    C = float(data.get('C', 0.001))

    model = TransientModel(R, L, C)
    t = np.linspace(0, 0.1, 50)
    initial_state = [0.0, 0.0]
    solution = model.solve(t, initial_state, lambda t: 100.0)

    final_current, final_voltage = solution[-1]

    return jsonify({
        "input": {
            "R": R,
            "L": L,
            "C": C
        },
        "result": {
            "current_i": round(final_current, 4),
            "voltage_uC": round(final_voltage, 4)
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)