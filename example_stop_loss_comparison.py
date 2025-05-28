import pandas as pd
import sys

try:
    import matplotlib.pyplot as plt
    have_matplotlib = True
    print("Successfully imported matplotlib")
except Exception as e:
    have_matplotlib = False
    print(f"Error importing matplotlib: {e}")

# Example stocks with different volatility profiles
stocks = [
    {"name": "High Volatility Stock (e.g., TSLA)", "price": 100.0, "atr": 5.2},
    {"name": "Medium Volatility Stock (e.g., AAPL)", "price": 50.0, "atr": 1.5},
    {"name": "Low Volatility Stock (e.g., KO)", "price": 40.0, "atr": 0.6}
]

# Constants
FIXED_STOP_LOSS = -0.06  # Original 6% stop loss
ATR_MULTIPLIERS = [1.5, 2.0, 2.5]  # Different ATR multipliers to test

# Create a dataframe to store results
data = []

# Process each stock
for stock in stocks:
    name = stock["name"]
    price = stock["price"]
    atr = stock["atr"]
    atr_percent = (atr / price) * 100
    
    # Calculate fixed stop loss in dollars
    fixed_stop_loss_dollars = price * FIXED_STOP_LOSS
    
    print(f"\n{name}:")
    print(f"Price: ${price:.2f}")
    print(f"ATR: ${atr:.2f} ({atr_percent:.2f}%)")
    print(f"Fixed 6% Stop Loss: ${fixed_stop_loss_dollars:.2f} ({FIXED_STOP_LOSS*100:.2f}%)")
    
    # Calculate dynamic stop losses with different multipliers
    for multiplier in ATR_MULTIPLIERS:
        # ATR-based stop loss price
        stop_price = price - (atr * multiplier)
        
        # Convert to percentage for consistency
        stop_loss_percent = (stop_price / price) - 1
        
        # Limit maximum stop loss to prevent excessive risk
        max_stop_loss = -0.10  # Maximum 10% stop loss
        adjusted_stop_loss = max(stop_loss_percent, max_stop_loss)
        
        # Stop loss in dollars
        stop_loss_dollars = price * adjusted_stop_loss
        
        print(f"Dynamic Stop Loss ({multiplier}x ATR): ${stop_loss_dollars:.2f} ({adjusted_stop_loss*100:.2f}%)")
        
        # Store data for plotting
        data.append({
            'Stock': name,
            'Price': price,
            'ATR': atr,
            'ATR%': atr_percent,
            'Stop Type': f'{multiplier}x ATR',
            'Stop%': adjusted_stop_loss * 100,
            'StopDollars': stop_loss_dollars
        })
    
    # Add fixed stop loss data point
    data.append({
        'Stock': name,
        'Price': price,
        'ATR': atr,
        'ATR%': atr_percent,
        'Stop Type': 'Fixed 6%',
        'Stop%': FIXED_STOP_LOSS * 100,
        'StopDollars': fixed_stop_loss_dollars
    })

# Create dataframe
df = pd.DataFrame(data)

print("\n--- COMPARISON TABLE ---")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
print(df[['Stock', 'Price', 'ATR%', 'Stop Type', 'Stop%', 'StopDollars']])

# Output comparison to text file for easier viewing
with open('stop_loss_comparison_results.txt', 'w') as f:
    f.write("DYNAMIC ATR-BASED STOP LOSS COMPARISON\n")
    f.write("======================================\n\n")
    
    for stock in stocks:
        name = stock["name"]
        price = stock["price"]
        atr = stock["atr"]
        atr_percent = (atr / price) * 100
        
        f.write(f"{name}:\n")
        f.write(f"Price: ${price:.2f}\n")
        f.write(f"ATR: ${atr:.2f} ({atr_percent:.2f}%)\n")
        f.write(f"Fixed 6% Stop Loss: ${price * FIXED_STOP_LOSS:.2f} ({FIXED_STOP_LOSS*100:.2f}%)\n")
        
        for multiplier in ATR_MULTIPLIERS:
            stop_price = price - (atr * multiplier)
            stop_loss_percent = (stop_price / price) - 1
            max_stop_loss = -0.10
            adjusted_stop_loss = max(stop_loss_percent, max_stop_loss)
            stop_loss_dollars = price * adjusted_stop_loss
            
            f.write(f"Dynamic Stop Loss ({multiplier}x ATR): ${stop_loss_dollars:.2f} ({adjusted_stop_loss*100:.2f}%)\n")
        f.write("\n")
    
    f.write("\nKey Observations:\n")
    f.write("1. High volatility stocks get wider stops to account for normal price movement\n")
    f.write("2. Low volatility stocks get tighter stops to maximize profits\n")
    f.write("3. All stops are capped at maximum 10% loss to limit risk exposure\n")
    f.write("4. ATR-based stops adapt to each stock's actual price behavior\n")

print("Detailed results written to stop_loss_comparison_results.txt")

# Output as CSV
df.to_csv('stop_loss_comparison_example.csv', index=False)
print("\nResults saved to stop_loss_comparison_example.csv")

# Create a visualization
if have_matplotlib:
    try:
        print("Creating visualization...")
        plt.figure(figsize=(12, 8))
        
        for i, stock in enumerate(stocks):
            name = stock["name"].split(" (")[0]  # Extract just the volatility part
            stock_data = df[df['Stock'] == stock["name"]]
            
            # Extract values for plotting
            stop_types = stock_data['Stop Type']
            stop_percentages = stock_data['Stop%']
            
            # Plot position
            x_pos = [i + j*0.15 for j in range(len(stop_types))]
            plt.bar(x_pos, stop_percentages, width=0.1, alpha=0.7, label=name if i == 0 else "")
            
            # Add labels
            for j, (x, y, label) in enumerate(zip(x_pos, stop_percentages, stop_types)):
                if j == 0:
                    plt.text(x, y-0.5, f"{name}\n{label}", ha='center', va='bottom', fontsize=8)
                else:
                    plt.text(x, y-0.5, label, ha='center', va='bottom', fontsize=8)
        
        plt.axhline(y=FIXED_STOP_LOSS*100, linestyle='--', color='red', alpha=0.5, label='Fixed 6% Stop Loss')
        plt.axhline(y=-10, linestyle='--', color='black', alpha=0.5, label='Maximum 10% Stop Loss')
        
        plt.ylabel('Stop Loss Percentage (%)')
        plt.title('Comparison of Fixed vs. Dynamic ATR-Based Stop Losses')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Save the plot
        plt.savefig('stop_loss_comparison.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as stop_loss_comparison.png")
    except Exception as e:
        print(f"Could not create visualization: {str(e)}")
else:
    print("Skipping visualization as matplotlib is not available")
