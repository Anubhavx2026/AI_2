import numpy as np

# Define probabilities from the Bayesian Belief Network (BBN)
P_X = {"yes": 0.8, "no": 0.2}  # Probability for X (Expertise)
P_Y = {"yes": 0.5, "no": 0.5}  # Probability for Y (Knowledge)
P_Z_given_X_Y = {  # Probability for Z (Performance) given X and Y
    ("yes", "yes"): {"Excellent": 0.9, "Average": 0.1},
    ("yes", "no"): {"Excellent": 0.7, "Average": 0.3},
    ("no", "yes"): {"Excellent": 0.6, "Average": 0.4},
    ("no", "no"): {"Excellent": 0.3, "Average": 0.7},
}
P_W_given_Z = {  # Probability for W (Workshop Participation) given Z
    "Excellent": {"yes": 0.8, "no": 0.2},
    "Average": {"yes": 0.2, "no": 0.8},
}
P_T_given_Z = {  # Probability for T (Training Program) given Z
    "Excellent": {"yes": 0.7, "no": 0.3},
    "Average": {"yes": 0.3, "no": 0.7},
}

# Monte Carlo Simulation Function
def simulate_bbn(target, conditions, num_iterations=10000):
    match_target = 0
    evidence_matches = 0

    for _ in range(num_iterations):
        # Sample X (Expertise)
        X = np.random.choice(["yes", "no"], p=[P_X["yes"], P_X["no"]])

        # Sample Y (Knowledge)
        Y = np.random.choice(["yes", "no"], p=[P_Y["yes"], P_Y["no"]])

        # Sample Z (Performance) based on X and Y
        Z_probabilities = P_Z_given_X_Y[(X, Y)]
        Z = np.random.choice(["Excellent", "Average"], p=[Z_probabilities["Excellent"], Z_probabilities["Average"]])

        # Sample W (Workshop Participation) based on Z
        W_probabilities = P_W_given_Z[Z]
        W = np.random.choice(["yes", "no"], p=[W_probabilities["yes"], W_probabilities["no"]])

        # Sample T (Training Program) based on Z
        T_probabilities = P_T_given_Z[Z]
        T = np.random.choice(["yes", "no"], p=[T_probabilities["yes"], T_probabilities["no"]])

        # Check if evidence matches the sampled values
        evidence_valid = True
        for node, value in conditions.items():
            if locals()[node] != value:
                evidence_valid = False
                break

        # Update counts based on evidence validity
        if evidence_valid:
            evidence_matches += 1
            if locals()[target] == "yes":
                match_target += 1

    # Calculate conditional probability
    if evidence_matches == 0:
        return 0  # Avoid division by zero
    return match_target / evidence_matches

# Example: Compute P(T = yes | X = yes, Y = no)
target_variable = "T"
given_conditions = {"X": "yes", "Y": "no"}
calculated_probability = simulate_bbn(target_variable, given_conditions)

print(f"Estimated P(T = yes | X = yes, Y = no): {calculated_probability}")
