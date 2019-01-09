from dataclasses import dataclass
from typing import List


@dataclass
class Stop:
    data: dict

    def is_bus_or_tram_stop(self) -> bool:
        return self.data["Category"]["CategoryId"] == "20"

    def get_name(self) -> str:
        return f'{self.data["Description"]} ({self.data["CustomerCode"]})'

    def get_code(self) -> str:
        return self.data["Code"]

    def get_customer_code(self) -> str:
        return self.data["CustomerCode"]

    def get_line_stops(self) -> List[dict]:
        return self.data["Lines"]

    def get_line_stop_codes(self) -> List[str]:
        return [line["Line"]["LineCode"] for line in self.get_line_stops()]

    def get_line_stops_names(self) -> List[str]:
        return [
            f'{line["Line"]["LineCode"]} - {line["Line"]["LineDescription"]}'
            for line in self.get_line_stops()
        ]

    def get_overview(self) -> str:
        name = f"🚏 *{self.get_name()}*"
        lines = "\n".join(self.get_lines_stops_overview())
        return name + "\n" + lines

    def get_lines_stops_overview(self):
        lines = []
        for line in self.get_line_stops():
            code = line["Line"]["LineCode"]
            description = line["Line"]["LineDescription"]
            wait = line["WaitMessage"]
            emoji = self.get_line_emoji(code)
            line_overview = f"{emoji} {code} - {description}"
            if wait is not None:
                line_overview += f" - {wait}"
            lines.append(line_overview)

        return lines

    @staticmethod
    def get_line_emoji(code: str) -> str:
        try:
            number = int(code)
            return "🚎" if number < 34 else "🚌"
        except ValueError:
            return "🚌"
