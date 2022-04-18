import sys
import PySimpleGUI as sg        # https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms

from datetime import datetime


# Default GUI command line options

def show_help():
    help_str  = f"\n"
    help_str += f"Usage:\n"
    help_str += f"  app [options]\n"
    help_str += f"\n"
    help_str += f"Options:\n"
    help_str += f"  -gui            show interface for parameter selection\n"
    help_str += f"  -nogui          do not show interface\n"
    help_str += f"  -webgui         show a web browser interface (coming soon...)\n"
    help_str += f"\n"

    print(help_str)

# FORM LAYOUT Helper functions
def sectors_group(default_values):
    sectors = [
        "test",
        "basic_industies",
        "capital_goods",
        "consumer_durable",
        "consumer_non_dur",
        "consumer_services",
        "energy",
        "finance",
        "health_care",
        "miscellaneous",
        "public_utilities",
        "technology",
        "transportation",
        "ARKK Invest fund"
    ]
    max_width = max([len(x) for x in sectors]) + 1

    list_box_group = [
        [sg.Text("Choose sector")],
        [sg.Listbox(sectors,size=(max_width,15), enable_events=False, key="-SECTOR-", default_values=default_values["sector"] )],
    ]
    
    return list_box_group

def config_data_group(default_values):
    # Layout parameters for form components
    labels_size = (10,1)
    inputs_size = (20,1)

    form_layout = [
        [sg.Text("Historical Data Parameters")],
        [sg.Text("Start date:", size=labels_size), sg.Input(key="-HD_START-", size=inputs_size, default_text=default_values["historical_start"])],
        [sg.Text("End   date:", size=labels_size), sg.Input(key="-HD_END-"  , size=inputs_size, default_text=default_values["historical_end"])],
        [sg.HSeparator()],
        [sg.Text("Start buying period")],
        [sg.Text("Start date:", size=labels_size), sg.Input(key="-BUY_START-", size=inputs_size, default_text=default_values["buying_start"])],
        [sg.Text("End   date:", size=labels_size), sg.Input(key="-BUY_END-"  , size=inputs_size, default_text=default_values["buying_end"])],
        [sg.HSeparator()],
        [sg.Text("Minimum Price Data Required")],
        [sg.Text("Minimum size:", size=labels_size), sg.Input(key="-MIN_DATA-", size=inputs_size, default_text=default_values["min_historical_data"])],
        [sg.HSeparator()],
        [sg.Text("Strategy configuration")],
        [sg.Text("Starting cash:", size=labels_size), sg.Input(key="-CASH-", size=inputs_size, default_text=default_values["start_cash"])],
        [sg.Text("Commissions:", size=labels_size), sg.Input(key="-COMM-", size=inputs_size, default_text=default_values["commission"])],
    ]
    return form_layout

def layout_01(default_values):
    title = "... Backtesting Strategies ..."
    
    layout = [
        [
            [
                sg.Frame("Sectors", sectors_group(default_values), size=(200,350)),
                sg.Frame("Parameters", config_data_group(default_values), size=(275,350))
            ],
            [sg.Button("OK"), sg.Button("CANCEL")]
        ]
    ]
    return title, layout

# Helper functions to extract data from GUI Form
def get_sector_value_from_gui(event, values):
    if len(values["-SECTOR-"]) > 0:
        # Default value
        input_sector = values["-SECTOR-"][0]
    else:
        input_sector = "test"
    
    return input_sector

def get_valid_date(values, key, default="2018-01-01"):
    input_date_str = values[key]
    try:
        valid = bool(datetime.strptime(input_date_str, "%Y-%m-%d"))
        date_str = input_date_str if valid else default
    except Exception as e:
        date_str = default  
    return date_str

def get_valid_int(values, key, default=0):
    input_int_str = values[key]
    try:
        int_value = int(input_int_str)
    except Exception as e:
        int_value = default
    return int_value

def get_valid_float(values, key, default=0):
    input_float_str = values[key]
    try:
        float_value = float(input_float_str)
    except Exception as e:
        float_value = default
    return float_value


# Extract data from GUI Input Forms and create a dictionnary to return
def get_forms_values_from_gui(event, values):
    input_hd_start   = get_valid_date(  values, "-HD_START-" )
    input_hd_end     = get_valid_date(  values, "-HD_END-"   )
    input_buy_start  = get_valid_date(  values, "-BUY_START-")
    input_buy_end    = get_valid_date(  values, "-BUY_END-"  )
    input_min_data   = get_valid_int(   values, "-MIN_DATA-" )
    input_cash       = get_valid_int(   values, "-CASH-"     )
    input_commission = get_valid_float( values, "-COMM-"     )

    form_values = {
        "start_historical_data":input_hd_start,                        # Historical data start_date
        "end_historical_data":input_hd_end,                            # Historical data end_date,
        "start_apply_strategy":input_buy_start,                        # Strategy apply date (skip price data before this date)
        "end_apply_strategy":input_buy_end,
        "minimum_data_required":input_min_data,
        "start_cash":input_cash,
        "commission":input_commission
    }
    return form_values

def show_gui(show_gui=False):
    default_values = {
        "sector"              : "test",
        "historical_start"    : "2018-01-01",
        "historical_end"      : datetime.today().date(),
        "buying_start"        : "2021-01-01",
        "buying_end"          : datetime.today().date(),
        "min_historical_data" : "300",
        "start_cash"          : "3000",
        "commission"          : "0.001"
    }
    
    # Layout setup with default values
    title, layout = layout_01(default_values)
    
    # Display the window    
    window = sg.Window(title, layout)
    
    strategy_config = None
    if show_gui:
        while True:
            event, values = window.read()
            if event in [sg.WIN_CLOSED, "CANCEL"]:
                strategy_config = None
                break
            if event in ["OK"]:
                strategy_config = get_forms_values_from_gui(event, values)  
                strategy_config["sector"] = get_sector_value_from_gui(event, values)
                break

    window.close()
    return strategy_config

if __name__ == "__main__":
    run_options = None
    if "-help" in sys.argv:
        print(f"DEBUG: Received a -help option")
        show_help()
    elif "-gui" in sys.argv:
        print(f"DEBUG: Received a -gui option")
        run_options = show_gui(show_gui=True)
    elif "-nogui" in sys.argv:
        print(f"DEBUG: Received a -nogui option")
        run_options = show_gui(show_gui=False)
    else:
        print(f"DEBUG: No command line arguments received")
        run_options = show_gui(show_gui=False)

    print(f"DEBUG:\nrun_options: {run_options}")
