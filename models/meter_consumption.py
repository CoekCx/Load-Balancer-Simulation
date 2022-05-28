from utils.color import in_color, Color


class DataPoint:
    def __init__(self, meter_id, value, month):
        self.meter_id = meter_id
        self.value = value
        self.month = month

    def __str__(self, show_color=False):
        if show_color:
            name = f'{in_color("Meter Consumption:", Color.YELLOW, True)}'
            meter_id = f'{in_color("Meter", Color.WHITE, True)}: {in_color(str(self.meter_id), Color.GREEN, True)}'
            value = f'{in_color("Value", Color.WHITE, True)}: {in_color(self.value, Color.GREEN, True)}'
            month = f'{in_color("Month", Color.WHITE, True)}: {in_color(self.month, Color.GREEN, True)}'
        else:
            name = 'Meter Consumption:'
            meter_id = f'Meter {self.meter_id}'
            value = f'Value {self.value}'
            month = f'Month {self.month}'
        return f'<{name} {meter_id}\t{value}\t{month}>'
