import cups
import threading

_printer_name = 'ThermalPrinterAPE'
_cups_server = 'thermalprinter.local'
_printer_connection = None

def print_file(file_path, use_printer=False):
    if not use_printer:
        print(f'Skipping printing file: {file_path}')
        return None

    def _print():
        global _printer_connection
        print_job_id = None

        if not _printer_connection:
            try:
                _printer_connection = cups.Connection(host=_cups_server)    
            except Exception as e:
                print(f'Error connecting to printer: {e}')
                _printer_connection = None
                return

        if _printer_connection:
            try:
                print_options = {}

                # Options are now part of the default config on the CUPS server
                # print_options = {'orientation-requested':'6'} # rotate 90 degrees counterclockwise, prints small

                print_job_id = _printer_connection.printFile(_printer_name, file_path, 'Print Job', print_options)
                print(f'Print job {print_job_id} submitted successfully')
            except Exception as e:
                print(f'Error printing file: {e}')
                _printer_connection = None

    thread = threading.Thread(target=_print, daemon=True)
    thread.start()
