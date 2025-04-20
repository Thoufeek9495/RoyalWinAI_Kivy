# ai_coach_app.py
# ✅ Final Version: Integrated Dice Pattern Engine + Quantum Predictor + Archive Memory + Visual Pattern Base

import statistics
from collections import Counter
import datetime
import json
import os

# --- Classification ---
def classify_odd_even(num):
    return "Odd" if num % 2 != 0 else "Even"

def count_distribution():
    odds = len([x for x in range(3, 19) if classify_odd_even(x) == "Odd"])
    evens = len([x for x in range(3, 19) if classify_odd_even(x) == "Even"])
    return odds, evens

# --- Dice Simulation Tools ---
def decompose_dice_sum(total):
    results = []
    for i in range(1, 7):
        for j in range(1, 7):
            for k in range(1, 7):
                if i + j + k == total:
                    results.append((i, j, k))
    return results

def most_common_faces(triples):
    flat = [num for tup in triples for num in tup]
    return Counter(flat).most_common(3)

# --- Pattern Tools ---
def detect_trend_direction(data):
    if len(data) < 3:
        return "Unclear"
    increasing = sum(1 for i in range(1, len(data)) if data[i] > data[i-1])
    decreasing = sum(1 for i in range(1, len(data)) if data[i] < data[i-1])
    if increasing > decreasing:
        return "Ascending"
    elif decreasing > increasing:
        return "Descending"
    else:
        return "Mixed"

def simulate_entropy(data):
    if len(data) < 10:
        return "Even", 50
    chunks = [data[i:i+5] for i in range(0, len(data)-4)]
    odd_runs = sum(1 for chunk in chunks if all(classify_odd_even(x) == "Odd" for x in chunk))
    even_runs = sum(1 for chunk in chunks if all(classify_odd_even(x) == "Even" for x in chunk))
    if odd_runs > even_runs:
        return "Even", 55
    elif even_runs > odd_runs:
        return "Odd", 55
    return classify_odd_even(data[-1]), 50

def analyze_prediction_log(prediction_log):
    if len(prediction_log) < 6:
        return "Stable"
    transitions = [1 if prediction_log[i] != prediction_log[i-1] else 0 for i in range(1, len(prediction_log))]
    switches = sum(transitions)
    if switches >= len(transitions) * 0.75:
        return "High Volatility"
    elif switches <= len(transitions) * 0.25:
        return "Strong Bias"
    return "Alternating"

def build_heatmap(memory):
    freq = Counter(memory)
    hot_numbers = freq.most_common(5)
    return hot_numbers

def calculate_gap_patterns(data):
    return [data[i] - data[i-1] for i in range(1, len(data))] if len(data) >= 2 else []

def estimate_cycle_window():
    now = datetime.datetime.now()
    return f"{now.hour}:{now.minute // 10 * 10}"

# --- Persistent Archive Engine ---
ARCHIVE_PATH = "results_archive.json"

def load_archive():
    if os.path.exists(ARCHIVE_PATH):
        try:
            with open(ARCHIVE_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Archive corrupted. Starting fresh.")
            return []
    return []

def save_to_archive(result):
    archive = load_archive()
    archive.append({"time": datetime.datetime.now().isoformat(), "value": result})
    with open(ARCHIVE_PATH, 'w') as f:
        json.dump(archive, f)

def archive_match_score(recent, archive):
    matches = []
    for i in range(len(archive) - len(recent)):
        window = [item['value'] for item in archive[i:i+len(recent)]]
        if window == recent:
            try:
                next_value = archive[i + len(recent)]['value']
                matches.append(next_value)
            except:
                continue
    if not matches:
        return None, 0
    guess = Counter(matches).most_common(1)[0][0]
    score = round((len(matches) / len(archive)) * 100, 2)
    return guess, score

# --- AI Coach Core ---
class AICoach:
    def __init__(self):
        self.memory = []
        self.stake_plan = [10, 20, 35, 60, 90, 140, 210, 300]
        self.total_profit = 0
        self.balance = 1000
        self.current_round = 0
        self.win_log = []
        self.loss_log = []
        self.prediction_log = []
        self.odd_even_stats = count_distribution()
        self.last_prediction = None
        self.last_predicted_number = None
        self.cycle_log = {}
        self.entropy_shift_log = []

    def learn(self, result):
        self.memory.append(result)
        if len(self.memory) > 100:
            self.memory.pop(0)

        cycle = estimate_cycle_window()
        if cycle not in self.cycle_log:
            self.cycle_log[cycle] = []
        self.cycle_log[cycle].append(result)

        if len(self.memory) >= 12:
            last_chunk = self.memory[-6:]
            prior_chunk = self.memory[-12:-6]
            last_odd = sum(1 for x in last_chunk if classify_odd_even(x) == "Odd")
            prior_odd = sum(1 for x in prior_chunk if classify_odd_even(x) == "Odd")
            if abs(last_odd - prior_odd) >= 5:
                self.entropy_shift_log.append((cycle, f"Entropy jump detected: {prior_odd} ➝ {last_odd}"))

        save_to_archive(result)

    def get_streak_info(self):
        if len(self.memory) < 4:
            return "Stable"
        last = [classify_odd_even(x) for x in self.memory[-4:]]
        if all(x == last[0] for x in last):
            return "Strong Repetition"
        elif last[-1] != last[-2] != last[-3]:
            return "Flip Potential"
        return "Mixed"

    def quantum_guess_range(self):
        if not self.memory:
            return [10, 11, 12]
        avg = round(statistics.mean(self.memory[-10:]))
        return [avg-1, avg, avg+1]

    def predict_next(self, history=None):
        data = history if history else self.memory[-30:]
        if len(data) < 10:
            return "Even", 50, 10, "Not enough data yet"

        trends = [classify_odd_even(x) for x in data]
        odd_count = trends.count("Odd")
        even_count = trends.count("Even")

        prediction = "Odd" if odd_count > even_count else "Even"
        confidence = 55 + abs(odd_count - even_count) * 2

        entropy_prediction, entropy_conf = simulate_entropy(data)
        if entropy_conf > confidence:
            prediction = entropy_prediction
            confidence = entropy_conf

        reverse_applied = False
        if len(data) >= 3 and all(classify_odd_even(x) == trends[-1] for x in data[-3:]):
            prediction = "Even" if prediction == "Odd" else "Odd"
            confidence -= 5
            reverse_applied = True

        parity_filtered = [x for x in data if classify_odd_even(x) == prediction]
        hot_number = Counter(parity_filtered).most_common(1)[0][0] if parity_filtered else 10
        self.last_predicted_number = hot_number

        quantum_range = self.quantum_guess_range()
        quantum_filtered = [x for x in quantum_range if classify_odd_even(x) == prediction]
        direction = detect_trend_direction(data)
        streak = self.get_streak_info()
        quantum_pattern = analyze_prediction_log(self.prediction_log)
        heatmap = build_heatmap(self.memory)
        gaps = calculate_gap_patterns(data[-6:])
        gap_pattern = f"Recent Gaps: {gaps}"

        archive = load_archive()
        archive_guess, archive_score = archive_match_score(data[-10:], archive)

        decomposed = decompose_dice_sum(hot_number)
        face_clues = most_common_faces(decomposed)

        reason = (
            f"Analyzed last {len(data)} results. Hot: {hot_number}. Trend: {prediction}.\n"
            f"Reverse logic: {'Yes' if reverse_applied else 'No'} | Pattern: {direction} | Streak: {streak}\n"
            f"Entropy Simulated: {entropy_prediction} ({entropy_conf}%) | Pattern Trend: {quantum_pattern}\n"
            f"Quantum Range: {quantum_filtered} | Heatmap Top: {heatmap}\n"
            f"{gap_pattern} | Cycle: {estimate_cycle_window()}\n"
            f"🎲 Dice Clue (hot={hot_number}): {face_clues} | Archive Suggestion: {archive_guess} ({archive_score}%)"
        )

        self.last_prediction = prediction
        self.prediction_log.append(prediction)
        return prediction, min(confidence, 95), archive_guess or hot_number, reason

    def evaluate_result(self, actual_result):
        actual_parity = classify_odd_even(actual_result)
        prediction = self.last_prediction or self.predict_next()[0]
        total_losses = sum(self.stake_plan[min(i, len(self.stake_plan) - 1)] for i in range(self.current_round + 1))
        target_profit = 10
        stake = total_losses + target_profit if self.current_round > 0 else self.stake_plan[0]

        win = prediction.lower() == actual_parity.lower()

        if win:
            self.balance += stake
            self.total_profit += (stake - total_losses)
            self.win_log.append(actual_result)
            self.current_round = 0
        else:
            self.balance -= stake
            self.total_profit -= stake
            self.loss_log.append(actual_result)
            self.current_round += 1

        self.learn(actual_result)
        return win, stake, self.current_round

    def get_summary(self):
        total_predictions = len(self.win_log) + len(self.loss_log)
        accuracy = round((len(self.win_log) / total_predictions) * 100, 2) if total_predictions else 0
        return {
            "wins": len(self.win_log),
            "losses": len(self.loss_log),
            "profit": self.total_profit,
            "balance": self.balance,
            "accuracy": accuracy
        }

    def next_stake(self):
        total_losses = sum(self.stake_plan[min(i, len(self.stake_plan) - 1)] for i in range(self.current_round + 1))
        return total_losses + 10 if self.current_round > 0 else self.stake_plan[0]

    def next_after_loss(self):
        return self.next_stake()

# ✅ Test mode (optional)
if __name__ == "__main__":
    coach = AICoach()
    print("✅ AICoach module loaded successfully.")
