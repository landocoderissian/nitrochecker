class NitroUtils:
    @staticmethod
    def check_existing_codes_from_file(view, file_path, separator):
        with open(file_path, 'r') as file:
            codes = file.read().split(separator or '\n')
        view.update_output(f"Checking {len(codes)} codes from file...\n")
        view.run_nitro_check_task(len(codes))

    @staticmethod
    def check_existing_codes_from_paste(view, codes):
        view.update_output(f"Checking {len(codes)} pasted codes...\n")
        view.run_nitro_check_task(len(codes))
