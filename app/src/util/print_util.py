import cups

# lp -d ThermalPrinterAPE assets/emoji_glyphs/32x32/1f3c4-1f3fc-200d-2640-fe0f.png

_printer_name = "ThermalPrinterAPE"
_cups_server = "10.10.10.186"
_printer_connection = None

def print_file(file_path):
    global _printer_connection
    if not _printer_connection:
        try:
            _printer_connection = cups.Connection(host=_cups_server)    
        except Exception as e:
            print(f"Error connecting to printer: {e}")
            return None

    return _printer_connection.printFile(_printer_name, file_path, "Print Job", {})

# Example usage
if __name__ == "__main__":
    file_path = "assets/emoji_glyphs/32x32/1f3c4-1f3fc-200d-2640-fe0f.png"

    job_id = print_file(file_path)
    print(f"Print job submitted with ID: {job_id}")