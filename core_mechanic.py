import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import get_candles
import get_portfolio
from datetime import datetime
import time
import threading
from tinkoff.invest import OperationType
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
import numpy as np

# Global variables
running = False
price_history = []
max_history_length = 50000

# Configuration
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Style configuration
bg_color = '#2D2D2D'
text_color = '#FFFFFF'
accent_green = '#2ECC71'
accent_red = '#E74C3C'
entry_bg = '#404040'
plot_bg = '#1E1E1E'

# GUI elements
root = None
interval_var = None
increase_var = None
decrease_var = None
instrument_var = None  # Новая переменная для INSTRUMENT
info_text = None
status_bar = None
canvas = None
ax = None
fig = None


def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('Dark.TFrame', background=bg_color)
    style.configure('Dark.TLabel', background=bg_color,
                    foreground=text_color, font=('Segoe UI', 10))
    style.configure('Dark.TEntry', fieldbackground=entry_bg,
                    foreground=text_color, borderwidth=2)
    style.configure('Dark.TButton', background='#404040',
                    foreground=text_color, font=('Segoe UI', 10, 'bold'),
                    borderwidth=0)
    style.map('Dark.TButton',
              background=[('active', '#505050'), ('disabled', '#303030')],
              foreground=[('active', text_color), ('disabled', '#808080')])

    style.configure('Green.TButton', background=accent_green,
                    foreground=text_color)
    style.map('Green.TButton',
              background=[('active', '#27AE60'), ('disabled', '#1E8449')])

    style.configure('Red.TButton', background=accent_red,
                    foreground=text_color)
    style.map('Red.TButton',
              background=[('active', '#C0392B'), ('disabled', '#922B21')])


def create_widgets():
    global interval_var, increase_var, decrease_var, instrument_var, info_text, status_bar

    # Control Frame
    control_frame = ttk.Frame(root, style='Dark.TFrame')
    control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Variables
    interval_var = tk.IntVar(value=5)
    increase_var = tk.DoubleVar(value=1.0)
    decrease_var = tk.DoubleVar(value=1.0)
    instrument_var = tk.StringVar(value='e6123145-9665-43e0-8413-cd61b8aa9b13')  # Инициализация переменной

    # Entries
    ttk.Label(control_frame, text="Interval (sec):", style='Dark.TLabel'
              ).grid(row=0, column=0, padx=10, pady=10)
    interval_entry = ttk.Entry(control_frame, textvariable=interval_var,
                               style='Dark.TEntry', width=10)
    interval_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(control_frame, text="Price Increase (%):", style='Dark.TLabel'
              ).grid(row=1, column=0, padx=10, pady=10)
    increase_entry = ttk.Entry(control_frame, textvariable=increase_var,
                               style='Dark.TEntry', width=10)
    increase_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(control_frame, text="Price Decrease (%):", style='Dark.TLabel'
              ).grid(row=2, column=0, padx=10, pady=10)
    decrease_entry = ttk.Entry(control_frame, textvariable=decrease_var,
                               style='Dark.TEntry', width=10)
    decrease_entry.grid(row=2, column=1, padx=10, pady=10)

    # Добавляем поле для INSTRUMENT
    ttk.Label(control_frame, text="Instrument ID:", style='Dark.TLabel'
              ).grid(row=3, column=0, padx=10, pady=10)
    instrument_entry = ttk.Entry(control_frame, textvariable=instrument_var,
                                 style='Dark.TEntry', width=36)
    instrument_entry.grid(row=3, column=1, padx=10, pady=10)

    # Buttons
    start_btn = ttk.Button(control_frame, text="Start", style='Green.TButton',
                           command=start_trading)
    start_btn.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

    stop_btn = ttk.Button(control_frame, text="Stop", style='Red.TButton',
                          command=stop_trading, state=tk.DISABLED)
    stop_btn.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

    # Info Text
    info_text = scrolledtext.ScrolledText(control_frame, height=15,
                                          state='disabled', bg=entry_bg,
                                          fg=text_color, insertbackground=text_color,
                                          font=('Segoe UI', 9))
    info_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Status Bar
    status_bar = ttk.Label(control_frame, text="Status: Stopped",
                           style='Dark.TLabel', anchor=tk.W, padding=(5, 2, 0, 2))
    status_bar.grid(row=6, column=0, columnspan=2, sticky="ew")

    # Configure grid weights
    control_frame.grid_rowconfigure(5, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)


def setup_plot():
    global fig, ax, canvas

    plot_frame = ttk.Frame(root, style='Dark.TFrame')
    plot_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

    fig = plt.Figure(figsize=(5, 4), dpi=100, facecolor=plot_bg)
    ax = fig.add_subplot(111)
    ax.set_facecolor(plot_bg)

    # Configure plot colors
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.title.set_color(text_color)
    for spine in ax.spines.values():
        spine.set_color(text_color)

    ax.set_title('Price History')
    ax.set_xlabel('Time Steps')
    ax.set_ylabel('Price')

    # Создаем градиент с использованием imshow
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    ax.imshow(
        gradient,
        aspect='auto',
        cmap=plt.get_cmap('Blues'),
        extent=(0, 1, 0, 0.3),  # Градиент на 30% высоты снизу
        alpha=0.2,
        transform=ax.transAxes
    )

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().configure(bg=bg_color)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def log_transaction(action: str, price: float):
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action} order at price {price:.10f}\n"
    with open('trades.log', 'a') as log_file:
        log_file.write(log_entry)
    update_info(f"Transaction logged: {action} at {price:.2f}")


def update_info(message: str):
    info_text.configure(state='normal')
    info_text.insert(tk.END, message + "\n")
    info_text.see(tk.END)
    info_text.configure(state='disabled')


def update_status(status: str):
    status_bar.config(text=f"Status: {status}")


def validate_inputs():
    try:
        int(interval_var.get())
        float(increase_var.get())
        float(decrease_var.get())
        return True
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values")
        return False


def start_trading():
    global running
    if not validate_inputs():
        return

    running = True
    update_status("Running")

    # Enable Stop button and disable Start button
    control_frame = root.grid_slaves(row=0, column=0)[0]
    stop_btn = control_frame.grid_slaves(row=4, column=1)[0]
    start_btn = control_frame.grid_slaves(row=4, column=0)[0]
    stop_btn.config(state=tk.NORMAL)
    start_btn.config(state=tk.DISABLED)

    trading_thread = threading.Thread(target=trading_loop, daemon=True)
    trading_thread.start()


def stop_trading():
    global running
    running = False
    update_status("Stopped")

    # Enable Start button and disable Stop button
    control_frame = root.grid_slaves(row=0, column=0)[0]
    stop_btn = control_frame.grid_slaves(row=4, column=1)[0]
    start_btn = control_frame.grid_slaves(row=4, column=0)[0]
    stop_btn.config(state=tk.DISABLED)
    start_btn.config(state=tk.NORMAL)


def trading_loop():
    FIGI = 'BBG004730N88'

    while running:
        start_time = time.time()

        try:
            # Получаем текущее значение INSTRUMENT из переменной
            INSTRUMENT = instrument_var.get()

            get_candles.last_price()
            ops_list = get_candles.get_orders()
            operations_obj = get_portfolio.get_ops()

            rub_sv = operations_obj[0].units
            kop_sv = operations_obj[0].nano
            price_order = rub_sv + (kop_sv * 0.000000001)

            rub = get_candles.rub
            kop = get_candles.kop
            current_price = rub + (kop * 0.000000001)

            root.after(0, update_display, operations_obj, current_price, price_order)

            if operations_obj[1] == OperationType.OPERATION_TYPE_BUY:
                target_sell = price_order * (1 + increase_var.get() / 100)
                if target_sell <= current_price and not ops_list.orders:
                    get_candles.order_send_sell()
                    root.after(0, log_transaction, 'SELL', target_sell)

            elif operations_obj[1] == OperationType.OPERATION_TYPE_SELL:
                target_buy = price_order * (1 - decrease_var.get() / 100)
                if target_buy >= current_price and not ops_list.orders:
                    get_candles.order_send()
                    root.after(0, log_transaction, 'BUY', target_buy)

        except Exception as e:
            root.after(0, handle_error, e)

        elapsed = time.time() - start_time
        sleep_time = max(0, interval_var.get() - elapsed)
        time.sleep(sleep_time)


def update_display(operations_obj, current_price, price_order):
    global price_history

    # Update price history
    price_history.append(current_price)
    if len(price_history) > max_history_length:
        price_history.pop(0)

    # Update plot
    ax.clear()
    ax.plot(price_history, color=accent_green)
    ax.set_title('Price History')
    ax.set_xlabel('Time Steps')
    ax.set_ylabel('Price')
    canvas.draw()

    # Update info
    info = (
        f"Last operation: {'BUY' if operations_obj[1] == 15 else 'SELL' if operations_obj[1] == 22 else 'UNKNOWN'}\n"
        f"Current price: {current_price:.4f}\n"
        f"Last order price: {price_order:.4f}\n"
        f"Target sell: {price_order * (1 + increase_var.get() / 100):.4f}\n"
        f"Target buy: {price_order * (1 - decrease_var.get() / 100):.4f}\n"
        "----------------------------------------"
    )
    update_info(info)


def handle_error(error):
    update_info(f"Error: {str(error)}")
    messagebox.showerror("Error", str(error))


def main():
    global root

    root = tk.Tk()
    root.title("Trading Bot")
    root.geometry("1200x600")
    root.configure(bg=bg_color)

    setup_styles()
    create_widgets()
    setup_plot()

    # Configure grid weights
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    root.mainloop()


if __name__ == "__main__":
    main()