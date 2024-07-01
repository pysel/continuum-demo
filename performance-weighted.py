import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initial sector data
token_amounts = {
    "BTC": 100000,
    "SOL": 100000,
    "ETH": 100000
}

token_weights = {
    "BTC": 1/3,
    "SOL": 1/3,
    "ETH": 1/3
}

userSupply = 0
userValue = 0

indexSupply = 1000

def provide_action():
    global token_weights, token_amounts, indexSupply, userSupply
    
    token = token_input.get()  # Get the value from the Token In input field
    amount = int(amount_input.get())  # Get the value from the Amount In input field

    # Update the sector data based on input (this example assumes a simple update mechanism)
    if token not in token_amounts:
        messagebox.showerror("Error", "Invalid token value")
        return
    
    if amount < 0: # if amount is negative, simply remove from supply
        token_amounts[token] += amount
        update_chart()
        update_token_amounts()
        return

    w = token_weights[token]
    addedFraction = amount / token_amounts[token]
    if addedFraction >= 1:
        messagebox.showerror("Error", "Too much token provided, Disallowed!")
        return
    
    wPrime = w * (1 - addedFraction)
    freed = w * addedFraction
    distributeWeight(freed, token)
    token_weights[token] = wPrime
    print(token_weights)
    
    q = ((token_amounts[token] + amount) / token_amounts[token]) ** wPrime - 1
    
    ttcOut = q * indexSupply
    indexSupply += ttcOut
    userSupply += ttcOut
    
    token_amounts[token] += amount  # Update the sector data based on the input
    
    update_chart()  # Update the pie chart when the "Provide" button is pressed
    update_token_amounts()  # Update the token amounts display
    messagebox.showinfo("Provided Successfully", f"Received ttc: {ttcOut:.5f}")

def redeem_action():
    global token_weights, token_amounts, indexSupply, userSupply, userValue
    
    token = token_out_entry.get()  # Get the value from the Token Out input field
    ttc = float(ttc_out_entry.get())  # Get the value from the TTC Out input field
    
    if token not in token_amounts:
        messagebox.showerror("Error", "Invalid token value")
        return
    
    if ttc < 0:
        messagebox.showerror("Error", "Invalid TTC value")
        return
    
    frac = ttc / indexSupply
    
    wPrime = token_weights[token] * (1 + frac)
    added = token_weights[token] * frac
    
    distributeWeight(-added, token)
    
    par = (1 - frac) ** (1 / wPrime)
    
    left = token_amounts[token] * par
    earned = token_amounts[token] - left
    
    token_amounts[token] = left
    
    indexSupply -= ttc
    userSupply -= ttc
    
    userValue += earned
    
    update_chart()
    update_token_amounts()
    
    messagebox.showinfo("Redeemed Successfully", f"Received {token}: {earned:.5f}")
    
    
def distributeWeight(freed, _from):
    global token_weights
    
    full = sum(token_weights[token] for token in token_weights if token != _from)
    if full == 0:
        return

    for token in token_weights:
        if token == _from:
            continue
        token_weights[token] += token_weights[token] / full * freed # distribute the freed weight to other tokens based on their weights
        
    return
    
def add_liquidity_action():
    global token_amounts
    token_amounts["BTC"] += 100
    token_amounts["ETH"] += 100
    token_amounts["SOL"] += 100
    
    update_chart()  # Update the pie chart when the "Add Liquidity" button is pressed
    update_token_amounts()  # Update the token amounts display

def nullify_user_supply():
    global userSupply, userValue
    userSupply = 0
    userValue = 0
    update_token_amounts()
    
def func(pct, allvals):
    absolute = int(pct/100.*sum(allvals))
    return "{:.5f}".format(absolute)

def update_chart():
    # Extract the keys and values from the dictionary
    sector_names = list(token_weights.keys())
    sector_values = list(token_weights.values())
    
    # Clear the previous pie chart
    ax.clear()
    # Create a new pie chart
    ax.pie(sector_values, labels=sector_names, autopct=lambda pct: "{:.5f}".format(pct/100*sum(sector_values)))
    # Draw the updated chart
    canvas.draw()

def update_token_amounts():
    amounts_text = "\n".join([f"{token}: ${amount}" for token, amount in token_amounts.items()])
    supply_text = f"Total Supply: {indexSupply:.1f} \nSingle Token Worth: ${computeValueOfSingleIndex()}"
    user_supply_text = f"User's Supply: {userSupply:.5f}"
    user_fraction_of_total = userSupply / indexSupply
    token_amounts_label.config(text="Stats: \n" + amounts_text + "\n" + supply_text + "\n\n" + user_supply_text + "\n" + f"User's Fraction of Total Supply: {user_fraction_of_total:.5f}" + "\n\nUser's Value: " + f"${userValue:.5f}")

def computeValueOfSingleIndex():
    total = sum(token_amounts.values())
    value = total / indexSupply
    return value

def exit_with_user_supply():
    global userSupply, indexSupply
    frac = userSupply / indexSupply
    sum = 0
    for token in token_amounts:
        sum += token_amounts[token] * frac
        token_amounts[token] = token_amounts[token] * (1 - frac)
    
    indexSupply -= userSupply
    userSupply = 0
    update_chart()
    update_token_amounts()
    messagebox.showinfo("Exited Successfully", f"Received ${sum:.5f}")
    
# Create the main window
root = tk.Tk()
root.title("Continuum Demo")

# Set the window size
root.geometry("1400x1000")

# Create and place the "Token In" label
token_label = tk.Label(root, text="Token In:")
token_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Create and place the Token In input field
token_input = tk.Entry(root)
token_input.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Create and place the "Amount In" label
amount_label = tk.Label(root, text="Amount In:")
amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Create and place the Amount In input field
amount_input = tk.Entry(root)
amount_input.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Create and place the "Provide" button
provide_button = tk.Button(root, text="Provide", command=provide_action)
provide_button.grid(row=2, column=0, columnspan=2, pady=20)

# Create and place the "Add Liquidity" button
add_liquidity_button = tk.Button(root, text="Add Liquidity", command=add_liquidity_action)
add_liquidity_button.grid(row=3, column=0, columnspan=2, pady=10)

nullify_user_supply_button = tk.Button(root, text="Nullify User", command=nullify_user_supply)
nullify_user_supply_button.grid(row=5, column=0, columnspan=2, pady=10)

exit_with_user_supply_button = tk.Button(root, text="Exit with User Supply", command=exit_with_user_supply)
exit_with_user_supply_button.grid(row=3, column=2, columnspan=2, pady=10)

# Create a label to display token amounts
token_amounts_label = tk.Label(root, text="", justify="left")
token_amounts_label.grid(row=4, column=0, columnspan=2, pady=10)

# COL 2
token_out_label = tk.Label(root, text="Token Out:")
token_out_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

token_out_entry = tk.Entry(root)
token_out_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

ttc_out = tk.Label(root, text="TTC Out:")
ttc_out.grid(row=1, column=2, padx=10, pady=5, sticky="w")

ttc_out_entry = tk.Entry(root)
ttc_out_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")

redeem_button = tk.Button(root, text="Redeem", command=redeem_action)
redeem_button.grid(row=2, column=2, columnspan=2, pady=20)

# Create a figure for the pie chart
fig = Figure(figsize=(4, 4))
ax = fig.add_subplot(111)
# Initial pie chart
sector_names = list(token_weights.keys())
sector_values = list(token_weights.values())
ax.pie(sector_values, labels=sector_names, autopct=lambda pct: "{:.5f}".format(pct/100*sum(sector_values)))

# Embed the pie chart in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=4, rowspan=8, padx=20, pady=20)

# Update the token amounts display initially
update_token_amounts()

# Run the main event loop
root.mainloop()
