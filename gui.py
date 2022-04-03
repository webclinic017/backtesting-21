import sys
import PySimpleGUI as sg        # https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms

from datetime import datetime


def show_help():
    help_str  = f"\n"
    help_str += f"Usage:\n"
    help_str += f"  app [options]\n"
    help_str += f"\n"
    help_str += f"Options:\n"
    help_str += f"  -gui            show interface for parameter selection\n"
    help_str += f"  -nogui          do not show interface\n"
    #help_str += f"  -sector:name    choose stock market sector (default:transportation)\n"
    help_str += f"\n"

    print(help_str)


def sectors_group():
    sectors = [
        "all",
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
        "test"
    ]
    max_width = max([len(x) for x in sectors]) + 1

    list_box_group = [
        [sg.Text("Choose sector")],
        [sg.Listbox(sectors,size=(max_width,15), enable_events=False, key="-SECTOR-" )],
    ]
    
    return list_box_group

def historical_data_group():
    # Layout parameters for form components
    labels_size = (10,1)
    inputs_size = (20,1)
    form_layout = [
        [sg.Text("Historical Data Parameters")],
        [sg.Text("Start date:", size=labels_size), sg.Input(key="-HD_START-", size=inputs_size)],
        [sg.Text("End   date:", size=labels_size), sg.Input(key="-HD_END-"  , size=inputs_size)],
        [sg.HSeparator()],
        [sg.Text("Start buying period")],
        [sg.Text("Start date:", size=labels_size), sg.Input(key="-BUY_START-", size=inputs_size)],
        [sg.Text("End   date:", size=labels_size), sg.Input(key="-BUY_END-"  , size=inputs_size)],
        [sg.HSeparator()],
        [sg.Text("Minimum Price Data Required")],
        [sg.Text("Minimum size:", size=labels_size), sg.Input(key="-MIN_DATA-", size=inputs_size)],
        [sg.HSeparator()],
        [sg.Text("Strategy configuration")],
        [sg.Text("Starting cash:", size=labels_size), sg.Input(key="-CASH-", size=inputs_size)],
        [sg.Text("Commissions:", size=labels_size), sg.Input(key="-COMM-", size=inputs_size)],

    ]
    return form_layout


def layout_01():
    title = "... Backtesting Strategies ..."
    
    layout = [
        [
            [
                sg.Frame("Sectors", sectors_group(), size=(200,350)),
                sg.Frame("Parameters", historical_data_group(), size=(275,350))
            ],
            [sg.Button("OK"), sg.Button("CANCEL")]
        ]
    ]
    return title, layout

def show_gui():
    title, layout = layout_01()
    window = sg.Window(title, layout)
    
    input_sector = "test"
    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED, "CANCEL"]:
            break
        if event in ["OK"]:
            #print(f"VALUES['-SECTOR-']: {values['-SECTOR-']}")
            #print(f"selected item: {values['-SECTOR-'][0]}")
            if len(values["-SECTOR-"]) > 0:
                # Default value
                input_sector = values["-SECTOR-"][0]
            else:
                input_sector = "transporation"
            break

    # TODO: Replace this section with inpouts from UI
    return {
            "start_historical_data":"2018-01-01",                          # Historical data start_date
            "end_historical_data":datetime.today().strftime('%Y-%m-%d'),   # Historical data end_date,
            "start_apply_strategy":"2021-01-01",                           # Strategy apply date (skip price data before this date)
            "minimum_data_required":300,
            "sector":input_sector
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()

    run_options = None
    if "-gui" in sys.argv:
        print(f"DEBUG: Received a -gui option")
        gui_on = True
        run_options = show_gui()
    elif "-nogui" in sys.argv:
        print(f"DEBUG: Received a -nogui option")
        gui_on = False

    if run_options is None:
        run_options = {
            "start_historical_data":"2018-01-01",                          # Historical data start_date
            "end_historical_data":datetime.today().strftime('%Y-%m-%d'),   # Historical data end_date,
            "start_apply_strategy":"2021-01-01",                           # Strategy apply date (skip price data before this date)
            "minimum_data_required":300,
            "sector":"transporation"
        }


    print(f"DEBUG:{run_options}")

