# Uber Wallet Tracker

A desktop application for Uber drivers to **track trips, earnings, and fuel usage**. Built with Python and Tkinter, it provides a simple interface for managing trip records, fuel logs, and generating financial reports.

---

## Features

- **Trip Management:**  
  - Add, edit, and delete Uber trip records.
  - Calculates earnings, discounts, fuel usage, and more.
  - Prevents duplicate trip entries.

- **Fuel Log Management:**  
  - Add, edit, and delete fuel refill records.
  - Calculates liters added and prevents refueling above tank capacity.

- **Reports & Summaries:**  
  - Generate daily, weekly, and monthly reports.
  - Visualize monthly earnings with graphs.
  - Export reports to CSV.

- **Settings:**  
  - Set default fuel efficiency and petrol price.
  - Backup your database.

- **Data Storage:**  
  - All data is stored locally in an SQLite database (`uber_wallet.db`).

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ride
    ```

2. **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **(Linux only) If you get errors about Tkinter:**
    ```bash
    sudo apt-get install python3-tk
    ```

---

## Usage

1. **Run the application:**
    ```bash
    python uber_prof.py
    ```

2. **Main Tabs:**
    - **Trips:** Add and manage trip records.
    - **Fuel:** Log fuel refills.
    - **Reports:** Generate and export reports.
    - **Settings:** Adjust fuel efficiency, petrol price, and backup data.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for Python package dependencies.

---

## Dependencies

- `tkinter` (GUI)
- `tkcalendar` (date picker)
- `matplotlib` (graphs)
- `reportlab` (PDF export, optional)
- `pytz` (timezone handling)
- `sqlite3` (database, included with Python)

---

## Data & Privacy

- All data is stored **locally** in `uber_wallet.db`.
- You can back up your data using the "Backup Data" button in Settings.

---

## License

MIT License

---

## Author

- [Your Name or GitHub Username]

---

## Screenshots

_Add screenshots here if desired._

---

## Notes

- This app is intended for personal use by Uber drivers.
- If you encounter issues, check the `uber_wallet.log` file for troubleshooting.
