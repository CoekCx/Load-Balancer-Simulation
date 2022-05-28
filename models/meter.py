from utils.color import in_color, Color


class Meter:
    def __init__(self, id, first_name, last_name, street_name, street_number, zip_code, city):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.street_name = street_name
        self.street_number = street_number
        self.zip_code = zip_code
        self.city = city

    def __eq__(self, other):
        if not isinstance(other, Meter):
            return False
        if self.id == other.id:
            return True
        return False

    def __str__(self, show_info=False, show_info_color=False):
        value = ''
        if show_info_color:
            value += in_color(f"Meter {self.id}", Color.GREEN, True)
            value += ':\t' + in_color(f"{self.first_name}", Color.WHITE)
            value += '\t' + in_color(f"{self.last_name}", Color.WHITE)
            value += '\t' + in_color(f"{self.street_name}", Color.WHITE)
            value += '\t' + in_color(f"{self.street_number}", Color.WHITE)
            value += '\t' + in_color(f"{self.zip_code}", Color.WHITE)
            value += '\t' + in_color(f"{self.city}", Color.WHITE)
        elif show_info:
            value += f'Meter {self.id}:'
            value += f'\t{self.first_name}'
            value += f'\t{self.last_name}'
            value += f'\t{self.street_name}'
            value += f'\t{self.street_number}'
            value += f'\t{self.zip_code}'
            value += f'\t{self.city}'
        else:
            value = f'Meter {self.id}'
            
        return value
