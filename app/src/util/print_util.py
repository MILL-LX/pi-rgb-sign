import cups

_printer_name = 'ThermalPrinterAPE'
_cups_server = 'thermalprinter.local' #TODO: update for printer on ApeFest Router
_printer_connection = None

def print_file(file_path):
    global _printer_connection
    print_job_id = None

    if not _printer_connection:
        try:
            _printer_connection = cups.Connection(host=_cups_server)    
        except Exception as e:
            print(f'Error connecting to printer: {e}')
            _printer_connection = None

    if _printer_connection:
        try:
            print_job_id = _printer_connection.printFile(_printer_name, file_path, 'Print Job', {})
        except Exception as e:
            print(f'Error printing file: {e}')
            _printer_connection = None

    return print_job_id
