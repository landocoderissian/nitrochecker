# nitro_gen.py

import random
import string
import asyncio
import aiohttp
from discord_webhook import DiscordWebhook


class NitroGen:
    def __init__(self, update_output_callback=None):
        self.fileName = "Nitro Codes.txt"
        self.update_output = update_output_callback

    def slow_type(self, text, speed, new_line=True):
        for i in text:
            if self.update_output:
                self.update_output(i)
            time.sleep(speed)
        if new_line and self.update_output:
            self.update_output('\n')

    async def quick_checker(self, nitro, notify=None, session=None):
        url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    if self.update_output:
                        self.update_output(f" Valid | {nitro} \n")
                    with open(self.fileName, "a") as file:
                        file.write(nitro + "\n")
                    if notify is not None:
                        DiscordWebhook(
                            url=notify,
                            content=f"Valid Nitro Code detected! @everyone \n{nitro}"
                        ).execute()
                    return nitro
                else:
                    if self.update_output:
                        self.update_output(f" Invalid | {nitro} \n")
                    return None
        except Exception as e:
            if self.update_output:
                self.update_output(f" Error | {nitro} | {e}\n")
            return None

    async def generate_and_check_async(self, num_codes, notify=None):
        valid_codes = []
        invalid = 0
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(num_codes):
                code = "".join(random.choices(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase,
                    k=16
                ))
                tasks.append(self.quick_checker(code, notify, session))

            results = await asyncio.gather(*tasks)

            for result in results:
                if result:
                    valid_codes.append(f"https://discord.gift/{result}")
                else:
                    invalid += 1

        return {"valid": valid_codes, "invalid": invalid}

    def run_async_check(self, num_codes, notify=None):
        return asyncio.run(self.generate_and_check_async(num_codes, notify))
