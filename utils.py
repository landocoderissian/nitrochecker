# tasks.py

import threading
from nitro_gen import NitroGen


def generate_until_valid(nitro_gen_app, num_valid_codes):
    valid_codes = []
    generator = NitroGen(update_output_callback=nitro_gen_app.update_output, webhook_url=nitro_gen_app.webhook_url)

    while len(valid_codes) < num_valid_codes and not nitro_gen_app.stop_generating:
        result = generator.run_async_check(1)  # Generate 1 code at a time
        if result['valid']:
            valid_codes.extend(result['valid'])
            for link in result['valid']:
                nitro_gen_app.update_valid_links(link)

    nitro_gen_app.update_output(f"\nFound {len(valid_codes)} valid codes!\n")


def keep_generating_until_stopped(nitro_gen_app):
    generator = NitroGen(update_output_callback=nitro_gen_app.update_output, webhook_url=nitro_gen_app.webhook_url)
    nitro_gen_app.stop_generating = False

    while not nitro_gen_app.stop_generating:
        result = generator.run_async_check(1)  # Generate 1 code at a time
        if result['valid']:
            for link in result['valid']:
                nitro_gen_app.update_valid_links(link)


def check_existing_codes(nitro_gen_app, file_path=None, separator='\n'):
    nitro_gen_app.update_output("Checking existing codes...\n")
    generator = NitroGen(update_output_callback=nitro_gen_app.update_output, webhook_url=nitro_gen_app.webhook_url)

    if file_path:
        with open(file_path, "r") as file:
            codes = file.read().split(separator)
    else:
        codes = []

    generator.run_async_check(len(codes))
