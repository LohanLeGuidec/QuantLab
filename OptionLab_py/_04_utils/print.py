def print_strategy_results(title, results, params=None):
    print(f"\n--- {title} ---")

    if params is not None:
        print("Paramètres optimisés :")
        for key, value in params.items():
            print(f"  {key:<15} : {value}")

    for key, value in results.items():
        if hasattr(value, "item"):
            value = value.item()
        print(f"{key:<15} : {value:.4f}" if isinstance(value, float) else f"{key:<15} : {value}")